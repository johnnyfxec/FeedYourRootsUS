# Feed Your Roots — Política de Gestión de Assets
**Versión 2.4 — 10 de octubre 2026**
**Propósito:** que cualquier persona o agente que cree, nombre, ubique o registre un asset nuevo lo haga sin tener que reconstruir esta lógica desde cero.

---

## 1. Principio rector

Todo asset se clasifica por **una sola pregunta**: ¿es identidad de marca reutilizable, o es contenido de marketing para publicar?

- **Identidad de marca** (`01_Brand_Assets`, `02_Decorative_Elements`, `03_Seed_Library`) → piezas atómicas sin fecha de caducidad, reutilizables en cualquier pieza futura.
- **Marketing** (`05_Marketing_Assets`) → contenido producido para un canal específico, con propósito de publicación.
- **Producto** (`04_Producto_Finalizado`) → lo que se vende. Incluye también sus portadas de venta (Covers), porque son la cara oficial del producto Y un asset reutilizable de marketing a la vez.
- **Materia prima narrativa** (`06_Narrative_Stock`) → escenas completas, sin espacio reservado para overlay, listas para usarse tal cual en video, post individual o carrusel.

Cuando algo no encaje limpio en una categoría, la pregunta correcta no es "¿dónde cabe mejor?" sino "¿para qué se va a usar realmente?" — la función define la ubicación, no la apariencia.

**Nota de gobernanza sobre `Themes`:** aunque esta política cubre assets visuales, el control de calidad empieza antes — en la tabla `Themes` misma. Ningún tema nuevo se crea sin verificar que no exista ya un duplicado semántico (mismo dolor del avatar en palabras distintas). El detalle mecánico de esa verificación vive en el `SKILL.md` (fuera del alcance de este documento), pero el principio es el mismo que rige aquí: la función define la existencia, no la redacción superficial.

---

## 2. Estructura de carpetas (Google Drive — `FYR/`)

```
FYR/
├── 00_Brand_Bible_Reference/
│   ├── Book_Elements/              (QR, DYK boxes — piezas reutilizables del libro)
│   └── Cover_Drafts_Archive/       (borradores históricos, no usar en producción)
├── 01_Brand_Assets/
│   ├── C01-C03_Logo_Concepts/     (exploracion historica -- ver C14 para el simbolo activo)
│   ├── C14_Brand_Mark/             (simbolo oficial de marca, lockups aprobados -- ver
│   │                              knowledge/FYR_Brand_Mark_Spec_v1.md para reglas medibles)
│   ├── C04-C05_Patterns/
│   ├── C06_Texture/
│   ├── C07-C08_Icon_Sets/
│   ├── C09-C10_PDF_Covers/
│   ├── C11_Corners/            (pendiente rehacer assets, ver Seccion 9)
│   ├── C12_Frames/             (marcos de madera reutilizables: FYR_ASSET_marco-madera_[4x5|9x16]_v1.png
│   │                          -- marco rectangular alto, mismo asset en ambos aspectos, usado para
│   │                          marco_grande y marco_grande_portada; FYR_ASSET_marco-cuadrado_9x16_v1.png
│   │                          -- marco cuadrado CON vid y hoja decorativa ya integrados, solo 9:16,
│   │                          exclusivo de marco_grande_cuadrado)
│   └── C13_Layout_Elements/    (assets de los layouts vigentes de Content_Pieces — ver knowledge/reference_assets/FYR_Layout_Specs_v1.md)
│       └── Style_References/   (referencias de estilo NO reutilizables; sin uso desde el 11-oct-2026)
├── 02_Decorative_Elements/          (E01-E36+, clip-art suelto 1:1, fondo transparente)
├── 03_Seed_Library/
│   └── WObg/                        (L01-L101, fondo transparente — única versión en uso)
├── 04_Producto_Finalizado/
│   ├── RGBc/                        (PDFs finales, no catalogados en Airtable)
│   ├── CMYK/                        (PDFs finales, no catalogados en Airtable)
│   └── Covers/
│       ├── Cuadradas_1x1/
│       ├── Verticales_2x3/
│       └── Horizontales_3x2/
├── 05_Marketing_Assets/
│   ├── Social_Media/
│   │   ├── TikTok_Covers/
│   │   ├── IG_Square/
│   │   ├── IG_Story/
│   │   ├── Pinterest_Pins/
│   │   ├── Video_Cover_Templates/
│   │   └── Content_Pieces/          (carruseles y videos completos generados desde la tabla Themes — ver Sección 6;
│   │                                cada `PZA_[tema]/[fecha]/` guarda SOLO archivos terminados: los PNG de cada slide del carrusel
│   │                                o el MP4 final del video. Las imágenes de entrada (escenas) viven en 06_Narrative_Stock;
│   │                                los WAV y timings.json del video son intermedios regenerables, no se suben)
│   ├── Ad_Creatives/
│   │   ├── Meta/
│   │   ├── Hooks/
│   │   └── Lifestyle/
│   ├── Web_Site/
│   │   └── Blog_Journal_Headers/
│   └── Video_Production/PZA_[tema]/ (insumos de trabajo de un video, p. ej. la portada ya compuesta; no es banco de recursos.
│                                    El render corre en GitHub Actions, ver knowledge/FYR_Protocolo_Edicion_Video.md; el producto final va a Content_Pieces/)
├── 06_Narrative_Stock/               (escenas 9:16 sin overlay, fuente de b-roll para cualquier canal)
└── 07_Influencer_Outreach/           (solo la lista fuente; el registro de comunicación vive en Airtable)
```

