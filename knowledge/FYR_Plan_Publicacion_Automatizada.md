# FYR — Plan de publicación automatizada (carrusel 4:5 / video 9:16)

**Documento único — consolidado 31-oct-2026.** Fusiona lo que antes vivía separado en dos archivos: `FYR_Plan_Publicacion_Automatizada_v1.md` (diseño original, 16-oct-2026, en el repo) y una continuación `v2.md` (27 al 29-oct-2026) que **nunca llegó a guardarse en el repo** — vivía solo como doc del Project de claude.ai, invisible para Code o cualquier sesión que no tuviera ese Project adjunto. Esa fue la causa real de la duplicación v1/v2: no fue un error de nomenclatura, fue que la mitad del conocimiento más reciente nunca llegó a la fuente de verdad del proyecto. Corregido aquí: un solo documento, en el repo, que cualquier sesión (Code incluido) puede leer.

**Estado general: 4 de 5 plataformas en producción real** (Instagram, Pinterest, YouTube, y TikTok en revisión de App Review). Falta Facebook y el orquestador (`fyr-publisher`, SKILL.md) que una todo lo ya construido.

---

## 0. Qué carpetas de Drive son públicas — regla crítica, aplica a TODAS las plataformas

**Solo `Content_Pieces/` (el output ya ensamblado/producido) tiene permiso público (`anyone`/reader).** La carpeta de banco de assets (tabla `Assets` en Airtable — `STOCK-`, `FYR_ASSET_`, `FYR_LAYOUT_`, etc., material crudo antes de ensamblarse) **no es pública**.

Confirmado empíricamente: un archivo de `Assets` usado como `image_url` directa devolvió 403/login-redirect en todos los formatos de URL de Drive probados. El mismo método con un archivo ya ensamblado de `Content_Pieces` funcionó sin problema (publicación real de Instagram, 26-oct-2026).

**Implicación para `fyr-publisher`:** cualquier lógica que resuelva una URL de imagen/video para publicar debe tomarla SIEMPRE de `Content_Pieces/PZA_X/<fecha>/`, nunca de `Assets`/banco de stock — aunque Airtable permita técnicamente enlazar cualquiera de los dos en `Assets Usados`.

**Para verificar si un archivo de Drive es público antes de usarlo como URL directa:**
```
curl -sL -o /dev/null -w "%{content_type} %{http_code} %{size_download}\n" "https://drive.google.com/uc?export=download&id=<FILE_ID>"
```
`content_type: text/html` → no es público (login/advertencia). `image/jpeg`/`image/png`/`video/mp4` con tamaño correcto → público, sirve para `image_url`/`video_url` directo.

**Caso especial Pinterest:** no sigue el redirect 303 de `drive.google.com/uc?export=download&id=X` (a diferencia de Meta, que sí lo sigue) — ver Sección 7 para el bug exacto y la solución ya implementada en el script.

---

## 0.1 Handles / usernames oficiales por plataforma

Unificados a partir de `feedyourroots_us` (handle que terminó quedando en Instagram, ya que `feedyourroots` sin separador estaba tomado). Cada plataforma tiene sus propias reglas de caracteres, el string exacto varía:

| Plataforma | Handle/username | Notas |
|---|---|---|
| Instagram | `feedyourroots_us` | Minúsculas, guion bajo. |
| Facebook (Página) | `FeedYourRoots.US` | Facebook Páginas **no acepta guion bajo** — solo letras, números y punto. URL: `facebook.com/FeedYourRoots.US`. |
| Pinterest | `FeedYourRoots_US` | Permite guion bajo. |
| TikTok | `FeedYourRoots_US` (o variante en minúsculas) | Permite guion bajo y punto. |
| YouTube | `FeedYourRoots_US` (o variante en minúsculas) | Handle (`@...`) permite letras/números + `_` `-` `.` `·`, 3-30 caracteres. |

**Para captions/menciones (`@...`) y links en `fyr-publisher`:** usar el handle exacto de la tabla por plataforma, nunca asumir que es el mismo string en todas.

---

## 1. Qué cambió respecto a la investigación original (16-oct-2026)

Contexto histórico — por qué los límites de abajo son los correctos y de dónde salen, no una tabla inventada:

