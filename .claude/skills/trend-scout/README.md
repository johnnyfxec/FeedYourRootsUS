# trend-scout

Skill 2 de 3 del sistema de contenido viral (productora → **buscadora** → performance).

## Instalación

1. Copiar la carpeta `trend-scout/` a `/mnt/skills/user/` (o donde vivan tus skills de usuario), junto a `fyr-content/`.
2. Copiar `brand.config.example.yaml` a la raíz de tu repo activo como `brand.config.yaml` y ajustar valores.
3. Importar `Trend_Signals_Airtable_Import.csv` a tu base de Airtable (borrar la fila TR-0000 de ejemplo tras importar).
4. (Opcional, gratis) Crear cuenta en trendsmcp.ai y conectar el MCP si quieres una segunda fuente además de TikTok Creative Center.

## Primer uso sugerido

"Busca tendencias en Home & Garden esta semana" → dispara el Flujo A completo.
"Analiza este video: [URL]" → dispara el Flujo B (deconstrucción puntual).

## Sin costo, sin conexiones nuevas

La skill funciona de entrada solo con `web_fetch`/`web_search` (TikTok Creative Center) y las herramientas locales `yt-dlp` + `ffmpeg` para deconstrucción de video. Apify y trendsmcp son mejoras opcionales, nunca requisitos.

Ver `references/fuentes.md` para el detalle de cada fuente y `references/schema_trend_signals.md` para el diccionario de datos completo de la tabla Airtable.
