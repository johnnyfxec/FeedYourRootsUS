# FYR — Rutas de producción (carrusel y video)

**Versión 1.0 — 14-oct-2026.** Fuente de verdad del paso a paso de cada formato. Está escrito para que Claude (aquí o en Claude Code, desde la tablet) lo ejecute sin ambigüedades: cada paso dice **quién actúa, dónde, qué se escribe en Airtable y cómo se comprueba**.

**Regla de oro:** las dos rutas **no se mezclan**. El carrusel **nunca** toca GitHub Actions. El video **solo** se renderiza en GitHub Actions. Lo único común es la Sección 0 (dónde vive cada cosa) y la Sección 1 (acceso a Drive).

---

## 0. Dónde vive cada cosa (válido para las dos rutas)

### 0.1 Mapa de destinos de cada imagen

| Qué es | Dónde se guarda en Drive | Nombre | ¿Fila en `Assets`? |
|---|---|---|---|
| Escena nueva generada en Gemini (4:5, 9:16 o 1:1 de portada) | `06_Narrative_Stock/` | `STOCK-[slug]_[aspecto]_v[n].png` | **Sí**, siempre |
| Ilustración botánica | `03_Seed_Library/WObg/` | `L##-[planta]-wobg_1x1_v1.png` | Sí (ya existen) |
| Marco, layout, plantilla | `01_Brand_Assets/C12_Frames/`, `C13_Layout_Elements/`, `Video_Cover_Templates/` | según Policy §3 | Sí (ya existen) |
| **Carrusel terminado** (un PNG por slide) | `05_Marketing_Assets/Social_Media/Content_Pieces/PZA_[tema]/[fecha]/` | `FYR_PZA_[tema]_S[n]_4x5_v[n].png` | **No** (se rastrea por `Content_Pieces.Carpeta Drive`) |
| **Video terminado** (MP4) | misma carpeta `Content_Pieces/PZA_[tema]/[fecha]/` | `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4` | **No** (igual) |
| Portada de video ya compuesta (insumo del render) | `05_Marketing_Assets/Video_Production/PZA_[tema]/` | `FYR_PZA_[tema]_PORTADA_9x16_v[n].png` | No (archivo de trabajo de la pieza; el JSON la referencia por ID de Drive) |

`Content_Pieces/` guarda **solo archivos terminados**. Nunca se copian ahí escenas del banco.

### 0.2 Qué tabla de Airtable guarda qué

| Tabla | Rol | Se crea | Se actualiza |
|---|---|---|---|
| `Themes` | El tema: estado, hook, fase, fecha de uso y de publicación, links de publicación | Al aprobar el brief (si no existe) | Al aprobar el brief; al publicar |
| `Content_Pieces` | La pieza: estado, copy, rutas del brief/JSON, carpeta de Drive, hook, assets usados, performance | Al aprobar el brief | En cada cambio de estado |
| `Assets` | Cada imagen **de entrada** (escenas, marcos, botánicas) y su memoria de uso | Al subir cada imagen nueva | `Veces usado`, `Último uso`, `En descanso` |

### 0.3 Dónde viven los archivos de trabajo (decisión 14-oct-2026)

La sesión de Claude corre en un contenedor que se borra. Por eso **todo lo que debe sobrevivir va a Git o a Drive**, nunca a una carpeta local:

- Brief y config de cada pieza: `production/pieces/PZA_[tema]/` en el repo (`brief.md`, `config.json` para carrusel o `pieza_[tema].json` para video). `Content_Pieces.Ruta .md` y `Ruta JSON` guardan esas rutas.
- La carpeta `production/briefs/` (ignorada por Git) queda **retirada**; no se usa más.
- Imágenes descargadas y PNG ensamblados son temporales: se regeneran siempre desde Drive.

### 0.4 Estados de `Content_Pieces.Estado Producción`

`Brief Generado` → `Assets en Drive` → `Ensamblado` → `Publicado`