**Regla de creación de carpetas nuevas:** antes de crear una carpeta, verificar si ya existe una que cumpla la misma función. Si aparece un tipo de asset nuevo sin casa clara, detenerse y decidir conscientemente (no crear "por si acaso").

---

## 3. Convención de nombres de archivo

```
[PREFIJO]_[categoría][número]_[slug-descriptivo]_[aspecto]_v[versión].[ext]
```

| Prefijo | Uso |
|---|---|
| `FYR_B##` | Social Media (Categoría B del Brand Bible) |
| `FYR_C##` | Brand Assets (Categoría C) |
| `FYR_D##` | Ad Creatives (Categoría D) |
| `E##` | Decorative Elements |
| `L##` | Seed Library (sufijo `-wobg` = fondo transparente) |
| `WEB-` | Banners y headers de sitio web |
| `TPL-` | Templates reutilizables (no assets terminados) |
| `STOCK-` | Narrative Stock |
| `COVER-` | Portadas de producto |
| `FYR_EXTRA_` | Asset aprobado sin categoría asignada al momento de crearlo |
| `FYR_PZA_[tema]` | Piezas completas de la Malla de Temas (carrusel/video, un archivo por slide). Video final: `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4` (la variante es el ID de subtítulo/cierre/voz, ver Protocolo de Edición de Video) |

**Regla de versión:** un archivo solo sube de número de versión (`v2`, `v3`...) **después** de que la versión anterior ya fue subida a Drive y confirmada. Nunca versionar en el nombre antes de tener la anterior archivada — evita huecos de versión sin sentido.

**Regla de aspecto:** siempre en formato `AxB` (ej. `9x16`, `1x1`, `4x5`, `2x3`, `3x2`) — nunca mezclar con formatos tipo `16:9` en el nombre de archivo (los dos puntos rompen compatibilidad con algunos sistemas de archivo).

---

## 4. Reglas de estilo de marca (para prompts de generación)

**Bloque de estilo base — usar siempre como punto de partida (actualizado 19-oct-2026: se quitó el "Output..." fijo del final, ver nota abajo):**
```
Hand-drawn storybook illustration in the tradition of Beatrix Potter, modernized with the flat, confident color sensibility of contemporary Oatly packaging. Fine ink linework: delicate, slightly imperfect 1–2pt lines with visible hand tremor. Soft watercolor washes, warm parchment background (#F5ECD7), palette of forest green, terracotta orange, warm brown, harvest gold. NEVER include: photorealism, 3D rendering, neon colors, digital gradients, plastic objects, hard black outlines.
```

**Regla de uso obligatoria (18-oct-2026, corrección tras detectar desviación en el lote PZA_3.1–PZA_9.3):** TODO prompt de Gemini generado por `fyr-content` o `fyr-video-assembler` empieza citando este bloque exacto, palabra por palabra — nunca una paráfrasis como "watercolor and ink illustration, vintage nature-journal style" (esa frase quedó obsoleta y NO debe volver a usarse).

