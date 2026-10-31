#!/usr/bin/env python3
"""Publica un video en YouTube via YouTube Data API v3 (videos.insert, resumable upload).

Formaliza el script de prueba puntual (`youtube_upload_test.py`, nunca llego a git --
vivia untracked en Termux) que confirmo el 28-oct-2026 que la cuenta de Google dedicada
+ canal nativo (no Brand Account) resuelve el bug estructural documentado en
`knowledge/FYR_Plan_Publicacion_Automatizada.md` Seccion 8. Tres diferencias reales frente
a esa prueba, no cosmeticas:
  1. La prueba recibia un access token ya canjeado a mano por variable de entorno
     (YT_ACCESS_TOKEN) -- de corta duracion, inservible para una corrida futura sin
     repetir el canje manual. Este script canjea el refresh token el mismo, en cada
     corrida, con el mismo patron exacto que ya usa production/scripts/drive/drive_client.py
     (metodo _access_token(), cache en memoria hasta 60s antes de expirar) -- nunca recibe
     un access token por entorno.
  2. La prueba no imprimia el id ni el channelTitle de la respuesta final -- por eso no se
     pudo verificar con certeza si una corrida dada fue la que produjo un video real ya
     documentado en otro lado. Este script siempre imprime ambos al terminar.
  3. La prueba exigia el binario ya descargado en disco local. Este script tambien acepta
     una URL publica de Drive como fuente (--source/posicional) y la transmite en streaming
     directo hacia el PUT de YouTube, SIN escribir el archivo completo a disco en ningun
     punto intermedio -- lee bloques de 1MB de la respuesta de Drive y los manda de
     inmediato al socket de YouTube (mismo patron que necesitaria correr sin cambios dentro
     de un runner headless de GitHub Actions, que tampoco deberia depender de guardar el
     binario completo). Sigue aceptando tambien una ruta local para cuando el binario ya
     esta en disco (p.ej. recien salido de un render local).

Variables de entorno requeridas (ya en el .env real, ninguna nueva que generar):
  GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET -- mismo client "Aplicacion de
                            escritorio" que ya usa drive_client.py (compartido con Drive,
                            confirmado en memoria del proyecto -- no es un client nuevo).
  GOOGLE_OAUTH_REFRESH_TOKEN_YT -- refresh token de la cuenta de Google DEDICADA al canal
                            de YouTube (distinta cuenta de la de Drive -- variable separada
                            a proposito, nunca usar GOOGLE_OAUTH_REFRESH_TOKEN aqui, ese es
                            el de Drive y apunta a otra cuenta).

Uso:
    # Desde una URL publica de Drive (link de "ver" o de descarga directa, cualquiera de
    # los dos formatos -- se normaliza solo) -- streaming puro, nada toca disco local:
    python3 youtube_publish_video.py "https://drive.google.com/file/d/<ID>/view" \\
        --title "<titulo>" [--description "<descripcion>"] [--category-id 26] \\
        [--privacy private|unlisted|public]

    # Desde un archivo ya en disco (p.ej. salida local de un render):
    python3 youtube_publish_video.py ~/video.mp4 --title "<titulo>"

    Sin --privacy: sube como "private" (default seguro, igual criterio que TikTok
    SELF_ONLY/Meta -- nunca public por defecto en una corrida de prueba).

Limites y notas reales (API Data v3, no estimados):
  Cuota default de proyecto nuevo: 10,000 unidades/dia, videos.insert cuesta 1,600 ->
  ~6 subidas/dia (ver Plan de publicacion Seccion 1). Pedir aumento de cuota solo cuando
  el volumen real lo exija.
  La regla critica de Seccion 0 del plan de publicacion sigue aplicando igual en modo
  streaming: la URL de origen debe resolver siempre desde Content_Pieces/PZA_X/<fecha>/
  (publico), nunca desde Assets/banco de stock (403, no publico).
"""
import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"
STREAM_BLOCK_BYTES = 1024 * 1024  # 1MB -- ni todo en memoria, ni todo a disco

_PRIVACY_CHOICES = ("private", "unlisted", "public")