| Estado | Significa | Condición verificable |
|---|---|---|
| Brief Generado | Brief aprobado, pieza registrada | Existe fila, brief y config en el repo, carpeta de Drive creada |
| Assets en Drive | **Todas** las imágenes de entrada existen en Drive y están en `Assets` | Cada slide tiene ID de Drive resuelto y verificado |
| Ensamblado | El producto final está terminado y aprobado por Johnny, subido a `Content_Pieces` | Carpeta con N archivos, checksum igual al local |
| Publicado | Publicado en la red | `Fecha de Publicación` y link en `Themes` |

### 0.5 Reglas transversales de escritura en Airtable

- Claude hace **todas** las escrituras. Johnny no edita Airtable.
- **Actualizar no es agregar al final:** si un dato cambió, se reescribe en su sitio.
- `Hook Usado` y `Hook Asignado` siempre con el **nombre completo** de la opción (`07 Contraste/Versus`). Las opciones sueltas `04`, `07`, `17` son restos viejos: no se usan.
- Selects: escribir el nombre de la opción; `typecast: true` solo si la opción de verdad es nueva y está justificada.
- Link a Drive siempre se arma desde el ID real: `https://drive.google.com/file/d/<ID>/view?usp=drivesdk`. El ID se extrae con `/d/([A-Za-z0-9_-]+)`.
- Lotes de máximo 50 registros por llamada.

### 0.6 Cómo se registra una imagen nueva en `Assets` (campos exactos)

| Campo | Valor |
|---|---|
| Nombre de archivo | El nombre exacto del archivo en Drive (`STOCK-lapiz-plano-huerto_1x1_v1.png`) |
| Categoría | `Narrative Stock` |
| Subcategoría/Uso | `Escena emocional` por defecto; usar otra opción solo si ya existe y describe exactamente la escena (p. ej. `Backyard scene, first-person POV`). No crear opciones nuevas |
| Aspecto | `4:5`, `9:16` o `1:1` (leído del archivo real, no del brief) |
| Link Drive | URL armada con el ID real, obligatorio |
| Carpeta Drive | `06_Narrative_Stock/` |
| Descripción breve | Una línea de qué se ve (sirve para buscar por concepto) |
| Fecha de creación | Fecha en que Johnny la subió |
| Tags | 3–6: palabras ya existentes primero; más el tag de aspecto (`4x5`, `9x16` o `cuadrado`). Un tag nuevo solo si ningún existente cubre el concepto |
| Proyecto/Producto | `Feed Your Roots US` |
| Reutilizable en | `Redes sociales` (+ `Video` si es 9:16 o 1:1 de portada) |
| Content_Pieces | Se linkea a la pieza que la usa |
| Veces usado / Último uso / En descanso | `1` / fecha de la pieza / marcado |

### 0.7 Memoria de uso (`Veces usado`, `Último uso`, `En descanso`)

- Al **aprobar el brief**: cada asset de escena de la pieza (no marcos ni plantillas) → `Veces usado` +1, `Último uso` = fecha del brief, `En descanso` = marcado.
- Al **publicar**: `Último uso` se corrige a la fecha de publicación.
- Al **aprobar el siguiente brief**: se desmarca `En descanso` de todo asset cuya última pieza no sea una de las **dos piezas más recientes**.
- Al buscar escenas (Paso 4 de `fyr-content`) se descartan las que tienen `En descanso` marcado y se prefiere la de menor `Veces usado`.

---

## 1. Acceso a Drive (requisito compartido)

**Regla de diseño (16-oct-2026): el conector de Drive hace todo lo que puede; la API solo sube.**

| Operación | Herramienta | Nota |
|---|---|---|
| Buscar, listar, leer metadatos | Conector de Drive (`search_files`, `get_file_metadata`) | Siempre por ID o nombre exacto |
| Descargar imágenes | Conector (`download_file_content`) | El resultado queda guardado en un archivo JSON con el contenido en base64; `run_pieza.py importar` lo decodifica y valida |
| Crear carpetas, copiar, mover, papelera | Conector (`create_file` con tipo carpeta, `copy_file`, `update_file` con `parentId`, `trash_file`) | Mover = `update_file(fileId, parentId = carpeta destino)` |
| **Subir archivos pesados (PNG ensamblados, MP4)** | **API de Drive** con `production/scripts/drive/drive_client.py` | El conector solo sube pegando el archivo entero dentro de la llamada (millones de caracteres por slide; un MP4 es imposible). El script sube con verificación `md5` |

