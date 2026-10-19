# Brief — PZA_5.3 · "GARDEN TO TABLE: THE RECIPE MY SON INVENTED" (Video 9:16)

**Estado:** brief generado en lote — Fase D, Parada 1 (primer lote real, 7 piezas). **Corrección 18-oct-2026:** los prompts de abajo llevaban la frase obsoleta "watercolor and ink illustration style/vintage illustration" en vez del bloque de estilo real — corregido. Todo prompt de este brief usa el **bloque de estilo base** de `FYR_Asset_Governance_Policy.md` §4 (Beatrix Potter + Oatly, ver texto exacto ahí) como prefacio fijo, que no se repite abajo — cada prompt lista solo el bloque de composición (ratio/fondo) + lo específico de esa escena. **Corrección 18-oct-2026 (segunda):** `TPL-video-cover-framed.png` en el beat 1 NO es un asset listo — es solo el marco `FYR_ASSET_marco-cuadrado_9x16_v1.png` (vid y hoja ya pintadas), con una ventana interior 1:1 vacía que necesita su propia imagen de escena. Corregido abajo con el prompt de portada faltante, mismo patrón que PZA_1.1.

## Ficha
| Campo | Valor |
|---|---|
| Tema | 5.3 · Pilar 5 Garden-to-Table Family Cookbook |
| Dolor/deseo | Deseo de conexión familiar a través de la comida |
| Formato / Medio | POV · Video 9:16 |
| Fase Embudo | **F2** (según lista aprobada en Parada 0) |
| Hook | **06 Secreto** (corregido — 04 Storytelling no es compatible con F2 en la tabla de `hooks_verbales_20_v2.md`; Secreto sí lo es y calza con el ángulo "lo que no esperabas que pasara") |
| Beats | 6, ~35s de referencia |
| Banco | Parcial — 1 de 6 (`STOCK-kitchen-table-harvest_9x16_v1.png`); 5 nuevas |
| Audiencia | Propia |

## Question Test
Cuando Morgan vea los primeros 3 segundos, la pregunta será: *"¿Qué es lo que nadie le dice a los padres sobre dejar a sus hijos cocinar con lo que cosechan?"* (El hook 06 no revela el secreto todavía — solo lo promete.)

## Guion por beat
| # | Beat | Imagen (banco o nueva) | Texto narrado |
|---|---|---|---|
| 1 | Portada (sin subtítulos) | `marco_grande_cuadrado` con `STOCK-child-harvest-basket-unplanned_1x1_v1.png` **[GENERAR EN GEMINI]** | "What nobody tells you about letting your kid loose with whatever's ready in the garden — he might actually out-cook you." |
| 2 | Cosecha sin plan | `STOCK-harvest-zucchini-cucumber-basket_9x16_v1.png` **[GENERAR EN GEMINI]** | "It started with him picking whatever looked ready. No recipe in mind, just... what's out here today." |
| 3 | Escribiendo la receta | `STOCK-child-recipe-card-handwriting_9x16_v1.png` **[GENERAR EN GEMINI]** | "Then he grabbed a card and started writing it down himself — spelling be damned, *his* recipe, *his* words." |
| 4 | Cocinando juntos | `STOCK-kitchen-table-harvest_9x16_v1.png` (banco) | "We cooked it exactly the way he wrote it. No substitutions, no corrections." |
| 5 | Probando en familia | `STOCK-family-tasting-kitchen-table_9x16_v1.png` **[GENERAR EN GEMINI]** | "And it was *good*. Not because it was perfect — because every bite was proof he'd actually been paying attention out there." |
| 6 | Cierre + CTA + loop | `STOCK-child-recipe-card-handwriting_9x16_v1.png` (reuso S3, crop distinto) | "His recipe is now page one of ours. Garden-to-table family cookbook, link in bio.// Here's what nobody tells you about handing them the harvest." |

Cierre en loop tipo A (frase cortada) — conecta directo con el inicio del video (la promesa del secreto se repite y reinicia el loop).

## Prompts nuevos a generar (4 imágenes)
*(Prefacio fijo omitido aquí — ver nota de arriba. Cada entrada = bloque de composición + específico, para pegar después del prefacio. Reescritos 18-oct-2026 aplicando la Regla de narrativa visual de Governance Policy §4 — ángulo con presencia implícita, contexto de uso real, variación de desgaste, detalle conectado a la intención del beat — mismo tratamiento aplicado en PZA_3.1.)*
0. **Portada (beat 1, 1:1, ventana del marco 722×728):** mismo patrón que PZA_1.1 — va DENTRO del marco, no lo reemplaza. Concepto: cosecha recién tomada, sin plan ni receta visible todavía — promete el secreto sin revelarlo.
*"Aspect ratio: exactly 1:1. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV looking down at a child's hands (visible, no face, noticeably smaller and pudgier than an adult hand) just setting down a slightly battered wicker basket on a sunlit porch step, zucchini and cucumbers picked at random angles with no clear plan, one stray garden leaf still caught in the basket's weave, warm midday light, forest green and terracotta tones — the randomness of the harvest, not yet a recipe, is the open question of the hook."*
Archivo: `STOCK-child-harvest-basket-unplanned_1x1_v1.png`, a `06_Narrative_Stock/` (insumo, no va a Content_Pieces).
1. **S2:** *"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV walking back from the garden rows, a child's hands (visible, no face, noticeably smaller and pudgier than an adult hand) holding a slightly battered wicker harvest basket with zucchini and cucumbers just picked, a stray leaf still clinging to one zucchini, garden bed visible softly out of focus behind, warm late-afternoon light, forest green and terracotta tones — the basket tilted a little off-balance, the way a kid actually carries one, not posed."*
2. **S3/S6:** *"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV, kitchen counter close-up of a child's hands (visible, no face, noticeably smaller and pudgier than an adult hand) writing on a blank recipe card with a stubby crayon, letters uneven and a crossed-out word visible, the just-harvested zucchini and cucumber still a little dirt-dusted beside the card, warm cozy kitchen light, terracotta and forest green tones — the imperfect handwriting is the point: this is the child's own recipe, not a parent's."*
3. **S5:** *"Aspect ratio: exactly 9:16. PNG format. Edge-to-edge composition, no drawn frame, border or margins. Background: fully painted scene, no unpainted parchment margins. First-person POV at a well-worn wooden kitchen table set for dinner, family hands of different ages and skin tones reaching in toward a shared plate of the finished dish, the handwritten recipe card from earlier propped against a water glass nearby, warm evening light, forest green and gold palette — the card visible but not the focus, a quiet callback that this meal started with a kid's own words."*

Diversidad de tonos de piel en manos.

## Voz / Variante
`en-US-Neural2-J`, speakingRate 0.92, pitch -4. Subtítulos `B-e14`. Cierre A (frase cortada) para variar frente a PZA_4.1 (que usa B) — mantiene la alternancia A/B del lote.

## CTA
"Garden-to-table family cookbook, link in bio." — recurso: página "Garden to Table" del activity pack.

## Registro previsto
`Content_Pieces`: ID `PZA_5.3`, Video, Hook Usado `06 Secreto`. `Themes` (5.3): alta nueva, F2, hook 06 Secreto.
