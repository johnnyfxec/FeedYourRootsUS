# Fuentes de señales de tendencia

Todas las fuentes están ordenadas de más a menos preferida. La skill SIEMPRE intenta la Vía Gratuita primero. La Vía de Pago solo se usa si el usuario confirma explícitamente que tiene el MCP/servicio conectado.

---

## 1. TikTok Creative Center (gratuita, sin cuenta)

URL base: `https://ads.tiktok.com/business/creativecenter/trends/home/pc/en`

No requiere API key ni MCP. Se accede con `web_fetch` directo a las páginas de:
- Trending Hashtags: `.../creativecenter/inspiration/popular/hashtag/pc/en`
- Trending Sounds: `.../creativecenter/inspiration/popular/music/pc/en`
- Trending Videos: `.../creativecenter/inspiration/popular/video/pc/en`

Filtros disponibles vía parámetros de URL: `period` (7/30/120 días), `region` (código de país, ej. `US`), `industry_slug` (ej. `home_garden`).

**Limitación conocida:** es una SPA (React) — `web_fetch` puede devolver solo el shell HTML sin los datos, que cargan por JS. Si esto ocurre:
1. Probar `web_search` con query tipo `"tiktok creative center trending hashtags home garden [mes] [año]"` — terceros suelen republicar los rankings.
2. Fallback a trendsmcp.ai (ver abajo) que sí expone los mismos datos vía API estructurada.

**Regla de honestidad:** si ninguna de las dos vías anteriores devuelve data verificable, decirlo explícitamente al usuario — nunca inventar hashtags o sonidos "trending" a partir de conocimiento general no verificado con fecha.

---

## 2. trendsmcp.ai (gratuita — 100 requests/día, sin tarjeta)

MCP server remoto. Requiere que el usuario cree una cuenta gratuita en trendsmcp.ai y obtenga una API key, luego la conecte como MCP en Claude (esto lo hace el usuario, no la skill).

Si el MCP está conectado (verificar con `tool_search` — buscar "trends" o "tiktok"), tiene tools para:
- Series de tendencia por keyword
- Growth % en ventanas de 1M/3M/12M
- Top trends por tipo (Tiktok/YouTube/Google)

Cubre también Google Trends y YouTube — útil para cruzar si una tendencia de TikTok ya migró a Shorts/Reels (señal de que va madurando, no que está naciendo).

---

## 3. Apify — TikTok Creative Center scrapers (de pago tras trial)

Solo si el usuario confirma que tiene cuenta Apify y el MCP de Apify conectado. Actors relevantes (buscar por nombre exacto en Apify Store, no adivinar IDs):
- "TikTok Hashtag Trends Scraper & Breakout Radar" — momentum, top creators, multi-país
- "TikTok Creative Center Scraper" (all-in-one) — hashtags + sonidos + videos + top ads

Output es JSON estructurado con rank, views, growth curve — más rico que web_fetch pero con costo de créditos por run.

**No usar Apify si el usuario no lo ha mencionado explícitamente como disponible.** No asumir que existe.

---

## 4. Deconstrucción de videos puntuales — claude-video / yt-dlp + ffmpeg (gratuita, local)

Cuando una señal de tendencia (hashtag/sonido) tiene videos líderes identificables por URL, se deconstruyen con herramientas locales — no requiere ningún MCP:

```bash
pip install yt-dlp --break-system-packages
pkg install ffmpeg -y   # Termux; en el sandbox de bash_tool puede ya estar disponible
```

Flujo mínimo (sin necesidad del skill claude-video instalado — se puede replicar a mano):
1. `yt-dlp --write-auto-sub --sub-lang en --skip-download [URL]` → intenta traer subtítulos gratis primero.
2. Si no hay subtítulos: `yt-dlp -f best -o video.mp4 [URL]` y extraer frames clave con `ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)'" -vsync vfr frame_%03d.jpg` (cambio de escena, no cada segundo — más barato en tokens).
3. Frames se leen con `view` (son imágenes) para identificar: hook visual del segundo 0-3, ritmo de cortes, paleta, si hay texto en pantalla.
4. Si el video no tiene subtítulos y se necesita el hook verbal exacto, se informa al usuario que requeriría Whisper (Groq tiene tier gratis, pero necesita API key que el usuario debe proveer) — no bloquear el análisis visual por esto.

**Nota legal/ética:** solo descargar contenido público para análisis de estructura (fair use de investigación de mercado), nunca para republicar el video ajeno. El output de este análisis es siempre una descripción en texto de la estructura, jamás el video o audio en sí.

---

## Resumen de qué requiere qué

| Fuente | Costo | Requiere acción previa del usuario |
|---|---|---|
| TikTok Creative Center vía web_fetch/web_search | Gratis | Ninguna |
| trendsmcp.ai | Gratis (100 req/día) | Crear cuenta + conectar MCP |
| Apify actors | De pago | Cuenta Apify + MCP conectado |
| yt-dlp + ffmpeg | Gratis | Ninguna (herramientas ya en el entorno) |
| Whisper (Groq) | Gratis con límite | API key del usuario |
