# FYR — Sistema Viral de 3 Skills — Fuente de Verdad
**Versión 1.0 — 24 de agosto 2026**
**Propósito:** que cualquier sesión de Claude (chat o Claude Code) entienda la arquitectura completa del sistema de producción+tendencias+performance sin tener que reconstruir el razonamiento desde cero. Este documento se edita in-place cuando algo del sistema cambia — no se le agregan entradas nuevas al final tipo changelog. Si una sección queda obsoleta, se reescribe esa sección.

---

## 1. Visión — qué problema resuelve este sistema

`fyr-content` (la skill productora, ya existente) sabía producir piezas siguiendo el Sistema Maestro CRS y la Malla de 60 Temas, pero producía **a ciegas de lo que está pasando afuera** — sin señal de qué formatos, sonidos o ángulos están funcionando en la plataforma en este momento.

El sistema completo tiene 3 skills que se reparten el trabajo:

1. **`trend-scout`** (construida en esta sesión) — caza señales virales externas y las traduce al lenguaje propio de la marca (Hook CRS + Fase de Embudo), dejándolas listas para producir.
2. **`fyr-content`** (ya existente, requiere un ajuste menor documentado en §5) — produce piezas, ahora con la opción de montarse sobre una señal de tendencia aprobada en vez de partir siempre de cero.
3. **`performance-lens`** (NO construida todavía — diseño reservado en §6) — mide qué piezas publicadas convirtieron mejor y retroalimenta tanto a `trend-scout` (qué tipo de señal vale la pena perseguir) como a `fyr-content` (qué patrones repetir).

**La ambición de fondo, no solo el mecanismo:** cuando `performance-lens` acumule suficientes datos, el sistema debe poder identificar un **formato firma** — una estructura propia que supera consistentemente el rendimiento de las tendencias externas montadas. Ese formato firma, ejecutado con constancia (candidato natural: la serie diaria "365 Days of Homestead"), es el mecanismo real por el cual una marca deja de perseguir tendencias y empieza a crear las suyas. El sistema no promete esto automáticamente — da la infraestructura de datos para que se pueda decidir con evidencia en vez de con intuición.

**Portabilidad:** las 3 skills están diseñadas para no tener nada de FYR hardcodeado en su lógica — toda referencia a marca, avatar, industria o país vive en un único archivo `brand.config.yaml` en la raíz del repo. Migrar el sistema a otra marca, industria o mercado (LATAM, Europa, u otro negocio completamente distinto) es, en teoría, copiar las skills y escribir un config nuevo. Esto no está probado todavía con una segunda marca real — es el diseño, no un hecho verificado.

---

## 2. Por qué las 3 skills nunca se invocan entre sí

Decisión de arquitectura deliberada: **las skills se comunican exclusivamente a través de Airtable, nunca directamente.**

Razón: si `trend-scout` invocara a `fyr-content` directamente (o viceversa), el sistema se vuelve frágil — un cambio en una skill puede romper la otra, y no se puede correr una sin la otra. Con Airtable como intermediario:

- `trend-scout` puede correr sola, sin que `fyr-content` esté siquiera instalada, y sigue siendo útil como banco de inspiración leído manualmente.
- `fyr-content` sigue funcionando exactamente igual que hoy si `trend-scout` nunca corrió esa semana — el chequeo de tendencias aprobadas es un paso opcional al inicio, no una dependencia dura.
- `performance-lens`, cuando exista, lee de ambas tablas sin que ninguna de las otras dos sepa que existe.

Esto también es lo que hace la portabilidad real: cada skill es independiente, el único contrato compartido es el schema de las tablas de Airtable.

---

## 3. Diagnóstico de origen — por qué se construyó esto

La sesión arrancó con un documento de investigación (pegado por Johnny, generado por otro asistente) que mezclaba herramientas reales con nombres inventados o no verificables — "Eden MCP", "Insightfulpipe MCP", "TikAdTools con Sound Velocity Mapping". Antes de construir nada se hizo una verificación real vía web_search de cada herramienta mencionada. Resultado de esa verificación:

**Existe y es usable:**
- Apify — actors del TikTok Creative Center (scraping estructurado, de pago tras trial).
- trendsmcp.ai — MCP remoto, tier gratis 100 requests/día, cubre TikTok + Google Trends + YouTube.
- claude-video (proyecto real de bradautomates, no "Video Toolkit" genérico) — skill open-source que usa yt-dlp + ffmpeg + Whisper para deconstruir video.
- meta-mcp para Instagram Graph API — insights reales (reach, saves, shares) pero requiere cuenta Business/Creator + Meta Developer App.

