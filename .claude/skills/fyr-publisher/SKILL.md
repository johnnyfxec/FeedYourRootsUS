---
name: fyr-publisher
description: Orquestador de publicación en redes sociales de FYR. Lee piezas ya ensambladas en Content_Pieces, deriva a qué plataformas les toca ir según su Tipo de Pieza, respeta la ventana de cautela por plataforma, despacha la llamada correcta a cada uno de los 7 scripts de publicación ya verificados (Instagram, Facebook, Pinterest, TikTok, YouTube — carrusel y video), usa siempre el copy real aprobado (nunca inventa captions), y escribe de vuelta Estado/Post ID/Link en Airtable sin que un fallo en una plataforma oculte el éxito en otra. Usar cuando el usuario pida "publica el lote de hoy", "publica PZA_X", "qué está pendiente de publicar" o "revisa el estado de publicación".
---

# FYR Publisher

Orquestador de publicación — la última capa del pipeline de FYR. `fyr-content` genera el brief y el copy; `fyr-video-assembler`/`assemble.py` producen el archivo final en `Content_Pieces/`; **esta skill es la única que toca redes sociales de verdad.** Ninguna otra skill del repo publica, ni automática ni manualmente — confirmado y corregido explícitamente en `CHANGELOG.md` 27/28-oct-2026.

## Principio rector

Esta skill nunca decide contenido. No elige qué decir, no acorta un caption, no inventa un board, no genera una portada. Todo lo que publica ya fue decidido por una persona o por `fyr-content` en el momento de crear la pieza — `fyr-publisher` **lee y despacha**, nunca **redacta ni improvisa**. La primera vez que se construyó esta skill (31-oct-2026), varios posts de prueba salieron con captions inventados de dos frases en vez del copy real ya aprobado en Airtable — el dueño del producto lo notó de inmediato y fue correcto que lo notara. Esta regla existe por esa razón exacta, no en abstracto.

---

## 0. Configuración (leer siempre primero)

Esta skill es portable entre marcas. Antes de cualquier publicación, leer `brand.config.yaml` en la raíz del repo activo — específicamente la sección `publicacion:`. Si no existe esa sección, **detenerse y pedirla** — no asumir valores ni field IDs.

```yaml
publicacion:
  content_pieces_table: tblevmNSbGTzdjuDF
  fields:
    id_pieza: fld1g5OjdT2BlFdmr
    tipo_pieza: fld7zgQouWTYgQdJ3
    estado_produccion: fldqEyriByKYZ0t3n
    copy_completo: fldYXJcdumHdu9du6
    carpeta_drive: fldpu7xim0PtA1tJS
    fecha_publicacion_programada: fldrMl8gQKUBa7j1T
    fecha_publicacion: fldzLDKI8biRw0uHZ
    board_pinterest: null   # ver Seccion 7 -- campo todavia no existe
    estado: {instagram: ..., facebook: ..., pinterest: ..., youtube: ..., tiktok: ...}
    post_id: {instagram: ..., facebook: ..., pinterest: ..., youtube: ..., tiktok: ...}
    link_publicacion: {instagram: ..., facebook: ..., pinterest: ..., youtube: ..., tiktok: ...}
  handles: {instagram: ..., facebook: ..., pinterest: ..., tiktok: ..., youtube: ...}
  landing_default: https://feedyourroots.us
  ventana_cautela:
    instagram: {inicio: "2026-10-26", dias: 7}
    # ... una por plataforma, cada una con su propio reloj
  pinterest:
    boards_disponibles: {backyard_chickens_bees: "...", ...}
  tiktok:
    pages_mirror_dir: production/scripts/tiktok/tmp-photos
    pages_base_url: https://feedyourroots.us
```

Todo lo que sigue en esta skill usa estas variables — **nunca hardcodear un field ID, un handle, un board ID o una URL de marca fuera de `brand.config.yaml`.** La lógica (cómo decide qué publicar, cómo respeta la ventana, cómo despacha, cómo escribe de vuelta) es 100% genérica; lo único que cambia entre marcas es este archivo.

