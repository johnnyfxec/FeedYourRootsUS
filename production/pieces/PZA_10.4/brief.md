# Brief — PZA_10.4 · "I OVERPAID FOR MY COOP" (Carrusel 4:5)

**Estado:** brief generado — Fase D piloto autónomo, Parada 1 (3 piezas). Pilar 10 virgen (nunca producido antes).

**Corrección 30-oct-2026 (revisión de no-compresión de PZA_6.5/PZA_10.4, tras cerrar PZA_1.2/3.1/8.6/11.2):** esta pieza ya pasaba el criterio real de acción (Morgan compararía precios), pero el texto de S4 nunca se verificó contra el ancho real del layout con `draw.textlength()` — la primera línea ("Three suppliers, three totally different prices for the same build.") medía 138% del ancho útil de `ventana_texto` (864px), un desborde físico que habría roto el render. Corregido abajo re-partiendo el mismo texto exacto en líneas más cortas — ningún contenido se quitó ni se resumió, solo se reacomodó el salto de línea.

**Corrección 30-oct-2026 (segunda, subtítulo de portada):** la portada (`marco_grande_portada`, carrusel 4:5) traía "Subtítulo: *Because I didn't compare prices.*" heredado de una versión anterior del brief — pero `marco_grande_portada` **no acepta `texto_subtitulo`** (`compositors/tipo_a.py`, `CompositorError`: "solo portadas de video 9:16 llevan subtitulo"). El `config.json` ya estaba correcto (sin `texto_subtitulo`); se quita de la tabla de este brief.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 10.4 · Pilar 10 Shopping & Sourcing Guide |
| Dolor/deseo | Arrepentimiento financiero, deseo de evitar el mismo error |
| Formato / Medio | Antes/Después · Carrusel 4:5 |
| Fase Embudo | **F2** (mostrar alternativa suave — aprobado en Parada 0) |
| Hook | **07 Contraste/Versus** (compatible F2/F3 — aprobado en Parada 0) |
| Slides | 5 (F2 = 5-6) |
| Banco | 0 de 5 — nada de gallinero/presupuesto/recibo en `Assets` todavía. Las 5 imágenes van `[GENERAR EN GEMINI]` |
| Audiencia | Propia |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Cuánto se pudo haber ahorrado si hubiera comparado precios?"* — la portada solo muestra el ANTES (recibo caro + gallinero), no revela el método todavía.

## Slide por slide
| # | Layout | % img | Imagen | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | — | `STOCK-coop-overpriced-receipt_4x5_v1.png` **[GENERAR EN GEMINI]** | Título: `I OVERPAID FOR MY COOP` | Abre loop: ¿qué hizo mal? |
| 2 | `marco_grande` | 75 | `STOCK-receipt-total-circled-closeup_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `The total didn't even look real the first time I read it.` | Agita: shock del precio real |
| 3 | `doble_marco` | — | S3a `STOCK-coop-overpriced-receipt_4x5_v1.png` (reuso S1) + S3b `STOCK-coop-modest-sourcing-guide_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `Same coop. Half the price, once I actually compared.` | Contraste directo (afinidad del hook 07) |
| 4 | `ventana_texto` | 60 | `STOCK-sourcing-guide-three-prices-compared_4x5_v1.png` **[GENERAR EN GEMINI]** | `Three suppliers, three\ntotally different prices\nfor the same build.\nI'd only ever called\nthe first one.` | Revela el método. **Texto re-partido 30-oct-2026** — mismo contenido, corregido el salto de línea que desbordaba el ancho real (ver corrección arriba). |
| 5 | `marco_grande` | 80 | `STOCK-coop-finished-modest-hens_4x5_v1.png` **[GENERAR EN GEMINI]** | pie: `Same coop, same hens — just not the overpriced version.` | Cierre + CTA |

Variedad: `marco_grande` 2 veces (S2, S5), dentro del límite. Sin lockup (va como última slide separada por `assemble.py`, no contada aquí). Texto de S4 verificado 30-oct-2026 contra el ancho real de `ventana_texto` (864px, Lora 40px) con `draw.textlength()` — ninguna línea excede el 90% (máx. 48%).