**No se pudo verificar / probablemente inventado por el otro asistente:**
- "Eden MCP" con "3 millones de publicaciones indexadas" — no localizado.
- "Insightfulpipe MCP" — no localizado.
- "TikAdTools" con "Sound Velocity Mapping" — terminología no verificable, suena a alucinación.

**Lección operativa que queda registrada aquí:** cualquier nombre de herramienta/MCP que aparezca en un documento pegado por el usuario (venga de donde venga) se verifica con búsqueda real antes de construir cualquier cosa sobre él. No se asume que "sonar técnico y específico" equivale a "existir".

---

## 4. La skill `trend-scout` — qué hace y cómo

### 4.1 Ubicación real en el repo

```
~/FeedYourRootsUS/.claude/skills/trend-scout/
├── SKILL.md
├── README.md
├── brand.config.example.yaml
├── references/
│   ├── fuentes.md
│   └── schema_trend_signals.md
└── scripts/
    └── deconstruct_video.sh   (permiso ejecutable, chmod +x aplicado)
```

**Nota de instalación importante:** originalmente se copió a `.claude/skills/user/trend-scout/`, asumiendo (sin verificar) que `fyr-content` vivía bajo un subnivel `user/`. Al inspeccionar el repo real se confirmó que `fyr-content` vive directo en `.claude/skills/fyr-content/`, sin ese subnivel. Se corrigió moviendo `trend-scout` a `.claude/skills/trend-scout/` — ambas skills son ahora hermanas al mismo nivel, consistente entre sí. **Lección:** nunca asumir estructura de carpetas de memoria; verificar con `find`/`ls` antes de decidir una ruta de instalación.

`brand.config.yaml` (copia real del `.example`, ya con valores de FYR) vive en la raíz del repo, mismo nivel que `knowledge/`.

### 4.2 Los dos flujos

**Flujo A — Barrido de tendencias** (uso semanal o bajo demanda):
1. Captura 8-15 señales candidatas (sonido/hashtag/formato) desde las fuentes disponibles.
2. Filtra por Score_Afinidad_Avatar (1-5); solo avanzan las que puntúan ≥3.
3. Traduce cada señal sobreviviente a Hook_CRS_Equivalente + Fase_Embudo_Sugerida + Brief_Adaptacion — este paso es el corazón de la skill, nunca se salta.
4. Registra en Airtable con Estado=Detectada; espera aprobación explícita del usuario antes de pasar a Aprobada.

**Flujo B — Deconstrucción de un video puntual** (bajo demanda, con URL):
1. Intenta subtítulos gratis con yt-dlp.
2. Si no hay, avisa que el hook verbal exacto requeriría Whisper/Groq (API key propia del usuario) — no bloquea, sigue con análisis solo visual.
3. Descarga el video, extrae frames por cambio de escena (no por segundo fijo, más barato en tokens) con ffmpeg.
4. Lee los frames con la tool `view`, identifica hook visual, ritmo de cortes, texto en pantalla.
5. Borra el video/audio descargado al terminar — solo se conservan frames si el usuario pide verlos. El output es siempre una descripción en texto de la estructura, nunca el material audiovisual ajeno reutilizado.

### 4.3 Fuentes de datos — gratis vs. pago

| Fuente | Costo | Requiere configuración previa |
|---|---|---|
| TikTok Creative Center (via web_fetch/web_search) | Gratis | Ninguna — vía por defecto |
| trendsmcp.ai | Gratis (100 req/día) | Cuenta + MCP conectado por el usuario |
| Apify actors | De pago tras trial | Cuenta Apify + MCP conectado; nunca asumir que existe |
| yt-dlp + ffmpeg (deconstrucción local) | Gratis | Ninguna, ya disponibles en el entorno |
| Whisper vía Groq | Gratis con límite | API key propia del usuario |

**Regla de honestidad no negociable de la skill:** si ninguna fuente devuelve data verificable con fecha, se dice explícitamente — nunca se presenta una tendencia "recordada" del entrenamiento del modelo como si fuera actual. Esta regla existe porque toda la cadena de valor del sistema depende de que la señal sea real.

### 4.4 Estado real de validación (honestidad operativa)

- **Lógica, estructura, prompts de scoring del SKILL.md:** completos y listos, sin necesitar ninguna conexión nueva.
- **Conexión a datos vivos de tendencias (Apify/trendsmcp):** NO probada en esta sesión — no hay ninguno de esos dos MCP conectados en la cuenta usada durante la construcción. La skill está escrita para usarlos en cuanto se conecten, pero no hay confirmación de que el JSON real que devuelvan calce exactamente con lo asumido. Primer uso real de Flujo A debe tratarse como prueba, no como operación rutinaria ya validada.
- **Flujo B (yt-dlp + ffmpeg):** herramientas locales, no probadas end-to-end todavía en esta sesión tampoco — pendiente de una primera corrida real.