| Punto | Investigación original (10-oct) | 2ª IA (16-oct) | Verificado (16-oct) |
|---|---|---|---|
| Límite IG en 24h | "100 (o 50, la doc se contradice)" | 50 | **50** — confirmado en doc oficial de Meta: `content_publishing_limit.quota_total` = 50 por `quota_duration` (86400s). Consultar ese endpoint antes de ráfagas, no asumir. |
| TikTok carrusel vía Buffer | Asumido automatizable | "Buffer no lo soporta, cae en Notification publishing" | Correcto el problema (TikTok separa foto/video estrictamente) — ya no aplica de todos modos, TikTok se resolvió vía API directa (Sección 9). |
| YouTube sin verificar | "100 subidas/día" | "Fuerza los videos a `private` hasta auditoría" | **Ambos mal.** El problema real es cuota: proyecto nuevo = 10,000 unidades/día, `videos.insert` cuesta 1,600 → **~6 subidas/día**. Pasado el límite, falla con 403, no queda privado. |
| App Review de Meta | No verificado | "No se requiere si solo publicas en tus propias cuentas" | Consistente — no bloquea nada mientras FYR publique solo en sus propias cuentas. |

---

## 2. Distribución por plataforma — estado real actual (31-oct-2026)

| Plataforma | Estado | Vía final | Límite real confirmado |
|---|---|---|---|
| **Instagram** | ✅ Producción — carrusel real publicado (29-oct) | API directa (Graph API) | **50 posts/24h** (`content_publishing_limit`) — consultar antes de ráfagas; hasta 15 min, 300MB |
| **Pinterest** | ✅ Producción — Standard access aprobado (29-oct), Pin real publicado | API directa (`/v5/pins`) | Sin carrusel (deprecado 2026) — regla de 2 Pines por pieza, ver Sección 7 |
| **YouTube** | ✅ Resuelto — cuenta de Google dedicada, canal nativo | API directa (`videos.insert`) | **~6 subidas/día con cuota default** — pedir aumento solo cuando el volumen real lo exija |
| **Facebook** | 🔲 Pendiente — siguiente en la cola | Por decidir: Buffer vs. API directa de Meta (ver nota abajo) | — |
| **TikTok** | 🟡 En revisión de App Review (enviado 29-oct) | API directa (Content Posting API) | Mientras no se apruebe: `SELF_ONLY` forzado, cuenta debe estar privada, máx. 5 usuarios/24h |

**Nota sobre Buffer (histórico):** el plan original (16-oct) proponía Buffer Free para Facebook + Pinterest, descartando TikTok de Buffer tras confirmar que no automatiza carrusel ahí. Pinterest terminó resolviéndose vía API directa (Sección 7), no por Buffer — queda abierto si todavía conviene usar Buffer solo para Facebook o si vale la pena buscar API directa de Meta también para FB, dado que Instagram (misma familia de API, Graph API de Meta) ya se resolvió sin Buffer.

---

## 3. Carrusel 4:5 vs video 9:16, por plataforma (endpoints)

| Plataforma | Carrusel 4:5 | Video 9:16 | ¿Mismo endpoint? |
|---|---|---|---|
| Instagram | `ig_publish_carousel`, 2-10 ítems | `ig_publish_reel` (`media_type: 'REELS'`) | Sí — mismo flujo contenedor→publicar, cambia `media_type` |
| Pinterest | **No existe carrusel** — ver Sección 7, regla de 2 Pines independientes | `source_type: video_id` | N/A, Pinterest no traslada 1:1 el carrusel de IG |
| TikTok | Endpoint `photo` (hasta 35 imágenes) | Endpoint `video` | No — dos tipos de contenido separados en la Content Posting API |
| Facebook | `/photos` (subida) + `/feed` con `attached_media` | Endpoint propio de Reels/video | No — rutas y permisos distintos |
| YouTube | No existe — plataforma solo-video | `videos.insert`, cuota ~6/día default | N/A — el skill descarta piezas tipo carrusel antes de intentar publicar aquí |

---

## 4. `fyr-publisher` — qué falta construir, en orden

