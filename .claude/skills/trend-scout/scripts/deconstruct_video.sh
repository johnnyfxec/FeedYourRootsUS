#!/usr/bin/env bash
# trend-scout / deconstruct_video.sh
# Uso: ./deconstruct_video.sh "<URL>" <carpeta_salida>
# Descarga subtítulos si existen (gratis), extrae frames por cambio de escena,
# y deja todo listo en <carpeta_salida> para que Claude lea los frames con `view`.
# Borra el video/audio descargado al final — solo deja frames + transcript.

set -e

URL="$1"
OUTDIR="${2:-./trend_scout_tmp}"

if [ -z "$URL" ]; then
  echo "Uso: $0 <URL> [carpeta_salida]"
  exit 1
fi

mkdir -p "$OUTDIR"
cd "$OUTDIR"

echo "== Paso 1: intentando subtítulos (gratis, sin descargar video) =="
yt-dlp --write-auto-sub --sub-lang en --skip-download -o "transcript.%(ext)s" "$URL" 2>&1 | tee yt_dlp_subs.log || true

if ls transcript*.vtt >/dev/null 2>&1; then
  echo "OK: subtítulos encontrados."
else
  echo "AVISO: sin subtítulos disponibles. El análisis será solo visual (frames) salvo que se provea Whisper/Groq API key."
fi

echo "== Paso 2: descargando video para extracción de frames =="
yt-dlp -f "best[height<=720]" -o "source_video.%(ext)s" "$URL"

echo "== Paso 3: extrayendo frames por cambio de escena (barato en tokens) =="
VIDEO_FILE=$(ls source_video.* | head -n1)
ffmpeg -y -i "$VIDEO_FILE" -vf "select='gt(scene,0.3)'" -vsync vfr -frame_pts true "frame_%03d.jpg" -loglevel error

FRAME_COUNT=$(ls frame_*.jpg 2>/dev/null | wc -l)
echo "Frames extraídos: $FRAME_COUNT"

echo "== Paso 4: limpieza — borrando video/audio fuente, conservando solo frames + transcript =="
rm -f "$VIDEO_FILE"

echo "== Listo. Contenido de $OUTDIR: =="
ls -la

echo ""
echo "Siguiente paso (lo hace Claude, no este script): leer cada frame_*.jpg con la tool 'view'"
echo "y cruzar con transcript*.vtt (si existe) para completar el Question Test y el Brief_Adaptacion."
