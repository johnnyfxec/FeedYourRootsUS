#!/usr/bin/env python3
"""Prueba del cliente de Drive contra un servidor Drive FALSO local (no toca Google)."""
import hashlib, json, os, re, tempfile, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import drive_client as dc

FILES = {}  # id -> dict(meta, data)
N = [0]

def newid():
    N[0] += 1
    return f"id{N[0]:04d}"

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, obj, code=200, raw=None):
        b = raw if raw is not None else json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def _body(self):
        return self.rfile.read(int(self.headers.get("Content-Length", 0)))
    def do_POST(self):
        u = urllib.parse.urlparse(self.path); b = self._body()
        if u.path == "/token":
            assert b"grant_type=refresh_token" in b
            return self._send({"access_token": "tok", "expires_in": 3600})
        assert self.headers["Authorization"] == "Bearer tok"
        if u.path == "/upload/drive/v3/files":
            return self._multipart(b, None)
        if u.path == "/drive/v3/files":
            j = json.loads(b); i = newid()
            FILES[i] = {"meta": {"id": i, "name": j["name"], "mimeType": j["mimeType"], "parents": j["parents"], "trashed": False}, "data": b""}
            return self._send(FILES[i]["meta"])
    def do_PATCH(self):
        u = urllib.parse.urlparse(self.path); b = self._body()
        m = re.match(r"/upload/drive/v3/files/(\w+)", u.path)
        if m: return self._multipart(b, m.group(1))
        m = re.match(r"/drive/v3/files/(\w+)", u.path)
        FILES[m.group(1)]["meta"]["trashed"] = json.loads(b)["trashed"]
        return self._send({"id": m.group(1), "trashed": True})
    def _multipart(self, b, fid):
        parts = b.split(b"\r\n--")  # [0]=--bnd+meta ...
        meta = json.loads(re.search(rb"\r\n\r\n(\{.*?\})\r\n", b, re.S).group(1))
        data = b.split(b"\r\n\r\n", 2)[2].rsplit(b"\r\n--", 1)[0]
        if fid is None:
            fid = newid(); FILES[fid] = {"meta": {"id": fid, "mimeType": "x", "parents": meta["parents"], "trashed": False}, "data": b""}
        FILES[fid]["meta"].update(name=meta["name"], md5Checksum=hashlib.md5(data).hexdigest(), size=str(len(data)))
        if os.environ.get("CORRUPT"): FILES[fid]["meta"]["md5Checksum"] = "0" * 32
        FILES[fid]["data"] = data
        return self._send(FILES[fid]["meta"])
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = urllib.parse.parse_qs(u.query)
        m = re.match(r"/drive/v3/files/(\w+)$", u.path)
        if m:
            f = FILES[m.group(1)]
            return self._send(None, raw=f["data"]) if q.get("alt") == ["media"] else self._send(f["meta"])
        qq = q["q"][0]; name = re.search(r"name = '(.*?)'", qq)
        par = re.search(r"'(\w+)' in parents", qq)
        out = [f["meta"] for f in FILES.values() if not f["meta"]["trashed"]
               and (not name or f["meta"]["name"] == name.group(1)) and (not par or par.group(1) in f["meta"]["parents"])]
        return self._send({"files": out})

srv = HTTPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{port}"
dc.TOKEN_URL = base + "/token"; dc.API = base + "/drive/v3/files"; dc.UPLOAD = base + "/upload/drive/v3/files"

d = dc.Drive("cid", "sec", "rt")
tmp = tempfile.mkdtemp()
raiz = d.mkdir("PZA_9.9", "ROOT"); assert d.mkdir("PZA_9.9", "ROOT")["id"] == raiz["id"], "mkdir debe ser idempotente"
sub = d.mkdir("2026-10-14", raiz["id"])
p = os.path.join(tmp, "a.png"); open(p, "wb").write(os.urandom(300000))
up = d.upload(p, sub["id"], "FYR_PZA_9.9_S1_4x5_v1.png")
again = d.upload(p, sub["id"], "FYR_PZA_9.9_S1_4x5_v1.png"); assert again["id"] == up["id"], "re-subida debe reemplazar, no duplicar"
assert len(d.ls(sub["id"])) == 1
out = os.path.join(tmp, "dl", "b.png"); d.download(up["id"], out); assert open(out, "rb").read() == open(p, "rb").read()
assert d.find("FYR_PZA_9.9_S1_4x5_v1.png", sub["id"])[0]["id"] == up["id"]
d.trash(up["id"]); assert d.ls(sub["id"]) == []
os.environ["CORRUPT"] = "1"
try:
    d.upload(p, sub["id"], "mala.png"); raise SystemExit("FALLO: debio detectar md5 distinto")
except dc.DriveError as e:
    assert "NO verificada" in str(e)
try:
    dc.Drive(None, None, None) if not os.environ.get("GOOGLE_OAUTH_CLIENT_ID") else None
    raise SystemExit("FALLO: debio exigir variables")
except dc.DriveError as e:
    assert "Faltan variables" in str(e)
print("OK: mkdir idempotente, subida verificada, reemplazo sin duplicar, descarga, papelera, md5 corrupto detectado, variables obligatorias")