1. ~~**Esquema Airtable**~~ — ✅ hecho (Sección 5).
2. **Borrar posts/pines/videos de prueba** que quedaron en las plataformas durante las pruebas — ver checklist al final de cada sección de plataforma (6-9).
3. **`SKILL.md` de `fyr-publisher`** — el trabajo real pendiente. Debe:
   - Leer `Content_Pieces` filtrando por `Estado Producción = Ensamblado` y `Estado <plataforma> = Pendiente`.
   - Calcular elegibilidad de plataforma desde `Tipo de Pieza` en el momento (Carrusel → Instagram/Facebook/Pinterest/TikTok; Video → esas 4 + YouTube) — **no** existe un campo `Plataformas Destino` guardado, se eliminó por ser 100% derivable.
   - Respetar la ventana de cautela (Sección 4.1): máx. 1 publicación/día por plataforma durante las primeras 1-2 semanas de cada cuenta — cada plataforma cuenta su propia ventana desde que arrancó, no comparten reloj.
   - Despachar la llamada correcta por tipo de pieza y plataforma (tabla Sección 3). **Pinterest es la excepción: despacha 2 llamadas por pieza, no 1** (regla de 2 Pines, Sección 7).
   - Actualizar `Estado <plataforma>` y `Post ID <plataforma>` al terminar cada una, independientemente de las demás — un fallo en una plataforma no detiene ni oculta el éxito en las otras.
   - Resolver URLs de imagen/video SIEMPRE desde `Content_Pieces`, nunca desde `Assets` (Sección 0).
   - Cuando TODAS las plataformas destino de una pieza queden en `Publicado`, mover `Estado Producción` (`fldqEyriByKYZ0t3n`) a `Publicado`.
4. Completar Facebook (decisión de vía pendiente) y esperar aprobación de TikTok.
5. **Escalonar la publicación** — mismo principio que la ventana de cautela, no publicar varias piezas de golpe en una cuenta nueva.

### 4.1 Ventana de cautela — qué dice realmente la gobernanza

El acuerdo documentado es: *"Escalonar la publicación: 1 pieza/día por cuenta las primeras 1-2 semanas, para no disparar detección de automatización en cuentas nuevas."*

No es "1 publicación diaria hasta el domingo" — es una ventana de **1 a 2 semanas desde que arranca cada cuenta individual**, luego se escala. Instagram arrancó el 26-oct-2026, así que su ventana corre del 26-oct al 2 o 9-nov (decisión abierta: 1 semana si todo va bien, 2 si se quiere más margen). Cada plataforma nueva (Facebook, TikTok cuando se apruebe) empieza su propia cuenta desde cero, no comparte la de Instagram.

### 4.2 Credenciales, por vía

- **Meta (Instagram/Facebook):** app en developers.facebook.com, modo Development, token de usuario Admin/Developer/Tester con `instagram_content_publish`.
- **YouTube:** proyecto de Google Cloud + OAuth "Desktop app" propia (distinta del service account de TTS). Ver Sección 8 para el modelo de cuenta correcto — crítico, hay una trampa estructural real documentada ahí.
- **TikTok:** cuenta business + app de developer de TikTok, credenciales propias para la Content Posting API.
- **Pinterest:** ver Sección 7 — Client ID/Secret + Standard access, scopes `boards:read`, `boards:write`, `pins:read`, `pins:write`.

Nombres reales de las variables de entorno (`.env`): ver memoria del proyecto, `/projects/.../credenciales-apis.md` — fuente única, no reconstruir de memoria.

---

## 5. Esquema Airtable en `Content_Pieces` (`tblevmNSbGTzdjuDF`) — ✅ HECHO (27-oct-2026)

Objetivo: que un fallo en una plataforma no bloquee ni oculte el éxito en otra (mismo principio ya aplicado a nivel de pieza en Fase D, Parada 3 — ahora a nivel de plataforma dentro de la misma pieza). Campos reales (ver `fyr-content/SKILL.md` para los `fieldId` exactos):

- `Estado IG` / `Estado FB` / `Estado Pinterest` / `Estado YouTube` / `Estado TikTok` (singleSelect: No aplica/Pendiente/Publicado/Fallido, cada uno independiente).
- `Post ID IG` / `Post ID FB` / `Post ID Pinterest` / `Post ID YouTube` / `Post ID TikTok` (texto — ID crudo de cada API, para auditar/borrar después). **Pinterest es la única plataforma donde una pieza puede necesitar DOS IDs** (regla de 2 Pines, Sección 7) — el campo sigue siendo texto único; si se guardan dos, usar separador `;`.
- `Fecha Publicación Programada` (date — separado de `Fecha de Generación`, que es cuando se generó el brief).