**Línea de output obligatoria — PNG + ratio correcto por layout (corrección 19-oct-2026: el "Output..." fijo que antes vivía en el bloque de estilo base se quitó de ahí porque su ratio variaba por layout y quedaba inconsistente; ahora es una línea separada que CADA prompt construye así):** inmediatamente después del bloque de estilo base, antes del bloque de composición, todo prompt lleva su propia línea `Output <ancho>x<alto>px, <ratio> portrait/square, PNG format.` — el formato PNG es SIEMPRE obligatorio, sin excepción, y el ratio se calcula según el layout real del slide (ver `reference_assets/FYR_Layout_Specs_v1.md` para el hueco exacto de cada layout — por ejemplo `marco_grande` usa 0.78:1 real, no el 4:5 genérico de `marco_grande_portada`; video 9:16 usa `Output 1080x1920px, 9:16 portrait, PNG format.`). Esta línea de output y el ratio declarado dentro del texto específico del prompt (si lo repite, p.ej. "Aspect ratio: exactly X:Y") deben coincidir siempre — nunca señales mixtas entre ambos.

**Regla de separación prompt-copiable / nota humana (19-oct-2026, corrección tras incidente real con Gemini — ver fila en §5):** el texto que se copia literalmente a Gemini (todo lo que va dentro de las comillas del prompt citado) contiene ÚNICAMENTE instrucciones técnicas de generación de imagen — nunca una nota operacional, editorial o de contexto de producción (ej. "va dentro de la ventana del marco, no es el canvas final del video", "el compositor ajusta a la ventana rotada", "recorte mínimo aceptable"). Ese tipo de nota es información para Johnny/el ensamblado, nunca para Gemini — si se incluye dentro del prompt citado, palabras como "marco", "ventana" o "video" pueden hacer que Gemini intente dibujar literalmente esos elementos como parte de la escena. Cualquier nota de ese tipo va SIEMPRE fuera de las comillas del prompt, como una nota aparte (ej. "*(Nota para Johnny, fuera del prompt: ...)*" o en el texto descriptivo de la entrada, nunca dentro del bloque citado).

**Separación prefacio/específico (regla de ahorro de tokens, 18-oct-2026):** al escribir el campo `prompt` de cada slide en el brief/JSON de una pieza, NO repetir el bloque de estilo base completo en cada slide — se declara una sola vez por pieza (o se referencia como constante) y cada slide solo lleva su texto específico (sujeto + encuadre + mood + lo que pide esa escena en particular, incluyendo la línea de output + el bloque de composición de Layout_Specs con el ratio/fondo que toque). La Mesa de Producción (herramienta de apoyo de Fase D) concatena prefacio + línea de output + bloque de composición + específico al momento de copiar, para que Johnny siempre pegue en Gemini el prompt completo con un solo botón.