Variables de entorno (plataforma, nunca en el repo — ver memoria del proyecto `credenciales-apis.md` para nombres reales, no reconstruir de memoria): `META_SYSTEM_USER_TOKEN`, `META_PAGE_ID`, `META_PAGE_ACCESS_TOKEN` (opcional, se deriva solo), `META_IG_BUSINESS_ID`, `PINTEREST_ACCESS_TOKEN`, `TIKTOK_ACCESS_TOKEN`, `TIKTOK_REFRESH_TOKEN`, `TIKTOK_CLIENT_KEY`/`SECRET`, `GOOGLE_OAUTH_CLIENT_ID`/`SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN_YT`, `AIRTABLE_API_KEY`.

---

## 1. Regla crítica de URLs — de dónde se resuelve cada archivo

**Toda URL de imagen/video que se pasa a un script de publicación se resuelve SIEMPRE desde `Content_Pieces/PZA_X/<fecha>/` (campo `carpeta_drive` de la pieza) — NUNCA desde `Assets`/banco de stock,** aunque Airtable permita técnicamente enlazar cualquiera de los dos en `Assets Usados`. Solo `Content_Pieces/` tiene permiso público (`anyone`/reader); `Assets/` no, y una URL de ahí falla con 403 o `{"message":"Sorry, this image is broken."}` según la plataforma.

**Verificar SIEMPRE antes de publicar, nunca asumir que una URL sirve:**
```bash
curl -sL -o /dev/null -w "%{content_type} %{http_code} %{size_download}\n" "https://drive.google.com/uc?export=download&id=<FILE_ID>"
```
`content_type: text/html` → no es pública (login/advertencia) → NO usar, detenerse y avisar. `image/*` o `video/*` con tamaño correcto → sirve.

**Excepción real y documentada:** la portada de un video (`Video_Production/PZA_X/FYR_PZA_X_PORTADA_9x16_v1.png`, usada como `cover_image_url` en un Pin de video de Pinterest) vive en `Video_Production/`, que normalmente NO es pública. Para ese caso específico, verificar con el mismo `curl` — si no es pública, **detenerse y pedirle a Johnny que la comparta como "cualquiera con el enlace"**, nunca generar una portada alternativa (nunca extraer un frame del video con ffmpeg — la portada correcta ya existe, fue compuesta durante el ensamblado).

---

## 2. Elegibilidad de plataforma — se deriva, nunca se guarda

No existe (ni debe recrearse) un campo `Plataformas Destino` — se eliminó el 28-oct-2026 por ser 100% derivable de `Tipo de Pieza`:

| Tipo de Pieza | Plataformas elegibles |
|---|---|
| Carrusel | Instagram, Facebook, Pinterest, TikTok |
| Video | Instagram, Facebook, Pinterest, TikTok, YouTube |

---

## 3. Ventana de cautela

Máx. **1 publicación/día por plataforma** durante las primeras 1-2 semanas de **cada cuenta individual** — cada plataforma cuenta su propio reloj desde `ventana_cautela.<plataforma>.inicio` en el config, no comparten ventana entre sí. Pasada la ventana, escalonar igual (no publicar varias piezas de golpe en una cuenta que sigue siendo nueva).

Antes de despachar cualquier publicación: contar cuántas publicaciones reales ya se hicieron en esa plataforma hoy (vía `Fecha de Publicación` en Airtable, filtrando por plataforma y fecha) — si ya hay 1, no publicar más en esa plataforma hoy, seguir con las demás.

---

## 4. El copy real — regla no negociable

**El caption/copy de cada publicación sale SIEMPRE de `Content_Pieces.Copy Completo` (campo `copy_completo` del config) — nunca se inventa, nunca se acorta, nunca se resume.**

Cómo extraer el caption real de ese campo (confirmado contra datos reales de 13 piezas, 31-oct-2026):