**Eliminado (28-oct-2026):** `Plataformas Destino` — era 100% derivable de `Tipo de Pieza`, así que `fyr-publisher` calcula la elegibilidad en el momento, nunca de un campo guardado. No recrear.

**Qué NO cambió:** `Estado Producción` (`fldqEyriByKYZ0t3n`) sigue siendo el estado del *proceso de armado* (Brief Generado → Assets en Drive → Ensamblado → Publicado). El orquestador lo mueve a `Publicado` solo cuando todas las plataformas destino quedan en `Publicado`.

**Nota de solape:** `Themes` ya tenía campos `Link Publicación IG/TikTok/Pinterest/FB/YouTube` (tipo url) para el link público del post. Los `Post ID X` de `Content_Pieces` son el ID crudo, no el link — sirven para operaciones de API (borrar, verificar status). Si se quiere también el link público legible, calcularlo desde el ID y escribirlo en `Themes` es un paso aparte que `fyr-publisher` tendría que hacer explícitamente.

---

## 6. Instagram — ✅ PRODUCCIÓN (29-oct-2026)

**Catálogo completo de lo que permite la Graph API en un post** (confirmado contra documentación de Meta, no asumido):

| Elemento | Parámetro | Notas |
|---|---|---|
| Hashtags | — (dentro de `caption`) | Texto plano, Instagram los detecta solo. |
| Menciones (@cuenta) | — (dentro de `caption`) | Texto plano `@feedyourroots_us`. |
| Ubicación | `location_id` | Requiere buscar el ID primero vía Facebook Places Search — no es string libre. |
| Etiquetas de usuario en foto | `user_tags` | Array `{username, x, y}` — solo fotos, no Reels. |
| Texto alternativo (accesibilidad) | `alt_text` | Gratis agregar, buena práctica. |
| Carrusel (2-10 ítems) | `children` (array de container IDs `is_carousel_item: true`) | ✅ Probado con éxito (5 slides reales de PZA_10.4, `media_id: 17996701389021317`). |
| Reels / video | `media_type: REELS` + `video_url` + `cover_url` opcional | Para `Medio = Video`. |
| Audio propio (Reels) | — (incrustado en el archivo) | Catálogo de música con licencia de Instagram NO accesible vía API, solo desde la app a mano. |
| Coautores | `collaborators` | Array de usernames — deben aceptar la invitación. |
| Comentario automático post-publicación | `POST /<media_id>/comments` (llamada separada) | Útil para CTA largo o link de afiliado sin saturar el caption. |
| **Permalink real** | `GET /<media_id>?fields=permalink` (llamada separada) | El shortcode real (`/p/DfFafzPjm2-/`) **NO es derivable** del `media_id` numérico — no hay relación algorítmica. `meta_publish_carousel.py` ya lo resuelve automáticamente; cualquier script nuevo debe hacer lo mismo. |

**Lo que la API NO permite, sin rodeo posible:** programar hora de publicación (no hay `scheduled_publish_time` como en Facebook — lo resuelve el orquestador decidiendo cuándo correr), elegir música con licencia del catálogo, Stories con stickers interactivos vía API.

**Script de producción:** `production/scripts/meta/meta_publish_carousel.py` — flujo completo: child containers (`is_carousel_item: true`) → container padre `CAROUSEL` → polling `status_code=FINISHED` → `media_publish` → resuelve permalink real.

**Pendiente inmediato:**
- [ ] Borrar el post de prueba genérico sobre la portada de PZA_10.4 (media ID `17913152523549908`, container `18105793094229735`) antes de cargar el calendario real: `curl -s -X DELETE "https://graph.instagram.com/v23.0/17913152523549908?access_token=$META_IG_ACCESS_TOKEN"`

---

## 7. Pinterest — ✅ PRODUCCIÓN (29-oct-2026)

**Standard access aprobado.** Scripts: `production/scripts/pinterest/pinterest_authorize_web.py` (autorización) y `pinterest_publish_pin.py` (publicación). Primer Pin real: `pin_id 1151725304742928915`, board "Backyard Chickens & Bees Integration", imagen de PZA_10.4 slide 5.

