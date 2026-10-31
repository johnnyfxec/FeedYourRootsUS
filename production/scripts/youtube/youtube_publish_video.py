#!/usr/bin/env python3
"""Publica un video en YouTube via YouTube Data API v3 (videos.insert, resumable upload).

Formaliza el script de prueba puntual (`youtube_upload_test.py`, nunca llego a git --
vivia untracked en Termux) que confirmo el 28-oct-2026 que la cuenta de Google dedicada
+ canal nativo (no Brand Account) resuelve el bug estructural documentado en
`knowledge/FYR_Plan_Publicacion_Automatizada.md` Seccion 8. Dos diferencias reales frente
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

Variables de entorno requeridas (ya en el .env real, ninguna nueva que generar):
  GOOGLE_OAUTH_CLIENT_ID / GOOGLE_OAUTH_CLIENT_SECRET -- mismo client "Aplicacion de
                            escritorio" que ya usa drive_client.py (compartido con Drive,
                            confirmado en memoria del proyecto -- no es un client nuevo).
  GOOGLE_OAUTH_REFRESH_TOKEN_YT -- refresh token de la cuenta de Google DEDICADA al canal
                            de YouTube (distinta cuenta de la de Drive -- variable separada
                            a proposito, nunca usar GOOGLE_OAUTH_REFRESH_TOKEN aqui, ese es
                            el de Drive y apunta a otra cuenta).

Uso:
    python3 youtube_publish_video.py <ruta_al_mp4> --title "<titulo>" \\
        [--description "<descripcion>"] [--category-id 26] \\
        [--privacy private|unlisted|public]

    Sin --privacy: sube como "private" (default seguro, igual criterio que TikTok
    SELF_ONLY/Meta -- nunca public por defecto en una corrida de prueba).

Limites y notas reales (API Data v3, no estimados):
  Cuota default de proyecto nuevo: 10,000 unidades/dia, videos.insert cuesta 1,600 ->
  ~6 subidas/dia (ver Plan de publicacion Seccion 1). Pedir aumento de cuota solo cuando
  el volumen real lo exija.
  La subida es un PUT unico del binario completo (sin Content-Range) -- confirmado
  funcionando end-to-end en la prueba real del 28-oct (HTTP 200, video lD4ND1gPI74). Las
  piezas de video de FYR (9:16, ~30-40s, 20-30MB) no requieren fragmentacion; si en el
  futuro se suben archivos mucho mas grandes, agregar manejo de Content-Range por chunks
  aqui (mismo aviso que ya tiene tiktok_publish_video.py para su propio limite de 64MB).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TOKEN_URL = "https://oauth2.googleapis.com/token"
UPLOAD_URL = "https://www.googleapis.com/upload/youtube/v3/videos"

_PRIVACY_CHOICES = ("private", "unlisted", "public")


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

    def upload(self, video_path, title, description, category_id, privacy_status):
        if not os.path.isfile(video_path):
            raise YouTubeError(f"No existe el archivo: {video_path}")
        video_size = os.path.getsize(video_path)

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

        # ---------- Paso 2: subir el binario completo (confirmado funcionando sin
        # fragmentar ni enviar Content-Range -- ver docstring) ----------
        print(f"Subiendo {video_size} bytes ...")
        with open(video_path, "rb") as f:
            video_data = f.read()
        put_req = urllib.request.Request(
            upload_url,
            data=video_data,
            headers={"Content-Type": "video/mp4"},
            method="PUT",
        )
        try:
            with urllib.request.urlopen(put_req, timeout=600) as r:
                body = json.loads(r.read())
                status = r.status
        except urllib.error.HTTPError as e:
            sys.exit(f"Subida fallo con HTTP {e.code}: {e.read().decode()[:800]}")
        print(f"  Upload status: {status}")

        video_id = body.get("id")
        channel_title = body.get("snippet", {}).get("channelTitle")
        channel_id = body.get("snippet", {}).get("channelId")
        if not video_id:
            sys.exit(f"La respuesta no trajo id de video: {json.dumps(body)[:600]}")

        return {"id": video_id, "channelTitle": channel_title, "channelId": channel_id, "raw": body}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video_path", help="Ruta local al archivo .mp4 a subir.")
    parser.add_argument("--title", required=True, help="Titulo del video.")
    parser.add_argument("--description", default="", help="Descripcion del video.")
    parser.add_argument("--category-id", default="26", help="categoryId numerico de YouTube (default 26 = Howto & Style).")
    parser.add_argument("--privacy", choices=_PRIVACY_CHOICES, default="private", help="privacyStatus (default: private).")
    args = parser.parse_args()

    yt = YouTube()
    result = yt.upload(args.video_path, args.title, args.description, args.category_id, args.privacy)

    print(f"\nPUBLICADO con exito.")
    print(f"video_id: {result['id']}")
    print(f"channelTitle: {result['channelTitle']}")
    print(f"channelId: {result['channelId']}")
    print(f"Ver en: https://www.youtube.com/watch?v={result['id']}")


if __name__ == "__main__":
    main()
