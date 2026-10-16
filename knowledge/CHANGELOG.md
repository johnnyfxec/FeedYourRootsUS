# FYR — Changelog de gobernanza

Registro legible de cambios a los documentos de `knowledge/` (fuente de
verdad del proyecto). Se actualiza junto con cada commit que toque estos
documentos — no reemplaza `git log`, lo complementa explicando el motivo
en lenguaje natural.

Formato: `AAAA-MM-DD — documento(s) — qué cambió y por qué`

---

## 2026-10-16 (continuación — Auditoría archivo por archivo)

Johnny pidió una primera pasada de auditoría de todo el repo (`knowledge/`, las 3 skills, `production/scripts/`, el workflow) buscando inconsistencias, referencias rotas y pasos que requieren intervención humana sin decirlo — motivada por los errores reales de propagación encontrados hoy mismo (ver entradas anteriores de este mismo día). Hallazgos y lo que se corrigió de inmediato (lo que no requería verificar nada contra Airtable/Drive real):

- **`fyr-video-assembler/SKILL.md` (Paso 4) tenía la arquitectura de Drive vieja.** Describía "subir a la raíz, mover con el conector" para la portada (B8) y para el MP4 final (B10) — exactamente el patrón que se corrigió hoy en `FYR_Rutas_De_Produccion.md` pero que no se había propagado a la skill. Corregido: ahora describe `video_production_folder()`/`content_pieces_folder()` resolviendo la carpeta sola, sin mover nada después.
- **`FYR_Protocolo_De_Trabajo.md` (línea 41) seguía diciendo `drive.file`** como el permiso de `drive_client.py`, cuando la migración de hoy lo cambió a OAuth de usuario con scope `drive` completo. Corregido, con referencia a `FYR_Rutas_De_Produccion.md` Sección 1.
- **`FYR_Rutas_De_Produccion.md` (B8, antes línea 223) también tenía rastro viejo**: decía `drive_client.py upload <png> <parent_id>` calculando la carpeta a mano con el conector, en vez de usar `video_production_folder(pieza_id)` que ya existe desde la Fase A de hoy. Corregido. Se agregó además una nota explícita en B10 aclarando por qué el video sí calcula el `parent_id` a mano (vía `.env`) mientras el carrusel ya no lo hace — es una diferencia real de dónde corre cada ruta (sandbox vs. Actions), no una inconsistencia.
- **`image_fetcher.py` no verificaba el asset de marco para el layout `marco_grande_portada`.** Causa real: ese layout reutiliza el mismo archivo físico que `marco_grande` (`_compose_marco_grande_portada` llama `_load_asset("marco_grande", ...)`), pero como no tenía su propia entrada en el dict `ASSETS` de `layout_specs.py`, una pieza que use `marco_grande_portada` sin ningún slide `marco_grande` nunca activaría la verificación previa — el fallo solo aparecería tarde, en el ensamblado real. Corregido agregando la entrada duplicada (mismo archivo, documentado por qué) a `ASSETS`.

**Quedó pendiente, ordenado por prioridad (ver mensaje de la sesión para el detalle completo):**
1. ~~Tercera vía de credenciales de Drive sin documentar~~ — **resuelto**, ver abajo.
2. ~~Contradicción de tipo de campo Airtable en `Trend_Signals`~~ — **marcado explícitamente para verificar**, ver abajo (no se puede cerrar sin consultar Airtable real).
3. ~~Contenido de otro negocio de Johnny mezclado sin traducir~~ — **resuelto parcialmente**, ver abajo.
4. Error ya conocido y documentado como pendiente en `FYR_Brand_Mark_Spec_v1.md` (el PDF cita `_v2.svg`, el archivo real es `_v1.svg`) — queda como estaba, se corrige en la próxima revisión del PDF, no bloquea nada.
5. `seed-library-final.md`: Johnny confirmó que el PDF real tiene 101 ilustraciones (ya las contó varias veces) — la discrepancia está en el `.md`, probablemente falta una fila/categoría. Johnny lo va a revisar él mismo contra el PDF y avisa qué falta exactamente antes de corregir el documento.

## 2026-10-16 (continuación — Auditoría, segunda pasada: correcciones 1-3)

- **Credencial de Drive #3 (cuenta de servicio) documentada.** Confirmado con Johnny: es la arquitectura vigente a propósito (el JSON que descargó y pegó como secreto el sábado), porque Actions no puede usar el OAuth de usuario de arriba (requiere interacción humana en navegador) para el paso automático de bajar imágenes. `FYR_Rutas_De_Produccion.md` Sección 1 ahora documenta este tercer mecanismo (`fetch_assets.mjs`, `GOOGLE_CREDENTIALS_JSON`, scope `drive.readonly`, solo ve lo compartido con rol Lector) junto a los otros dos (conector, OAuth de usuario de `drive_client.py`).
- **Contradicción de schema en `Trend_Signals` — no resuelta, pero ya no es ambigua.** Johnny no supo decir cuál documento es el correcto; sin acceso a Airtable real desde aquí no se puede verificar. Se dejó una nota explícita en ambos documentos (`FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` §5 y `trend-scout/references/schema_trend_signals.md`) marcando los 3 campos en disputa (`Pilar_Relacionado`, `Tema_Vinculado`, `Content_Piece_Generada`) con instrucción de correr `get_table_schema` antes de la primera escritura a cualquiera de ellos, en vez de asumir el tipo de cualquiera de los dos documentos.
- **Contenido de JIFU/trading en `knowledge/` — ejemplos traducidos para hooks, límite de alcance para CRS.** Johnny confirmó que sí quiere ejemplos ya traducidos al avatar Morgan, manteniendo el principio psicológico universal. Para `hooks_verbales_20_v2.md` (documento compartido con el otro negocio, no se edita): se creó `.claude/skills/fyr-content/references/hooks_ejemplos_morgan.md`, 2 ejemplos en inglés ya traducidos por cada uno de los 20 hooks, referenciado desde `fyr-content/SKILL.md` Paso 2. Para `Sistema_Maestro_CRS_v2.md` (documento más grande, con ejemplos dispersos en varias secciones en vez de una lista limpia): se optó por **acotar el alcance** en vez de traducir todo — `fyr-content/SKILL.md` ahora dice explícitamente que solo aplican las Partes 1-6 (estrategia/fases/hook/arquitectura/ejecución/distribución/optimización); la Parte 8 ("Temas por Fase", banco de 30 temas de trading sin traducir) y la Parte 9 ("Sistema de DMs", prospección/inscripción de JIFU) quedan explícitamente fuera — no aplican a FYR y no se traducen.