**Bug real encontrado y corregido: Pinterest no sigue redirects.** A diferencia de Meta, Pinterest no sigue el redirect 303 de `drive.google.com/uc?export=download&id=X` hacia `drive.usercontent.google.com/download?id=X&export=download` — falla con `{"code":1,"message":"Sorry we could not fetch the image."}`. **Solución ya implementada:** `pinterest_publish_pin.py` normaliza automáticamente cualquier URL con ese patrón antes de mandarla a la API (`_normalize_image_url()`). Si se usa otra fuente de imágenes que también redirija, el mismo error puede volver a aparecer.

**Pinterest NO tiene carrusel.** Deprecó los Idea Pins (formato multi-página) en 2026 (anuncio oficial de Pinterest). Formatos vigentes: Pin de imagen única, o Pin de video (hasta 5 min). Un carrusel de Instagram no se traslada 1:1.

**Regla de publicación: 2 Pines por pieza (dolor / resultado).** Cada pieza de carrusel publica 2 Pines independientes, cada uno con su propia imagen, título y descripción — mismo link de destino en ambos, porque no cambia el CTA, cambia la intención de búsqueda que cada imagen capta:
1. **Pin "dolor"** — slide de agitación/problema (normalmente slide 2), orientado a búsqueda de alguien que recién reconoce el problema.
2. **Pin "resultado"** — slide de cierre/resultado, orientado a búsqueda de alguien que ya busca la solución.

Por qué funciona en Pinterest específicamente (y no en IG): Pinterest es un motor de búsqueda visual, cada Pin se indexa de forma independiente por su propia imagen+título+descripción — dos ángulos de búsqueda = más superficie de descubrimiento, no canibalización.

**Sobre el link de destino:** mientras el journal/blog de la página esté vacío, AMBOS pines apuntan a la landing general (`feedyourroots.us`), nunca directo al bundle — tráfico frío directo a venta rinde peor sin explicar el problema primero. Cuando exista contenido de blog, revisar si el Pin de "dolor" debería apuntar ahí — pendiente, no decidido.

**Elección de board:** no hay regla fija — se evalúa pieza por pieza cuál de los 6 boards reales calza mejor con cada ángulo.

**Pendiente antes de formalizar en `fyr-publisher`:** la regla de 2 Pines solo se probó manualmente una vez (29-oct) — falta repetirla con 2-3 piezas más antes de codificarla como lógica fija.

**Lección aprendida: `image_url` necesita un archivo verdaderamente público.** Un primer intento con un archivo de `Assets` (banco, prefijo `STOCK-`) falló con `{"code":235,"message":"Sorry, this image is broken."}` — sin permiso público, a diferencia de `Content_Pieces`. Ver regla crítica completa en Sección 0.

### 7.1 Pin de video — ✅ PRODUCCIÓN (31-oct-2026)

**Flujo real, distinto y más largo que el Pin de imagen.** Pinterest NO acepta una URL de video directa en `/v5/pins` (a diferencia de `image_url` para imágenes) — hay que registrar la subida, subir el binario a un bucket S3 de Pinterest (multipart/form-data, campos de `upload_parameters` tal cual + `file` al final), esperar a que procese, y recién ahí crear el Pin. Script: `production/scripts/pinterest/pinterest_publish_video_pin.py`. Primer Pin de video real: `PZA_9.3`, board "Seed to Pantry Homesteading System".

**`cover_image_url` es obligatorio, aunque la doc "how-to" de Pinterest no lo marque claro.** Omitirlo da un `401 Unauthorized` engañoso (debería ser un `400` descriptivo) — confirmado contra reportes reales de la comunidad de desarrolladores de Pinterest, no asumido. El script lo exige siempre como argumento, nunca opcional.

**De dónde sale la portada — regla fija, no inventar una nueva cada vez:** la imagen de portada ya existe para TODA pieza de video, compuesta durante el ensamblado (ver `FYR_Protocolo_Edicion_Video.md`) y guardada en Drive como `Video_Production/PZA_X/FYR_PZA_X_PORTADA_9x16_v1.png` — **nunca extraer un frame del MP4 con ffmpeg ni generar una portada nueva**, la correcta ya está ahí. Decisión explícita de Johnny (31-oct-2026): no cambiar el pipeline para que esa portada se copie también a `Content_Pieces/` — se mantiene en `Video_Production/` como siempre.