---

## 5. Tabla Airtable `Trend_Signals` — schema final verificado

**Base:** `appMy5aOwifSbBLPR` — **Tabla:** `Trend_Signals` (`tblxdaRsgEy8CHvV9`)

| Campo | Tipo Airtable real | Config / Notas |
|---|---|---|
| Signal_ID | Single line text (primary) | Formato `TR-####`, consecutivo. Antes de asignar uno nuevo, consultar el último existente — nunca adivinar. |
| Fecha_Deteccion | Date (ISO) | |
| Tipo_Señal | Single select | Sonido / Hashtag / Formato / Ángulo narrativo |
| Nombre_Señal | Single line text | |
| Plataforma | Single select | TikTok / Instagram Reels / YouTube Shorts |
| Pais | Single select (solo "US" por ahora) | Decisión explícita de Johnny: de momento solo se atiende mercado US. Cuando haya expansión a LATAM/Europa, se agregan las opciones necesarias en ese momento — no antes. |
| Industria_CC | Single line text | |
| Curva_Momentum | Single select | Ascendente / Meseta / Descendente |
| Volumen_Uso | Number (integer) | Puede quedar vacío si la fuente no lo da |
| Ventana_Vida_Estimada | Single line text | Texto libre ("7-14 dias"), estimación cualitativa, no un dato duro |
| Score_Afinidad_Avatar | Number | 1-5, criterio en SKILL.md §Paso 2 |
| Pilar_Relacionado | **Link to another record → Themes** | Verificar nombre exacto contra `Themes` real antes de escribir — nunca de memoria |
| Hook_CRS_Equivalente | **Single select propio, 20 opciones (01 Negativo → 20 Revelación)** | **Corregido en esta sesión** — ver §5.1 |
| Fase_Embudo_Sugerida | Single select | F1 / F2 / F3 / F4 |
| Formato_Sugerido | Single select | POV / Antes-Después / Countdown / Storytime |
| Brief_Adaptacion | Long text | Output central de la traducción CRS |
| Sonido_URL_Referencia | URL | |
| Video_Referencia_URL | URL | |
| Estado | Single select | Detectada / Aprobada / Usada / Expirada / Descartada |
| Tema_Vinculado | Link to another record → Themes | |
| Content_Piece_Generada | Link to another record → Content_Pieces | Cierra el loop: qué pieza terminó usando esta señal |
| Fecha_Aprobacion | Date | |
| Fecha_Expiracion | Date | Calculada al aprobar, a partir de Ventana_Vida_Estimada |
| Resultado_Post_Uso | **Single select: Alto / Medio / Bajo / Sin datos** | **Corregido en esta sesión** — ver §5.2. Mismo vocabulario que `Content_Pieces.Performance` a propósito, para que ambas tablas crucen sin traducción |
| Notas | Long text | |

### 5.1 — Bug corregido: Hook_CRS_Equivalente

Al importar el CSV y convertir tipos manualmente, el campo quedó como `multipleRecordLinks` hacia `Themes` (heredando el hook de un tema linkeado) en vez de ser una selección propia. Esto obligaba a vincular un tema completo solo para heredar su hook — un rodeo sin sentido, y además duplicaba conceptualmente el campo `Hook Asignado` que ya vive en `Themes`.

**Corrección aplicada:** convertido a `singleSelect` independiente con las 20 opciones del catálogo de hooks verbales, sin ningún link. Esto rompió 2 dependencias automáticas de Airtable (un lookup propio de `Trend_Signals` y el campo espejo inverso en `Themes`) — se confirmó que esa ruptura era la esperada y correcta antes de confirmar el cambio, no un error.

**API no soportó el cambio de tipo de campo directamente** (`update_field` de la tool Airtable disponible no permite cambiar de `multipleRecordLinks` a `singleSelect`, ni crear ni borrar campos) — el cambio se hizo manualmente en la UI de Airtable por Johnny, siguiendo instrucción exacta dada en el chat.

### 5.2 — Bug corregido: Resultado_Post_Uso

Se había convertido a singleSelect antes de que existieran datos con los que generar opciones, dejando una única opción con nombre vacío (`""`), inservible. Corregido manualmente en la UI agregando las 4 opciones correctas: Alto, Medio, Bajo, Sin datos.