**Bloque de composición por layout — se añade SIEMPRE al bloque base (11-oct-2026):** ratio exacto según el hueco del layout (tabla de `reference_assets/FYR_Layout_Specs_v1.md`), composición a sangre sin marco ni márgenes dibujados, sujetos clave a ≥ 5 % del ancho de los bordes laterales, y el fondo según la marca `fondo` del slide: `pergamino` (liso #F5ECD7 hasta el borde, obligatorio si la imagen queda suelta sobre el pergamino en `ventana_texto`/`texto_lateral`) o `color_completo` (escena a todo color sin márgenes; se usa tal cual, sin difuminar). Texto exacto del bloque en Layout_Specs. El motor rellena el espacio con tolerancia de ratio del 2 % y avisa `RATIO:` si la imagen llegó con otra proporción.

**Regla de narrativa visual (estándar obligatorio, 18-oct-2026 — detectado comparando dos generaciones de la misma escena, S1 de PZA_3.1):** el texto específico de cada prompt (lo que va después del bloque base + composición) nunca puede ser una descripción mínima tipo "POV looking down at a messy shoebox, dim indoor light, muted brown tones" — eso produce una imagen plana, cenital, de "catálogo", sin vida. El estándar es que la imagen cuente la historia de esa escena **sin necesidad de texto escrito**, igual que ya lo logran los mejores assets del banco actual. Para eso, todo prompt específico debe construirse con estos ingredientes, conectados directamente a la intención narrativa de ese slide (no decorativos sueltos):
- **Ángulo con presencia humana implícita:** preferir perspectiva 3/4 o a la altura de quien está trabajando, no cenital puro salvo que la intención del slide sea literalmente "vista de arriba" (ej. un plano de jardín). Un ángulo ligeramente oblicuo sugiere que alguien está ahí, viviendo la escena.
- **Contexto de uso real:** 1-2 props del entorno que expliquen dónde y cuándo ocurre esto (una mesa de trabajo, una herramienta cercana, luz de una ventana, un paño) — no la escena aislada en un vacío.
- **Variación de desgaste/tiempo:** los objetos protagonistas no deben verse todos nuevos y uniformemente saturados; mezclar texturas envejecidas con elementos frescos da sensación de vida real y paso del tiempo, dentro de la paleta de marca (verde bosque, terracota, café, dorado — nunca grises/azules fríos que se salgan de la paleta).
- **El detalle debe servir a la idea del slide, no ser gratuito:** cada elemento añadido (un rótulo manuscrito, una herramienta, una mancha de uso) debe reforzar específicamente el dolor/deseo o el giro narrativo de ese slide — si no conecta con la intención, no se agrega solo por "verse más vivo".
Esta regla aplica a TODA generación nueva de aquí en adelante, no solo a la escena que la originó — es un estándar de calidad de prompt, no una corrección puntual.

**Caso de referencia aprobado (18-oct-2026):** PZA_3.1 S1 ("MY SEED BOX WAS A DISASTER UNTIL THIS", shoebox de semillas desordenado) — tras dos rondas de ajuste, Johnny confirmó el resultado como el estándar visual de "bien hecho": ángulo 3/4 sobre mesa de trabajo real (pala, cuchillo de trasplante, macetas de barro apiladas, un cajón con más macetas abajo), sobres amontonados y rebalsando *dentro y justo sobre el borde* de la caja — nunca dispersos en abanico sobre la mesa —, variación real de desgaste entre sobres (colores, ataduras de cordel, una pestaña asomando), sin ningún texto legible en los sobres, paleta de marca correcta. Usar esta imagen como vara de medida al evaluar generaciones nuevas con el mismo patrón (objetos múltiples + desorden genuino que debe leerse como incómodo, no curado).

**Excepciones aprendidas (cuándo desviarse conscientemente del bloque base):**
- **Patrones tileables (C4-C5):** el fondo debe pedirse **perfectamente plano, sin textura de papel**, o el patrón no repetirá sin costuras. La textura de papel es incompatible con seamless tiling.
- **Stickers decorativos con color botánico real (ej. semilla partida, corona de trigo):** cuando el propósito es destacar y ser memorable, el color botánico honesto (verde-musgo, ámbar de abeja) puede superar a la paleta estricta de 2 colores. Se decide caso por caso, nunca por defecto.
- **Simbolo/logo de marca (C14):** el bloque de estilo base (acuarela, linea con temblor) se abandona por completo para el simbolo activo de marca. Un logo necesita sobrevivir a 16px, bordado y troquelado -- la textura de acuarela se vuelve mancha ilegible a esos tamanos. Excepcion aprobada: tinta plana solida, un solo color, sin textura de papel, silueta cerrada. Ver `knowledge/FYR_Brand_Mark_Spec_v1.md` para las reglas exactas. Esto NO aplica a ilustraciones de marca como el Tree of Life (C01), que si sigue el bloque base.
- **Recibos, carteles, objetos cuya identidad depende de tener texto:** la regla "no text" no aplica cuando el texto es parte de la narrativa del objeto (ej. un recibo de supermercado). Si el texto es decorativo/rotulado, sí se prohíbe.

**Regla de diversidad étnica (no negociable):** toda figura humana (manos, personas parciales, rostros) debe representar diversidad de tonos de piel a través del conjunto de contenido — nunca default a piel clara como estándar.

**Regla de rostros (v2.0):** Brand Assets, íconos y elementos decorativos NUNCA muestran rostro humano — manos cortadas en la muñeca siguen siendo el estándar ahí. Pero escenas narrativas POV/emocionales (piezas de `Content_Pieces`, Sección 6) SÍ pueden mostrar rostro completo con expresión cuando la emoción es el punto de la toma — aplicando siempre la regla de diversidad de arriba.

---

## 5. Errores conocidos de generación (Gemini/Nano Banana) — verificar antes de aprobar

| Problema | Cómo se manifiesta | Corrección |
|---|---|---|
| Contenido de jars/frascos | Interpreta líquidos genéricos en vez del contenido pedido (miel opaca sale como té translúcido) | Describir textura física exacta + acción física reconocible (ej. "miel espesa goteando de cuchara") |
| Escala de manos | Manos de niño salen con proporción de adulto | Especificar "noticeably smaller and pudgier than an adult hand, proportioned like a toddler" |
| Simetría en composiciones circulares | Elementos se concentran en un lado (ej. moras solo a la derecha) | Exigir explícitamente que ambas mitades contengan la mezcla completa de elementos |
| Texto no solicitado | Aparecen letras/números en objetos sin pedirlo | Añadir "no legible text, no readable numbers" si el objeto no necesita texto para su identidad |
| Texto no solicitado en escenas con MUCHOS objetos iguales (18-oct-2026, PZA_3.1 S1) | La prohibición "no text" del bloque de estilo base no basta cuando la escena tiene varias superficies candidatas a rotular (ej. varios sobres/paquetes/etiquetas en la misma imagen) — Gemini rotuló cada sobre con el nombre de la semilla (SWEET PEAS, CARROTS...) pese al bloque base | Cuando el prompt describe múltiples packets/envelopes/labels/signs en la misma escena, reforzar explícitamente en el texto específico (no asumir que el bloque base alcanza): "no legible text, lettering or labels on any packet/envelope/surface — plain unmarked paper/fabric texture only" |
| Desorden que sale "exhibido" en vez de "amontonado" (18-oct-2026, PZA_3.1 S1) | Al pedir desorden dentro de un contenedor + algo "disperso en los bordes" ("scattered at the edges"), Gemini interpreta el contenido disperso como objetos individuales prolijamente desplegados en abanico alrededor del contenedor, en vez de amontonados — se ve curado/aspiracional, no como el momento incómodo que el slide necesita transmitir | Para desorden genuino (no exhibición), especificar que el desborde queda CONTENIDO cerca del borde del contenedor (ej. "a few packets spilling just over the rim, not spread out") y evitar frases como "scattered at the edges" que invitan a composición tipo flat-lay expuesto |
| Patrones no tileable | Costura visible al repetir en mosaico | Pedir fondo perfectamente plano sin textura; **verificar con mosaico 2x2/3x3 antes de aprobar**, nunca asumir |
| Ratio no exacto | Gemini no respeta la proporción al pixel (4:5 sale 928×1152 = 0.806; 9:16 sale 768×1376 = 0.558) y a veces el papel sale más claro o amarillo que #F5ECD7 | El ensamblado rellena con tolerancia de 2 % (aviso `RATIO:` si hay más desvío); pedir el ratio y el fondo con el bloque de composición (§4); verificar el borde de la imagen en `ventana_texto`/`texto_lateral` |
| Resolución menor al canvas del video | Gemini entrega las escenas 9:16 en 768×1376 px; el video es 1080×1920, así que el render las reescala ~1.4× (aceptable en el piloto PZA_4.2, pero resta nitidez) | Pedir/exportar a ≥1080×1920 cuando se pueda; verificar el tamaño real antes de aprobar (el render avisa si no es 9:16) |
| "Logo" con exceso de detalle vectorial | Sale como ícono de app genérico, sin conexión a la marca | Para piezas de marca "logo", usar el bloque de estilo completo (acuarela, no línea vectorial limpia) salvo que se pida explícitamente minimalismo |

---

## 6. Flujo de aprobación (cómo se decide qué se sube)

1. **Generar** con prompt basado en el bloque de estilo + brief específico.
2. **Revisar contra el brief original** — ¿cumple composición, mood, elementos pedidos?
3. **Verificar reglas técnicas** (tiling si aplica, diversidad si hay personas, ausencia de texto no deseado).
4. Si falla: **ajustar el prompt de forma quirúrgica** (una variable a la vez) — no regenerar desde cero sin diagnóstico.
5. Si pasa 2-3 intentos sin lograrlo: pausar y repensar el enfoque en vez de seguir iterando a ciegas.
6. **Aprobado** → nombrar según convención (Sección 3) → subir a la carpeta que corresponde por tipo de archivo (Sección 2): **toda escena nueva (4:5, 9:16 o 1:1) va a `06_Narrative_Stock/`**, nunca a `Content_Pieces/` → registrar en Airtable (Sección 7).

**Qué va a `Content_Pieces/PZA_[tema]/[fecha]/`:** únicamente el producto terminado (PNG de cada slide ensamblado, o el MP4). La carpeta se crea al aprobar el brief. El paso a paso de cada formato, con lo que se escribe en Airtable en cada etapa, está en `knowledge/FYR_Rutas_De_Produccion.md`.

---

## 6-bis. Regla anti-desincronización Mesa ↔ `brief.md` (incidente 19-oct-2026, PZA_4.1)

**Hay dos copias de la decisión de contenido de cada pieza: la Mesa de Producción (artefacto HTML, donde Johnny realmente trabaja y genera en Gemini) y `production/pieces/PZA_[tema]/brief.md` en el repo (de donde lee CC). Ninguna de las dos se actualiza sola cuando la otra cambia.** El incidente: el commit `d2afd86` cambió en `brief.md` qué assets usa PZA_4.1 (de banco-reuso a generación nueva) para resolver un riesgo de reciclaje visual con PZA_4.2 — pero ese cambio nunca se aplicó en la Mesa. Johnny, trabajando desde la Mesa (no desde git), generó y aprobó las imágenes según la versión vieja. Un Claude distinto mezcló después ambas versiones en `brief.md` sin cruzarlas contra la Mesa ni contra lo ya generado/subido, y reportó a CC un estado que no correspondía a la realidad.

**Reglas obligatorias para que esto no se repita:**

1. **Un cambio de CONTENIDO** (qué asset va en qué beat, qué beats existen, qué se genera vs. qué es banco) **hecho solo en `brief.md` no es válido hasta que se refleje en la Mesa**, y viceversa. Mientras no estén sincronizados, ambos deben considerarse "en conflicto" para esa pieza — nunca asumir que uno es automáticamente el correcto porque es "más reciente" en git.
2. **Antes de reportar a CC (o a cualquiera) el estado de una pieza como "ya generada" o "lista para Airtable", quien reporta debe verificar contra la Mesa real** (captura de pantalla o lectura directa del artefacto) — nunca inferirlo solo de que `brief.md` sea internamente consistente.
3. Si al revisar un historial de git aparece un commit de OTRA sesión que cambió contenido de un brief (identificable por un `Claude-Session:` distinto en el mensaje de commit), ese cambio **no se asume aplicado en la Mesa** — se verifica explícitamente antes de construir nada encima.
4. Una corrección de **formato/estilo** (PNG format, bloque de estilo, separación prompt/nota) sí puede aplicarse directo en `brief.md` sin tocar la Mesa, porque no cambia qué imagen va en qué beat — pero una corrección de **contenido** (qué va en qué beat) sí requiere antes verificar/actualizar la Mesa.
5. Si se detecta una pieza ya generada/aprobada por Johnny con una decisión de contenido distinta a la que haya quedado en `brief.md` por cualquier motivo, **gana lo ya generado/aprobado** — se corrige `brief.md` para que coincida con la realidad ejecutada, nunca al revés, salvo instrucción explícita de Johnny de regenerar.

---

## 7. Registro en Airtable — tabla `Assets`

**Base:** Feed Your Roots US Data Sheets (`appMy5aOwifSbBLPR`)
**Tabla:** `Assets` (`tblkzOtjS4KK5B2Xn`)

| Campo | Tipo | Notas |
|---|---|---|
| Nombre de archivo | Texto | Debe coincidir exacto con el nombre en Drive |
| Categoría | Selección única | Social Media / Ad Creative / Brand Asset / Elemento Decorativo / Web / Narrative Stock / Producto Finalizado |
| Subcategoría/Uso | Selección única | TikTok Cover, IG Square, Hook, Blog Header, etc. |
| Aspecto | Selección única | 1:1, 9:16, 4:5, 2:3, 3:2, 16:9 |
| Link Drive | URL | **Obligatorio** — sin esto el registro no sirve para nada |
| Carpeta Drive | Selección única | Ruta legible, debe coincidir con Sección 2 |
| Descripción breve | Texto largo | Una línea de contenido, suficiente para buscar por concepto |
| Fecha de creación | Fecha | |
| Tags | Selección múltiple | Palabras sueltas de búsqueda libre — el campo más importante para recuperación real |
| Proyecto/Producto | Selección única | Hoy solo "Feed Your Roots US"; reservado para expansión LATAM/España futura |
| Reutilizable en | Selección múltiple | Redes sociales / Blog / Libro / Publicidad / Web / Video / Marca |

**Regla de oro:** ningún asset se considera "terminado" hasta que tiene su fila en Airtable **con el Link Drive real** (no un placeholder). Un asset sin link es un asset invisible para cualquier agente futuro.

**Excepción:** los archivos terminados de `Content_Pieces/` (PNG de slides, MP4) y la portada compuesta de `Video_Production/` NO llevan fila en `Assets`; se rastrean desde `Content_Pieces.Carpeta Drive`. Los valores exactos que lleva cada campo al registrar una escena nueva (Subcategoría por defecto `Escena emocional`, tags, memoria de uso) están en `knowledge/FYR_Rutas_De_Produccion.md`, Sección 0.6 y 0.7.

**Nota sobre `ID Pieza` en `Content_Pieces`:** usa el mismo identificador que la carpeta de Drive (`PZA_[tema]`, ej. `PZA_3.1`) — nunca un consecutivo genérico aparte. El tema es el identificador natural; dos sistemas de ID para la misma pieza desincroniza Drive y Airtable sin necesidad.

**Cómo obtener el link correcto sin errores:** listar la carpeta de Drive completa (`search_files` con `parentId`), nunca escribir un link de memoria o adivinado. Cruzar por nombre de archivo exacto, nunca por posición o suposición de orden.

---

## 8. Producción en lote — lecciones de eficiencia

- **Listar carpetas completas > buscar archivo por archivo.** Una llamada que trae 20-100 resultados es más segura y más barata que 20-100 llamadas individuales.
- **Lotes de Airtable:** máximo 50 registros por llamada de creación/actualización. Para más, dividir en sub-lotes.
- **Verificar antes de asumir:** cuando algo parece automático (ej. tiling nativo de Gemini), comprobarlo con evidencia (mosaico de prueba) antes de aplicar postproceso innecesario.
- **Un error de nombre corrompe silenciosamente.** Nombres parecidos (`E86-rutabaga` vs `E87-rutabaga`, `B01` vs `B02`) requieren doble verificación antes de escribir en lote.

---

## 9. Qué NO está automatizado todavía (honestidad operativa)

- Generación de imagen en Gemini/Nano Banana — sigue siendo un paso manual de Johnny.
- Ensamblaje de carrusel — lo hace Claude con `assemble.py` en su sesión (Pillow, ver `FYR_Motor_Ensamblado_Arquitectura_v1.md`) usando `production/scripts/assemble/run_pieza.py`; nunca pasa por Actions. Descarga y mueve archivos con el conector de Drive; solo la subida de los PNG terminados usa la API de Drive (ver Sección 1 de `FYR_Rutas_De_Produccion.md`).
- Ensamblaje de video — el render corre en GitHub Actions (voz con Google Cloud TTS + render con Clipkit), documentado en `FYR_Protocolo_Edicion_Video.md`; la portada la compone Claude con `assemble.py`. Validado de punta a punta con PZA_4.2 (en PC); el motor aún es una copia de carpeta por pieza (falta el motor único).
- Publicación/programación en redes sociales — no hay conector de publicación directa disponible; sigue siendo manual.
- Producción de copy/guión — puede generarse por Claude a partir del banco de temas (Malla de 61 + temas nuevos de los PDFs) + este documento, pero requiere revisión humana antes de publicar.
- Producción recurrente por cadencia (semanal/quincenal) — depende de una futura skill de análisis de performance que le indique a `fyr-content` qué ángulos priorizar; hasta entonces, cada corrida la inicia el usuario manualmente.

---

*Este documento se actualiza cada vez que se descubre una regla nueva, un error recurrente, o se ajusta la estructura. No es un documento estático — es la memoria operativa del sistema.*