**Excepción real a la regla crítica de la Sección 0:** `Video_Production/` normalmente NO es público — pero el archivo `PORTADA` específico de cada pieza debe compartirse manualmente como "cualquiera con el enlace" (Johnny, desde Drive) antes de poder usarlo como `cover_image_url` de un Pin de video. Esto se va a repetir en cada pieza de video que se publique en Pinterest — no es un paso único. Verificar con el mismo `curl` de la Sección 0 antes de asumir que ya es pública.

**Ventana de poll real medida, no estimada:** el procesamiento del video en Pinterest tardó más de 60s en la prueba real (`PZA_9.3`, archivo de ~25MB, seguía en `status=processing` tras 15 intentos x 4s) — el script quedó ajustado a 40 intentos x 6s (4 min). No tratar un timeout corto como señal de error, es que la ventana original estaba mal calibrada contra el tiempo real de Pinterest.

**Pendiente inmediato:**
- [ ] Borrar el pin de prueba de Sandbox (`1151725304742853168`).
- [ ] Borrar el Pin de video de prueba de `PZA_9.3`.
- [ ] Probar la regla de 2 Pines en 2-3 piezas más antes de formalizarla en `fyr-publisher`.
- [ ] Decidir si el Pin de "dolor" debe apuntar a blog/journal una vez que exista.
- [ ] Decidir si `fyr-publisher` debe recordarle a Johnny compartir la `PORTADA` públicamente antes de intentar un Pin de video (o si el orquestador lo verifica solo con el `curl` de la Sección 0 y se detiene con un mensaje claro si no lo está).

---

## 8. YouTube — ✅ RESUELTO (28-oct-2026): cuenta de Google dedicada con canal nativo

**Estado: conectado y validado.** El canal "Feed Your Roots US" original era una Brand Account "limitada a YouTube" (residuo de infraestructura descontinuada de Google+ Pages) con un bloqueo estructural irresoluble vía OAuth de terceros. La solución fue crear una **cuenta de Google nueva y dedicada**, con un canal que nace como principal/default de esa cuenta (no como Brand Account administrada) — mismo modelo que ya funcionaba con el canal personal de Johnny.

### Qué se hizo
1. Cuenta de Google nueva, correo dedicado.
2. Canal "Feed Your Roots US" creado como canal principal de esa cuenta nueva (no Brand Account) — `channelId: UC5ntyoURYmn-qyPfOVkMe2w`.
3. App de Google Cloud puesta en **Production** (no Testing) — necesario porque Testing + scopes sensibles (`youtube.upload`) da refresh tokens que caducan a los 7 días sin excepción, sin importar la lista de test users.
4. Autorización OAuth completada sin error — al no haber Brand Account vinculada, nunca aparece la pantalla "Elige tu cuenta o una cuenta de marca" que disparaba el bug.
5. Refresh token guardado como `GOOGLE_OAUTH_REFRESH_TOKEN_YT` (variable separada de `GOOGLE_OAUTH_REFRESH_TOKEN`, que sigue siendo el de Drive — son dos cuentas de Google distintas, no deben pisarse).
6. **Prueba real exitosa:** video ID `lD4ND1gPI74`, confirmado `channelTitle: "Feed Your Roots US"` en la respuesta.

### Diagnóstico del bloqueo original (no reintentar estas rutas con una Brand Account "limitada a YouTube")

Google documenta oficialmente que los usuarios con **"channel permissions"** (modelo de manager vía YouTube Studio, post-2021) **no pueden gestionar el canal vía las APIs de YouTube**. Solo el modelo clásico Owner/Manager pre-2021, o un canal nativo de la cuenta, funcionan con OAuth de terceros.

| Ruta descartada | Resultado | Motivo |
|---|---|---|
| Parámetro de API para apuntar a otro canal (`channelId`) | No existe | Solo `onBehalfOfContentOwnerChannel`, exclusivo de YouTube Content Partners con CMS. |
| Service Account | Bloqueado por diseño | Google prohíbe vincular Service Accounts a canales de YouTube. |
| Crear Brand Account "completa" | Ya no existe ese tipo | Descontinuado desde ago-2021. |
| Device Flow en vez de loopback | Mismo bloqueo | Mismo account chooser. |
| Buffer.com | Mismo bloqueo exacto | Debe iniciar sesión como Owner, no Manager — mismo OAuth2 de Google. |
| Google Workspace en vez de Gmail | No resuelve nada | La restricción es sobre el modelo de permisos del canal, no el tipo de cuenta. |

