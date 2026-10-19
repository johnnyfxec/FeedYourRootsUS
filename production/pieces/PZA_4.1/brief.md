# Brief — PZA_4.1 · "WHAT YOUR 5-YEAR-OLD CAN (AND CAN'T) DO" (Video 9:16)

**Estado:** brief generado en lote — Fase D, Parada 1 (primer lote real, 7 piezas). **Corrección 18-oct-2026:** el prompt de abajo llevaba la frase obsoleta "watercolor and ink vintage nature-journal illustration" en vez del bloque de estilo real — corregido. Todo prompt de este brief usa el **bloque de estilo base** de `FYR_Asset_Governance_Policy.md` §4 (Beatrix Potter + Oatly, ver texto exacto ahí) como prefacio fijo, que no se repite abajo — el prompt lista solo el bloque de composición (ratio/fondo) + lo específico de esa escena. **Corrección 18-oct-2026 (segunda):** `TPL-video-cover-framed.png` en el beat 1 NO es un asset listo — es solo el nombre informal que usé para `FYR_ASSET_marco-cuadrado_9x16_v1.png`, el marco con vid y hoja ya pintadas (ver `FYR_Layout_Specs_v1.md` §13). Ese marco tiene una ventana interior 1:1 (722×728) vacía que necesita su propia imagen de escena — nunca se generó. Corregido abajo: se agrega el prompt de portada faltante, mismo patrón que PZA_1.1 (ver ese brief como referencia).

## Ficha
| Campo | Valor |
|---|---|
| Tema | 4.1 · Pilar 4 Family Homestead Starter Kit |
| Dolor/deseo | Miedo a sobre-exigir o subestimar a los niños |
| Formato / Medio | POV · Video 9:16 |
| Fase Embudo | **F1** (según lista aprobada en Parada 0) |
| Hook | **02 Pregunta** (corregido — 11 Mito no es compatible con F1 en la tabla de `hooks_verbales_20_v2.md`; Pregunta sí lo es y calza con el ángulo "can/can't" del tema) |
| Beats | 6 (portada + 5), ~35s de referencia |
| Banco | **Resuelto en Parada 2: 2 de 6 del banco de PZA_4.2 (siembra, riego) + 3 nuevas** — ver detalle abajo |
| Audiencia | Propia |

**Resolución del riesgo de reciclaje visual (Parada 2):** PZA_4.2 ya usó los 5 stock de niño en invernadero/riego/siembra/cosecha/canasta. Para evitar que 4.1 se vea repetido si se publica cerca, se mantienen solo los 2 beats más genéricos/fundacionales (siembra con etiquetas, riego) y se generan 3 nuevas imágenes con ángulos distintos (frijoles en vez de tomate cherry, tijeras supervisadas, entrega del cosecho en la puerta en vez de canasta sola) — 2-3 banco + 2-3 nuevas, como quedó anotado en Parada 1.

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Cuánto le estoy dejando hacer realmente a mi hijo de 5 años — o lo estoy subestimando?"*

## Guion por beat
| # | Beat | Imagen (banco o nueva) | Texto narrado |
|---|---|---|---|
| 1 | Portada (sin subtítulos) | `marco_grande_cuadrado` con `STOCK-child-hands-garden-tool-reaching_1x1_v1.png` **[GENERAR EN GEMINI]** | "How much do you actually let your *five-year-old* do out here — before deciding for them that they can't?" |
| 2 | CAN — siembra con etiquetas | `STOCK-planting-labeled-seeds_9x16_v1.png` (banco) | "At five, they *can* read a seed packet and plant exactly what it says — that's not luck, that's a kindergarten skill already at work." |
| 3 | CAN — riego cuidadoso | `STOCK-watering-seedling-tray_9x16_v1.png` (banco) | "They *can* water a seedling tray without drowning it. Small can, slow pour — five-year-old hands are plenty steady for that." |
| 4 | CAN — cosecha de frijoles (nueva, ángulo distinto a 4.2) | `STOCK-child-picking-green-beans_9x16_v1.png` **[GENERAR EN GEMINI]** | "They *can* pick beans clean off the low vines. What they *can't* do yet is the pruning shears — that one's still yours." |
| 5 | CAN'T (nueva, el giro honesto) | `STOCK-child-pruning-shears-supervised_9x16_v1.png` **[GENERAR EN GEMINI]** | "Not because they're not capable — because sharp tools and five-year-olds need an adult hand right there, every time." |
| 6 | Cierre + CTA + loop (nueva, ángulo distinto a 4.2) | `STOCK-child-presenting-basket-doorway_9x16_v1.png` **[GENERAR EN GEMINI]** | "Know the line between ready and not-yet-ready. Age-by-age garden guide, link in bio.// So how much do you actually let them do?" |

