#!/usr/bin/env python3
"""Cliente minimo de la API de Google Drive para FYR (solo libreria estandar).

Credenciales: SIEMPRE por variables de entorno, nunca en el repo.
  GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REFRESH_TOKEN

ALCANCE: `drive.file` (el minimo). Con ese alcance este cliente SOLO ve y toca los archivos que el mismo
creo. Por eso su unica tarea real es SUBIR archivos binarios (PNG/MP4) a la raiz del Drive de Johnny y
verificar el md5; despues Claude los MUEVE a su carpeta con el conector de Drive (update_file con parentId).
Todo lo demas (listar, descargar, crear carpetas, mover, papelera) se hace con el conector de Drive.

Uso como libreria:
  from drive_client import Drive
  d = Drive()
  info = d.upload("local.png", nombre="FYR_PZA_1.2_S1_4x5_v1.png")   # a la raiz, verifica md5
  d.find("nombre") / d.find_prefix("prefijo") / d.metadata(id) / d.trash(id)
  (descargar y crear carpetas solo funcionan sobre lo que este cliente creo)

Uso como CLI (para comprobar el acceso):
  python3 drive_client.py check
  python3 drive_client.py download <id> <ruta>
  python3 drive_client.py upload <ruta> [nombre]
  python3 drive_client.py ls
"""
import hashlib
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

TOKEN_URL = "https://oauth2.googleapis.com/token"
API = "https://www.googleapis.com/drive/v3/files"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files"
FIELDS = "id,name,mimeType,size,md5Checksum,parents,webViewLink,trashed"


class DriveError(RuntimeError):
    pass