**Pendiente (housekeeping, no bloqueante):**
- [ ] Borrar el canal viejo "Feed Your Roots US" (Brand Account bloqueada, cero suscriptores/videos).
- [ ] Borrar el video de prueba `lD4ND1gPI74`.
- [ ] En el `SKILL.md` de `fyr-publisher`, documentar que la subida usa `GOOGLE_OAUTH_REFRESH_TOKEN_YT` (no la variable de Drive) y requiere descarga previa del binario (`videos.insert` no acepta URL directa, a diferencia de Meta).

---

## 9. TikTok — 🟡 EN REVISIÓN (29-oct-2026): app enviada a App Review

**Estado: app "FYR Content Publisher" en revisión.** App ID `7701834638989477906`. Mientras no llegue la aprobación, opera en Sandbox con las limitaciones de cliente sin auditar.

### Resumen del camino
1. La Content Posting API NO requiere registro legal de empresa (eso es exclusivo de TikTok Ads/Business Center, flujo distinto).
2. Basic Information + verificación de dominio resuelta.
3. Products/Scopes en Sandbox: Login Kit + Content Posting API (Direct Post), scopes `user.info.basic`, `video.publish`, `video.upload`.
4. **Bug no documentado confirmado empíricamente:** el portal rechaza "Invalid Redirect Uri" con cualquier URI con ruta propia, aunque responda HTTP 200 normal — solo la raíz exacta del dominio se deja guardar. Solución: el callback OAuth vive en `index.html` (overlay activado solo si hay `?code=`/`?error=` en la URL).
5. OAuth real exitoso contra Sandbox.
6. Publicación real exitosa vía Content Posting API, Direct Post, flujo `FILE_UPLOAD` (elegido sobre `pull_by_url` para evitar requisito de dominio verificado por video).
7. **Limitaciones de cliente sin auditar (confirmadas con errores reales):**
   - Todo contenido forzado a `SELF_ONLY`, sin importar `privacy_level` pedido.
   - La CUENTA debe estar en modo privado al publicar (error: `unaudited_client_can_only_post_to_private_accounts`), el cambio tarda ~1-2 min en propagar.
   - Máximo 5 usuarios publicando en 24h.
8. Video demo grabado y enviado como parte de App Review.

### Scripts de producción
- `production/scripts/tiktok/tiktok_authorize_web.py` — OAuth, redirect_uri = raíz del dominio (sin servidor local, TikTok exige HTTPS absoluto).
- `production/scripts/tiktok/tiktok_publish_video.py` — publicación vía FILE_UPLOAD, sin fragmentación todavía (solo ≤64MB; piezas FYR rondan 20-30MB, no es problema actual).

**Pendiente inmediato:**
- [ ] Esperar resultado de App Review (sin ETA).
- [ ] Una vez aprobada: revertir cuenta a pública.
- [ ] Borrar videos de prueba de Sandbox.
- [ ] Implementar fragmentación (chunking) si se necesita subir >64MB.
- [ ] Implementar refresh de `TIKTOK_ACCESS_TOKEN` vía `TIKTOK_REFRESH_TOKEN` para producción (access token actual expira en 24h).

---

## 10. Avatares / foto de perfil circle-safe — ✅ HECHO (28-29-oct-2026)

Los archivos originales de `01_Brand_Assets/C14_Brand_Mark/` fueron diseñados para favicon/app icon (recorte cuadrado, ~2.9% de margen) — insuficiente para recorte circular (profile picture de Pinterest, YouTube, TikTok, Instagram). Causó recorte visible del símbolo.

**Solución:** familia nueva (`FYR_C14_avatar-symbol_1x1_v1[-color]` y `FYR_C14_avatar-lockup-vertical_1x1_v1[-color]`, 4 colores, PNG+SVG, 2400×2400px, margen ~15-20% circle-safe). Integrada en `assets/brand/avatars/` (repo), `01_Brand_Assets/C14_Brand_Mark/` (Drive), y 16 registros en `Assets`.

**Variante adicional:** `FYR_C14_avatar-symbol-white-bg_1x1_v1.png` — mismo isotipo sobre fondo blanco sólido (no transparente), porque Instagram rellena transparencia con un color no deseado al subir como foto de perfil.

