# Brief — PZA_1.1 · "I STARTED WITH HALF AN ACRE AND A PENCIL" (Video 9:16)

**Estado:** propuesto (11-oct-2026). Falta generar la imagen de la portada (1 imagen nueva).

## Ficha
| Campo | Valor |
|---|---|
| Tema | 1.1 · Pilar 1 Half-Acre Blueprint · Core Bundle |
| Dolor/deseo | Abrumado por la idea de que autosuficiencia = mucho terreno y dinero |
| Formato / Medio | POV · Video 9:16 |
| Fase Embudo | **F1** — incomoda sin mencionar el producto (baja conciencia) |
| Hook | **04 Storytelling** (compatible F1 y Conexión en el CRS) |
| Cierre | **B** — pregunta cuya respuesta son las primeras palabras del video |
| Slides | 6 · ~423 caracteres (~28 s) |
| Banco | **5 de 6 slides salen del banco** (9:16). La portada se compone con 1 imagen nueva (1:1). |
| Audiencia | Propia |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Cómo se empieza con solo media acre y un lápiz?"*

## Slide por slide (todos `full_bleed`, texto lo ponen los subtítulos)
| # | Imagen | Narración (`texto_narrado`) |
|---|---|---|
| 1 | Portada compuesta: `marco_grande_cuadrado` con `STOCK-lapiz-plano-huerto_1x1_v1.jpg` **[GENERAR]** | `*Half an acre* and a pencil. That's all I started with.` |
| 2 | `STOCK-patio-abandonado-notas_9x16_v1.png` | `No farm. No five acres. Just a tired, patchy backyard and a *plan* on paper.` |
| 3 | `STOCK-open-hand-single-seed_9x16_v1.png` | `One season. One seed at a time. The pencil made it *small* enough to start.` |
| 4 | `STOCK-bare-feet-soil_9x16_v1.png` | `Standing in my own soil changed what I thought was *possible*.` |
| 5 | `STOCK-patio-prospero-notas_9x16_v1.png` | `Same yard. Same half acre. It was never the land that was *missing*.` |
| 6 | `STOCK-kitchen-table-harvest_9x16_v1.png` | `Now dinner starts at my own table.// Wait, what did my whole homestead start with?` |

Portada: título `I STARTED WITH HALF` / `AN ACRE AND A PENCIL`, subtítulo `Every homestead` / `begins on paper.`
Cierre B: la pregunta no contiene la respuesta; la respuesta son las primeras palabras ("Half an acre and a pencil"). CTA: ninguno (F1); el caption cierra con la idea del subtítulo.

## Prompt de la portada (1:1, ventana 722×728)
```
First-person POV: a hand holding a pencil over a sheet of paper on a wooden kitchen table at dawn. On the paper, a hand-drawn bird's-eye garden layout in simple ink lines: raised beds, a small greenhouse, a winding path, a few fruit trees. Soft morning light through a window, cozy rustic kitchen blurred in the background. No lettering, no labels, no numbers anywhere on the paper. Hands with a warm medium-brown skin tone.

Hand-drawn storybook illustration in the tradition of Beatrix Potter, modernized with the flat, confident color sensibility of contemporary Oatly packaging. Fine ink linework: delicate, slightly imperfect 1–2pt lines with visible hand tremor, precise on subjects, looser at edges. Color applied as soft watercolor washes that bleed gently past the linework, layered over a warm parchment background (#F5ECD7) — never pure white. Palette limited to forest green (#4A7C59), terracotta orange (#D4732A), warm brown (#8B5E3C), harvest gold (#F0C040). Light paper grain, dry-brush edges, occasional pencil under-sketch showing through. NEVER include: photorealism, 3D rendering, neon or saturated primary colors, digital gradients, text or lettering, sci-fi or fantasy elements, plastic objects, hard black outlines, pure white backgrounds.

Aspect ratio: exactly 1:1. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges.
Fully painted scene filling the whole canvas, no unpainted parchment margins.
```
Archivo: `STOCK-lapiz-plano-huerto_1x1_v1.jpg`, a `06_Narrative_Stock/` (es insumo, no va a Content_Pieces).

## Producción (todo en Actions, sin PC)
Cola `production/queue/pza-1.1.env` → el workflow baja las imágenes, compone la portada, genera la voz y renderiza. Variante de subtítulo B-e14, `TAIL_LAST=0.35` (cierre B).