1. Si el texto contiene una línea que empieza con `Caption:` — ese es el caption exacto. Usar todo lo que sigue después de `Caption:`, tal cual, sin recortar.
2. Si NO tiene línea `Caption:` (patrón típico de piezas de video): el texto suele terminar con `// <pregunta o CTA>` — el separador `//` marca el cierre real. Usar el **texto completo de `Copy Completo`** como caption (quitando solo los prefijos `S1:`/`S2:`/etc. si estorban la lectura, nunca el contenido). No hay excepción donde valga inventar algo más corto "porque se ve mejor" — ese fue exactamente el error que motivó esta regla.
3. Si el campo está vacío para una pieza que ya debería tenerlo — **detenerse y avisar a Johnny**, nunca publicar sin caption real ni rellenar con algo genérico.

Esta regla aplica igual a **todas** las plataformas: Instagram, Facebook, Pinterest (título/descripción del Pin), TikTok (title/description), YouTube (description). Cada plataforma puede necesitar una porción distinta del mismo `Copy Completo` (ver Sección 7 para Pinterest específicamente), pero el origen del texto es siempre ese campo, nunca una redacción nueva de la skill.

---

## 5. Tabla de despacho — qué script por plataforma y tipo

Los 7 scripts ya existen y están verificados con publicaciones reales (31-oct-2026). Ninguno descarga a disco local salvo cuando es estrictamente necesario (TikTok Photo, por el requisito de dominio verificado — ver Sección 7); todos los demás transmiten en streaming o pasan la URL directa.

| Plataforma | Tipo | Script | Uso |
|---|---|---|---|
| Instagram | Carrusel | `production/scripts/meta/meta_publish_carousel.py` | `"<caption>" <url_img_1> ... <url_img_N>` (2-10 imgs) |
| Instagram | Video (Reel) | `production/scripts/meta/meta_publish_instagram_reel.py` | `"<caption>" <url_video> [--solo-reels]` |
| Facebook | Carrusel | `production/scripts/meta/meta_publish_facebook_carousel.py` | `"<caption>" <url_img_1> ... <url_img_N>` (min 2) |
| Facebook | Video (Reel) | `production/scripts/meta/meta_publish_facebook_reel.py` | `"<caption>" <url_video>` |
| Pinterest | Carrusel (2 Pines) | `production/scripts/pinterest/pinterest_publish_pin.py` | `--board-id <ID> --title "<t>" --description "<d>" --image-url <url> [--link <url>]` — **dos corridas**, ver Sección 7 |
| Pinterest | Video | `production/scripts/pinterest/pinterest_publish_video_pin.py` | `--board-id <ID> --title "<t>" --description "<d>" --video-url <url> --cover-image-url <url> [--link <url>]` |
| TikTok | Video | `production/scripts/tiktok/tiktok_publish_video.py` | `<url_o_ruta_video> "<titulo>" [--publico]` |
| TikTok | Carrusel (fotos) | `production/scripts/tiktok/publish_images_to_pages.py` + `tiktok_publish_photo.py` | dos pasos, ver Sección 7 |
| YouTube | Video | `production/scripts/youtube/youtube_publish_video.py` | `<url_drive> --title "<t>" [--description "<d>"] [--category-id N] [--privacy private\|unlisted\|public]` |

Sin `--publico`/`--privacy public`: todo publica en modo privado/restringido por defecto en **pruebas**. En producción real, usar el nivel de privacidad que corresponda según el estado de auditoría de cada app (ver credenciales-apis.md y Sección 8).

---

## 6. Flujo completo, pieza por pieza

