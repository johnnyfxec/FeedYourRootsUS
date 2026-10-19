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

Uso:
  AIRTABLE_API_KEY=<token> python3 check_field_coverage.py

Exit code 0 si las 4 tablas coinciden exactamente con lo documentado.
Exit code 1 si hay cualquier divergencia -- imprime la lista exacta de campos
huerfanos en cada direccion, tabla por tabla, para que se corrija antes de producir.

No corre nada mas, no escribe nada en Airtable ni en el repo: es solo lectura.
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


def main():
    try:
        at = Airtable()
    except AirtableError as e:
        sys.exit(f"✗ {e}")

    try:
        documentado = parse_campos_documentados(RUTAS_DOC)
    except Exception as e:  # parseo del doc, no de Airtable
        sys.exit(f"✗ Error leyendo {RUTAS_DOC}: {e}")

    hay_divergencia = False
    reporte = []

    for nombre_tabla, table_id in TABLAS.items():
        try:
            schema = at.get_table_schema(BASE_ID, table_id)
        except AirtableError as e:
            sys.exit(f"✗ No se pudo leer el schema real de '{nombre_tabla}' ({table_id}): {e}")

        campos_reales = {f["name"] for f in schema["fields"]}
        campos_doc = documentado.get(nombre_tabla, set())

        if nombre_tabla not in documentado:
            hay_divergencia = True
            reporte.append(
                f"✗ {nombre_tabla}: la tabla NO aparece en absoluto en el bloque "
                f"CAMPOS-DOCUMENTADOS de {os.path.basename(RUTAS_DOC)} "
                f"({len(campos_reales)} campos reales sin ninguna cobertura)."
            )
            continue

        huerfanos_reales = sorted(campos_reales - campos_doc)
        huerfanos_doc = sorted(campos_doc - campos_reales)

        if not huerfanos_reales and not huerfanos_doc:
            reporte.append(f"✓ {nombre_tabla}: {len(campos_reales)} campos, cobertura completa.")
            continue

        hay_divergencia = True
        if huerfanos_reales:
            reporte.append(
                f"✗ {nombre_tabla}: {len(huerfanos_reales)} campo(s) REAL(ES) en Airtable "
                f"que NINGUN documento nombra todavia:"
            )
            for c in huerfanos_reales:
                reporte.append(f"    - {c}")
        if huerfanos_doc:
            reporte.append(
                f"✗ {nombre_tabla}: {len(huerfanos_doc)} campo(s) DOCUMENTADO(S) que ya "
                f"no existen con ese nombre exacto en Airtable (renombrado, borrado, o "
                f"error de tipeo en el bloque):"
            )
            for c in huerfanos_doc:
                reporte.append(f"    - {c}")

    print("\n".join(reporte))
    print()
    if hay_divergencia:
        print(
            "✗ check_field_coverage: HAY DIVERGENCIA. No arrancar el lote (Parada 0) hasta "
            "resolver -- actualizar la Seccion 0.8 en prosa Y el bloque CAMPOS-DOCUMENTADOS "
            "de FYR_Rutas_De_Produccion.md, o corregir el campo en Airtable si el error esta ahi."
        )
        sys.exit(1)
    print("✓ check_field_coverage: las 4 tablas coinciden exactamente con lo documentado.")


if __name__ == "__main__":
    main()
