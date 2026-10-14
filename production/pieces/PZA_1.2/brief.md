# Brief — PZA_1.2 · "5 ACRES VS HALF AN ACRE" (Carrusel 4:5)

**Estado:** aprobado por Johnny con ajustes (11-oct-2026): fase resuelta por Claude, sin lockup. Falta generar la imagen del slide 5.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 1.2 · Pilar 1 Half-Acre Blueprint · Core Bundle |
| Dolor/deseo | Comparación/envidia con quien tiene más terreno; creencia "autosuficiencia = 5 acres" |
| Formato / Medio | Antes-Después · Carrusel 4:5 |
| Fase Embudo | **F2** — muestra la alternativa (el plan, no el tamaño) sin vender. El hook 07 Contraste solo es compatible con F2/F3 en el CRS. |
| Hook | **07 Contraste/Versus** |
| Slides | 5 (F2 = 5–6) |
| Banco | **4 de 5 slides salen del banco** (5 imágenes). El slide 5 es la única imagen nueva. |
| Audiencia | Propia |
| Drive | `Content_Pieces/PZA_1.2/2026-10-11/` (ID `1zriDufnwJfuORGoajKv9hTr-V_wzV2NR`) |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Cómo va a cosechar más media acre que cinco?"* (La portada muestra el terreno grande subutilizado; no resuelve el loop.)

## Slide por slide
| # | Layout | % img | Imagen (archivo en la carpeta de Drive) | Texto exacto | Intención |
|---|---|---|---|---|---|
| 1 | `marco_grande_portada` | 85–90 | `STOCK-vecino-terreno-subutilizado_4x5_v1.png` (banco) | Título: `5 ACRES` / `VS HALF AN ACRE` | Abre loop 1: ¿quién gana? |
| 2 | `marco_grande` | 75 | `STOCK-comparacion-vecino-libreta_4x5_v1.png` (banco) | pie: `He has ten times the land. I have a notebook.` | Agita; abre loop 2: ¿qué hay en la libreta? |
| 3 | `doble_marco` | — | S3a `..._patio-abandonado_...` + S3b `..._patio-prospero_...` (banco) | pie: `Same yard. Different plan.` | Contraste directo (afinidad del hook 07) |
| 4 | `ventana_texto` | 60 | `STOCK-plano-ideal-homestead_4x5_v1.png` (banco) | `It was never the size of the land.` / `It was the layout.` | Revela: cierra loops 1 y 2 |
| 5 | `marco_grande` | 80 | `STOCK-vecino-transformado_4x5_v1.png` **[GENERAR EN GEMINI]** · fondo `color_completo` | pie: `Half an acre. One plan.` | Cierre + loop visual con la portada |

Variedad: `marco_grande` aparece 2 veces (S2 y S5), el máximo permitido. Sin lockup (decisión de Johnny).

## Prompt del slide 5 (loop visual con la portada)
Adjuntar en Gemini la portada (`STOCK-vecino-terreno-subutilizado_4x5_v1.png`) como referencia de ángulo y estilo.

```
Same view as the reference image: standing at the wooden fence looking across the neighbor's large, mostly empty lot, same fence line in the foreground, same angle and horizon. Transformed state: the big lot behind stays quiet and unused, but on our side of the fence in the foreground a compact half-acre plot is now thriving — tidy raised beds full of vegetables, a small greenhouse, a few fruit trees, a narrow path between the beds, warm golden-hour light. Same fence, same angle, different story: small and planned beats big and idle.

Hand-drawn storybook illustration in the tradition of Beatrix Potter, modernized with the flat, confident color sensibility of contemporary Oatly packaging. Fine ink linework: delicate, slightly imperfect 1–2pt lines with visible hand tremor, precise on subjects, looser at edges. Color applied as soft watercolor washes that bleed gently past the linework, layered over a warm parchment background (#F5ECD7) — never pure white. Palette limited to forest green (#4A7C59), terracotta orange (#D4732A), warm brown (#8B5E3C), harvest gold (#F0C040). Light paper grain, dry-brush edges, occasional pencil under-sketch showing through. NEVER include: photorealism, 3D rendering, neon or saturated primary colors, digital gradients, text or lettering, sci-fi or fantasy elements, plastic objects, hard black outlines, pure white backgrounds.

Aspect ratio: exactly 4:5. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges.
Fully painted scene filling the whole canvas, no unpainted parchment margins.
```
Si aparecen personas: diversidad de tonos de piel (regla no negociable). Archivo final: `STOCK-vecino-transformado_4x5_v1.png`, exportado a `06_Narrative_Stock/` (es insumo, no va a Content_Pieces).

## CTA (F2, suave)
Sin Bundle en las slides. Caption: `Half an acre is enough when every square foot has a job. Full layout → link in bio.` (no hay recurso gratuito identificado para nombrar.)

## Registro previsto
`Content_Pieces`: ID `PZA_1.2`, Carrusel, 5 slides, Hook Usado `07 Contraste/Versus`, Tema 1.2 (alta en `Themes`: F2, hook 07), Assets Usados = los 5 del banco (+ el S5 cuando exista en `Assets`). Después `Veces usado` +1 y `En descanso` marcado.