1. Leer `Content_Pieces` filtrando `Estado Producción = Ensamblado` y, para cada plataforma elegible (Sección 2), `Estado <plataforma> = Pendiente`.
2. Para cada plataforma elegible con `Estado = Pendiente`:
   a. Verificar ventana de cautela (Sección 3) — si ya se agotó el cupo de hoy en esa plataforma, saltar, seguir con la siguiente.
   b. Resolver las URLs de imagen/video desde `carpeta_drive` (Sección 1), verificar que sean públicas.
   c. Extraer el copy real de `Copy Completo` (Sección 4).
   d. Despachar el script correspondiente (Sección 5, reglas específicas en Sección 7).
   e. Si el script termina con éxito: resolver el permalink real (varios scripts ya lo hacen — `Ver en: ...` en su salida), y escribir en Airtable: `Estado <plataforma> = Publicado`, `Post ID <plataforma>` (el ID crudo), `Link Publicación <plataforma>` (el permalink real).
   f. Si el script falla: `Estado <plataforma> = Fallido`, no escribir Post ID ni Link, **continuar con las demás plataformas de la misma pieza** — un fallo en una nunca bloquea ni oculta el éxito en otra (principio ya establecido a nivel de pieza en Fase D, Parada 3, aplicado aquí a nivel de plataforma).
3. Cuando **todas** las plataformas elegibles de una pieza queden en `Publicado`: mover `Estado Producción` a `Publicado` y llenar `Fecha de Publicación` (hoy).

---

## 7. Reglas específicas por plataforma (no genéricas, no mover a otra sección)

**Instagram** — `META_SYSTEM_USER_TOKEN` directo (nunca Page token). Reels: `share_to_feed=true` por defecto para que aparezca en feed y en Reels (confirmado contra doc oficial — sin esto, solo aparece en la pestaña Reels).

**Facebook** — requiere `META_PAGE_ACCESS_TOKEN`, **derivado** del System User (`GET /{page_id}?fields=access_token`, nunca el System User directo — ese falla con error de permiso en `/photos` y `/feed`). Los scripts ya lo derivan solos si la variable no está en el entorno. Carrusel real = `/photos` (`published=false` por imagen) + `/feed` con `attached_media` — nunca una sola foto cuando la pieza es Carrusel.

**Pinterest — Carrusel, regla de 2 Pines (dolor/resultado):** cada pieza Carrusel publica **2 Pines independientes**, no 1:
1. **Pin "dolor"** — imagen del slide de agitación (normalmente slide 2). Título/descripción: usar el texto real de ESE slide dentro de `Copy Completo` (no el caption general de IG/FB).
2. **Pin "resultado"** — imagen del slide de cierre (último slide). Mismo criterio de texto real.
Mismo `link` en ambos — mientras no exista blog/journal, usar `landing_default` del config, nunca el link directo al bundle. Board: leer `board_pinterest` del config/pieza si existe (ver más abajo); si no existe el campo o está vacío, **detenerse y preguntarle a Johnny qué board usar** — nunca elegir uno por cuenta propia ni usar siempre el mismo por default.

**Pinterest — Video:** necesita `cover_image_url` obligatorio (omitirlo da un 401 engañoso, no un 400 descriptivo). Usar siempre `Video_Production/PZA_X/FYR_PZA_X_PORTADA_9x16_v1.png` (ver excepción de la Sección 1 sobre hacerla pública). Ventana de poll real: el procesamiento puede tardar varios minutos, no asumir timeout corto como fallo.

**TikTok — fuera del cronograma automático por ahora (ver Sección 9.2).** Lo que sigue documenta el flujo técnico, ya probado, para cuando se reincorpore tras la aprobación de App Review — no correr en el cronograma automático mientras tanto.

**TikTok — Video:** `FILE_UPLOAD` o URL de Drive en streaming (el script ya soporta ambos) — nunca requiere dominio verificado. `TIKTOK_ACCESS_TOKEN` expira en 24h; si falla con `access_token_invalid`, renovar via `TIKTOK_REFRESH_TOKEN` (refresh automático no implementado en el script todavía — ver Sección 9.1).