**Cómo se sube (A11 y B10, vigente desde 16-oct-2026):** el cliente de la API usa OAuth de **usuario** (no cuenta de servicio) con scope `drive` completo, autorizado por flujo **web/loopback** (no flujo de dispositivo: ese rechaza el scope completo). Con ese scope, `parent_id` puede ser cualquier carpeta de Johnny — sube **directo** a la carpeta final (`Content_Pieces/PZA_x/<fecha>/` o `Video_Production/PZA_x/`) y verifica el `md5`; no hace falta que el conector la mueva después. Historia completa de por qué `drive.file` y el flujo de dispositivo no sirven: ver las notas de diseño en `drive_client.py`, `drive_authorize_web.py` y `drive_authorize.py` (este último queda como registro, obsoleto).

| Pieza | Qué es | Dónde queda |
|---|---|---|
| Red de la sesión | Configuración → Capacidades → Lista de dominios permitidos: `*.googleapis.com` y `accounts.google.com` | Ajustes de Claude |
| Cliente OAuth "Aplicación de escritorio" | Scope `drive` completo. Mientras la pantalla de consentimiento esté en status **Testing**, solo admite **un test user a la vez** (el límite de 100 solo aplica una vez Verificada/En producción) — ver checklist de proceso en `FYR_Protocolo_De_Trabajo.md` | Google Cloud Console |
| Cuenta dueña del Drive de FYR | `johnnyhacetrading@gmail.com` (NO `johnnybravol1995@gmail.com`) | — |
| Credenciales | `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN` | Secretos de GitHub (deben existir ahí con el mismo refresh token de `johnnyhacetrading@gmail.com` para que Actions suba el MP4 directo a Drive — confirmado 16-oct-2026 que **no existían**, ver B10) y, en una sesión de chat, se las pasa Johnny a Claude al inicio si hay que subir archivos. **Nunca en el repo ni en el Proyecto** |
| Autorización única | `production/scripts/drive/drive_authorize_web.py` (flujo web/loopback: Johnny abre la URL impresa en SU navegador, inicia sesión con `johnnyhacetrading@gmail.com` y toca Permitir) | Repo |
| Cliente | `production/scripts/drive/drive_client.py` (`upload`, `find`, `find_prefix`, `metadata`, `trash`) y su prueba `test_drive_client.py` | Repo |

Toda subida se verifica: `md5Checksum` que devuelve Drive = md5 del archivo local. Si no coincide, la subida **no cuenta** y se repite.

**Tercer mecanismo de acceso a Drive (solo lectura, solo dentro de Actions):** el paso "Bajar imagenes de Drive" del workflow (`production/scripts/video/_ci/fetch_assets.mjs`) NO usa el OAuth de usuario de arriba ni el conector — usa una **cuenta de servicio** de Google Cloud, vía `GoogleAuth` con scope `drive.readonly`, autenticada con el JSON de esa cuenta guardado en el secreto de GitHub `GOOGLE_CREDENTIALS_JSON` (el mismo JSON que Johnny descargó y pegó como secreto cuando esto se diseñó para correr vía PC/Git Bash; ya no hay PC, pero el mecanismo sigue siendo válido porque Actions lo necesita igual: Actions no puede usar el OAuth de usuario de arriba porque ese flujo requiere interacción humana en un navegador, y la cuenta de servicio no la requiere). Por diseño, esa cuenta solo ve lo que esté compartido con ella (rol Lector) — si falta compartir una carpeta nueva del banco de assets con esa cuenta, el paso falla de forma visible (`✗ slide N: no encuentro "..." en Drive`), nunca en silencio. Si `GOOGLE_CREDENTIALS_JSON` deja de existir como secreto o la cuenta pierde acceso a una carpeta, este es el primer lugar a revisar.

Hasta que la autorización esté hecha, el carrusel y el video **se detienen en el paso de subida** y Claude lo dice; no se improvisa otra vía.

---

# RUTA A — CARRUSEL (4:5)

**Quién hace qué:** Johnny solo (1) aprueba el brief, (2) genera en Gemini lo que falte y lo exporta a `06_Narrative_Stock`, (3) aprueba los slides terminados, (4) publica. Todo lo demás lo hace Claude.
**Herramientas:** Airtable (MCP), Drive (conector para todo; API solo para subir los PNG terminados), `assemble.py`. **Nunca Actions.**

