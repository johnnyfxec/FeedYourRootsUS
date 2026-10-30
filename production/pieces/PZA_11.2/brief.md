# Brief — PZA_11.2 · "5 SIGNS YOUR SOIL IS SICK" (Carrusel 4:5)

**Estado:** brief generado — Fase D piloto autónomo, Parada 1 (3 piezas). Pilar 11 virgen (nunca producido antes).

**Corrección 30-oct-2026 (subtítulo de portada):** la portada (`marco_grande_portada`, carrusel 4:5) traía "Subtítulo: *The problem you can't always see.*" — pero `marco_grande_portada` **no acepta `texto_subtitulo`** (`compositors/tipo_a.py`, `CompositorError`: "solo portadas de video 9:16 llevan subtitulo"). El `config.json` ya estaba correcto (sin `texto_subtitulo`); se quita de la tabla de este brief para que no vuelva a copiarse a ningún otro lugar (Mesa de Producción incluida) como si fuera válido.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 11.2 · Pilar 11 Homestead Troubleshooting Field Guide |
| Dolor/deseo | Miedo a un problema invisible que arruina la cosecha |
| Formato / Medio | Countdown · Carrusel 4:5 |
| Fase Embudo | **F1** (dolor sin mencionar el producto — aprobado en Parada 0) |
| Hook | **20 Revelación** (compatible F1/F2/F3 — aprobado en Parada 0; preferido sobre 03 Numérico/13 Lista, que son F2/F4 exclusivos y no calzan con el F1 ya aprobado) |
| Slides | 7 (hook + 5 cuerpo + cierre) — ver corrección 30-oct-2026 |
| Banco | ~12% — `FYR_B07_soil-crosssection_1x1_v1.png` (brand asset) y `E04-worm.jpg` (botánico aislado) existen pero no calzan como escena narrativa de "revisar el propio suelo"; las 5 imágenes de escena van `[GENERAR EN GEMINI]` |
| Audiencia | Propia |

**Corrección 30-oct-2026 (gate de valor real, commit `85a5c60` — este es el caso que originalmente motivó la regla; y corrección de criterio sobre el tamaño del carrusel, misma fecha):** la versión anterior de este brief agrupaba los 5 síntomas 2+2+1 en 3 slides para quedar dentro del rango genérico de F1 (4-5 slides) — y esa compresión, para que el texto cupiera, llegó a fragmentar frases en líneas cortadas artificialmente. Eso es exactamente el error que la Regla de longitud real (Paso 3 de `fyr-content/SKILL.md`: "el rango por Fase es un límite, no un objetivo") prohíbe: recortar contenido real para encajar en un número de slides. Cada uno de los 5 síntomas tiene su propio mecanismo real (ciencia de suelo básica y verificable, nada inventado ni cifras falsas — prohibido por el espíritu del Hook 17): agua estancada = suelo compactado, sin canales para que el agua se mueva; ausencia de lombrices = mismo problema, sin oxígeno ni espacio poroso no sobreviven; costra blanca = sal acumulada por riego superficial repetido; marchitamiento en tarde = el agua no llega a la raíz aunque se haya regado; olor a huevo podrido = anaerobiosis, el suelo se quedó sin oxígeno. Son 5 puntos de valor reales y distintos — el contenido amerita un slide por síntoma, no una compresión. La pieza pasa de 5 a 7 slides (1 portada + 5 cuerpo + 1 cierre), fuera del rango genérico de F1 (4-5) pero justificado por la cantidad real de mecanismo explicado, exactamente el caso que la Regla de longitud real contempla. El hook y el cierre (ya funcionan — auditoría 30-oct confirmó que el cierre de engagement es el mejor ejecutado de las 6 piezas del lote) no cambian.

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Mi suelo tiene alguno de estos problemas sin que yo lo sepa?"* — la portada muestra el gesto de comprobar sin decir qué está buscando, abre el loop del hook 20 Revelación.

## Slide por slide
| # | Layout | % img | Imagen | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | — | `STOCK-soil-compaction-test-press_4x5_v1.png` **[GENERAR EN GEMINI]** | Título: `5 SIGNS YOUR SOIL IS SICK` | Abre loop: ¿qué está comprobando? |
| 2 | `ventana_texto` | 60 | `STOCK-soil-standing-water_4x5_v1.png` **[GENERAR EN GEMINI]** | `1. Water sits on top instead of soaking in.\nThat means the soil is compacted — no\nchannels left for air or water to move.` | Signo 1 + mecanismo (compactación) |
| 3 | `texto_lateral` | 50 | `STOCK-soil-no-earthworms_9x16_v1.png` **[GENERAR EN GEMINI]** | `2. Dig a shovel's width —\nzero earthworms.\nNothing survives\nwithout air or space.` | Signo 2 + mecanismo (mismo origen: compactación, sin oxígeno/espacio poroso) |
| 4 | `ventana_texto` | 60 | `STOCK-soil-white-crust_4x5_v1.png` **[GENERAR EN GEMINI]** | `3. A crust forms once the\nsurface dries out.\nSalt building up from\nshallow watering.` | Signo 3 + mecanismo (sal por riego superficial) |
| 5 | `texto_lateral` | 50 | `STOCK-soil-wilted-plant-afternoon_9x16_v1.png` **[GENERAR EN GEMINI]** | `4. It wilts by\nafternoon anyway.\nThe water never\nreached the roots.` | Signo 4 + mecanismo (mismo origen: el agua no penetra, se queda en la superficie) |
| 6 | `solo_texto` | — | — | `5. It smells like rotten eggs when you turn it over — that's the real tell.\nThat smell means the soil ran out of oxygen.` | Signo 5 + mecanismo (anaerobiosis), giro final. **Cambiado de `marco_grande` a `solo_texto` el 30-oct-2026** — el `texto_pie` de `marco_grande` mide ~866px útiles con Lora negrita cursiva 47px y ni la versión más corta de síntoma+mecanismo entra sin exceder el 90%, verificado con `draw.textlength()`; `ventana_texto` y `texto_lateral` ya están en el tope de 2 usos cada uno, así que corresponde `Solo texto`, que el propio gate da como opción cuando el punto de Valor no cabe en Marco grande. |
| 7 | `solo_texto` | — | — | `Your soil's been trying to tell you. Soil health troubleshooting guide, link in bio.` | Cierre + CTA |

