# Brief — PZA_2.1 · "I PLANTED TOMATOES AT THE WRONG TIME (AGAIN)" (Video 9:16)

**Estado:** brief generado — Fase D piloto autónomo, Parada 1 (3 piezas). Pilar 2 virgen (nunca producido antes).

## Ficha
| Campo | Valor |
|---|---|
| Tema | 2.1 · Pilar 2 Half-Acre Quick Calendar |
| Dolor/deseo | Miedo a desperdiciar tiempo/dinero por mal timing de siembra |
| Formato / Medio | POV · Video 9:16 |
| Fase Embudo | **F1** (dolor sin mencionar el producto — aprobado en Parada 0) |
| Hook | **01 Negativo** (compatible F1/F3 — aprobado en Parada 0) |
| Slides | 5 (F1 = 4-5) |
| Banco | ~10% — hay stock de cosecha de tomate reusable para otras piezas, pero ninguna escena de calendario/helada específica para esta; las 5 imágenes (portada + 4 cuerpo) van `[GENERAR EN GEMINI]` |
| Audiencia | Propia |
| Cierre en loop | **Tipo B (pregunta)** — el lote anterior cerró las 4 piezas de video en tipo A; alterno a B para variar la medición, como pide el protocolo |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Qué tiene de malo seguir la fecha del sobre de semillas?"* — la portada no responde todavía, abre el loop del hook 01 Negativo (desafía una creencia común).

## Guion (slide-beat)
| # | Layout | Imagen | Texto narrado | Intención |
|---|---|---|---|---|
| 1 | `marco_grande_cuadrado` (portada) | `STOCK-seed-packet-reverent-read_1x1_v1.png` **[GENERAR EN GEMINI]** | "Here's the planting mistake almost nobody questions — they follow the date on the seed packet like it's gospel." | Abre loop: desafía la creencia (01 Negativo) |
| 2 | `full_bleed` | `STOCK-frost-damaged-tomato-seedling_9x16_v1.png` **[GENERAR EN GEMINI]** | "I did too. Right month, right depth, exactly what it said — and still lost half my tomato seedlings to a frost it never warned me about." | Confesión personal, agita |
| 3 | `full_bleed` | `STOCK-seed-rack-identical-packets_9x16_v1.png` **[GENERAR EN GEMINI]** | "Turns out that packet date isn't written for your yard. It's written for an entire climate zone at once, which means it's really written for *no one's* yard." | Giro: revela por qué falla |
| 4 | `full_bleed` | `STOCK-personal-frost-date-journal_9x16_v1.png` **[GENERAR EN GEMINI]** | "The number that actually matters is your own average last frost date — and depending where you live, that can be *weeks* off from what the packet assumes." | Revela el criterio real |
| 5 | `full_bleed` | `STOCK-journal-replaces-packet-closing_9x16_v1.png` **[GENERAR EN GEMINI]** | "Quick Calendar, built around your real frost dates, link in bio.// Wait, so what's actually wrong with just following the seed packet?" | Cierre + CTA + loop visual (ver nota) + loop verbal tipo B |

**Regla de loop visual (cierre):** el prompt de S5 cita el elemento de portada (el sobre de semillas sostenido con reverencia) y lo repite transformado — ahora de fondo, fuera de foco, reemplazado por el diario personal como objeto de atención. Ver prompt abajo.

**Checklist cierre tipo B (verificado):** la pregunta ("what's actually wrong with just following the seed packet?") NO contiene la respuesta específica (que es "está escrito para una zona climática entera, no para tu patio, y el detalle de 'como si fuera biblia'") — deja un hueco real que la apertura llena. Comparte solo 2 palabras seguidas con la apertura ("seed packet"), no 3+.

## Prompts nuevos a generar (5 imágenes)
*(Prefacio fijo omitido aquí — ver `FYR_Asset_Governance_Policy.md` §4. Cada entrada = línea de output + bloque de composición + específico, aplicando la Regla de narrativa visual de Governance Policy §4.)*

0. **Portada (beat 1, 1:1, ventana del marco 722×728):**
*"Output 1080x1080px, 1:1 square, PNG format. Aspect ratio: exactly 1:1. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, close-up of a pair of hands holding a single seed packet up at eye level with visible care, thumb marking a spot on the back instructions as if re-reading it, a faint smudge of soil on one knuckle, soft midday light through a nearby window, forest green and terracotta tones, no legible text or lettering on the packet — the reverent handling of a plain instruction card is the open question: why does this packet get treated like it has all the answers?"*
Archivo: `STOCK-seed-packet-reverent-read_1x1_v1.png`, a `06_Narrative_Stock/` (insumo, no va a Content_Pieces).

1. **S2 (9:16):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, kneeling beside a raised garden bed, hands gently lifting a wilted, frost-blackened tomato seedling still in its original nursery pot, a crumpled seed packet half-tucked in a back pocket visible at the frame's edge, cool early-morning light with visible frost still clinging to nearby leaves, muted blue-green and brown tones within the brand palette, no legible text on the packet — the frost damage caught in the act, not after the fact, ties directly to the 'I did everything the packet said' confession."*
Archivo: `STOCK-frost-damaged-tomato-seedling_9x16_v1.png`.

2. **S3 (9:16):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, standing in front of a weathered wooden seed rack at a small local store, rows of identical tomato seed packets repeating down the shelf, one hand reaching to pull a single packet from the middle of the row, warm indoor shop light, forest green and gold tones, no legible text, lettering or labels on any packet — the repetition of the same packet down the rack is the visual proof that this date was never written for any one yard in particular."*
Archivo: `STOCK-seed-rack-identical-packets_9x16_v1.png`.

3. **S4 (9:16):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, hands writing a circled date directly onto a personal garden journal page at a wooden desk, the same seed packet now resting closed beside the journal, a small thermometer visible nearby reading a cool early-spring temperature, warm desk lamp light, forest green and terracotta palette, no legible text except the handwritten circled date (part of the narrative, not decorative) — the act of writing a number onto paper, not reading one off a mass-printed packet, carries the quiet shift toward reclaiming the date as personal."*
Archivo: `STOCK-personal-frost-date-journal_9x16_v1.png`.

4. **S5 — cierre, loop visual (9:16):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV at the same wooden desk as the previous scene, the same seed packet from the opening now resting closed and set aside at the table's edge, slightly out of focus, while a personal garden journal lies open and in sharp focus in the foreground with its circled frost date catching warm late-afternoon light, forest green and gold tones, no legible text except the circled date — the packet's role visually demoted from the single object in frame to the background, the journal now the object actually looked at."*
Archivo: `STOCK-journal-replaces-packet-closing_9x16_v1.png`.

Diversidad de tonos de piel en manos si aparecen.

## Voz / Variante
`en-US-Neural2-J`, speakingRate 0.92, pitch -4. Subtítulos `B-e14`. Cierre B (pregunta) — alterna frente a las 4 piezas tipo A del lote anterior.

## CTA
"Quick Calendar, built around your real frost dates, link in bio." — recurso: Half-Acre Quick Calendar (Starter Bundle, Pilar 2).

## Registro previsto
`Content_Pieces`: ID `PZA_2.1`, Video, Hook Usado `01 Negativo`. `Themes` (2.1): alta nueva, F1, hook 01 Negativo, Bundle Relacionado `Starter` (Pilar 2 → Starter Bundle, según `FYR_Malla_60_Temas_Virales_v2.md`).