### A0 — Selección del tema
- Claude: revisa `Trend_Signals` aprobadas vigentes; si Johnny dio número `X.Y`, lo busca en `Themes` y luego en la Malla; si dijo "el siguiente", elige por cobertura del banco y mezcla de fases; si es tema nuevo, búsqueda semántica obligatoria (Sección 3 de `fyr-content`).
- Un tema `Usado` no se repite sin confirmación de Johnny.
- Airtable: solo lectura.
- Salida: tema elegido + cuántos slides salen del banco.

### A1 — Diseño de la pieza
- Claude: Question Test, hook (nombre completo), fase, nº de slides por fase, layout de cada slide (Paso 2 y 3 de `fyr-content`), texto exacto de cada slide, CTA, caption.
- **Cada slide declara su layout y si lleva texto.** `full_bleed` nunca lleva texto; si el hook pide mensaje sobre imagen, `ventana_texto`. Una fila de imágenes sin texto solo existe si el brief lo decide a propósito.
- Airtable: ninguna escritura.

### A2 — Inventario de imágenes (banco primero)
- Claude: para cada slide con escena, busca en `Assets` por Tags, Descripción y Aspecto (4:5); descarta `En descanso`; elige menor `Veces usado`. Marcos y plantillas: por nombre exacto.
- Por slide el brief anota: **record de Assets + ID de Drive + nombre**, o `[GENERAR EN GEMINI]` con el nombre final `STOCK-[slug]_4x5_v1.png`, el prompt completo (estilo + diversidad + composición, ratio exacto del hueco) y `fondo: pergamino | color_completo`.
- Airtable: ninguna escritura.

### A3 — Brief y config
- Claude escribe `production/pieces/PZA_[tema]/brief.md` y `config.json` (schema en `FYR_Motor_Ensamblado_Arquitectura_v1.md` §6; `ventana_texto` usa `texto_overlay`).
- Los nombres de imagen del config son los nombres reales del banco (`STOCK-...`).
- Validación: `config_loader` acepta el config; cada imagen del config existe en `Assets` o está marcada `[GENERAR]`.

### A4 — PAUSA: aprobación del brief (Johnny)
- Johnny confirma o pide cambios. Los cambios se parchean in situ en brief **y** config.

### A5 — Apertura de la pieza (tras la aprobación)
Claude escribe, en este orden:
1. **Drive:** crea `Content_Pieces/PZA_[tema]/` si no existe y la subcarpeta `[fecha de hoy]/` dentro.
2. **Themes:** crea o actualiza el tema: `Estado = Usado`, `Fecha de uso`, `Hook Asignado`, `Fase Embudo`, Título/Subtítulo/Prompt, CTA, Plataforma.
3. **Content_Pieces:** crea la fila: `ID Pieza = PZA_[tema]`, `Tipo de Pieza = Carrusel`, `Fecha de Generación`, `Número de Slides`, `Copy Completo` (slides + caption), `Ruta .md`, `Ruta JSON`, `Tema Relacionado`, `Hook Usado` (nombre completo), `Audiencia = Propia`, `Carpeta Drive` (URL de la subcarpeta de fecha), `Assets Usados` (los del banco), **`Estado Producción = Brief Generado`**.
4. **Assets (del banco):** memoria de uso según 0.7.
5. Commit del brief y config a `main`.

### A6 — Generación de lo que falta (Johnny, solo si hay `[GENERAR]`)
- Claude entrega **un** prompt a la vez. Johnny genera en Gemini, revisa contra Policy §5/§6 (composición, diversidad, sin texto no deseado, ratio), exporta a `06_Narrative_Stock/` **con el nombre exacto** y escribe "listo".
- Si no falta nada, este paso se salta.

### A7 — Registro de las imágenes nuevas
- Claude: lista `06_Narrative_Stock/` (`search_files` con la carpeta como padre), cruza **por nombre exacto**, descarga cada archivo nuevo, **mide ancho×alto reales** y verifica la proporción (4:5 ≈ 0.8; tolerancia ±2 %). Si no cuadra: se detiene y avisa.
- Airtable: crea las filas en `Assets` (0.6), las linkea en `Content_Pieces.Assets Usados`, **`Estado Producción = Assets en Drive`**.
- Si no hubo imágenes nuevas, el estado pasa a `Assets en Drive` aquí mismo tras verificar los IDs del banco.