**TikTok — Carrusel de fotos:** el endpoint de fotos SOLO acepta `PULL_FROM_URL` (no existe `FILE_UPLOAD` para fotos) — exige que la URL esté en un dominio **ya verificado** en developers.tiktok.com. Drive no sirve. Flujo obligatorio en 2 pasos:
1. `publish_images_to_pages.py <urls...>` — convierte a JPEG (TikTok rechaza PNG, confirmado por `file_format_check_failed` real), comitea a `tiktok.pages_mirror_dir` del config (**nunca una carpeta que empiece con `_`** — Jekyll la ignora sin avisar si no hay `.nojekyll`), pushea, espera a que Pages lo sirva, devuelve URLs reales en `tiktok.pages_base_url`.
2. `tiktok_publish_photo.py` con esas URLs.
Este paso de mirror-a-Pages corre donde corre el resto del orquestador (Code vía Termux hoy, Actions después) — nunca es un paso manual de Johnny.

**YouTube:** streaming puro desde la URL de Drive (nunca descarga a disco), refresh automático via `GOOGLE_OAUTH_REFRESH_TOKEN_YT` (cuenta dedicada, distinta de la de Drive). Sin modo Carrusel — plataforma solo-video.

---

## 8. Administración (borrado) — no solo publisher

`fyr-publisher` también administra lo que ya publicó, no solo publica:

| Plataforma | Borrado vía API | Comando |
|---|---|---|
| Instagram | Sí | `DELETE https://graph.facebook.com/v21.0/<media_id>?access_token=$META_SYSTEM_USER_TOKEN` |
| Facebook | Sí | `DELETE https://graph.facebook.com/v21.0/<post_id>?access_token=$META_PAGE_ACCESS_TOKEN` |
| Pinterest | Sí | `DELETE https://api.pinterest.com/v5/pins/<pin_id>` (Bearer `$PINTEREST_ACCESS_TOKEN`) |
| YouTube | **No con el scope actual** — `GOOGLE_OAUTH_REFRESH_TOKEN_YT` se autorizó con `youtube.upload`, insuficiente para `videos.delete`. Requiere re-autorizar con scope `youtube`/`youtube.force-ssl` antes de poder automatizar esto. | Manual: YouTube Studio → Contenido → Eliminar |
| TikTok | **No existe endpoint de borrado en la Content Posting API**, en ninguna versión. | Manual, desde la app |

---

## 9. Ejecución, cronograma y pendientes conocidos

### 9.1 Modelo de ejecución real: Code dirige, Actions ejecuta

No es "Code O Actions" — es Code decidiendo y Actions corriendo, mismo patrón exacto que ya funciona en `render-video.yml` (Code empuja `production/queue/<pieza>.env` o dispara `workflow_dispatch`; el job de Actions, con los secrets ahí, hace el trabajo real). Para `fyr-publisher`:

1. **Code** (vía un trigger programado, no bajo demanda cada vez) lee `Content_Pieces`, aplica la ventana de cautela (Sección 3), decide qué pieza+plataforma le toca publicar hoy.
2. **Code** dispara un workflow de Actions por cada publicación que le toca (mismo mecanismo de cola que ya usa el render de video), pasándole la pieza, la plataforma y lo ya resuelto (URLs, copy real, board).
3. **Actions**, con los secrets de la plataforma correspondiente ya registrados ahí, corre el script de despacho (Sección 5) y devuelve el resultado.
4. **Code** recibe el resultado y escribe de vuelta en Airtable (Sección 6, paso e/f).

Esto todavía no está construido — el workflow de Actions para publicación no existe (a diferencia de `render-video.yml`, que sí). Mientras no exista, el flujo real es Code completo de punta a punta (como se probó toda esta sesión, desde Termux) — funciona igual, solo que sin la capa de Actions todavía.

**Bloqueantes confirmados para dar el salto a Actions real:**
- [ ] Confirmar que los secrets de las 5 plataformas estén replicados en GitHub Actions (hoy solo confirmados en el `.env` de Termux — no se pudo verificar desde una sesión en la nube, el proxy bloquea leer Secrets).
- [ ] Refresh automático de `TIKTOK_ACCESS_TOKEN` (hoy es manual, vía `tiktok_authorize_web.py`) — sin esto, cualquier corrida de TikTok sin supervisión falla pasadas las 24h. Punto discutible: con TikTok fuera del cronograma (ver 9.2), este bloqueante deja de ser urgente para el resto de plataformas.
- [ ] Construir el workflow de Actions en sí (no existe todavía).