Cierre en loop tipo B (pregunta) — reinicia hacia el tono de PZA_4.2 sin repetir su contenido exacto.

## Prompts nuevos a generar (3 imágenes)

**Portada (beat 1, 1:1, ventana del marco 722×728):** mismo patrón que PZA_1.1 — imagen de escena que va DENTRO del marco `FYR_ASSET_marco-cuadrado_9x16_v1.png`, no lo reemplaza. Concepto: insinuar la pregunta "can/can't" sin responderla todavía.
*"Aspect ratio: exactly 1:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV at a raised garden bed, a small child's hand (visible, no face, noticeably smaller and pudgier than an adult hand) reaching toward a well-used garden trowel half-stuck in the soil, fingers close but not yet gripping it, a scattering of pea gravel and a few stray weeds pulled aside nearby, morning light — the hand caught mid-reach, not yet holding the tool, should read as the open question of the hook: can they, or can't they, do this themselves."*
Archivo: `STOCK-child-hands-garden-tool-reaching_1x1_v1.png`, a `06_Narrative_Stock/` (insumo, no va a Content_Pieces).

**Beat 4 — cosecha de frijoles (nueva, ángulo distinto a PZA_4.2 — resuelto en Parada 2, ver nota de Banco arriba; reescrito 19-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 y agregando PNG format):**
*"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV at a raised garden bed, a child's hand (visible, no face, noticeably smaller and pudgier than an adult hand) picking a cluster of green beans from a low vine, a few beans already resting in a small cloth bag draped over the bed's edge, morning light through the leaves, forest green palette — the casual bag-over-the-edge, not a posed basket, should read as an ordinary moment of a kid pitching in, not a staged demonstration."*
Archivo: `STOCK-child-picking-green-beans_9x16_v1.png`, a `06_Narrative_Stock/` (insumo, no va a Content_Pieces).

**Beat 5 (9:16, reescrito 18-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 — ángulo con presencia implícita, contexto de uso real, variación de desgaste, detalle conectado a la intención del beat — mismo tratamiento aplicado en PZA_3.1; PNG format agregado 19-oct-2026):**
*"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV at a garden bed, worn leather work gloves half-on the adult's hands (visible, no face) holding a pair of well-used pruning shears with a faded wooden handle, a small child's hands (visible, no face, noticeably smaller and pudgier than an adult hand) resting lightly on the adult's forearm rather than reaching for the blades, overgrown tomato vines needing a trim just ahead, warm late-afternoon light — the child's hands staying back, not grabbing, should read as the exact moment of 'watching, not yet doing.'"*

**Beat 6 — cierre, entrega en la puerta (nueva, ángulo distinto a PZA_4.2 — resuelto en Parada 2, ver nota de Banco arriba; reescrito 19-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 y agregando PNG format):**
*"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV, a child's hands (visible, no face, noticeably smaller and pudgier than an adult hand) holding up a small basket of mixed vegetables — beans, a couple of tomatoes, a stray herb sprig — toward an adult standing just inside a doorway (adult visible from chest down, no face, one hand reaching to take the basket), warm late-afternoon light spilling through the doorway, forest green and terracotta tones — the mid-handoff moment, not a posed presentation, should read as an everyday close of the day's harvest."*
Archivo: `STOCK-child-presenting-basket-doorway_9x16_v1.png`, a `06_Narrative_Stock/` (insumo, no va a Content_Pieces).

## Voz / Variante
`en-US-Neural2-J`, speakingRate 0.92, pitch -4 (base validada). Subtítulos `B-e14`. Cierre B (pregunta) por defecto para este lote — alternar con A en la siguiente corrida si hace falta más dato.

## CTA
"Age-by-age garden guide, link in bio." — recurso: skill map por edad (ya referenciado como CTA visual del tema).

## Registro previsto
`Content_Pieces`: ID `PZA_4.1`, Video, Hook Usado `02 Pregunta`. `Themes` (4.1): alta nueva, F1, hook 02 Pregunta.