## 2026-10-16 (continuación — Fase D)

- **`FYR_Fase_D_Produccion_Recurrente_v1.md` (nuevo).** Diseño aprobado por Johnny para pasar de producción conversacional pieza-por-pieza a lotes semanales en Claude Code. Cubre: planificación semanal con 3 fuentes de contenido (banco de temas / trend-scout / actualidad) y disparo automático los lunes; formato carrusel-vs-video decidido por tipo de contenido (no forzado por plataforma — YouTube se puebla como efecto secundario de los videos que ya se producen); las 4 paradas de producción agrupadas por lote en vez de por pieza, con manejo de fallos puntuales que no detienen el lote completo; tamaño de lote a calibrar empíricamente en la primera corrida real, no fijado de antemano. Fase B (verificar app OAuth en Google) descartada por Johnny — cada proyecto nace con su propio client+test user. Fase C (alertas de Actions sin supervisión) pospuesta hasta que el modo de trabajo deje de ser síncrono. Pendiente: implementar el trigger semanal y correr el primer lote real.

## 2026-10-16

- **Drive — migración de arquitectura de subida.** `FYR_Rutas_De_Produccion.md`: corregida la descripción de cómo A11/B8 suben archivos — ya no "API sube a la raíz con `drive.file`, el conector mueve", sino OAuth de usuario con scope `drive` completo por flujo web/loopback, subida directa a la carpeta final. Causa: `drive.file` + flujo de dispositivo resultó estar restringido por Google de forma no configurable (confirmado con reporte público idéntico de otro usuario); la arquitectura real quedó documentada en los docstrings de `drive_client.py`, `drive_authorize_web.py` y `drive_authorize.py` (este último obsoleto, se deja como registro). Se documenta también la cuenta dueña del Drive de FYR (`johnnyhacetrading@gmail.com`).
- **Protocolo de trabajo — 2 lecciones nuevas.** `FYR_Protocolo_De_Trabajo.md`: verificar con qué cuenta de Google se autentica antes de asumir que es la correcta (causó horas de debugging hoy); una app OAuth en status "Testing" admite un solo test user a la vez, no varios de antemano (el límite de 100 es solo tras Verificación).
- **Video (B10) — el MP4 nunca llegaba a Drive.** Confirmado con Johnny: el paso "Subir MP4 a Drive" del workflow `render-video.yml` tiene `continue-on-error` y se salta en silencio si faltan los secretos `GOOGLE_OAUTH_*` en GitHub — y nunca existieron. El resultado real de cada corrida era solo el artefacto de GitHub (link de descarga de 7 días), jamás un archivo en Drive, aunque el job marcara `success`. Corregido: `upload_mp4.py` ahora acepta `parent_id` y sube directo a la carpeta final (ya no a la raíz con "pendiente moverlo a mano"); `render-video.yml` agrega el input `parent_id` (manual y por archivo de cola `.env`) y lo pasa al script.
- **Piloto de video PZA_4.2 — cerrado de punta a punta.** Johnny cargó los 3 secretos `GOOGLE_OAUTH_*` en GitHub Actions. Corrida de prueba (run `38971329029`) disparada vía API REST de GitHub (el comando `gh workflow run` falla en este sandbox por bloqueo de GraphQL en el proxy; `gh api .../dispatches` sí funciona): TTS + render + subida exitosos, confirmado con el conector que el MP4 (`FYR_PZA_4.2_VIDEO_B-e14_9x16_v1.mp4`, 24.7 MB, owner `johnnyhacetrading@gmail.com`) existe — no solo que el job dijera "success". Verificación técnica (1080×1920, 41.3s, audio estéreo, subtítulos palabra-por-palabra sincronizados por frame) y aprobación de Johnny completadas; `Estado Producción` → `Publicado`. **Error cometido y corregido en el mismo día:** el MP4 subió a `Video_Production/PZA_4.2/` (carpeta de insumos de trabajo del video, solo para la portada) en vez de `Content_Pieces/PZA_4.2/2026-10-16/` (destino real del producto terminado, junto con los carruseles, según `FYR_Asset_Governance_Policy.md` Sección 0.1) — confusión entre la carpeta de B8 (portada) y B10 (producto final). Archivo movido, Airtable `Carpeta Drive` corregida, carpeta vieja borrada. Con esto, tanto el piloto de carrusel (PZA_1.2) como el de video (PZA_4.2) quedaron probados de punta a punta con la arquitectura de Drive nueva.
- **Fase A de optimización del proceso (post-pilotos).** Tres mejoras de bajo riesgo, pedidas por Johnny tras revisar los 2 pilotos:
  1. `drive_client.py` gana `content_pieces_folder(pieza_id, fecha)` y `video_production_folder(pieza_id)` — resuelven/crean la ruta completa en una llamada idempotente (IDs raíz como constantes), en vez de que cada corrida busque y cree carpetas a mano como pasó hoy. `run_pieza.py subir` (A11) ahora las usa sola, ya no recibe `parent_id` como argumento externo — elimina la clase de error que causó el punto anterior.
  2. Verificación real de llegada a Drive: `upload_mp4.py` y `run_pieza.py subir` confirman con `find()` que el archivo aparece en el `parent_id` esperado tras subir (no solo que `upload()` no haya lanzado excepción) y fallan explícitamente si no. En `render-video.yml`, el paso de subida ya NO tiene `continue-on-error` incondicional: ahora un step previo revisa si los secretos existen (si faltan → warning, no error, es config pendiente) y solo entonces corre la subida sin red de seguridad — un fallo real de subida ahora hace fallar el job de verdad, visible en el estado de la corrida sin tener que leer el log.
  3. `validate_pieza.py` (nuevo): valida la estructura de `pieza_X.json` (campos requeridos, slides consecutivos, `drive_id` presente con mensaje específico si falta por B8 incompleto, énfasis `*...*` bien cerrados, aspecto/canvas correctos) sin red, como primer step del workflow — adelanta cualquier fallo de forma a los primeros segundos en vez de después de los ~5-6 min de TTS+render. Probado contra ambas piezas reales (`pza-4.2` pasa, `pza-1.1` detecta correctamente que falta el `drive_id` de portada de B8) y contra 3 casos sintéticos rotos.

