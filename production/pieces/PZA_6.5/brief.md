# Brief — PZA_6.5 · "ZONE 5 VS ZONE 9" (Carrusel 4:5)

**Estado:** brief generado en lote — Fase D, Parada 1 (primer lote real, 7 piezas). **Corrección 18-oct-2026:** los prompts de abajo llevaban la frase obsoleta "watercolor and ink illustration... vintage nature-journal style" en vez del bloque de estilo real — corregido. Todo prompt de este brief usa el **bloque de estilo base** de `FYR_Asset_Governance_Policy.md` §4 (Beatrix Potter + Oatly, ver texto exacto ahí) como prefacio fijo, que no se repite abajo — cada prompt lista solo el bloque de composición (ratio/fondo) + lo específico de esa escena.

**Corrección 30-oct-2026 (revisión de no-compresión de PZA_6.5/PZA_10.4, tras cerrar PZA_1.2/3.1/8.6/11.2):** esta pieza ya pasaba el criterio real de acción (Morgan replanificaría con su propia fecha de helada), pero su texto nunca se verificó contra el ancho real de los layouts con `draw.textlength()` — 4 de sus 6 slides (S2, S3, S5, S6) desbordaban entre 96% y 122% del ancho útil, un desborde físico que habría roto el render. Corregido abajo re-partiendo cada frase en 2 líneas más cortas — ningún contenido se quitó ni se resumió, solo se reacomodó el salto de línea (no es el error de compresión-de-contenido de las otras 4 piezas, es un error de ajuste de línea nunca verificado).

## Ficha
| Campo | Valor |
|---|---|
| Tema | 6.5 · Pilar 6 Climate Zone Garden Planner |
| Dolor/deseo | Frustración de recibir consejos genéricos que no aplican a su zona |
| Formato / Medio | Antes-Después · Carrusel 4:5 |
| Fase Embudo | **F4** (según lista aprobada en Parada 0) |
| Hook | **19 Demostración** (corregido — 07 Contraste no es compatible con F4 en la tabla de `hooks_verbales_20_v2.md`; Demostración sí lo es, F4, y calza con mostrar evidencia concreta de "qué pasa cuando sigues el calendario equivocado") |
| Slides | 6 (F4 necesita evidencia visual, más que el mínimo F2) |
| Banco | 0 de 6 — sin cobertura confirmada en Parada 0, se mantiene |
| Audiencia | Propia |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Qué pasa realmente si sigo el consejo de alguien en una zona distinta a la mía?"*

## Slide por slide
| # | Layout | % img | Imagen | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | — | `STOCK-zone5-vs-zone9-split_4x5_v1.png` **[GENERAR EN GEMINI]** (prompt ya en la Malla 6.5) | Título: `ZONE 5` / `VS ZONE 9` / Subtítulo: *Why your Florida neighbor's advice won't work.* | Abre loop: ¿qué pasa si no distingo? |
| 2 | `marco_grande` | 75 | `STOCK-frost-killed-seedlings-calendar_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `Plant on their calendar,\nand frost gets there first.` | Demostración 1: la consecuencia real |
| 3 | `doble_marco` | — | S3a `STOCK-zone5-timing-thriving_4x5_v1.png` + S3b `STOCK-zone9-timing-thriving_4x5_v1.png` **[GENERAR EN GEMINI x2]** | pie: `Same plant. Different calendar.\nBoth thriving.` | Demostración 2: cada zona correcta funciona |
| 4 | `ventana_texto` | 60 | `STOCK-frost-date-map-closeup_4x5_v1.png` **[GENERAR EN GEMINI]** | `Your frost date isn't a suggestion.\nIt's the only calendar that matters.` | Revela el criterio real |
| 5 | `solo_texto` | — | — | `The zone number is just\nshorthand for your frost dates.` | Reframe de autoridad (F4) |
| 6 | `marco_grande` | 80 | `STOCK-zone-correct-garden-thriving_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `Know your zone.\nGrow on its calendar.` | Cierre + CTA |

Variedad: `marco_grande` 2 veces (S2, S6, dentro del límite), `doble_marco` 1 vez, `ventana_texto` 1 vez, `solo_texto` 1 vez. Sin lockup. Texto re-partido 30-oct-2026 en S2, S3, S5, S6 — verificado contra el ancho real de cada layout (`marco_grande` texto_pie 866px Lora negrita cursiva 47px; `ventana_texto`/`solo_texto` 864px Lora 40px) con `draw.textlength()`; ninguna línea excede el 90% (máx. 78%). S4 ya estaba dentro del budget (máx. 74%), sin cambios.