## Prompts nuevos a generar (4 imágenes — S3a reusa S1)
*(Prefacio fijo omitido aquí — ver `FYR_Asset_Governance_Policy.md` §4. Cada entrada = línea de output + bloque de composición + específico, aplicando la Regla de narrativa visual de Governance Policy §4.)*

1. **S1 — ANTES (marco_grande_portada, 4:5 real):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Aspect ratio: exactly 4:5. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV at a kitchen table, one hand holding up a long printed receipt with a circled total, a plain wooden chicken coop visible through a window in the soft background, overcast morning light, muted gray-brown tones with a faint red accent on the circled total, no legible text on the receipt except the circled total itself (part of the narrative) — the receipt held at reading distance, not displayed flat, reads as a private moment of realizing the number is real."*
Archivo: `STOCK-coop-overpriced-receipt_4x5_v1.png`.

2. **S2 — closeup shock (marco_grande, 0.78:1 real):**
*"Output 1080x1232px, 0.78:1 portrait, PNG format. Aspect ratio: exactly 0.78:1. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. Close-up at a slight angle of a thumb pressing against a receipt's circled total, the paper slightly creased from being folded and unfolded, a coffee cup ring stain nearby on the table, warm indoor light, muted brown tones with the same red accent on the number, no legible text except the circled total — the crease and the ring stain suggest this receipt has been looked at more than once, unable to quite believe it."*
Archivo: `STOCK-receipt-total-circled-closeup_4x5_v1.png`.

3. **S3b — DESPUÉS (doble_marco, recorte mínimo con 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Aspect ratio: exactly 4:5. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV at the same kitchen table, an illustrated sourcing guide booklet open to a page with a lower price range circled, the same style of wooden chicken coop now visible through the window looking identical but the receipt is gone, warm golden-hour light, forest green and terracotta tones — the guide now occupying the space the receipt used to, the coop unchanged but the cost behind it completely different."*
Archivo: `STOCK-coop-modest-sourcing-guide_4x5_v1.png`.

4. **S4 — revelación del método (ventana_texto, 4:5):**
*"Output 1080x1350px, 4:5 portrait, PNG format. Aspect ratio: exactly 4:5. Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges. Close-up at a slight angle of a hand circling three different price figures written in a row on an open sourcing guide page, a pencil resting mid-motion, a phone with a call log faintly visible at the edge of the frame, warm desk light, forest green and gold tones, no legible text except the three price figures themselves (part of the narrative) — the pencil still in motion signals this comparison is happening for the first time, not a finished chart on display."*
Archivo: `STOCK-sourcing-guide-three-prices-compared_4x5_v1.png`.

5. **S5 — cierre (marco_grande, 0.78:1 real):**
*"Output 1080x1232px, 0.78:1 portrait, PNG format. Aspect ratio: exactly 0.78:1. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. First-person POV in a backyard, the same modest wooden coop from the DESPUÉS scene now with two hens visible near its entrance, a worn watering can resting against its base, warm late-afternoon light, forest green and terracotta palette — the hens and the worn watering can signal this coop has been in real use for a while, not staged for a photo the day it arrived."*
Archivo: `STOCK-coop-finished-modest-hens_4x5_v1.png`.

Diversidad de tonos de piel en manos si aparecen.

## Voz / Variante
N/A (carrusel).

## CTA
"Shopping & Sourcing Guide, real price ranges included — link in bio." — recurso: Shopping & Sourcing Guide (Complete Bundle, Pilar 10).

## Registro previsto
`Content_Pieces`: ID `PZA_10.4`, Carrusel, Hook Usado `07 Contraste/Versus`. `Themes` (10.4): alta nueva, F2, hook 07 Contraste/Versus, Bundle Relacionado `Homestead Complete` (Pilar 10 → Complete Bundle, según `FYR_Malla_60_Temas_Virales_v2.md` — nota: la opción ya existe en Airtable como `Homestead Complete`, creada el 19-oct-2026 para los pilares 8-9; se reutiliza aquí para el pilar 10 por ser el mismo bundle).