## 2026-10-14

Rutas de producción definidas por formato (decisión de Johnny: "como un reloj suizo"), sin PC.

- **FYR_Rutas_De_Produccion.md (v1.0, NUEVO)** -- fuente de verdad del paso a paso. Sección 0 común (destino de cada imagen, qué guarda cada tabla, estados, campos exactos de `Assets`, memoria de uso, reglas de escritura en Airtable); Sección 1 (acceso a Drive); Ruta A carrusel (A0–A13, nunca Actions); Ruta B video (B0–B14, render solo en Actions). Cada paso dice quién actúa, qué se escribe y cómo se verifica.
- **Decisiones tomadas por Claude tras la auditoría:** brief y config viven en Git (`production/pieces/PZA_[tema]/`), porque la sesión es efímera y `production/briefs/` (ignorada) se perdía; `Content_Pieces` solo recibe terminados y toda escena nueva va a `06_Narrative_Stock`; la portada de video compuesta se aloja en `Video_Production/PZA_[tema]/` para que Actions la baje por ID; los terminados no llevan fila en `Assets` (se rastrean por `Content_Pieces.Carpeta Drive`); el MP4 lo sube el workflow a `Content_Pieces`; `Último uso` se corrige a la fecha de publicación; `En descanso` se libera cuando la pieza que usó el asset ya no es una de las dos más recientes.
- **Código:** `production/scripts/drive/drive_client.py` (subir con verificación md5 a la raíz, buscar, papelera; solo librería estándar; credenciales por variables de entorno), `drive_authorize.py` (autorización única por flujo de dispositivo) y `test_drive_client.py` (prueba contra un Drive simulado); `production/scripts/assemble/run_pieza.py` (importar lo descargado con el conector / ensamblar / subir del carrusel, con validación de proporción, tamaño y nombres); `production/scripts/video/_ci/upload_mp4.py` y paso "Subir MP4 a Drive" en `render-video.yml` (no falla la corrida si faltan los secretos; el artefacto de 7 días se conserva).
- **Retirado:** paso `Portada (ensamblador)` del workflow y `_ci/make_cover.py`; carpeta `production/briefs/` y su línea en `.gitignore`.
- **Piezas:** `production/pieces/PZA_1.2/` (brief, config y `imagenes.json` con los nombres y IDs reales del banco; el slide 5 espera `STOCK-vecino-transformado_4x5_v1.png`) y `production/pieces/PZA_1.1/` (brief, `portada_config.json`, `imagenes.json`; imagen nueva `STOCK-lapiz-plano-huerto_1x1_v1.png`). `pieza_1.1.json`: slide 1 apunta a la portada compuesta (`drive_id` pendiente hasta compuesta y alojada).
- **Documentos corregidos en su sitio:** Policy (§2 Content_Pieces/Video_Production, §6 destino de escenas nuevas, §7 excepción de terminados, §9 ensamblado), Protocolo de Edición de Video (§1 y §9: Actions, sin PC), Protocolo de Trabajo (sin PC; código a `main`), Plan de Reutilización, `fyr-content` (Paso 5 reescrito sobre las dos rutas; `Hook Usado` con nombre completo; campo `Carpeta Drive`) y `fyr-video-assembler` (Pasos 4–6 sin comandos de PC).
- **Airtable (aplicado por Claude):** `Hook Usado` con nombre completo en PZA_4.2 (`17 Resultados/Transformación`), PZA_1.2 (`07 Contraste/Versus`) y PZA_1.1 (`04 Storytelling`). Las opciones sueltas `04`, `07`, `17` quedan sin uso (el conector no permite borrar opciones).
- **Drive (diseño final, 16-oct-2026):** el conector de Drive hace todo lo que puede (buscar, descargar, carpetas, mover, papelera); la API de Drive solo sube los archivos pesados (PNG ensamblados, MP4), con el permiso mínimo `drive.file`, a la raíz del Drive, y Claude los mueve a su carpeta con el conector. Motivo: `create_file` del conector exige pegar el archivo entero en base64 dentro de la llamada (inviable para PNG/MP4). Detalle en `FYR_Rutas_De_Produccion.md` §1.
- **Pendiente de Johnny:** cliente OAuth tipo "TVs y dispositivos de entrada limitada" en `clipkit-production-v1` (app en producción) y autorización única con `drive_authorize.py`. La red de la sesión ya permite `*.googleapis.com` y `accounts.google.com` (Configuración → Capacidades).