Variedad: `ventana_texto` 2 veces (S2, S4), `texto_lateral` 2 veces (S3, S5), `solo_texto` 2 veces (S6, S7) — todos dentro del límite (máx. 2 por layout); ningún layout de asset fijo sin espacio real para texto (`marco_grande`) se usó donde el punto de Valor no cabía. Cada línea del cuerpo verificada contra el ancho real del layout con `draw.textlength()` (Lora 40px regular en `ventana_texto`/864px y `texto_lateral`/410px; Lora 47px negrita cursiva en `marco_grande`/~866px) — ninguna excede el 90% de la Regla de ancho del Paso 3 de `fyr-content/SKILL.md`.

## Prompts nuevos a generar (4 imágenes — S6 y S7 son `solo_texto`, sin imagen)
*(Prefacio fijo omitido aquí — ver `FYR_Asset_Governance_Policy.md` §4. Cada entrada = línea de output + bloque de composición + específico, aplicando la Regla de narrativa visual de Governance Policy §4.)*

0. **Portada (marco_grande_portada, 4:5 real):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Aspect ratio: exactly 4:5. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, a hand pressing two fingers into the surface of a garden bed, the soil visibly hard and slightly cracked where pressed, a small puddle of standing water nearby that hasn't soaked in, a worn garden fork resting just out of frame at the edge, overcast midday light, muted brown and gray-green tones within the brand palette — the testing gesture, not yet explained, opens the question of what the hand is actually checking for."*
Archivo: `STOCK-soil-compaction-test-press_4x5_v1.png`.

1. **S2 — signo 1, agua estancada (ventana_texto, 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges. Close-up at a slight angle of a shallow puddle of standing water sitting on top of visibly dense, cracked soil, not soaking in, a worn garden fork resting nearby, soft overcast light, muted brown tones — the water sitting on the surface rather than disappearing into it is the visual proof of the mechanism (compacted soil, no channels)."*
Archivo: `STOCK-soil-standing-water_4x5_v1.png`.

2. **S3 — signo 2, sin lombrices (texto_lateral, 9:16 real):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. Close-up at a slight angle of a small trowel holding a scoop of dry, dense, dug-up soil at chest height, visibly empty of any worms or insects, soft overcast light, muted brown tones — the trowel held up for inspection, visibly barren, ties directly to 'dig and find nothing.'"*
Archivo: `STOCK-soil-no-earthworms_9x16_v1.png`.

3. **S4 — signo 3, costra blanca (ventana_texto, 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges. Close-up at a slight angle of a dry garden bed surface with a faint pale, crusted film visible across the top layer of soil, a watering can resting nearby, warm but slightly harsh midday light, muted brown tones — the crust visible right at the surface, distinct from the darker soil beneath it where a corner has been lightly brushed away, ties directly to repeated shallow watering leaving salt behind."*
Archivo: `STOCK-soil-white-crust_4x5_v1.png`.

4. **S5 — signo 4, marchitamiento en tarde (texto_lateral, 9:16 real):**
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV, a wilted vegetable plant drooping in harsh afternoon sun despite visibly damp soil at its base, a watering can set down just out of frame, warm but slightly harsh light, muted green and brown tones — the contrast between damp soil and a wilted plant is the visual proof that watering alone isn't reaching the roots."*
Archivo: `STOCK-soil-wilted-plant-afternoon_9x16_v1.png`.

**S6 (signo 5, anaerobiosis) y S7 (cierre) son `solo_texto` — sin imagen, texto sobre fondo de marca (Parchment #F5ECD7).**

Diversidad de tonos de piel en manos si aparecen.

## Voz / Variante
N/A (carrusel).

## CTA
"Your soil's been trying to tell you. Soil health troubleshooting guide, link in bio." — recurso: Homestead Troubleshooting Field Guide (Complete Bundle, Pilar 11).

## Registro previsto
`Content_Pieces`: ID `PZA_11.2`, Carrusel, Hook Usado `20 Revelación`. `Themes` (11.2): alta nueva, F1, hook 20 Revelación, Bundle Relacionado `Homestead Complete` (Pilar 11 → Complete Bundle).
