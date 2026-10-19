#!/usr/bin/env python3
"""Verifica que todo campo REAL de Airtable (Themes, Content_Pieces, Assets,
Trend Signals) este nombrado en el bloque <!-- CAMPOS-DOCUMENTADOS --> de
knowledge/FYR_Rutas_De_Produccion.md -- y viceversa: que todo campo documentado
siga existiendo de verdad en Airtable con ese nombre exacto.

Por que existe (19-oct-2026): el incidente real de `Bundle Relacionado` -- quedo
vacio en 6 filas de Themes del primer lote porque ningun documento lo mencionaba
como campo a llenar -- no lo detecto ninguna auditoria dinamica de fila-contra-fila
(ver fase-d-planner/SKILL.md Seccion 9), porque TODO el lote omitia el mismo campo
por igual: no habia ninguna fila "buena" contra la cual comparar. La unica forma de
detectar ese tipo de hueco es compararlo contra algo EXTERNO al lote -- el schema
real de Airtable -- y eso es lo que este script hace, antes de que el lote arranque.

Este script NO reemplaza la auditoria dinamica de la Seccion 9 (esa sigue haciendo
falta para detectar un campo que SI esta documentado pero una fila especifica omitio
por error de ejecucion). Este script cubre el otro lado: un campo real que ningun
documento sabe que existe, o un campo documentado que ya no existe de verdad.

Uso (canal REST -- GitHub Actions, o cualquier maquina con salida directa a
api.airtable.com, p. ej. la PC/Termux de Johnny):
  AIRTABLE_API_KEY=<token> python3 check_field_coverage.py

Exit code 0 si las 4 tablas coinciden exactamente con lo documentado.
Exit code 1 si hay cualquier divergencia -- imprime la lista exacta de campos
huerfanos en cada direccion, tabla por tabla, para que se corrija antes de producir.

No corre nada mas, no escribe nada en Airtable ni en el repo: es solo lectura.

NOTA DE CANAL POR CONTEXTO (19-oct-2026, incidente real): este modulo asumio que
api.airtable.com tendria salida permitida desde el sandbox de una sesion de Claude
Code en la nube, por mala analogia con Drive (`*.googleapis.com` si esta permitido
ahi) -- nunca se agrego Airtable a esa lista, y cambiar la politica de red del
entorno a mitad de sesion no sirve: una sesion ya arrancada no recarga esa lista en
caliente (confirmado en vivo: 3 intentos identicos, incluido uno despues del cambio
de configuracion, mismo 403 del proxy de egress los 3). Por eso esta logica se separo
en `comparar_tabla()` / `comparar_todas()` / `resumen_final()`, puras funciones de
comparacion sin ningun fetch de red adentro: en una sesion interactiva de Claude Code
(donde el MCP de Airtable SI esta cargado y funciona todo el dia, por una via
distinta a la salida HTTP cruda del sandbox) se importan esas 3 funciones, se arma
`schemas_por_tabla` con `mcp__Airtable__get_table_schema` para las 4 tablas, y se
invoca `comparar_todas()` directo -- mismo chequeo mecanico, mismo formato de salida,
canal distinto. Ver FYR_Rutas_De_Produccion.md Seccion 1 para el detalle completo de
por que cada canal aplica donde aplica.
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "drive"))  # no usado hoy, placeholder de simetria con otros scripts del repo
sys.path.insert(0, os.path.dirname(__file__))

from airtable_client import Airtable, AirtableError  # noqa: E402

BASE_ID = "appMy5aOwifSbBLPR"

# tabla real de Airtable (nombre exacto, con espacio donde corresponda) -> tableId.
# Los tableId vienen de mcp__Airtable__list_tables_for_base, confirmados en vivo
# 19-oct-2026 (ver FYR_Rutas_De_Produccion.md Seccion 0.2 y CHANGELOG 16-oct).
TABLAS = {
    "Themes": "tblRggZtw1E38ZQJs",
    "Content_Pieces": "tblevmNSbGTzdjuDF",
    "Assets": "tblkzOtjS4KK5B2Xn",
    "Trend Signals": "tblxdaRsgEy8CHvV9",
}

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
RUTAS_DOC = os.path.join(REPO_ROOT, "knowledge", "FYR_Rutas_De_Produccion.md")

BLOQUE_RE = re.compile(
    r"<!--\s*CAMPOS-DOCUMENTADOS\s*\n(.*?)\n\s*-->", re.DOTALL
)
# Dentro del bloque: "NombreTabla: campo1, campo2,\n  campo3, ..." -- una tabla puede
# partirse en varias lineas con indentacion; el separador de campo es siempre la coma.
ENTRADA_TABLA_RE = re.compile(
    r"^(\S.*?):\s*(.*?)(?=^\S.*?:|\Z)", re.DOTALL | re.MULTILINE
)


def parse_campos_documentados(ruta_doc):
    """Lee el bloque <!-- CAMPOS-DOCUMENTADOS --> de FYR_Rutas_De_Produccion.md y
    devuelve {nombre_tabla: set(nombres_de_campo)}. No usa ningun LLM ni heuristica
    de lenguaje natural -- es un parseo de texto estructurado, deliberadamente
    literal: si el bloque no tiene el formato exacto, falla con un mensaje claro
    en vez de adivinar."""
    if not os.path.isfile(ruta_doc):
        sys.exit(f"✗ No existe {ruta_doc}")
    texto = open(ruta_doc, encoding="utf-8").read()
    m = BLOQUE_RE.search(texto)
    if not m:
        sys.exit(
            f"✗ No se encontro el bloque <!-- CAMPOS-DOCUMENTADOS --> en {ruta_doc}. "
            f"Sin ese bloque este script no tiene contra que comparar -- revisar que "
            f"no se haya borrado por error en una edicion anterior."
        )
    bloque = m.group(1)
    resultado = {}
    for entrada in ENTRADA_TABLA_RE.finditer(bloque):
        tabla = entrada.group(1).strip()
        campos_raw = entrada.group(2)
        campos = {c.strip() for c in campos_raw.replace("\n", " ").split(",") if c.strip()}
        resultado[tabla] = campos
    if not resultado:
        sys.exit(f"✗ El bloque CAMPOS-DOCUMENTADOS en {ruta_doc} esta vacio o no se pudo parsear.")
    return resultado


def comparar_tabla(nombre_tabla, campos_reales, documentado, ruta_doc=RUTAS_DOC):
    """Compara un set de campos reales (de UNA tabla, sin importar si vinieron del
    cliente REST o del MCP de Airtable) contra lo que el bloque CAMPOS-DOCUMENTADOS
    dice para esa tabla. No toca la red -- es pura comparacion de sets + formato.
    Devuelve (ok: bool, lineas_de_reporte: list[str])."""
    if nombre_tabla not in documentado:
        return False, [
            f"✗ {nombre_tabla}: la tabla NO aparece en absoluto en el bloque "
            f"CAMPOS-DOCUMENTADOS de {os.path.basename(ruta_doc)} "
            f"({len(campos_reales)} campos reales sin ninguna cobertura)."
        ]

    campos_doc = documentado[nombre_tabla]
    huerfanos_reales = sorted(campos_reales - campos_doc)
    huerfanos_doc = sorted(campos_doc - campos_reales)

    if not huerfanos_reales and not huerfanos_doc:
        return True, [f"✓ {nombre_tabla}: {len(campos_reales)} campos, cobertura completa."]

    reporte = []
    if huerfanos_reales:
        reporte.append(
            f"✗ {nombre_tabla}: {len(huerfanos_reales)} campo(s) REAL(ES) en Airtable "
            f"que NINGUN documento nombra todavia:"
        )
        reporte += [f"    - {c}" for c in huerfanos_reales]
    if huerfanos_doc:
        reporte.append(
            f"✗ {nombre_tabla}: {len(huerfanos_doc)} campo(s) DOCUMENTADO(S) que ya "
            f"no existen con ese nombre exacto en Airtable (renombrado, borrado, o "
            f"error de tipeo en el bloque):"
        )
        reporte += [f"    - {c}" for c in huerfanos_doc]
    return False, reporte


def comparar_todas(schemas_por_tabla, documentado, tablas_orden=tuple(TABLAS), ruta_doc=RUTAS_DOC):
    """schemas_por_tabla: {nombre_tabla: set(nombres_de_campo_reales)} -- el origen de
    ese set (REST o MCP) es indiferente aqui, por eso esta funcion es el punto de
    reuso real entre check_field_coverage.py (canal REST, usado en GitHub Actions) y
    una sesion interactiva de Claude Code con el MCP de Airtable cargado (canal MCP,
    usado cuando el proxy del sandbox no tiene api.airtable.com permitido -- ver nota
    de canal por contexto en el docstring del modulo y en FYR_Rutas_De_Produccion.md
    Seccion 1). Misma logica de diff, mismo formato de salida, sin importar quien
    llamo a Airtable. Devuelve (hay_divergencia: bool, reporte: list[str])."""
    hay_divergencia = False
    reporte = []
    for nombre_tabla in tablas_orden:
        ok, lineas = comparar_tabla(nombre_tabla, schemas_por_tabla[nombre_tabla], documentado, ruta_doc)
        if not ok:
            hay_divergencia = True
        reporte.extend(lineas)
    return hay_divergencia, reporte


def resumen_final(hay_divergencia):
    """Linea de cierre identica para cualquier canal -- REST o MCP."""
    if hay_divergencia:
        return (
            "✗ check_field_coverage: HAY DIVERGENCIA. No arrancar el lote (Parada 0) hasta "
            "resolver -- actualizar la Seccion 0.8 en prosa Y el bloque CAMPOS-DOCUMENTADOS "
            "de FYR_Rutas_De_Produccion.md, o corregir el campo en Airtable si el error esta ahi."
        )
    return "✓ check_field_coverage: las 4 tablas coinciden exactamente con lo documentado."


def main():
    """Canal REST -- usado en GitHub Actions (salida de red normal a APIs externas) y
    en cualquier maquina con acceso directo a api.airtable.com (PC/Termux de Johnny).
    NO es el canal a usar dentro de una sesion de Claude Code en el sandbox de la nube
    -- ahi el proxy de egress no tiene api.airtable.com permitido y una sesion ya
    arrancada no recarga ese permiso en caliente aunque se cambie despues. En ese
    contexto, usar el MCP de Airtable (mcp__Airtable__get_table_schema) para armar
    schemas_por_tabla e invocar comparar_todas()/resumen_final() directamente -- ver
    FYR_Rutas_De_Produccion.md Seccion 1."""
    try:
        at = Airtable()
    except AirtableError as e:
        sys.exit(f"✗ {e}")

    try:
        documentado = parse_campos_documentados(RUTAS_DOC)
    except Exception as e:  # parseo del doc, no de Airtable
        sys.exit(f"✗ Error leyendo {RUTAS_DOC}: {e}")

    schemas_por_tabla = {}
    for nombre_tabla, table_id in TABLAS.items():
        try:
            schema = at.get_table_schema(BASE_ID, table_id)
        except AirtableError as e:
            sys.exit(f"✗ No se pudo leer el schema real de '{nombre_tabla}' ({table_id}): {e}")
        schemas_por_tabla[nombre_tabla] = {f["name"] for f in schema["fields"]}

    hay_divergencia, reporte = comparar_todas(schemas_por_tabla, documentado)

    print("\n".join(reporte))
    print()
    print(resumen_final(hay_divergencia))
    if hay_divergencia:
        sys.exit(1)


if __name__ == "__main__":
    main()