### A8 — Descarga
- Claude llama al conector (`download_file_content`) una vez por cada ID de `imagenes.json` (nombre → ID de Drive, que Claude mantiene en el paso A7); cada resultado queda guardado en un archivo JSON.
- Luego: `python3 production/scripts/assemble/run_pieza.py importar production/pieces/PZA_[tema] <trabajo> <archivo1.json> <archivo2.json> …`. El script decodifica, comprueba que el ID y el nombre coinciden con `imagenes.json`, que no falte ninguna imagen y que la proporción real coincida con el sufijo (`4x5`, `9x16`, `1x1`, ±2 %); copia los marcos de `production/assets_local/`. Si una imagen no tiene ID, se detiene.

### A9 — Ensamblado
- Claude: `python3 production/scripts/assemble/run_pieza.py ensamblar production/pieces/PZA_[tema] <trabajo> [--version N]`.
- Resultado esperado: N PNG de 1080×1350 en `<trabajo>/final/`, ya con el nombre `FYR_PZA_[tema]_S[n]_4x5_v[n].png`. El script comprueba tamaño y falla si algo no cuadra. Si el motor falla, se corrige el config (no el motor, salvo bug confirmado).

### A10 — Revisión visual y PAUSA de aprobación
- Claude abre cada PNG y comprueba: texto completo y sin cortes, ningún texto fuera de su caja, sin palabras prohibidas, loop visual del cierre (el último slide transforma un elemento de la portada), orden y numeración. Reporta los hallazgos.
- Claude envía los slides a Johnny (`SendUserFile`). Johnny aprueba o pide cambios.
- Cambios: se corrige el config y se vuelve a A9. Versión nueva = `v2`; solo se sube la versión aprobada, y las anteriores en la carpeta se mandan a la papelera.

### A11 — Subida y verificación
- Claude: `python3 production/scripts/assemble/run_pieza.py subir production/pieces/PZA_[tema] <trabajo> [fecha]`. El script resuelve solo `Content_Pieces/PZA_[tema]/<fecha>/` (`Drive.content_pieces_folder`, la crea si falta — ya no requiere que Claude calcule ni pase el `parent_id` a mano), sube cada PNG directo ahí (reemplaza si ya existían, sin duplicar), verifica el checksum, y además confirma con `find()` que cada archivo aparece en esa carpeta con ese ID exacto — si no, el script falla explícitamente en vez de reportar éxito.
- Claude confirma además con el conector (`search_files`, parentId = esa carpeta) que la cuenta de archivos coincide con `Número de Slides`. Las versiones anteriores de la carpeta se mandan a la papelera con `trash_file`.
- Airtable: **`Estado Producción = Ensamblado`**, `Carpeta Drive` confirmada.
- Claude entrega a Johnny: link de la carpeta + caption final.

### A12 — Publicación (Johnny)
- Johnny publica y avisa plataforma, fecha y link.
- Claude: `Content_Pieces.Estado Producción = Publicado`; `Themes`: `Fecha de Publicación` y el campo `Link Publicación` de la plataforma; `Assets`: `Último uso` = fecha de publicación (0.7).

### A13 — Medición
- La skill de performance actualiza `Content_Pieces.Performance`. Hasta que exista, `Sin datos`.

**Verificación final de la pieza (Claude la reporta):** brief y config en el repo · config validado · N archivos en Drive con checksum · fila de Airtable con `Carpeta Drive`, `Assets Usados`, `Hook Usado` y estado correctos.

---

# RUTA B — VIDEO (9:16)

**Quién hace qué:** Johnny (1) aprueba el brief, (2) genera en Gemini lo que falte y lo exporta a `06_Narrative_Stock`, (3) aprueba el MP4, (4) publica. Claude hace todo lo demás y dispara el render en GitHub Actions.
**Herramientas:** Airtable (MCP), Drive (conector; la API solo sube la portada y, desde Actions, el MP4), `assemble.py` (solo la portada), GitHub Actions (render). El render **solo** ocurre en Actions.