class Drive:
    def __init__(self, client_id=None, client_secret=None, refresh_token=None):
        self.client_id = client_id or os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        self.refresh_token = refresh_token or os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN")
        faltan = [n for n, v in (("GOOGLE_OAUTH_CLIENT_ID", self.client_id),
                                 ("GOOGLE_OAUTH_CLIENT_SECRET", self.client_secret),
                                 ("GOOGLE_OAUTH_REFRESH_TOKEN", self.refresh_token)) if not v]
        if faltan:
            raise DriveError("Faltan variables de entorno: " + ", ".join(faltan))
        self._token = None
        self._exp = 0.0

    # ---------- autenticacion ----------
    def _access_token(self):
        if self._token and time.time() < self._exp - 60:
            return self._token
        data = urllib.parse.urlencode({
            "client_id": self.client_id, "client_secret": self.client_secret,
            "refresh_token": self.refresh_token, "grant_type": "refresh_token"}).encode()
        r = self._open(urllib.request.Request(TOKEN_URL, data=data), auth=False)
        j = json.loads(r)
        self._token = j["access_token"]
        self._exp = time.time() + int(j.get("expires_in", 3600))
        return self._token

    def _open(self, req, auth=True, retries=4):
        if auth:
            req.add_header("Authorization", "Bearer " + self._access_token())
        for i in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=300) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")[:500]
                if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                    time.sleep(2 ** i)
                    continue
                raise DriveError(f"HTTP {e.code} en {req.full_url.split('?')[0]}: {body}")
            except urllib.error.URLError as e:
                if i < retries - 1:
                    time.sleep(2 ** i)
                    continue
                raise DriveError(f"Sin conexion con {req.full_url.split('?')[0]}: {e.reason}")

    def _json(self, url, method="GET", body=None):
        req = urllib.request.Request(url, method=method)
        if body is not None:
            req.data = json.dumps(body).encode()
            req.add_header("Content-Type", "application/json")
        raw = self._open(req)
        return json.loads(raw) if raw else {}

    # ---------- lectura ----------
    def metadata(self, file_id):
        return self._json(f"{API}/{file_id}?fields={FIELDS}&supportsAllDrives=true")

    def find_prefix(self, prefix, parent_id="root"):
        """Archivos del cliente cuyo nombre empieza por `prefix` (Drive solo busca por palabra; se filtra aqui)."""
        q = "name contains '%s' and trashed = false and '%s' in parents" % (
            prefix.split("_v")[0].replace("\\", "\\\\").replace("'", "\\'"), parent_id)
        url = (f"{API}?q={urllib.parse.quote(q)}&fields=files({FIELDS})&pageSize=100&supportsAllDrives=true")
        return [f for f in self._json(url).get("files", []) if f["name"].startswith(prefix)]

    def find(self, name, parent_id=None):
        q = "name = '%s' and trashed = false" % name.replace("\\", "\\\\").replace("'", "\\'")
        if parent_id:
            q += f" and '{parent_id}' in parents"
        url = (f"{API}?q={urllib.parse.quote(q)}&fields=files({FIELDS})&pageSize=20"
               "&orderBy=modifiedTime%20desc&supportsAllDrives=true&includeItemsFromAllDrives=true")
        return self._json(url).get("files", [])

    def ls(self, parent_id):
        out, page = [], None
        while True:
            q = f"'{parent_id}' in parents and trashed = false"
            url = (f"{API}?q={urllib.parse.quote(q)}&fields=nextPageToken,files({FIELDS})&pageSize=200"
                   "&supportsAllDrives=true&includeItemsFromAllDrives=true")
            if page:
                url += "&pageToken=" + page
            j = self._json(url)
            out += j.get("files", [])
            page = j.get("nextPageToken")
            if not page:
                return out

    def download(self, file_id, dest):
        """Descarga y verifica contra md5Checksum de Drive. Devuelve la metadata."""
        meta = self.metadata(file_id)
        raw = self._open(urllib.request.Request(f"{API}/{file_id}?alt=media&supportsAllDrives=true"))
        md5 = hashlib.md5(raw).hexdigest()
        if meta.get("md5Checksum") and md5 != meta["md5Checksum"]:
            raise DriveError(f"Descarga corrupta de {meta.get('name')}: md5 {md5} != {meta['md5Checksum']}")
        os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
        with open(dest, "wb") as f:
            f.write(raw)
        return meta

    # ---------- escritura ----------
    def mkdir(self, name, parent_id):
        """Crea la carpeta si no existe (idempotente). Devuelve su metadata."""
        for f in self.find(name, parent_id):
            if f["mimeType"] == "application/vnd.google-apps.folder":
                return f
        return self._json(f"{API}?fields={FIELDS}&supportsAllDrives=true", "POST", {
            "name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]})

    def upload(self, path, parent_id=None, name=None):
        """Sube (multipart) y VERIFICA md5 contra lo que Drive guardo. Sin `parent_id` va a la raiz de Drive
        (lo unico permitido con alcance drive.file). Si el cliente ya subio un archivo con ese nombre, lo
        reemplaza (mismo ID) para no duplicar."""
        name = name or os.path.basename(path)
        with open(path, "rb") as f:
            data = f.read()
        local_md5 = hashlib.md5(data).hexdigest()
        mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
        existing = [f for f in self.find(name, parent_id or "root") if f["mimeType"] != "application/vnd.google-apps.folder"]
        meta = {"name": name} if existing else ({"name": name, "parents": [parent_id]} if parent_id else {"name": name})
        boundary = uuid.uuid4().hex
        body = (f"--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode()
                + json.dumps(meta).encode()
                + f"\r\n--{boundary}\r\nContent-Type: {mime}\r\n\r\n".encode()
                + data + f"\r\n--{boundary}--".encode())
        if existing:
            url = f"{UPLOAD}/{existing[0]['id']}?uploadType=multipart&fields={FIELDS}&supportsAllDrives=true"
            method = "PATCH"
        else:
            url = f"{UPLOAD}?uploadType=multipart&fields={FIELDS}&supportsAllDrives=true"
            method = "POST"
        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Content-Type", f"multipart/related; boundary={boundary}")
        info = json.loads(self._open(req))
        if info.get("md5Checksum") != local_md5:
            raise DriveError(f"Subida NO verificada para {name}: md5 Drive {info.get('md5Checksum')} != local {local_md5}")
        return info

    def trash(self, file_id):
        return self._json(f"{API}/{file_id}?fields=id,trashed&supportsAllDrives=true", "PATCH", {"trashed": True})


def link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/view?usp=drivesdk"


def _cli(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, d = argv[1], Drive()
    if cmd == "check":
        j = d._json("https://www.googleapis.com/drive/v3/about?fields=user(emailAddress,displayName)")
        print("OK, conectado como:", j["user"]["emailAddress"])
    elif cmd == "download":
        print(json.dumps(d.download(argv[2], argv[3]), indent=1))
    elif cmd == "upload":
        print(json.dumps(d.upload(argv[2], None, argv[3] if len(argv) > 3 else None), indent=1))
    elif cmd == "ls":
        for f in d.ls("root"):
            print(f["id"], f["mimeType"].split(".")[-1], f.get("size", "-"), f["name"])
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(_cli(sys.argv))
    except DriveError as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