---

## 2026-10-11

Marca C14, poda de layouts y ajuste de los layouts aprobados en el motor de ensamblado (desarrollado en la rama `claude/brand-mark-compositor`; ya está en `main`). Reemplaza la primera versión del día (icono en esquina y firma de cierre), descartada tras la revisión de Johnny.

- **Poda de layouts (decisión de Johnny):** se eliminan del código y de todos los documentos etiqueta colgante, nota-kraft en esquina, ventana polaroid, palabra-acuarela, tachado/corrección y los acentos cordel guía y migas de progreso, porque no embellecían las composiciones y no valía el trabajo de hacerlos funcionar. Desaparecen `compositors/tipo_b.py`, `tipo_c.py` y `acentos.py`, los Tipos B, C y D, el campo `acento` (un config que lo traiga falla con error claro) y `imagen_final`. Los archivos de Drive quedan sin uso, no se borran. Quedan: marco grande, doble marco, portadas (4:5 y 9:16), full-bleed, ventana+texto, solo texto, texto+lateral y lockup de cierre.
- **`compositors/base.py`** -- el icono C14 (91 px) va solo en carruseles **4:5**, en slides secundarias, **abajo al centro**; lo llevan `ventana_texto`, `solo_texto` y `texto_lateral`, y el contenido se ajusta a la zona superior. **9:16 no lleva icono.** `solo_texto` centra el texto (`posicion_texto: "tercio_superior"` como variante); `ventana_texto` sube la imagen a 2/3 del alto en 4:5 (900 px) y a 3/4 en 9:16 (1440 px) con el texto centrado en todo el espacio bajo la imagen; `texto_lateral` muestra la imagen **9:16 completa a 540×960, sin recorte** (la proporción que se pide a Gemini tal cual) y centra el texto en altura respecto a ella; `full_bleed` sigue sin icono y a canvas completo. Layout nuevo `lockup_cierre` (lockup vertical centrado): última slide del carrusel y recurso opcional en video. Se elimina `marca_cierre`. La marca se lee de `assets/brand/` desde la raíz del repo, no de `assets_dir`.
- **`compositors/tipo_a.py` / `config_loader.py`** -- el texto bajo `marco_grande` y `doble_marco` va en el campo nuevo `texto_pie`, con el rol subtítulo (Lora negrita cursiva); el título dorado con borde queda exclusivo de las portadas (`texto_titulo`/`texto_subtitulo` en esos dos layouts dan error). Se corrige la caja del pie de `doble_marco`, que en 4:5 medía 10 px de alto y truncaba siempre el título.
- **`main.py` / `layout_specs.py`** -- advertencia para portadas 4:5 con contenido a menos de 34 px (duro) o 48 px (objetivo) del borde lateral, por el recorte 3:4 de la cuadrícula de Instagram. `lockup_cierre` registrado en `LAYOUT_TYPES` y `config_loader.py`.
- **Documentos reescritos en su sitio:** `FYR_Motor_Ensamblado_Arquitectura_v1.md` (v1.3: §0, §1, §2.1, §2.5, tipografía, módulos, schema JSON y campos), `FYR_Layout_Specs_v1.md` (secciones eliminadas; 1, 2b, 3, 4, 7 y 13 ajustadas; sección 14 Lockup nueva; tabla "Proporciones de imagen a pedir a Gemini": portada 9:16 pide 1:1, ventana+texto 9:16 pide 3:4, texto+lateral pide 9:16), `FYR_Principios_De_Composicion.md` (v1.1: sin acentos ni el rol `dato_al_margen`), `FYR_Brand_Mark_Spec_v1.md` (§07), `FYR_Protocolo_Edicion_Video.md` (§4: sin icono en video; lockup opcional como variante), `FYR_Asset_Governance_Policy.md` y el SKILL de `fyr-content` (afinidad hook → layout y búsqueda de assets sin los layouts eliminados). Aclaración en Arquitectura §1: las zonas seguras verticales son un concepto de 9:16, y se documenta el recorte de la cuadrícula de Instagram.
- **Relleno de espacios y prompts (decisión de Johnny, tras revisar sus imágenes reales de Gemini):** `compositors/base.py` rellena siempre el espacio de la imagen en `full_bleed`, `ventana_texto` y `texto_lateral` con tolerancia de ratio de 2 % (`RATIO_TOL`, recorte mínimo); fuera de la tolerancia no recorta, contiene la imagen y emite `RATIO:` para regenerar. Nuevo **bloque de composición obligatorio** en los prompts de Gemini (Layout_Specs, Policy §4, SKILL de `fyr-content`): ratio exacto del hueco, composición a sangre, sujetos a ≥ 5 % de los bordes laterales y marca `fondo` por slide (`pergamino` = liso #F5ECD7, obligatorio si la imagen queda suelta sobre el pergamino; `color_completo` = escena a todo color, sin difuminar). Policy §5 gana la fila "Ratio no exacto". Las imágenes ya generadas se dan por buenas.
- **FYR_Plan_Reutilizacion_y_Serie_Botanica.md (v1.0, NUEVO)** -- decisión de Johnny: el banco de 241 assets pasa a ser parte del proceso (primero el banco, de assets a temas, memoria de uso, generar kits para el banco, métrica de reutilización). Incluye el inventario real (21 escenas narrativas, 16 libres; 136 ilustraciones botánicas transparentes), el informe de cobertura Malla vs banco, la serie semanal "Conoce la planta" (2 plantas por semana en carrusel y video; 101 plantas ≈ 51 semanas), la primera corrida (1.2 carrusel 4:5 y 1.1 video 9:16) y el orden de ejecución.
- **fyr-content (SKILL.md)** -- reglas de reutilización: Paso 0 con cobertura del banco y camino "desde el banco"; Paso 4 con "primero el banco" (el brief declara X de N slides del banco, lo generado debe ser reutilizable); Paso 5.6 con la memoria de uso en `Assets` (`Veces usado`, `Último uso`, `En descanso`, que Claude escribe). Los tres campos los creó Johnny y se llenaron para PZA_4.2.
- **Airtable (aplicado por Claude)** -- `PZA_4.2`: `Estado Producción = Ensamblado` (video producido por completo, pendiente de publicar) y `Hook Usado = 17` (el asignado en `Themes`).
- **Rutas de producción (decisión de Johnny, 11-oct-2026):** el carrusel NO pasa por Actions: Claude baja las imágenes de Drive (Drive MCP), las ensambla con `assemble.py` y deja los terminados en `Content_Pieces/PZA_[tema]/[fecha]/`, con Airtable actualizado en cada paso. Actions (`render-video.yml`) es solo para video. En `Content_Pieces` van solo archivos terminados; las imágenes de entrada viven en el banco (`06_Narrative_Stock`) y se registran en `Assets`.
- **Airtable y Drive (aplicado por Claude):** PZA_1.2 (carrusel 4:5, tema 1.2, F2, hook 07) con carpeta `Content_Pieces/PZA_1.2/2026-10-11/` (para los terminados); alta de 1.2 en `Themes`; `Content_Pieces` en `Brief Generado`; memoria de uso actualizada (5 escenas en descanso, las de PZA_4.2 liberadas).
- **PZA_1.1 (video 9:16, tema 1.1, F1, hook 04 Storytelling, cierre B):** `production/scripts/video/pza-1.1/` (copia del motor de 4.2 con `pieza_1.1.json`). La portada la compone Claude con `assemble.py` antes del render (ver 2026-10-14); el paso `Portada (ensamblador)` del workflow y `_ci/make_cover.py` fueron retirados.

---

## 2026-10-10

Piloto de video PZA_4.2 (voz + subtitulos + render local). Se escribio la politica de video y se corrigio en su sitio lo que habia quedado desactualizado.

- **FYR_Protocolo_Edicion_Video.md (v1.0, NUEVO)** -- politica de video: pipeline, anatomia del slide-beat, marcas de narracion y tabla de pausas, cierre en loop A/B, voz (Neural2-J, pitch -4, velocidad 0.92) con costos y alternativas, subtitulos B-e14, constantes de linea de tiempo, variantes, procedimiento Git Bash, registro en Drive/Airtable, pendientes. Cada regla lleva estado VALIDADO / EN PRUEBA / PENDIENTE.
- **.claude/skills/fyr-video-assembler/SKILL.md (v1, NUEVO)** -- skill de ejecucion de video: brief aprobado -> pieza_X.json + comandos para la PC. No decide contenido; se comunica con fyr-content solo via Airtable/repo.
- **FYR_Asset_Governance_Policy.md (v2.4)** -- Content_Pieces admite el MP4 final (WAV/timings no se suben); naming del MP4; nueva fila de resolucion menor al canvas del video (768x1376 -> 1080x1920); la mencion de Canva en la seccion de herramientas se reemplazo por assemble.py y el pipeline de video.
- **FYR_Motor_Ensamblado_Arquitectura_v1.md (v1.2)** -- el alcance queda limitado a slides estaticos; el video tiene pipeline propio. Zonas seguras solo aplican a la portada del video; subtitulos al centro.
- **FYR_Principios_De_Composicion.md** -- Fase 4 (video) marcada INICIADA con el resultado del piloto: unidad = slide-beat, duracion fijada por la voz.
- **FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md (v1.1)** -- Malla de 61 temas; referencia de seccion corregida; nueva capa de ensamblado (fyr-video-assembler, assemble.py); seccion 7 reescrita como "escrito, sin probar" con el id real `PZA_[tema]`; regla de skills de ejecucion.
- **FYR_Protocolo_De_Trabajo.md** -- tercer entorno (PC Windows/Git Bash), flujo push/pull + Drive, excepcion para sesiones en la nube (solo rama), y subseccion de particularidades de la PC (CRLF, parches, identidad git, credenciales fuera del repo).
- **FYR_Malla_60_Temas_Virales_v2.md** -- linea de Sistema con el stack real (Canva no se usa; KIE.ai/Blotato no implementados), nota de portada de video, logo -> simbolo C14, nota video vs carrusel (sin costo de animacion), checklist actualizado.
- **Sistema_Maestro_CRS_v2.md** -- mecanismo de loop refinado y nueva subseccion "El loop de replay (cierre circular)"; nota en el Paso 6.
- **.claude/skills/fyr-content/SKILL.md** -- salida pasa de CSV de Canva a config JSON (carrusel: assemble.py; video: pipeline de video), bloque de video en el Paso 3, estados de produccion reales de Airtable (Brief Generado / Assets en Drive / Ensamblado / Publicado), fuentes de conocimiento nuevas, regla no negociable para video.
- **trend-scout (SKILL.md y schema_trend_signals.md)** -- el id de pieza `PZA-###` pasa a `PZA_[tema]`, que es el formato real.
- **FYR_Layout_Specs_v1.md** -- se quita la mencion a Canva en la nota de estilo.
- **production/scripts/video/pza-4.2/** -- `lib.mjs` lee `FYR_TAIL_LAST` del entorno (cierre A); `pieza_4.2.json` con cierre B ("Wait, how early can a kid really start gardening?", version mas conversacional); `LEEME.md` reescrito para Git Bash, voz J y el flujo actual.
- **FYR_Protocolo_De_Trabajo.md (reescrito)** -- ya no se copia nada a mano entre Termux, Descargas y el Proyecto: una sesion de Claude Code con el repo clonado edita, hace commit y sube; escribe el espejo del Proyecto con `project_write`. Nueva tabla "Donde escribe Claude" (contenido y skills a `main` directo si Johnny lo pide; codigo de la PC en rama). Los patrones de comando (grep + Python + assert) pasan a ser solo respaldo. Estrategia de ramas actualizada.
- **Airtable (verificado en vivo)** -- `Estado Producción` tiene Brief Generado / Assets en Drive / Ensamblado / Publicado (no existe "En Edicion" ni "En Canva o Edicion"); `Ruta JSON` ya existe en Content_Pieces; solo falta `ID de variante`. Docs y skills corregidos para usar los estados reales.
- **Modelo de temas (fyr-content, Malla, Governance, Sistema Viral)** -- la Malla (61 temas, conteos de formato y medio corregidos: 22 POV / 14 A-D / 12 Countdown / 13 Storytime; 34 Video / 27 Carrusel) es un banco semilla que NO se carga en Airtable; `Themes` registra solo lo que se produce. Nueva seccion 3 de fyr-content: temas nuevos extraidos de los PDFs (numeracion por pilar, duplicado semantico, Fase y Hook, OK del usuario). Se elimina la 'migracion de 61 temas' y la cola 'Prioridad = Alta + Pendiente'.
- **Airtable (aplicado por Claude)** -- campo `ID de variante` creado; registro `PZA_4.2` en Content_Pieces (Video, 6 slides, 41.27 s, 6 assets enlazados, tema 4.2 marcado Usado); borrados el registro de ejemplo `PZA-001` y un registro vacio de Themes; campo `Imported table` de Content_Pieces renombrado a `Señales_Origen`. Regla nueva: Claude hace todas las escrituras en Airtable, Johnny ninguna a mano.
- **Video PZA_4.2** -- espera entre el final y el reinicio del loop recortada a la mitad por pedido de Johnny: `TAIL_LAST` por defecto 0.90 -> 0.35 (cierre A: 0.15 -> 0.05). Veredicto del piloto: se mantienen ambos cierres; la pregunta B debe sonar mas organica.

## 2026-09-16

- **favicon.ico** -- publicado en la raiz del repo (era el ultimo pendiente
  de la Rama web del handoff del simbolo C14). Fuente: Drive
  `01_Brand_Assets/C14_Brand_Mark/favicon.ico`.
- **Wordmark solo (cuarta variante de marca)** -- 'Feed Your Roots' sin simbolo, Playfair Display Bold, 4 colores. Aprobado solo para cuando el simbolo ya aparece en otra parte de la misma pieza -- nunca como primera aparicion de marca. Documentado en FYR_Brand_Mark_Spec_v1.md Seccion 05 y en el PDF del manual. Registrado en Airtable y Drive (01_Brand_Assets/C14_Brand_Mark/).
- **FYR_Protocolo_De_Trabajo.md** -- se prohibe `sed -n` como comando de
  lectura por indice de linea; se reemplaza por `cat -n` / `awk` con `NR`
  en los tres puntos del documento que lo mencionaban. Se agrega regla
  nueva: cuando el texto de un reemplazo (`old`) tiene mas de una linea
  y contiene tildes o ene, usar reemplazo por indice de linea
  (`readlines()` + `assert` de la linea esperada) en vez de heredoc de
  texto largo como primer intento -- evita fallos de assert por
  diferencias de codificacion/normalizacion Unicode.
- **Rama web completada** -- las 16 referencias originales a la marca vieja
  (nav, footer, 4 paginas legales, 6 correos transaccionales) se reemplazaron
  por el simbolo C14 (Root Black en nav, lockup vertical en footer).
  build/build.py se corrio para propagar los cambios a las paginas generadas.
  Los 10 archivos del logo viejo (assets/brand/) y los 8 del lockup vertical
  4x5 obsoleto se borraron del repo tras confirmar cero referencias activas.
- **Lockup vertical corregido (segunda revision)** -- el archivo 1x1 generado
  inicialmente traia fondo solido incorrecto en la variante -parchment
  (deberia ser transparente, como el resto del sistema). Se regenero con
  Claude Design, fondo transparente en las 4 variantes de color, verificado
  con svgelements antes de aceptar. Actualizado en repo, Drive y Airtable.
- **assets/brand/ reestructurado** -- la subcarpeta c14/ (36 archivos mezclados)
  se separo en icons/, lockups-horizontal/, lockups-vertical/, wordmarks/ por
  tipo de pieza. Las 24 referencias en 13 archivos del sitio se actualizaron
  a las nuevas rutas. Nombres de archivo intactos por trazabilidad con
  Drive/Airtable.
- **7 plantillas de Resend actualizadas** -- thankyou-complete, -homestead,
  -family, -starter, -core y outreach-creators. Header con wordmark-solo,
  footer con lockup-vertical (160px, sin el SVG decorativo de brote que
  tenian antes). Padding del footer reducido para no duplicar el margen
  interno del propio lockup. 6 correos de prueba enviados y verificados.
- **og:image y favicon adaptativo** -- index.html y las 4 paginas legales
  ganan etiquetas og:image/twitter:image (simbolo 1024px, para preview de
  WhatsApp/redes) que faltaban. Favicon con dos variantes SVG segun
  prefers-color-scheme (negro en modo claro, parchment en modo oscuro) --
  antes el favicon negro se perdia en tabs con tema oscuro.
- **FYR_Protocolo_De_Trabajo.md** -- se documenta el proceso estandar para
  actualizar el project knowledge de Claude.ai: editar primero en el repo
  de Termux, copiar a Downloads/knowledge-update/, Johnny sube manualmente.
  Nunca generar contenido nuevo directo para Downloads sin que exista
  primero en el repo.


## 2026-09-15

- **Simbolo oficial de marca (C14)** -- alta del logo/isotipo aprobado
  (frasco con arbol), trazado en vector desde el original de Johnny.
  4 variantes de color + lockup horizontal + lockup vertical, registrados
  en Airtable (4 filas, un registro por pieza maestra agrupando sus
  variantes). Nuevo `knowledge/FYR_Brand_Mark_Spec_v1.md` con reglas
  medibles (espacio de proteccion X = 15.6% altura, minimo 32px con
  excepcion favicon 16px, proporcion fija 1:1.405).
- **FYR_Asset_Governance_Policy.md** -- v2.3: separacion de C14_Brand_Mark
  de C01-C03_Logo_Concepts (que pasa a ser exploracion historica), y
  excepcion de estilo documentada para el simbolo de marca (tinta plana,
  sin acuarela -- unica excepcion al bloque de estilo base).
- **Badge FYR retirado** de uso activo (no llego a existir en repo/Airtable,
  solo en Drive). **Tree of Life (C01)** reclasificado: ya no es "logo
  oficial", pasa a ilustracion insignia de marca -- descripcion en Airtable
  corregida.
- **Pendiente v1.1** (no bloqueante): gap del lockup vertical mide 142px,
  deberia ser X=99.5px -- ver seccion "Pendientes" en FYR_Brand_Mark_Spec_v1.md.

## 2026-09-13 a 2026-09-14

- **Bug critico resuelto: centrado impredecible en marco_grande_portada** --
  mismo patron que el bug de 30-ago mencionado abajo, ahora en el titulo de
  portada de carrusel: render_text_block centraba el texto dentro de su box,
  generando offset cuando fit_text reducia la fuente. Fix: render_text_block_top
  con margen fijo de 20px bajo el marco.
- **Salto de linea manual en titulos (\n en texto_titulo)** -- _wrap_text
  hacia text.split(), que colapsaba \n como espacio -- no habia forma de
  forzar jerarquia retorica en un titulo de 2 lineas. Fix: _wrap_text respeta
  \n como salto forzado, wrap automatico dentro de cada segmento.
- **full_bleed corregido de raiz + ventana_texto (layout nuevo)** -- full_bleed
  recortaba la imagen al canvas completo y pegaba un overlay semi-transparente
  encima, dejando SIEMPRE imagen real visible detras del texto sin importar el
  contenido. Confirmado con evidencia visual real en PZA_1.2 Slide 2.
  full_bleed se corrige a SOLO imagen (modo contain, nunca crop), nunca texto.
  ventana_texto (nuevo) reemplaza el uso-con-texto: imagen contenida arriba +
  franja de texto SOLIDA (sin transparencia) abajo. Refaccion completa de
  punta a punta: codigo (base.py, config_loader.py, layout_specs.py),
  gobernanza (FYR_Layout_Specs_v1.md, FYR_Motor_Ensamblado_Arquitectura_v1.md,
  FYR_Principios_De_Composicion.md), SKILL.md (3 referencias corregidas), y
  migracion de los 4 briefs existentes que usaban full_bleed con texto.
- **Proporcion derivada en ventana_texto** -- la zona de imagen ya no es 2/3
  fijo, se calcula a partir del ratio real de la imagen (ancho canvas / ratio),
  con tope maximo 80% imagen / piso minimo 20% texto. Validado con caso real
  (portada del Half-Acre Blueprint, ratio 0.773 -> 78% imagen calculado antes
  del tope, coincide con el 80% pedido).
- **render_text_block_top aplicado a texto de cuerpo** -- solo_texto,
  ventana_texto, texto_lateral usaban render_text_block (centrado, con el
  mismo bug de offset). Los 3 migrados a render_text_block_top.
- **Politica de salto de linea manual en texto de cuerpo (gobernanza nueva)**
  -- 3 formas retoricas identificadas (producto/activo nombrado -> linea
  propia; serie de clausulas cortas -> setup agrupado + remate aislado; caso
  general -> pausa gramatical mas cercana al punto medio), con verificacion
  de ancho real via draw.textlength() antes de fijar el corte. Documentado en
  FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 3.
- **Puentes narrativos entre slides de imagen pura (gobernanza nueva,
  FYR_Principios_De_Composicion.md Seccion 8)** -- Test de Silueta (principio
  de animacion clasica) + apertura/cierre de loop narrativo (ya documentado
  en Sistema_Maestro_CRS_v2.md) combinados en una regla: cuando una secuencia
  de full_bleed cambia de sujeto o abre un loop sin nombrarlo, insertar un
  slide solo_texto puente -- nunca agregarle texto a la imagen. Fase 4 del
  roadmap (extension a video/reels) identificada y anotada, no iniciada.
- **Limpieza de repositorio:** .gitignore actualizado (produccion nunca va a
  Git -- production/briefs/, assets_local/, output/, pdfs_normalized/);
  archivos ya trackeados desde antes sacados del tracking con git rm --cached
  (contenido intacto en disco). Confirmado que las 3 piezas demo
  (PZA_demo/_seeds/_reel) usaban placeholders sinteticos que ocultaban el bug
  de full_bleed -- no son referencia confiable hasta regenerarse.
- **FYR_Protocolo_De_Trabajo.md** -- 6 reglas de comportamiento nuevas:
  codigo siempre con indice de linea, grep/sed de confirmacion en el mismo
  bloque que el cambio, comando de Termux automatico ante pedidos de
  actualizar/verificar, prohibicion de /tmp, evitar `!` en heredocs de bash
  interactivo (history expansion), y registro obligatorio en este CHANGELOG
  tras hitos importantes.

## 2026-08-30

- **assemble.py (COMPLETO)** -- el motor de ensamblado local queda terminado:
  main.py (orquestador), image_fetcher.py (verificacion de assets, no
  descarga directa), compositores Tipo A/B/C/BASE/acentos completos y
  probados. Primera pieza real generada de punta a punta (PZA_demo, 5
  slides en produccion/output/).
- **marco_grande_cuadrado (layout nuevo)** -- portada de reel/video 9:16,
  asset fijo con vid+hoja integrados (FYR_ASSET_marco-cuadrado_9x16_v1.png,
  registrado en Airtable y Drive C12_Frames), sin escalado dinamico.
- **marco_grande_portada (layout nuevo)** -- portada de carrusel 4:5, sin
  subtitulo, ancho fijo (808px) replicando el mismo ancho absoluto que la
  portada 9:16 -- decision de consistencia de marca (4:5 vertical / 9:16
  cuadrado como default de toda portada).
- **Bug critico resuelto: centrado vertical impredecible en texto
  encadenado** -- render_text_block centraba el texto dentro de su box,
  generando offset variable cuando el tamano de fuente se reducia
  internamente. Fix: render_text_block_top (nueva funcion), y decision de
  usar posiciones Y absolutas (medidas independientes) en vez de
  encadenadas para titulo/subtitulo de portada.
- **Herramienta nueva: editor_posicion_texto.html** -- carga la portada
  real y permite ajustar posicion/tamano/interlineado de texto con
  sliders sobre la imagen real, exportando valores en pixeles reales.
- **Geometria rotada medida:** doble_marco, etiqueta_colgante,
  nota_esquina -- todos confirmados rotados en el asset real (~8-12 grados)
  con medidor_esquinas.html, corrigiendo el algoritmo simple original que
  asumia alineacion a ejes.
- **FYR_Asset_Governance_Policy.md** -- aclarada la descripcion de
  C12_Frames (dos tipos de marco distintos: rectangular alto vs cuadrado
  con decoracion integrada).
- **Feed-Your-Roots-Brand-Bible.md** -- excepcion tipografica Source Serif
  Pro corregida (nombre real, no el sucesor Source Serif 4).
- **FYR_Protocolo_De_Trabajo.md** -- fusionada estrategia de ramas desde
  CLAUDE.md (rama de Claude Code).
- **TikTok:** cuenta activa (estaba bloqueada por SIM prepago, ya resuelto).

## 2026-08-28

- **FYR_Protocolo_De_Trabajo.md** — agrega sección "Estrategia de ramas",
  fusionando el conocimiento que vivía en CLAUDE.md (rama de Claude Code):
  main es producción en vivo vía GitHub Pages, código de sitio va en rama
  separada con revisión previa, contenido/texto puede ir directo a main.

- **FYR_Motor_Ensamblado_Arquitectura_v1.md** (creado) — especifica los 6
  dominios de diseño de `assemble.py`: geometría de canvas, los 4 tipos de
  layout (A/B/C/D), tipografía, recorte de imagen, contrato del script,
  schema JSON. Es la base sobre la que se escribió todo el código de
  `production/scripts/assemble/` hasta la fecha.
- **Feed-Your-Roots-Brand-Bible.md** — agregada excepción tipográfica:
  Source Serif Pro Regular reemplaza a Playfair Display específicamente
  para el título de portada/cierre en contenido de video/carrusel
  (Instagram, TikTok). Medido por píxel contra mockup real: 93px,
  cap-height 61px, contorno 6px. Playfair Display se mantiene sin cambios
  para el sitio web y piezas impresas grandes — la Malla ya documentaba
  este criterio de uso por formato, el Brand Bible no lo reflejaba.

## 2026-08-23 a 2026-08-24 (previo a este changelog)

- **FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md** (creado) — arquitectura
  de los 3 skills (fyr-content, trend-scout, performance-lens) comunicados
  vía Airtable.
- **FYR_Asset_Governance_Policy.md** — v2.2: estructura C09-C13 (Frames,
  Layout_Elements), renombre de layout_specs a FYR_Layout_Specs_v1,
  corrección de 5 referencias rotas en SKILL.md.
- **reference_assets/FYR_Layout_Specs_v1.md** — mismo commit que arriba,
  primera versión con el nombre actual.
- **Feed-Your-Roots-PDF-Guide.md**, **seed-library-final.md** — gobernanza
  de layouts (Hook→Layout, slides por Fase, loop visual en cierre).

## 2026-08-22 (previo a este changelog)

- **FYR_Malla_60_Temas_Virales_v2.md**, **Sistema_Maestro_CRS_v2.md**,
  **hooks_verbales_20_v2.md** — creación inicial junto con la skill
  fyr-content y la base de conocimiento del sistema de contenido.

---

*Para el historial completo de cualquier documento: `git log --follow -- knowledge/NOMBRE.md`*
