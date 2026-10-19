#!/usr/bin/env python3
"""Cliente minimo de la API REST de Airtable para FYR (solo libreria estandar),
mismo patron de diseno que production/scripts/drive/drive_client.py: credenciales
SOLO por variable de entorno, nunca en el repo; libreria + CLI en el mismo archivo.

No reemplaza el MCP de Airtable que usan las sesiones de Claude/Claude Code para
leer y escribir registros -- este cliente existe para un caso que el MCP no cubre:
que un script de gobernanza (sin sesion de Claude detras, por ejemplo corriendo en
GitHub Actions) pueda leer el SCHEMA real de una base sin depender de que haya un
agente con el MCP cargado en ese momento.

Credenciales (variable de entorno, NUNCA en el repo):
  AIRTABLE_API_KEY   -- Personal Access Token con scope schema.bases:read como minimo
                        (data.records:read si algun script futuro necesita leer filas)

Uso como libreria:
  from airtable_client import Airtable
  at = Airtable()
  schema = at.get_table_schema("appMy5aOwifSbBLPR", "tblRggZtw1E38ZQJs")
  nombres_de_campo = [f["name"] for f in schema["fields"]]

Uso como CLI:
  python3 airtable_client.py schema <base_id> <table_id>
  python3 airtable_client.py tables <base_id>
"""
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://api.airtable.com/v0"


class AirtableError(RuntimeError):
    pass


class Airtable:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("AIRTABLE_API_KEY")
        if not self.api_key:
            raise AirtableError(
                "Falta AIRTABLE_API_KEY en el entorno. Nunca se pasa por argumento "
                "ni se guarda en el repo -- ver docstring de este archivo."
            )

    def _get(self, path):
        req = urllib.request.Request(
            f"{API}{path}",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise AirtableError(f"HTTP {e.code} en {path}: {body}") from e

    def list_tables(self, base_id):
        """Devuelve la lista cruda de tablas (id, name, fields[]) de una base."""
        return self._get(f"/meta/bases/{base_id}/tables")["tables"]

    def get_table_schema(self, base_id, table_id_or_name):
        """Devuelve el dict {id, name, fields:[{id,name,type,...}], ...} de UNA tabla,
        buscando por tableId o por nombre exacto dentro de la respuesta de list_tables
        (la API de meta no tiene un endpoint de 'una sola tabla', siempre trae todas)."""
        for t in self.list_tables(base_id):
            if t["id"] == table_id_or_name or t["name"] == table_id_or_name:
                return t
        raise AirtableError(
            f"No se encontro la tabla '{table_id_or_name}' en la base {base_id}"
        )


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    at = Airtable()
    if cmd == "tables":
        base_id = sys.argv[2]
        for t in at.list_tables(base_id):
            print(f"{t['id']}\t{t['name']}\t{len(t['fields'])} campos")
    elif cmd == "schema":
        if len(sys.argv) < 4:
            sys.exit("Uso: airtable_client.py schema <base_id> <table_id_o_nombre>")
        base_id, table = sys.argv[2], sys.argv[3]
        t = at.get_table_schema(base_id, table)
        print(json.dumps(t, indent=2, ensure_ascii=False))
    else:
        sys.exit(f"Comando desconocido: {cmd}")


if __name__ == "__main__":
    main()
