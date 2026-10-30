# Brief — PZA_8.6 · "FROM EMPTY YARD TO FULL LAYOUT IN ONE AFTERNOON" (Carrusel 4:5)

**Estado:** brief generado en lote — Fase D, Parada 1 (primer lote real, 7 piezas). **Corrección 18-oct-2026:** los prompts de abajo llevaban la frase obsoleta "watercolor and ink illustration... vintage nature-journal style" en vez del bloque de estilo real — corregido. Todo prompt de este brief usa el **bloque de estilo base** de `FYR_Asset_Governance_Policy.md` §4 (Beatrix Potter + Oatly, ver texto exacto ahí) como prefacio fijo, que no se repite abajo — cada prompt lista solo el bloque de composición (ratio/fondo) + lo específico de esa escena.

**Corrección 30-oct-2026 (gate de valor real, commit `85a5c60`; y corrección de criterio sobre el tamaño del carrusel, misma fecha):** la versión anterior de este brief solo decía "planear cada cama en papel antes de salir" — un consejo genérico de jardinería que Morgan ya conoce, no un mecanismo propio del Half-Acre Blueprint. El mecanismo real (confirmado contra el Master Layout real en el Proyecto) tiene 3 puntos distintos, no uno: camas elevadas y cocina cerca de la casa (visita diaria, cosecha/riego); gallinero y compostera también cerca (visita diaria, huevos/mantenimiento); invernadero y árboles frutales a media distancia (visita menos frecuente). Son 3 puntos de valor reales — comprimirlos en una sola frase de `ventana_texto` sería el mismo error de recortar contenido real que ya se corrigió en PZA_11.2 (ver su brief), así que la pieza pasa de 5 a 6 slides (dentro del rango de F2) para darle al mecanismo su propio slide completo. El criterio real es **zonificar por cuántas veces al día/semana se visita cada cosa, no solo "dibujarlo antes de salir"**.

**Corrección 30-oct-2026 (segunda, subtítulo de portada):** la portada (`marco_grande_portada`, carrusel 4:5) traía "Subtítulo: *The plan made it possible.*" heredado de una versión anterior del brief — pero `marco_grande_portada` **no acepta `texto_subtitulo`** (`compositors/tipo_a.py`, `CompositorError`: "solo portadas de video 9:16 llevan subtitulo"). El `config.json` ya estaba correcto (sin `texto_subtitulo`); se quita de la tabla de este brief para que no vuelva a copiarse a ningún otro lugar (Mesa de Producción incluida) como si fuera válido.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 8.6 · Pilar 8 Property Layout & Zoning Mastery |
| Dolor/deseo | Deseo de rapidez y claridad en la planeación |
| Formato / Medio | Antes-Después · Carrusel 4:5 |
| Fase Embudo | **F2** (según lista aprobada en Parada 0) |
| Hook | **07 Contraste/Versus** (corregido — 17 Resultados/Transformación es solo F4 en la tabla de `hooks_verbales_20_v2.md`; Contraste sí es F2 y calza natural con "hoja en blanco vs. plano lleno") |
| Slides | 6 (F2 = 5-6; sube de 5 a 6 para dar espacio real al mecanismo de zonificación, ver corrección 30-oct-2026) |
| Banco | **Parcial-alta — 1 asset reusado 2 veces**: `STOCK-plano-ideal-homestead_4x5_v1.png` (ya usado en PZA_1.2 como DESPUÉS; mismo rol aquí) |
| Audiencia | Propia |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Qué pasó entre la hoja en blanco y el plano lleno?"* (El hook 07 no revela el método todavía.)