### B0 y B1 — Selección y diseño
- Igual que A0 y A1, con estas diferencias (leer `FYR_Protocolo_Edicion_Video.md` completo):
  - Slide 1 = portada compuesta con `marco_grande_cuadrado` (imagen 1:1 + título + subtítulo). Slides 2–N = imagen 9:16 `full_bleed`, una línea narrada por slide. Sin lockup, sin texto horneado, sin numerales en pantalla.
  - Marcas en el guion: `*palabra*` énfasis, `//` pausa extra, `…` pausa larga.
  - Cierre en loop de replay (A o B, alternando); el CTA va antes, separado con `//`.
  - Longitud de referencia ~525 caracteres (~35 s).
  - El tipo de cierre y la variante (`voz|subtítulo|cierre`) se registran como variable a medir.

### B2 — Inventario de imágenes
- Igual que A2 pero: escenas **9:16** del banco para los slides 2–N y **una imagen 1:1** para la portada (banco o `[GENERAR]`). Las ilustraciones botánicas 1:1 entran directo a la portada.
- Nombres nuevos: `STOCK-[slug]_9x16_v1.png` y `STOCK-[slug]_1x1_v1.png`, ambos en `06_Narrative_Stock/`.

### B3 — Brief y JSON
- Claude escribe `production/pieces/PZA_[tema]/brief.md` y `production/scripts/video/pza-[tema]/pieza_[tema].json` (contrato del Protocolo §2). Slides 2–N llevan el ID de Drive de la escena; el slide 1 (`asset` = nombre de la portada compuesta, `drive_id`) se completa en B8. Si está en `null`, B9 falla a propósito.
- Validación: JSON válido; cada escena del banco existe en `Assets`; longitud del guion; sin palabras prohibidas; el cierre cumple el tipo elegido.

### B4 — PAUSA: aprobación del brief (Johnny). Igual que A4.

### B5 — Apertura de la pieza
Igual que A5, con: `Tipo de Pieza = Video`, `Duración` estimada, `ID de variante`, tipo de cierre al inicio de `Copy Completo`, `Ruta JSON` = ruta del `pieza_[tema].json`. `Estado = Brief Generado`.

### B6 y B7 — Generar y registrar lo nuevo
- Igual que A6 y A7 (proporciones: 9:16 ≈ 0.5625, 1:1 = 1.0; ±2 %). `Estado = Assets en Drive`.

### B8 — Portada compuesta
- Claude: con `production/pieces/PZA_[tema]/portada_config.json` (`marco_grande_cuadrado`, `texto_titulo`, `texto_subtitulo`) y `imagenes.json` (la imagen 1:1): descargar con el conector y `run_pieza.py importar …`, y luego `run_pieza.py ensamblar … --config portada_config.json --portada` → `FYR_PZA_[tema]_PORTADA_9x16_v1.png`, 1080×1920.
- Revisa la portada visualmente y la manda a Johnny para su OK **junto con la aprobación del resto** (B11 no la repite).
- Sube la portada con la API directo a `Video_Production/PZA_[tema]/`: `drive_client.py video-production-folder PZA_[tema]` resuelve sola (y crea si falta) el `parent_id` de esa carpeta — ya no hace falta crearla a mano con el conector —, y luego `drive_client.py upload <png> <parent_id>` sube ahí. Comprueba que está, escribe su ID en el slide 1 del JSON (`asset`, `drive_id`) y quita el bloque `portada`. Commit.
- El paso "Portada (ensamblador)" del workflow y `_ci/make_cover.py` ya fueron eliminados (14-oct-2026).

### B9 — Verificación previa al render
Claude comprueba, con el conector (`get_file_metadata`), que **cada ID de Drive del JSON** existe, es PNG y tiene tamaño > 0; que el slide 1 es 1080×1920; que el guion está completo. Si algo falla, no se dispara el render.
**Defensa adicional dentro del propio workflow (16-oct-2026):** el primer step de `render-video.yml` corre `validate_pieza.py` (estructura del JSON, slides consecutivos, `drive_id` presente, énfasis `*...*` bien cerrados, aspecto/canvas correctos) sin red, antes de instalar Playwright o bajar nada — si el JSON está mal formado, el job falla ahí mismo, en segundos, no después de los ~5-6 min de TTS+render. Esto no reemplaza la verificación de B9 (que sí confirma contra Drive de verdad), es una segunda capa para cuando B9 se salta o corre sin supervisión directa.