**Estándar:** Root Black como avatar por defecto en todas las plataformas (fondo transparente), excepto Instagram (variante `-white-bg`).

**Pendiente:** confirmar que el avatar quedó subido manualmente en Pinterest y YouTube (Instagram ya confirmado).

---

## 11. Privacy Policy — ✅ HECHO (29-oct-2026)

`privacy.html` solo mencionaba Hotmart — no decía nada de las integraciones propias de FYR (Meta Graph API, TikTok Content Posting API, Pinterest API v5), exactamente lo que un revisor de TikTok o Pinterest verifica. Riesgo real de rechazo en ambas revisiones, corregido antes de convertirse en problema.

Agregada Sección 6 "Social Media Platform Integrations" en `build/src/privacy.html` → regenerado `privacy.html` vía `build/build.py`: aclara que son cuentas propias de FYR (nunca de terceros), lista scopes/alcance real por plataforma, deja explícito que ninguna integración lee DMs/contactos/datos de otros usuarios.

**Pendiente aparte:** exploración de cookies de retargeting (Meta/TikTok/Pinterest Pixel) + analytics de comportamiento, derivada a conversación separada. Cuando se decida el stack, `privacy.html` necesitará otra sección nueva.

---

## 12. Safe zones por plataforma (texto/título)

Detectado texto tapado por la interfaz de TikTok en un video ya publicado (handle/botón de seguir sobre el título). Causa raíz y corrección completa documentadas en `knowledge/reference_assets/FYR_Layout_Specs_v1.md` Sección 15 (tablas de zona segura por plataforma) y ya corregidas en el motor (`production/scripts/assemble/layout_specs.py`, constante `SAFE_PRACTICAL`).

**Decisión de alcance:** un solo render de video sirve para las 3 plataformas (TikTok/Reels/Shorts) — no se renderiza por plataforma destino. El margen protege contra el peor caso combinado de las tres.

**Relevante para `fyr-publisher`:** no hace falta lógica de "render distinto por plataforma" en el orquestador — el MP4/PNG que sale del motor de ensamblado ya es válido para las tres sin transformación adicional.

**Nota importante de criterio (30-oct-2026, corregida en sesión aparte sobre `doble_marco`):** `SAFE_PRACTICAL` (la zona segura vertical) protege contra la UI de descubrimiento del feed/reel — aplica a **portadas**. Un layout de **cuerpo** (slide 2+) no necesariamente la necesita por categoría, pero lo que decide si hay riesgo real es si el elemento cae físicamente dentro de esa zona, no si es portada o cuerpo — verificar con el número real en cada caso, y confirmar contra plataforma real cuando el cálculo teórico y la práctica puedan discrepar (ver ejemplo documentado en `FYR_Layout_Specs_v1.md` Sección 7, con capturas reales de Reels/TikTok).

---

## 13. Decisiones abiertas (no asumidas, confirmar antes de cerrar `fyr-publisher`)

- [ ] ¿Ventana de cautela de Instagram: 1 semana o 2?
- [ ] ¿Facebook vía Buffer o API directa de Meta (dado que Instagram ya no usa Buffer)?
- [ ] ¿Se usa `location_id` en los posts?
- [ ] ¿Se agrega siempre un comentario automático con el link del recurso/bundle, separado del caption?
- [ ] ¿Alt text se genera junto con el brief (en `fyr-content`) o se calcula aparte en `fyr-publisher`?
- [ ] ¿Qué stack de analytics/retargeting usar (GA4, Plausible, Meta Pixel, etc.)?
- [ ] ¿El Pin de "dolor" en Pinterest debe apuntar a blog/journal en vez de a la landing general, una vez que exista contenido ahí?
- [x] **El orquestador (`fyr-publisher` SKILL.md)** — escrito y pusheado 31-oct-2026 (`.claude/skills/fyr-publisher/SKILL.md`). Los 7 scripts de publicación (Sección 3 de este documento) están construidos y verificados con publicaciones reales en las 5 plataformas; pendientes reales que quedan: campo `Board Pinterest` en Airtable (Sección 4.1 de `fyr-publisher/SKILL.md`), refresh automático de TikTok, scope ampliado de YouTube para borrado, y la decisión de ejecución bajo demanda vs. cron en Actions (ver `fyr-publisher/SKILL.md` Sección 9).
