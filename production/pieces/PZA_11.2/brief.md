# Brief — PZA_11.2 · "5 SIGNS YOUR SOIL IS SICK" (Carrusel 4:5)

**Estado:** brief generado — Fase D piloto autónomo, Parada 1 (3 piezas). Pilar 11 virgen (nunca producido antes).

## Ficha
| Campo | Valor |
|---|---|
| Tema | 11.2 · Pilar 11 Homestead Troubleshooting Field Guide |
| Dolor/deseo | Miedo a un problema invisible que arruina la cosecha |
| Formato / Medio | Countdown · Carrusel 4:5 |
| Fase Embudo | **F1** (dolor sin mencionar el producto — aprobado en Parada 0) |
| Hook | **20 Revelación** (compatible F1/F2/F3 — aprobado en Parada 0; preferido sobre 03 Numérico/13 Lista, que son F2/F4 exclusivos y no calzan con el F1 ya aprobado) |
| Slides | 5 (F1 = 4-5; los 5 signos se agrupan 2+2+1 para no alargar el golpe, ver nota) |
| Banco | ~15% — `FYR_B07_soil-crosssection_1x1_v1.png` (brand asset) y `E04-worm.jpg` (botánico aislado) existen pero no calzan como escena narrativa de "revisar el propio suelo"; las 4 imágenes de escena van `[GENERAR EN GEMINI]` |
| Audiencia | Propia |

**Nota de diseño (agrupación de signos):** un Countdown de 5 señales normalmente pide 5 slides de cuerpo + portada = 6, por encima del rango F1 (4-5). Para respetar la Fase ya aprobada sin alargar el golpe, agrupé las 5 señales en 3 slides de cuerpo (2+2+1) en vez de uno por señal — el hook 20 Revelación encaja bien con esta compresión porque el punto es "revelar de una vez" la lista completa, no demorar la revelación slide por slide.

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Mi suelo tiene alguno de estos problemas sin que yo lo sepa?"* — la portada muestra el gesto de comprobar sin decir qué está buscando, abre el loop del hook 20 Revelación.

## Slide por slide
| # | Layout | % img | Imagen | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | — | `STOCK-soil-compaction-test-press_4x5_v1.png` **[GENERAR EN GEMINI]** | Título: `5 SIGNS YOUR SOIL IS SICK` / Subtítulo: *The problem you can't always see.* | Abre loop: ¿qué está comprobando? |
| 2 | `ventana_texto` | 60 | `STOCK-soil-standing-water-dry-crust_4x5_v1.png` **[GENERAR EN GEMINI]** | `1. Water just sits on top instead of soaking in.\n2. You dig a shovel's width and find zero earthworms.` | Revela signos 1-2 |
| 3 | `ventana_texto` | 60 | `STOCK-soil-wilted-plant-afternoon_4x5_v1.png` **[GENERAR EN GEMINI]** | `3. A white crust forms on the surface after it dries.\n4. Plants wilt by afternoon even on days you watered.` | Revela signos 3-4 |
| 4 | `marco_grande` | 80 | `STOCK-soil-turned-closeup-smell_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `5. It smells like rotten eggs when you turn it over — that's the real tell.` | Revela signo 5, giro final (afinidad hook 20 con evidencia visual) |
| 5 | `solo_texto` | — | — | `Your soil's been trying to tell you. Soil health troubleshooting guide, link in bio.` | Cierre + CTA |

Variedad: `ventana_texto` 2 veces (S2, S3), dentro del límite.

## Prompts nuevos a generar (4 imágenes)
*(Prefacio fijo omitido aquí — ver `FYR_Asset_Governance_Policy.md` §4. Cada entrada = línea de output + bloque de composición + específico, aplicando la Regla de narrativa visual de Governance Policy §4.)*

0. **Portada (marco_grande_portada, 4:5 real):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Aspect ratio: exactly 4:5. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, a hand pressing two fingers into the surface of a garden bed, the soil visibly hard and slightly cracked where pressed, a small puddle of standing water nearby that hasn't soaked in, a worn garden fork resting just out of frame at the edge, overcast midday light, muted brown and gray-green tones within the brand palette — the testing gesture, not yet explained, opens the question of what the hand is actually checking for."*
Archivo: `STOCK-soil-compaction-test-press_4x5_v1.png`.

1. **S2 — signos 1-2 (ventana_texto, 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges. Close-up at a slight angle of a small trowel holding a scoop of dry, dug-up soil at chest height, visibly empty of any worms or insects, a shallow puddle of standing water still visible in the hole behind it, soft overcast light, muted brown tones — the trowel held up for inspection, with the empty hole and standing water both in frame, ties directly to 'dig and find nothing' and 'water just sits.'"*
Archivo: `STOCK-soil-standing-water-dry-crust_4x5_v1.png`.

2. **S3 — signos 3-4 (ventana_texto, 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges. First-person POV, a wilted vegetable plant drooping in afternoon sun despite visibly damp soil at its base, a faint pale crust visible on the soil surface nearby, warm but slightly harsh midday light, muted green and brown tones — the contrast between damp soil and a wilted plant is the visual proof that watering alone isn't the problem."*
Archivo: `STOCK-soil-wilted-plant-afternoon_4x5_v1.png`.

3. **S4 — signo 5, giro final (marco_grande, 0.78:1 real):**
*"Output 1080x1232px, 0.78:1 portrait, PNG format. Aspect ratio: exactly 0.78:1. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. Extreme close-up of a garden fork turning over a clump of dark, dense soil, a faint grayish tint visible in the freshly exposed underside compared to the lighter topsoil, a single earthworm's tail just barely visible retreating into an undisturbed section nearby for contrast, warm late-afternoon light, forest green and brown tones — the freshly turned, denser underside caught mid-motion is the moment of discovery the whole piece has been building toward."*
Archivo: `STOCK-soil-turned-closeup-smell_4x5_v1.png`.

Diversidad de tonos de piel en manos si aparecen.

## Voz / Variante
N/A (carrusel).

## CTA
"Your soil's been trying to tell you. Soil health troubleshooting guide, link in bio." — recurso: Homestead Troubleshooting Field Guide (Complete Bundle, Pilar 11).

## Registro previsto
`Content_Pieces`: ID `PZA_11.2`, Carrusel, Hook Usado `20 Revelación`. `Themes` (11.2): alta nueva, F1, hook 20 Revelación, Bundle Relacionado `Homestead Complete` (Pilar 11 → Complete Bundle).