### 5.3 — Limitación real de las tools de Airtable disponibles en esta cuenta

Confirmado en esta sesión: las tools conectadas (`Airtable:update_field`, `get_table_schema`, `create_records_for_table`, `update_records_for_table`, `search_records`, `submit_form`, `delete_table`, `delete_records_for_table`) **no incluyen crear campo, borrar campo individual, ni editar las opciones de un singleSelect ya existente.** Cualquier cambio estructural de ese tipo requiere edición manual en la UI de Airtable — esto no es un límite de la skill, es un límite del conector MCP tal como está configurado hoy. Si en el futuro se agregan tools de creación/borrado de campo, esta nota queda obsoleta y debe eliminarse.

---

## 6. La skill `performance-lens` — diseño reservado, NO construida

No existe todavía como archivo. Este es el contrato de diseño que debe respetar cuando se construya:

- Lee `Content_Pieces.Performance` + `Trend_Signals.Content_Piece_Generada` para calcular qué tipo de señal (por Tipo_Señal, Hook_CRS_Equivalente, Pilar_Relacionado) convierte mejor.
- Escribe el resultado de vuelta en `Resultado_Post_Uso` de la fila de `Trend_Signals` correspondiente.
- Mide con un **Índice Viral Compuesto** de pesos configurables por plataforma (para Reels: saves+shares pesan doble que likes; para TikTok: retención completa pesa más) — los pesos deben vivir en `brand.config.yaml`, no hardcodeados.
- Fuente de datos primaria: Instagram Graph API vía MCP (meta-mcp), que requiere cuenta Business/Creator + Meta Developer App — ninguna de las dos cosas está confirmada como ya configurada por Johnny.
- Para TikTok orgánico propio, la API es más hostil — el plan pragmático es fallback a export CSV manual de TikTok Studio, parseado por la skill.
- Cadencia sugerida: medición a las 72h post-publicación y de nuevo a los 7 días.
- **No construir hasta tener ~10 piezas publicadas con datos reales** — antes de eso no hay señal suficiente que minar, y construir la skill antes sería trabajo especulativo sin forma de validarse.

---

## 7. El módulo de conexión pendiente en `fyr-content`

`trend-scout/SKILL.md` §5 documenta el lado de la conexión que le corresponde a `trend-scout` (dejar señales en Estado=Aprobada, nunca invocar nada). **El lado correspondiente en `fyr-content` no ha sido verificado ni modificado en esta sesión** — sigue pendiente confirmar si ya existe o si debe agregarse.

Lo que debe pasar en `fyr-content/SKILL.md`, en su paso de selección de tema (antes de la cola normal): consultar `Trend_Signals` filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`; si hay resultados, ofrecer producir la pieza montada sobre esa señal (usando su Hook_CRS_Equivalente, Formato_Sugerido y Brief_Adaptacion como punto de partida) antes de caer al flujo normal. Al usar una señal, `fyr-content` debe escribir el `PZA-###` resultante de vuelta en `Content_Piece_Generada` de esa fila de `Trend_Signals`.

Como `fyr-content/SKILL.md` no tiene subcarpetas `references/` ni `scripts/` (confirmado por inspección real del repo — solo tiene el archivo `SKILL.md` suelto), cualquier edición a esto se hace en ese único archivo, siguiendo el patrón grep → Python heredoc con assert → grep que dicta `FYR_Protocolo_De_Trabajo.md` — nunca regenerando el archivo completo.

---

## 8. Reglas no negociables del sistema completo

Consolidado de lo que gobierna a las 3 skills, no solo a una:

- Ninguna skill inventa una tendencia sin fuente verificable con fecha.
- Ninguna señal pasa a Aprobada sin traducción CRS completa (Hook + Fase + Brief).
- Confirmación explícita del usuario para: aprobar señales, marcar expiradas, cualquier escritura en lote.
- Nombres de campos singleSelect que deben cruzar entre tablas (Pilar, Hook) se verifican contra la tabla real antes de escribir — nunca de memoria.
- Fail loudly: tabla no encontrada, config faltante, fuente sin datos → detenerse y reportarlo, nunca simular éxito parcial.
- Media descargada para deconstrucción de video se borra al cerrar la sesión de análisis, salvo pedido explícito de conservarla.
- Todo archivo que ya vive en el repo de Termux se edita ahí por comando (grep → heredoc con assert → grep) — nunca se regenera completo desde el chat. Única excepción: primera creación de un archivo que no existía.
- Este documento (`FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md`) se edita in-place cuando algo del sistema cambia — nunca se le agregan entradas al final tipo bitácora.
