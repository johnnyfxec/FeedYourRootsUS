#!/usr/bin/env python3
"""Verifica que todo campo REAL de Airtable (Themes, Content_Pieces, Assets,
Trend Signals) este nombrado en el bloque <!-- CAMPOS-DOCUMENTADOS --> del
documento que es DUEÑO de cada tabla -- y viceversa: que todo campo documentado
siga existiendo de verdad en Airtable con ese nombre exacto.

Las 4 tablas NO viven en un unico documento (correccion 19-oct-2026, segundo error
real de diseno que el gate se encargo de sacar a la luz el mismo dia que se escribio):
Themes/Content_Pieces/Assets las gestiona knowledge/FYR_Rutas_De_Produccion.md;
Trend Signals la gestiona knowledge/FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md
Seccion 5.4, porque esa es la skill (trend-scout) dueña real de esa tabla --
Rutas_De_Produccion.md solo la CONSUME en A0/B0, nunca la gestiona (ver su 0.2).
El primer bloque CAMPOS-DOCUMENTADOS se escribio ignorando esa distincion, que el
propio documento ya establecia antes de que este script existiera -- corregido
moviendo el bloque de Trend Signals a su dueño real, en vez de duplicar la tabla
en dos lugares (el mismo patron de divergencia que ya causo la contradiccion de
schema de 16-oct-2026 entre dos documentos de trend-scout).

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
VIRAL_DOC = os.path.join(REPO_ROOT, "knowledge", "FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md")

# Documentos a parsear, EN ORDEN -- cada uno aporta el bloque CAMPOS-DOCUMENTADOS de
# las tablas de las que es dueño. Si una tabla aparece en mas de uno (no deberia pasar
# nunca -- es el mismo error que este comentario explica en el docstring del modulo),
# parse_campos_documentados() lo trata como error y se detiene, no como un merge
# silencioso de sets: dos documentos reclamando la misma tabla es en si mismo el bug
# a corregir, no algo para promediar.
DOCUMENTOS_FUENTE = (RUTAS_DOC, VIRAL_DOC)

BLOQUE_RE = re.compile(
    r"<!--\s*CAMPOS-DOCUMENTADOS\s*\n(.*?)\n\s*-->", re.DOTALL
)
# Dentro del bloque: "NombreTabla: campo1, campo2,\n  campo3, ..." -- una tabla puede
# partirse en varias lineas con indentacion; el separador de campo es siempre la coma.
ENTRADA_TABLA_RE = re.compile(
    r"^(\S.*?):\s*(.*?)(?=^\S.*?:|\Z)", re.DOTALL | re.MULTILINE
)


def _parse_un_documento(ruta_doc):
    """Lee el bloque <!-- CAMPOS-DOCUMENTADOS --> de UN documento y devuelve
    {nombre_tabla: set(nombres_de_campo)}. No usa ningun LLM ni heuristica de
    lenguaje natural -- es un parseo de texto estructurado, deliberadamente
    literal: si el bloque no tiene el formato exacto, falla con un mensaje claro
    en vez de adivinar. Un documento sin el bloque devuelve {} (no es error --
    no todo documento fuente tiene por que documentar alguna tabla; el error real
    es que NINGUNO de los documentos de DOCUMENTOS_FUENTE lo tenga, eso lo valida
    parse_campos_documentados())."""
    if not os.path.isfile(ruta_doc):
        sys.exit(f"✗ No existe {ruta_doc}")
    texto = open(ruta_doc, encoding="utf-8").read()
    m = BLOQUE_RE.search(texto)
    if not m:
        return {}
    bloque = m.group(1)
    resultado = {}
    for entrada in ENTRADA_TABLA_RE.finditer(bloque):
        tabla = entrada.group(1).strip()
        campos_raw = entrada.group(2)
        campos = {c.strip() for c in campos_raw.replace("\n", " ").split(",") if c.strip()}
        resultado[tabla] = campos
    return resultado


def parse_campos_documentados(rutas_doc=DOCUMENTOS_FUENTE):
    """Combina el bloque CAMPOS-DOCUMENTADOS de varios documentos -- cada tabla de
    Airtable tiene UN dueño (ver docstring del modulo: Themes/Content_Pieces/Assets
    en FYR_Rutas_De_Produccion.md, Trend Signals en
    FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md). Si dos documentos reclaman la
    misma tabla, es un error real -- significa que alguien volvio a duplicar el
    schema de una tabla en dos lugares, exactamente el patron que causo la
    contradiccion de Trend_Signals de 16-oct-2026 -- y el script se detiene en vez
    de promediar o quedarse con el primero en silencio."""
    resultado = {}
    for ruta in rutas_doc:
        parcial = _parse_un_documento(ruta)
        for tabla, campos in parcial.items():
            if tabla in resultado:
                sys.exit(
                    f"✗ La tabla '{tabla}' aparece en el bloque CAMPOS-DOCUMENTADOS de "
                    f"MAS DE UN documento -- revisar {os.path.basename(ruta)} y los demas "
                    f"de DOCUMENTOS_FUENTE. Cada tabla debe tener un unico documento dueño "
                    f"(ver docstring del modulo)."
                )
            resultado[tabla] = campos
    if not resultado:
        sys.exit(
            f"✗ Ningun documento de {[os.path.basename(r) for r in rutas_doc]} tiene el "
            f"bloque CAMPOS-DOCUMENTADOS. Sin eso este script no tiene contra que comparar "
            f"-- revisar que no se haya borrado por error en una edicion anterior."
        )
    return resultado


def comparar_tabla(nombre_tabla, campos_reales, documentado):
    """Compara un set de campos reales (de UNA tabla, sin importar si vinieron del
    cliente REST o del MCP de Airtable) contra lo que el bloque CAMPOS-DOCUMENTADOS
    dice para esa tabla, en CUALQUIERA de los DOCUMENTOS_FUENTE (ya combinados en
    `documentado` por parse_campos_documentados()). No toca la red -- es pura
    comparacion de sets + formato. Devuelve (ok: bool, lineas_de_reporte: list[str])."""
    if nombre_tabla not in documentado:
        nombres_docs = ", ".join(os.path.basename(r) for r in DOCUMENTOS_FUENTE)
        return False, [
            f"✗ {nombre_tabla}: la tabla NO aparece en absoluto en el bloque "
            f"CAMPOS-DOCUMENTADOS de ninguno de los documentos fuente ({nombres_docs}) "
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


def comparar_todas(schemas_por_tabla, documentado, tablas_orden=tuple(TABLAS)):
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
        ok, lineas = comparar_tabla(nombre_tabla, schemas_por_tabla[nombre_tabla], documentado)
        if not ok:
            hay_divergencia = True
        reporte.extend(lineas)
    return hay_divergencia, reporte


def resumen_final(hay_divergencia):
    """Linea de cierre identica para cualquier canal -- REST o MCP."""
    if hay_divergencia:
        return (
            "✗ check_field_coverage: HAY DIVERGENCIA. No arrancar el lote (Parada 0) hasta "
            "resolver -- actualizar la prosa (Seccion 0.8 de FYR_Rutas_De_Produccion.md o "
            "Seccion 5 de FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md, segun la tabla) Y "
            "el bloque CAMPOS-DOCUMENTADOS correspondiente, o corregir el campo en Airtable "
            "si el error esta ahi."
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
        documentado = parse_campos_documentados()
    except Exception as e:  # parseo de los docs, no de Airtable
        sys.exit(f"✗ Error leyendo los documentos fuente: {e}")

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