## Prompts nuevos a generar (6 imágenes)
*(Prefacio fijo omitido aquí — ver nota de arriba. Cada entrada = bloque de composición + específico, para pegar después del prefacio. Reescritos 18-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 — ángulo con presencia implícita, contexto de uso real, variación de desgaste, detalle conectado a la intención del slide — mismo tratamiento aplicado en PZA_3.1. S1 es composición dividida por diseño del hook 19; cada mitad igual lleva su propio contexto de uso, no solo clima.)*
1. **S1 — portada** (ventana del marco de `marco_grande_portada`, reforzado 18-oct-2026 tras auditoría general — nota preventiva sobre el mapa; **PNG format agregado 19-oct-2026**): *"Aspect ratio: exactly 0.78:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Split composition at a slight three-quarter angle (not flat-on), left side a frost-covered raised garden bed with a pair of worn gardening gloves left out overnight, in muted cold blue-gray tones, right side a sun-drenched raised bed with the same style gloves now dry and dusty beside it, in warm gold and terracotta tones, an illustrated zone map subtly visible in the seam between the two halves — the map rendered as a hand-painted illustration only, no legible text or numbers — the matching gloves on both sides should read as 'same gardener, same gear, different calendar.'"*
2. **S2** (`marco_grande`; **PNG format agregado 19-oct-2026**): *"Aspect ratio: exactly 0.78:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter angle close-up of frost-killed seedlings slumped over in a raised bed, blackened leaf edges, muted blue-gray tones, a weathered calendar page tucked into the bed's corner post with a crossed-out early planting date circled in faded ink, morning frost still visible on the wood rim."*
3. **S3a** (`doble_marco`; **corregido 19-oct-2026: la nota "recorte mínimo, el compositor ajusta..." se sacó de dentro del prompt citado — nunca debe ir texto operacional en el prompt que se copia a Gemini, ver Governance Policy §4 — y se agregó PNG format**. Nota para Johnny, fuera del prompt: recorte mínimo, el compositor ajusta a la ventana rotada): *"Aspect ratio: exactly 4:5. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter angle of healthy spring seedlings in a raised bed, a small hand-written wooden plant marker leaning in the soil beside them, cool pale daylight, frost-free morning, forest green tones — the marker's handwriting (illegible at this scale, just texture) signals a gardener who planted on purpose, not by luck."*
4. **S3b** (`doble_marco`; **corregido 19-oct-2026: misma corrección que S3a — nota operacional sacada del prompt citado, PNG format agregado**. Nota para Johnny, fuera del prompt: recorte mínimo, el compositor ajusta a la ventana rotada): *"Aspect ratio: exactly 4:5. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter angle of healthy seedlings in a raised bed, a matching wooden plant marker in the soil (same style as S3a, for visual echo), warm golden winter sun, terracotta and gold tones — same deliberate planting, different season, different zone."*
5. **S4** (`ventana_texto`, hueco 1080×900 = 6:5, se pide en 4:5; **PNG format agregado 19-oct-2026**): *"Aspect ratio: exactly 4:5. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge. Close-up at a slight angle of a hand resting on an open, slightly dog-eared paper zone almanac, index finger pointing to a specific frost-date region, a stub of pencil and a coffee ring stain on the page corner, warm desk light, forest green and gold palette — the worn, well-used almanac signals this is a reference someone actually checks, not a prop."*
6. **S6** (`marco_grande`; **PNG format agregado 19-oct-2026**): *"Aspect ratio: exactly 0.78:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter angle of a thriving raised garden bed suited to its zone's calendar, overflowing with full, lush growth, a watering can resting nearby mid-use with a few drops still falling, warm golden-hour light, forest green and terracotta palette — the mid-use watering can signals an ongoing, tended rhythm, not a one-time staged result."*

Diversidad de tonos de piel si aparecen manos.

## CTA (F4, autoridad)
Caption: `Your zone, your calendar, your plan. Climate Zone Garden Planner → link in bio.`

## Registro previsto
`Content_Pieces`: ID `PZA_6.5`, Carrusel, 6 slides, Hook Usado `19 Demostración`. `Themes` (6.5): alta nueva, F4, hook 19 Demostración.