### 9.2 Cronograma automático real — qué entra hoy y qué no (decisión 31-oct-2026)

| Plataforma | Estado en el cronograma |
|---|---|
| Instagram | Dentro, programado |
| Facebook | Dentro, programado |
| Pinterest | Dentro, programado |
| YouTube | **Bloqueado a `private` por Google, confirmado — no es decisión nuestra.** Construido y verificado, pero no se promete `public` en el cronograma todavía (ver abajo) |
| TikTok | **Fuera del cronograma por completo, sin fecha.** Mientras la app no esté auditada, cualquier post real exige alternar la cuenta entre privada/pública a diario (`unaudited_client_can_only_post_to_private_accounts`) — eso rompe el punto mismo de automatizar sin supervisión. Se reincorpora cuando llegue la aprobación de App Review, no antes. |

**YouTube — por qué se queda en privado (confirmado contra documentación oficial de Google, 31-oct-2026, no es incertidumbre):** desde el 28-julio-2020, **todo video subido vía la YouTube Data API desde un proyecto de API no auditado queda forzado a `private`, sin importar el `privacyStatus` que se mande en la petición.** No es la verificación de teléfono del canal (eso es otra cosa, y no bloquea videos cortos en público) ni la pantalla de consentimiento OAuth ("Google no ha verificado esta app", ya resuelta poniendo el proyecto en Production) — es un trámite tercero y separado: el **"YouTube API Services Compliance Audit"**, exactamente la misma categoría que el App Review de TikTok y el Standard access de Pinterest — aprobación externa de Google, no algo que un script pueda rodear.

**Acción pendiente (Johnny):** enviar el **"YouTube API Services Audit and Quota Extension Form"** desde `console.cloud.google.com`, proyecto de la cuenta dedicada (canal `UC5ntyoURYmn-qyPfOVkMe2w`). Hasta que se apruebe, `youtube_publish_video.py` se sigue invocando con `--privacy private` en el cronograma real — un video ya bloqueado en `private` por este motivo **tampoco se puede pasar a público a mano después** en YouTube Studio, hay que esperar la aprobación y volver a subirlo.

### 9.3 Pendientes técnicos restantes

- [ ] Scope de YouTube ampliado (`youtube`/`youtube.force-ssl`) para poder borrar vía API — hoy solo autorizado con `youtube.upload`.
- [ ] Campo `Board Pinterest` en `Content_Pieces` — todavía no existe. Hasta que exista, esta skill **siempre pregunta**, nunca asume un board.
- [ ] Facebook vía Buffer vs. API directa — ya resuelto a favor de API directa (Sección 7), este punto queda cerrado, se deja aquí solo como registro.

---

## 10. Reglas no negociables

- **El copy siempre sale de `Copy Completo`, nunca se inventa** (Sección 4) — la regla que motivó reescribir esta skill desde cero una vez.
- **Las URLs siempre se resuelven desde `Content_Pieces`, nunca desde `Assets`** (Sección 1), y siempre se verifican con `curl` antes de usarlas.
- **Un fallo en una plataforma nunca bloquea ni oculta el éxito en otra** (Sección 6).
- **Nunca se elige un board de Pinterest por cuenta propia** mientras no exista el campo `Board Pinterest` — se pregunta.
- **Nunca se genera una portada nueva** cuando ya existe una real en `Video_Production/` — se usa esa, y si no es pública se pide que la compartan, nunca se improvisa un reemplazo.
- **Nada se marca `Publicado` sin que el script haya devuelto un ID real** — nunca optimismo, nunca "debería haber funcionado".
- **Fail loudly:** field ID faltante en el config, `Copy Completo` vacío, URL no pública, board sin definir → detenerse y reportar, nunca simular éxito parcial ni rellenar con un valor inventado.