## Slide por slide
| # | Layout | % img | Imagen | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | — | `STOCK-blank-grid-sheet_4x5_v1.png` **[GENERAR EN GEMINI]** (prompt ANTES ya en la Malla 8.6) | Título: `FROM EMPTY YARD` / `TO FULL LAYOUT` | Abre loop: ¿qué cambió? |
| 2 | `marco_grande` | 75 | `STOCK-blank-grid-closeup_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `A blank grid is just... intimidating.` | Agita: la parálisis inicial |
| 3 | `doble_marco` | — | S3a `STOCK-blank-grid-sheet_4x5_v1.png` (reuso S1) + S3b `STOCK-plano-ideal-homestead_4x5_v1.png` **(banco — ya en `Assets`)** | pie: `Same yard. One afternoon. One plan.` | Contraste directo (afinidad del hook 07) |
| 4 | `ventana_texto` | 60 | `STOCK-colored-pencils-grid-marking_4x5_v1.png` **[GENERAR EN GEMINI]** | `Every bed on paper first.\nNo guessing once you're outside.` | Revela que se planea, abre la pregunta de "¿con qué criterio?" |
| 5 | `texto_lateral` | 50 | `STOCK-homestead-zones-daily-visit_9x16_v1.png` **[GENERAR EN GEMINI]** | `Beds and kitchen\nclose to the house,\nvisited daily.\nCoop and compost\nclose too — same\ndaily habit.\nGreenhouse and\ntrees farther out,\nvisited less often.` | Revela el criterio real: zonificar por frecuencia de visita, no solo "dibujarlo". **Slide nuevo, 30-oct-2026** — este es el mecanismo real que faltaba, movido aquí desde una frase comprimida en S4. |
| 6 | `marco_grande` | 80 | `STOCK-plano-ideal-homestead_4x5_v1.png` **(reuso, banco)** | pie: `The Half-Acre Blueprint template, ready when you are.` | Cierre + CTA |

Variedad: `marco_grande` 2 veces (S2, S6), `ventana_texto` 1 vez (S4), `texto_lateral` 1 vez (S5), `doble_marco` 1 vez (S3) — todos dentro del límite. Sin lockup. Línea de S5 verificada contra el ancho real de `texto_lateral` (410px, Lora 40px) con `draw.textlength()` — ninguna línea excede el 90%.

## Prompts nuevos a generar (4 imágenes)
*(Prefacio fijo omitido aquí — ver nota de arriba. Cada entrada = bloque de composición + específico, para pegar después del prefacio. Reescritos 18-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 — ángulo con presencia implícita, contexto de uso real, variación de desgaste, detalle conectado a la intención del slide — mismo tratamiento aplicado en PZA_3.1.)*
1. **S1/S3a — ANTES** (portada, ventana del marco): *"Aspect ratio: exactly 0.78:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter angle view (not straight overhead) of a blank grid sheet on a weathered outdoor picnic table, a mug of coffee gone cold beside it, a pencil set down at an angle rather than in hand, the yard faintly visible blurred beyond the table edge, muted parchment tones under flat overcast light — the untouched pencil and cold coffee should read as 'sat down to plan, got stuck before starting.'"*
2. **S2** (`marco_grande`): *"Aspect ratio: exactly 0.78:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. Three-quarter close-up of an empty hand-drawn grid sheet on the same picnic table, a pencil resting on the edge untouched, faint eraser smudges in one corner where a start was made and abandoned, muted parchment tones."*
3. **S4** (`ventana_texto`): *"Aspect ratio: exactly 4:5. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge. Close-up at a slight angle of a hand marking a grid sheet with a well-used set of colored pencils (a couple worn down short, one freshly sharpened), a few beds already sketched in forest green and terracotta, warm afternoon light — the mix of worn and sharp pencils signals an afternoon of real, ongoing work, not a single tidy sketch."*

4. **S5** (`texto_lateral`, 9:16 real — slide nuevo 30-oct-2026): *"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. Overhead view of a finished homestead layout sketch on the grid sheet, color-coded zones visible: raised beds and a small house icon clustered close together near one edge, a chicken coop and compost bins clustered just as close on the other side of the house, a greenhouse and a few fruit trees drawn farther out near the back of the plot, warm afternoon light, forest green and terracotta tones — the visible clustering by distance from the house is the proof of the real criterion: zoned by how often each thing gets visited, not by available space."*
Archivo: `STOCK-homestead-zones-daily-visit_9x16_v1.png`.

`STOCK-plano-ideal-homestead_4x5_v1.png` ya existe en `Assets` (usado en PZA_1.2) — confirmar en Parada 2 que sigue disponible y no está `En descanso`.

## CTA (F2, suave)
Caption: `It was never about the size of the yard. Half-Acre Blueprint template → link in bio.`

## Registro previsto
`Content_Pieces`: ID `PZA_8.6`, Carrusel, 6 slides, Hook Usado `07 Contraste/Versus`. `Themes` (8.6): alta nueva, F2, hook 07 Contraste/Versus.
