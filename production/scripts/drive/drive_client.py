#!/usr/bin/env python3
"""Cliente minimo de la API de Google Drive para FYR (solo libreria estandar).

Credenciales: OAuth de USUARIO (no cuenta de servicio), variables de entorno -- NUNCA en el repo:
  GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET   (client tipo "Aplicacion de escritorio")
  GOOGLE_OAUTH_REFRESH_TOKEN                            (obtenido una vez con drive_authorize_web.py)

NOTA DE DISENO (16-oct-2026): se probaron 3 arquitecturas antes de esta y las 3 fallaron por razones de
plataforma (no bugs propios):
  1. OAuth usuario, scope `drive.file`, flujo de dispositivo: funciona para subir, pero `drive.file` SOLO
     permite escribir en objetos creados por la propia app -- Google rechaza escribir dentro de una carpeta
     que Johnny ya tenia (confirmado via error y corroborado por un reporte publico identico de otro usuario
     con el mismo tipo de conector: ver issue "User cannot add children"). Por eso tampoco servia que el
     conector de Drive (MCP) viera o moviera lo subido por la API: son identidades de acceso separadas ante
     Google aunque autentiquen el mismo Gmail.
  2. OAuth usuario, scope `drive` completo, flujo de dispositivo: Google RECHAZA ese scope en ese flujo
     ("Invalid device flow scope") -- restriccion de Google para clientes tipo "TV y dispositivos de entrada
     limitada", no configurable.
  3. Cuenta de servicio: autentica bien y lee cualquier carpeta compartida con ella, pero no puede escribir
     en Drive personal/consumidor ("Service Accounts do not have storage quota") -- esa capacidad de escribir
     solo existe en Shared Drives (Google Workspace), que una cuenta Gmail personal no tiene aunque pague por
     espacio en Google One.

La solucion real: mismo OAuth de usuario, mismo scope `drive` completo, pero con flujo WEB/loopback
(drive_authorize_web.py) en vez de flujo de dispositivo -- ese flujo si acepta scopes sensibles porque pasa
por un navegador real. Una vez autorizado, el cliente funciona igual sin importar en que maquina corra
despues (este sandbox, la tablet de Johnny via Termux, un servidor): el problema nunca fue "donde corre el
script", fue el tipo de client OAuth y el scope.

Uso como libreria:
  from drive_client import Drive
  d = Drive()
  info = d.upload("local.png", parent_id="<id_carpeta>", name="FYR_PZA_1.2_S1_4x5_v1.png")
  d.find("nombre") / d.find_prefix("prefijo", parent_id) / d.metadata(id) / d.trash(id)
  d.mkdir("nombre", parent_id)  # idempotente

Uso como CLI (para comprobar el acceso):
  python3 drive_client.py check
  python3 drive_client.py download <id> <ruta>
  python3 drive_client.py upload <ruta> [nombre] [parent_id]
  python3 drive_client.py ls [parent_id]
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
    def __init__(self):
        self._cid = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        self._sec = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        self._refresh = os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN")
        faltan = [k for k, v in (
            ("GOOGLE_OAUTH_CLIENT_ID", self._cid),
            ("GOOGLE_OAUTH_CLIENT_SECRET", self._sec),
            ("GOOGLE_OAUTH_REFRESH_TOKEN", self._refresh),
        ) if not v]
        if faltan:
            raise DriveError("Faltan variables de entorno: " + ", ".join(faltan) +
                              " (correr drive_authorize_web.py una vez para obtener el refresh token).")
        self._token = None
        self._exp = 0.0

    # ---------- autenticacion (cambia el refresh token por un access token de corta duracion) ----------
    def _access_token(self):
        if self._token and time.time() < self._exp - 60:
            return self._token
        data = urllib.parse.urlencode({
            "client_id": self._cid,
            "client_secret": self._sec,
            "refresh_token": self._refresh,
            "grant_type": "refresh_token",
        }).encode()
        r = self._open(urllib.request.Request(TOKEN_URL, data=data), auth=False)
        j = json.loads(r)
        if "access_token" not in j:
            raise DriveError("No se pudo renovar el token: " + json.dumps(j)[:400])
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
        """Archivos cuyo nombre empieza por `prefix` (Drive solo busca por palabra; se filtra aqui)."""
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
        """Sube (multipart) y VERIFICA md5 contra lo que Drive guardo. Con el scope `drive` completo,
        `parent_id` puede ser CUALQUIER carpeta de Johnny -- no esta limitado a carpetas creadas por esta
        app (esa era la restriccion de `drive.file`, ver nota de diseno arriba). Sin `parent_id` va a la
        raiz de Mi unidad. Si ya existe un archivo con ese nombre en el mismo destino, lo reemplaza (mismo
        ID) para no duplicar."""
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
        name = argv[3] if len(argv) > 3 else None
        parent_id = argv[4] if len(argv) > 4 else None
        print(json.dumps(d.upload(argv[2], parent_id, name), indent=1))
    elif cmd == "ls":
        parent_id = argv[2] if len(argv) > 2 else "root"
        for f in d.ls(parent_id):
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
