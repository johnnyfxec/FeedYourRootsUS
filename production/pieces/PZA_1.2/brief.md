# Brief — PZA_1.2 · "5 ACRES VS HALF AN ACRE" (Carrusel 4:5)

**Estado:** aprobado por Johnny con ajustes (11-oct-2026): fase resuelta por Claude, sin lockup. Falta generar la imagen del slide 5 (ahora slide 6, ver corrección abajo).

**Corrección 30-oct-2026 (gate de valor real, commit `85a5c60`; corrección de criterio sobre el tamaño del carrusel; y corrección de cannibalización con PZA_8.6, misma fecha):** la versión anterior cerraba con "It was never the size of the land. It was the layout." — el mismo giro genérico que resultó débil en PZA_8.6 antes de su corrección, y además **cannibalizaba** a PZA_8.6: ambas piezas venden el Half-Acre Blueprint con el mismo ángulo de "tamaño vs. plan" sin un mecanismo propio que las distinga. PZA_8.6 ya usa el mecanismo de **zonificación por frecuencia de visita** (camas/cocina/gallinero cerca de la casa, invernadero/frutales más lejos) — así que PZA_1.2 necesita su propio ángulo real y distinto. El mecanismo elegido (confirmado contra `Master Layout — Feed Your Roots` en el Proyecto): **cada elemento del plano tiene una medida fijada por su función, no por el espacio disponible** — camas de 4×8 ft con 3 ft de pasillo (ancho real de trabajo, no relleno), invernadero orientado al sur, colmena orientada al este (sol de mañana), frutales enanos con 6 ft de espaciado. El vecino con 5 acres tiene espacio de sobra pero sin ese criterio de medida — por eso "más terreno" no se traduce en más cosecha. Ese mecanismo amerita su propio slide (nuevo S4), así que la pieza pasa de 5 a 6 slides (dentro del rango de F2, 5-6), sin comprimir el punto en la frase genérica que antes ocupaba el slide de revelación.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 1.2 · Pilar 1 Half-Acre Blueprint · Core Bundle |
| Dolor/deseo | Comparación/envidia con quien tiene más terreno; creencia "autosuficiencia = 5 acres" |
| Formato / Medio | Antes-Después · Carrusel 4:5 |
| Fase Embudo | **F2** — muestra la alternativa (el plan, no el tamaño) sin vender. El hook 07 Contraste solo es compatible con F2/F3 en el CRS. |
| Hook | **07 Contraste/Versus** |
| Slides | 6 (F2 = 5-6; sube de 5 a 6 para dar espacio real al mecanismo de dimensionado por función, ver corrección 30-oct-2026) |
| Banco | **4 de 6 slides salen del banco** (4 imágenes ya existentes). El nuevo S4 (mecanismo) y el cierre (antes S5) son imágenes nuevas. |
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
| 4 | `texto_lateral` | 50 | `STOCK-raised-bed-measuring-path_9x16_v1.png` **[GENERAR EN GEMINI]** | `Every bed is\n4×8ft with a\n3ft path —\nsized to work,\nnot to fill\nempty space.` | Revela el mecanismo real: cada medida tiene una razón funcional. **Slide nuevo, 30-oct-2026** — resuelve la cannibalización con PZA_8.6, que usa el mecanismo distinto de zonificación por visita. |
| 5 | `ventana_texto` | 60 | `STOCK-plano-ideal-homestead_4x5_v1.png` (banco) | `It was never the size of the land.\nIt was every inch having a reason.` | Cierra loops 1 y 2, conectado directamente al mecanismo de S4 |
| 6 | `marco_grande` | 80 | `STOCK-vecino-transformado_4x5_v1.png` **[GENERAR EN GEMINI]** · fondo `color_completo` | pie: `Half an acre. One plan.` | Cierre + loop visual con la portada |

Variedad: `marco_grande` 2 veces (S2, S6), `doble_marco` 1 vez (S3), `texto_lateral` 1 vez (S4), `ventana_texto` 1 vez (S5) — todos dentro del límite (máx. 2 por layout). Sin lockup (decisión de Johnny). Línea de S4 verificada contra el ancho real de `texto_lateral` (410px, Lora 40px) con `draw.textlength()` — ninguna línea excede el 90% (máx. 77%). Líneas de S5 verificadas contra `ventana_texto` (864px) — máx. 72%.

## Prompt del nuevo slide 4 (mecanismo — medida por función)
*"Output 1080x1920px, 9:16 portrait, PNG format. Aspect ratio: exactly 9:16. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges. Fully painted scene filling the whole canvas, no unpainted parchment margins. Close-up at a slight angle of a hand holding a measuring tape stretched along the edge of a raised garden bed, a clear walking path visible between this bed and the next one over, morning light, forest green and warm brown tones — the measuring tape mid-use against the bed's edge, with the walking path clearly wide enough to kneel and work in, is the visual proof of the mechanism: every dimension set by what the task needs, not by how much open ground there happens to be."*

Hand-drawn storybook illustration in the tradition of Beatrix Potter, modernized with the flat, confident color sensibility of contemporary Oatly packaging. Fine ink linework: delicate, slightly imperfect 1–2pt lines with visible hand tremor, precise on subjects, looser at edges. Color applied as soft watercolor washes that bleed gently past the linework, layered over a warm parchment background (#F5ECD7) — never pure white. Palette limited to forest green (#4A7C59), terracotta orange (#D4732A), warm brown (#8B5E3C), harvest gold (#F0C040). Light paper grain, dry-brush edges, occasional pencil under-sketch showing through. NEVER include: photorealism, 3D rendering, neon or saturated primary colors, digital gradients, text or lettering, sci-fi or fantasy elements, plastic objects, hard black outlines, pure white backgrounds.

Archivo: `STOCK-raised-bed-measuring-path_9x16_v1.png`.

## Prompt del slide 6 (loop visual con la portada, antes slide 5)
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
`Content_Pieces`: ID `PZA_1.2`, Carrusel, 6 slides, Hook Usado `07 Contraste/Versus`, Tema 1.2 (alta en `Themes`: F2, hook 07), Assets Usados = los 4 del banco (+ S4 y S6 cuando existan en `Assets`). Después `Veces usado` +1 y `En descanso` marcado.