_DRIVE_FILE_PATH_RE = re.compile(r"drive\.google\.com/file/d/([^/?]+)")
_DRIVE_ID_PARAM_RE = re.compile(r"[?&]id=([^&]+)")


def _normalize_drive_url(url):
    """Acepta tanto el link de 'ver' de Drive (.../file/d/<ID>/view...) como el de
    descarga directa (uc?export=download&id=<ID>) -- siempre devuelve la forma de
    descarga directa. Mismo principio que _normalize_image_url() en
    pinterest_publish_pin.py: no hacer que quien llama tenga que saber la diferencia."""
    m = _DRIVE_FILE_PATH_RE.search(url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    if "drive.google.com" in url and "export=download" not in url:
        m = _DRIVE_ID_PARAM_RE.search(url)
        if m:
            return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    return url


def _is_url(s):
    return s.startswith("http://") or s.startswith("https://")


class YouTubeError(RuntimeError):
    pass


class YouTube:
    def __init__(self):
        self._cid = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        self._sec = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        self._refresh = os.environ.get("GOOGLE_OAUTH_REFRESH_TOKEN_YT")
        faltan = [k for k, v in (
            ("GOOGLE_OAUTH_CLIENT_ID", self._cid),
            ("GOOGLE_OAUTH_CLIENT_SECRET", self._sec),
            ("GOOGLE_OAUTH_REFRESH_TOKEN_YT", self._refresh),
        ) if not v]
        if faltan:
            raise YouTubeError(
                "Faltan variables de entorno: " + ", ".join(faltan) +
                " (ver .env real -- GOOGLE_OAUTH_REFRESH_TOKEN_YT es el de la cuenta "
                "dedicada de YouTube, NO el GOOGLE_OAUTH_REFRESH_TOKEN de Drive)."
            )
        self._token = None
        self._exp = 0.0

    # ---------- autenticacion: canjea el refresh token por un access token de corta
    # duracion, el mismo patron exacto que drive_client.py::_access_token() ----------
    def _access_token(self):
        if self._token and time.time() < self._exp - 60:
            return self._token
        data = urllib.parse.urlencode({
            "client_id": self._cid,
            "client_secret": self._sec,
            "refresh_token": self._refresh,
            "grant_type": "refresh_token",
        }).encode()
        req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                j = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise YouTubeError(f"No se pudo renovar el token: HTTP {e.code} {e.read().decode()[:400]}")
        if "access_token" not in j:
            raise YouTubeError("No se pudo renovar el token: " + json.dumps(j)[:400])
        self._token = j["access_token"]
        self._exp = time.time() + int(j.get("expires_in", 3600))
        return self._token

    # ---------- resuelve la fuente (URL de Drive o archivo local) a un stream legible
    # (.read(n)) + el tamano total en bytes, sin materializar el archivo completo ----------
    @staticmethod
    def _open_source(source):
        if _is_url(source):
            url = _normalize_drive_url(source)
            print(f"Abriendo stream desde Drive: {url}")
            resp = urllib.request.urlopen(url, timeout=60)
            size = resp.getheader("Content-Length")
            content_type = resp.getheader("Content-Type", "")
            if content_type.startswith("text/html"):
                resp.close()
                raise YouTubeError(
                    "La URL devolvio text/html en vez del binario -- casi siempre significa "
                    "que el archivo de Drive NO es publico (ver regla critica Seccion 0 del "
                    "plan de publicacion: solo Content_Pieces/ es publico, Assets/ no)."
                )
            if not size:
                resp.close()
                raise YouTubeError(
                    "La respuesta de Drive no trajo Content-Length -- no se puede iniciar "
                    "la sesion resumable sin el tamano exacto de antemano."
                )
            return resp, int(size), True  # True = hay que cerrar el stream al terminar
        if not os.path.isfile(source):
            raise YouTubeError(f"No existe el archivo local: {source}")
        return open(source, "rb"), os.path.getsize(source), True

    def upload(self, source, title, description, category_id, privacy_status):
        stream, video_size, debe_cerrar = self._open_source(source)
        try:
            metadata = {
                "snippet": {
                    "title": title,
                    "description": description or "",
                    "categoryId": str(category_id),
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "selfDeclaredMadeForKids": False,
                },
            }

            # ---------- Paso 1: iniciar la sesion resumable ----------
            print("Iniciando sesion resumable (videos.insert) ...")
            init_req = urllib.request.Request(
                f"{UPLOAD_URL}?{urllib.parse.urlencode({'uploadType': 'resumable', 'part': 'snippet,status'})}",
                data=json.dumps(metadata).encode(),
                headers={
                    "Authorization": f"Bearer {self._access_token()}",
                    "Content-Type": "application/json; charset=UTF-8",
                    "X-Upload-Content-Type": "video/mp4",
                    "X-Upload-Content-Length": str(video_size),
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(init_req, timeout=60) as r:
                    upload_url = r.headers.get("Location")
                    init_status = r.status
            except urllib.error.HTTPError as e:
                sys.exit(f"Init fallo con HTTP {e.code}: {e.read().decode()[:500]}")
            print(f"  Init status: {init_status}")
            if not upload_url:
                sys.exit("La respuesta de init no trajo el header Location (upload URL).")

            # ---------- Paso 2: subir en streaming, bloque a bloque (1MB), sin
            # materializar el binario completo ni en disco ni en memoria ----------
            print(f"Subiendo {video_size} bytes en streaming (bloques de 1MB) ...")
            status, body_bytes, enviados = self._put_stream(upload_url, stream, video_size)
            print(f"  Upload status: {status} ({enviados} bytes enviados)")
            if status not in (200, 201):
                sys.exit(f"Subida fallo con HTTP {status}: {body_bytes.decode(errors='replace')[:800]}")
            body = json.loads(body_bytes)
        finally:
            if debe_cerrar:
                stream.close()

        video_id = body.get("id")
        channel_title = body.get("snippet", {}).get("channelTitle")
        channel_id = body.get("snippet", {}).get("channelId")
        if not video_id:
            sys.exit(f"La respuesta no trajo id de video: {json.dumps(body)[:600]}")

        return {"id": video_id, "channelTitle": channel_title, "channelId": channel_id, "raw": body}

    @staticmethod
    def _put_stream(upload_url, source_stream, total_size):
        """PUT de bajo nivel (http.client, no urllib.request) para poder mandar el body
        bloque a bloque en vez de pasar bytes completos de una sola vez -- urllib.request
        exige tener todo el body en memoria antes de llamar urlopen(), http.client permite
        escribir al socket incrementalmente via conn.send() despues de endheaders()."""
        parsed = urllib.parse.urlsplit(upload_url)
        conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
        conn = conn_cls(parsed.netloc, timeout=600)
        path = parsed.path + (("?" + parsed.query) if parsed.query else "")
        try:
            conn.putrequest("PUT", path)
            conn.putheader("Content-Type", "video/mp4")
            conn.putheader("Content-Length", str(total_size))
            conn.endheaders()
            enviados = 0
            while True:
                bloque = source_stream.read(STREAM_BLOCK_BYTES)
                if not bloque:
                    break
                conn.send(bloque)
                enviados += len(bloque)
            resp = conn.getresponse()
            body_bytes = resp.read()
            status = resp.status
        finally:
            conn.close()
        return status, body_bytes, enviados


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="URL publica de Drive (link de ver o de descarga directa) o ruta local al .mp4.")
    parser.add_argument("--title", required=True, help="Titulo del video.")
    parser.add_argument("--description", default="", help="Descripcion del video.")
    parser.add_argument("--category-id", default="26", help="categoryId numerico de YouTube (default 26 = Howto & Style).")
    parser.add_argument("--privacy", choices=_PRIVACY_CHOICES, default="private", help="privacyStatus (default: private).")
    args = parser.parse_args()

    yt = YouTube()
    result = yt.upload(args.source, args.title, args.description, args.category_id, args.privacy)

    print(f"\nPUBLICADO con exito.")
    print(f"video_id: {result['id']}")
    print(f"channelTitle: {result['channelTitle']}")
    print(f"channelId: {result['channelId']}")
    print(f"Ver en: https://www.youtube.com/watch?v={result['id']}")


if __name__ == "__main__":
    main()