### B10 — Render en Actions
1. Claude toma, vía el conector o `drive_client.py content-pieces-folder PZA_[tema] <fecha>`, el `parent_id` de `Content_Pieces/PZA_[tema]/<fecha>/` (se crea sola si falta). Hace commit a `main` del JSON y del archivo de cola `production/queue/pza-[tema].env` con `PIEZA`, `VARIANTE`, `TAIL_LAST` y **`PARENT_ID`** (ese `parent_id`; si se omite, el MP4 sube a la raíz de Mi unidad y hay que moverlo a mano). **Por qué Claude lo calcula a mano aquí y no en el carrusel (A11):** `run_pieza.py subir` (Ruta A) corre en el sandbox y puede llamar a `content_pieces_folder()` él mismo; el workflow de Actions (Ruta B) no tiene ese contexto antes de arrancar, así que el `parent_id` tiene que venir ya resuelto en el `.env` que dispara el push. No es una inconsistencia, es una diferencia de dónde corre cada ruta. **El MP4 final va a `Content_Pieces/`, igual que el carrusel — nunca a `Video_Production/`, que es solo para insumos de trabajo del video como la portada de B8** (error real cometido el 16-oct-2026 en el piloto PZA_4.2, corregido moviendo el archivo).
2. Ese push dispara el workflow "Render video" (voz TTS + subtítulos palabra por palabra + render).
3. El workflow verifica primero si existen los secretos `GOOGLE_OAUTH_*`; si faltan, deja un warning y el MP4 queda solo como artefacto de GitHub (7 días) **sin fallar el job** (es config pendiente, no un error de la corrida). Si existen, sube el MP4 (paso `upload_mp4.py`) **directo a `PARENT_ID`**, con el nombre `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4` (la versión sube sola), confirma con `find()` que el archivo quedó presente en esa carpeta (si no, **falla el job de verdad** — ya no hay `continue-on-error` que esconda una subida fallida), y deja el registro de la corrida, con el enlace del MP4, en `production/runs/`.
   **Requisito: los secretos `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` / `GOOGLE_OAUTH_REFRESH_TOKEN` deben existir en GitHub → Settings → Secrets and variables → Actions, con el mismo refresh token de `johnnyhacetrading@gmail.com` que usa el sandbox** (ya cargados desde el 16-oct-2026).
4. Claude espera el registro de la corrida; si el workflow falla (incluido un fallo real de subida, visible ahora en el estado del job, no solo en el log), lee el log, corrige la causa y vuelve a B9. Máximo 3 intentos; después reporta.

### B11 — Revisión y PAUSA de aprobación
- Claude descarga el MP4 con el conector, comprueba duración, resolución 1080×1920, audio presente, y extrae fotogramas de cada slide para revisar subtítulos y cortes.
- Johnny ve el MP4 desde la carpeta de Drive y aprueba o pide cambios. Cambio = corregir JSON → B9 → B10; la versión nueva es `v2` y las anteriores se mandan a la papelera tras la aprobación.

### B12 — Registro final
- Airtable: **`Estado Producción = Ensamblado`**, `Duración` real, `ID de variante`, `Carpeta Drive`.
- Claude entrega el link y el caption.

### B13 y B14 — Publicación y medición
- Igual que A12 y A13.

**Verificación final:** brief y JSON en el repo · IDs verificados · registro de la corrida · MP4 en Drive con checksum · fila de Airtable correcta.

---

## 2. Qué NO se hace (para que no haya dudas)

- No se copian escenas del banco a `Content_Pieces`.
- No se usa Actions para carruseles, ni siquiera para ensamblar.
- No se trabaja en una PC: no existe. Todo corre en la sesión de Claude (tablet) y en Actions.
- No se guardan credenciales en el repo (es público).
- No se usa `--force` en Git.
- Lockup y texto horneado: solo si Johnny lo pide expresamente para esa pieza.
