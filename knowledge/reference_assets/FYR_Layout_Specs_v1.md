# FYR — Especificaciones técnicas de layouts

Medidas reales extraídas de los assets aprobados (no teóricas). Cualquier imagen de fondo generada para estos layouts debe pedirse a Gemini exactamente en las dimensiones de "ventana de contenido" indicadas, para calzar sin hueco ni desbordamiento.

**Ambos aspectos completos: 1080×1350px (4:5, carrusel) y 1080×1920px (9:16, video).** Los assets 9:16 se generaron reescalando el canvas de los assets 4:5 ya aprobados (mismo objeto, mismo trazo, solo más espacio de fondo alrededor) — no son interpretaciones nuevas, así que ambos aspectos son visualmente el mismo elemento en proporciones distintas.

---

## 1. Marco grande (imagen enmarcada)

**Assets:** `FYR_ASSET_marco-madera_4x5_v1.png`, `FYR_ASSET_marco-madera_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C12_Frames/`
**Rol narrativo:** evidencia visual clara, resultado, contraste directo.
**Activador (Hook):** 07 Contraste/Versus, 17 Resultados/Transformación, 19 Demostración.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Ventana interior transparente | x: 59–1022 (963px ancho) / y: 59–1291 (1232px alto) | x: 72–1010 (938px ancho) / y: 66–1854 (1788px alto) |
| Grosor de madera | ~59px por lado (~5%) | ~66-72px por lado (~4-6%) |
| Imagen de fondo a pedir en Gemini | Exactamente 963×1232px | Exactamente 938×1788px |
| Padding entre madera y escena | 0px — la escena toca la madera directamente, sin aire | 0px |

**Texto bajo el marco (11-oct-2026; tamaño corregido 30-oct-2026):** va en `texto_pie`, con el rol `subtitulo` (Lora-BoldItalic, **42px** — bajado de 47px, ver Sección 16 "Contrato tipográfico" para la jerarquía completa y por qué), centrado en el espacio que deja el marco. El estilo de título dorado con borde queda reservado a las portadas para no restarle peso. Nota: `doble_marco` ya NO comparte este rol — tiene su propio rol `veredicto` (56px), ver Sección 7.

**Nota de estilo:** la imagen de fondo puede o no incluir su propia vid decorativa integrada — ambas variantes son válidas (ver Sección 6, Regla de variedad). No usar el marco de ReportLab (assemble.py) ENCIMA de una imagen que ya trae su propio marco pintado — es doble-marco, error confirmado en iteración previa.

---

## 2. Full-bleed (solo imagen)

**Corrección 13-sep-2026:** este layout NUNCA lleva texto — decisión de Johnny tras detectar que la versión anterior (con overlay semi-transparente) siempre dejaba imagen real visible detrás del texto, sin importar el contenido de la imagen. Si el slide necesita texto, usar Sección 2b (Ventana + texto) en su lugar.

**Asset:** ninguno — la imagen generada ocupa el layout completo.
**Rol narrativo:** inmersión visual pura, sin mensaje verbal superpuesto.
**Activador:** cualquier hook donde la imagen sola comunique el mensaje (ver Sección 2b para el caso con texto).

| | Especificación |
|---|---|
| Imagen a pedir en Gemini | **La proporción del canvas: 4:5 en carrusel, 9:16 en video** (Gemini entrega 1:1, 4:5, 3:4 y 9:16). Así llena el canvas sin margen alguno. Si el ratio real difiere ≤ 2 % (Gemini no es exacto al píxel) se recorta lo mínimo; si difiere más, el compositor contiene la imagen entera, sobra parchment y avisa `RATIO:` |
| Espacio sobrante | Si la proporción de la imagen no llena el canvas exacto, el espacio libre se rellena en parchment sólido (#F5ECD7), nunca se recorta la imagen para forzar el encaje |
| Texto | Nunca lleva — campo `texto_overlay` no aceptado, error de validación si se incluye |

---

## 2b. Ventana + texto

**Layout nuevo, 13-sep-2026** — reemplaza el uso con texto que antes vivía (incorrectamente) dentro de "Full-bleed con overlay". La imagen rellena su espacio (tolerancia de ratio de 2 %, ver "Relleno de espacios") en la parte superior; el tercio inferior es una franja de texto SÓLIDA, sin imagen detrás, sin transparencia.

**Asset:** ninguno.
**Rol narrativo:** inmersión emocional con mensaje verbal — el caso que antes se llamaba "Full-bleed con overlay".
**Activador:** 04 Storytelling, 10 Dolor/Frustración, 01 Negativo, 14 Advertencia, 09 Predicción.

| | Especificación |
|---|---|
| Imagen a pedir en Gemini | **9:16 → 3:4** (la zona de imagen mide 1080×1440 = 3:4 exacto, llena sin margen). **4:5 → 4:5**: la zona mide 1080×900 (6:5), que no coincide con ninguna proporción de Gemini, así que la imagen 4:5 queda de 720×900 centrada, con 180 px de parchment a cada lado. La altura de la imagen es ancho ÷ proporción, con tope de 2/3 del alto en 4:5 (900 px) y de 3/4 en 9:16 (1440 px) |
| Espacio sobrante | Relleno en parchment sólido (#F5ECD7) si la proporción no llena exacto los dos tercios |
| Franja de texto | Fondo parchment SÓLIDO (sin transparencia, sin imagen detrás) debajo de la imagen; texto centrado verticalmente en todo el espacio que deja la imagen: hasta el icono C14 en 4:5 y hasta el borde del canvas en 9:16 (sin icono). **Advertencia 9:16:** el centro de esa franja (~y=1680) queda bajo el límite duro de 83.3 % (y=1600), zona que la interfaz de reels/TikTok suele tapar |
| Corrección 11-oct-2026 | La especificación decía "720px" en 4:5, que no equivale a 2/3 del alto (900px); se corrige a 900px a pedido de Johnny. En 9:16 el tope pasa de 1280px (2/3) a 1440px (3/4) porque sobraba espacio vacío |

---

## 3. Solo texto

**Asset:** ninguno.
**Rol narrativo:** tensión pura, dato numérico, pregunta que sostiene el loop.
**Activador:** 03 Numérico, 13 Lista, 11 Mito, 05 Error Común.

| | Especificación |
|---|---|
| Fondo | Parchment sólido (#F5ECD7), sin imagen |
| Texto | Centrado, rol cuerpo |
| Posición del texto | Centrado en la zona de contenido (default; en 4:5, la zona sobre el icono) o, variante, centrado sobre la línea del primer tercio del canvas (`posicion_texto: "tercio_superior"`) |
| Icono C14 | Solo en 4:5, abajo al centro. En 9:16 no lleva |

## 4. Texto + imagen lateral

**Asset:** ninguno — imagen sin marco; llena el canvas (recorte mínimo solo dentro de la tolerancia de 2 %, ver "Relleno de espacios").
**Rol narrativo:** explicación breve con apoyo visual.
**Activador:** 06 Secreto, 20 Revelación, 12 Curiosidad.

| | Especificación |
|---|---|
| Imagen a pedir en Gemini | **9:16, en 4:5 y en 9:16.** El compositor la coloca a **540×960 px** (9:16 exacto; recorte mínimo solo si el ratio real difiere ≤ 2 %, si no avisa `RATIO:`). Pedir la imagen con el sujeto bien visible dentro del encuadre 9:16 |
| Posición de la imagen | Pegada al borde del canvas del lado indicado (`lado_imagen`: izquierda o derecha) y centrada verticalmente en la zona de contenido (en 4:5, sobre el icono C14) |
| Texto | En el lado opuesto, 410 px de ancho, alineado hacia el borde exterior y **centrado en altura respecto a la imagen** |
| Corrección 11-oct-2026 | Antes la imagen se recortaba a 540×1141 (4:5) o 540×1369 (9:16) y el recorte (16 % a 30 % del ancho) podía cortar lo que la imagen quería comunicar; `porcentaje_imagen` y `ancla_recorte` ya no aplican aquí |

## 7. Doble marco superpuesto

Assets: FYR_LAYOUT_doble-marco_4x5_v1.png, FYR_LAYOUT_doble-marco_9x16_v1.png
Ubicacion en Drive: 01_Brand_Assets/C13_Layout_Elements/
Rol narrativo: antes/despues en un solo slide, sin repetir Marco grande dos veces.
Activador: 07 Contraste/Versus (uso primario, alternativa a Marco grande x2).

ACTUALIZADO 30-ago-2026: pendiente resuelto -- ambas ventanas medidas por separado con medidor_esquinas.html (4 esquinas reales de cada una).

Medidas nativas (sin reescalar), para referencia de como se midio el asset original:

| | 4:5 -- trasero | 4:5 -- frontal | 9:16 -- trasero | 9:16 -- frontal |
|---|---|---|---|---|
| Ancho x Alto | 434.8 x 584.4 | 448.0 x 588.0 | 439.9 x 598.1 | 451.8 x 589.3 |
| Angulo | -8.47 grados | 10.89 grados | -8.70 grados | 10.93 grados |
| Centro (cx, cy) | 349.1, 441.8 | 702.6, 907.6 | 347.7, 721.3 | 704.0, 1193.1 |

**CORREGIDO 30-oct-2026 (bug real de truncamiento, PZA_6.5 S3 -- "Same plant. Different calendar. / Both thriving." se cortaba a 1 linea en el render real):** el `texto_pie` de este layout dejo de usar el rol `subtitulo` y ahora usa el rol propio **`veredicto`** (ver Seccion 16 "Contrato tipografico" mas abajo para la justificacion de jerarquia completa). La franja de texto sobre los marcos era un residuo fijo nunca dimensionado para 2 lineas -- en vez de parcharla de nuevo, se reescalo y desplazo TODO el conjunto (frame + ambas ventanas) para regalarle al texto el espacio real que `veredicto` (56px, 2 lineas fijas) necesita SIEMPRE a tamano completo:

| | 4:5 | 9:16 |
|---|---|---|
| `shrink_px` (desplazamiento hacia abajo) | 73 px | 161 px |
| `scale` (factor de reduccion) | 0.94593 | 0.91615 |
| Caja de `texto_pie` resultante | ~130px (top=5, bottom=BBOX.y0\*scale+shrink_px-10) | ~165px |

Las dimensiones nativas de la tabla de arriba se multiplican por `scale`, y `cx`/`cy` de cada ventana se recalculan: `cx' = cx*scale + canvas_w*(1-scale)/2`, `cy' = cy*scale + shrink_px`. El frame_asset completo se reescala por el mismo `scale` y se pega en `(x centrado, y=shrink_px)` en vez de `(0,0)`. Ver `layout_specs.DOBLE_MARCO_SHRINK` y `compositors/tipo_a.py::_compose_doble_marco` para la implementacion exacta -- verificado con render real del compositor (no wireframe aproximado) comparado visualmente con Johnny antes de implementar.

Nota de criterio (correccion de un error real durante el diagnostico, 30-oct-2026 -- version anterior de esta nota mezclaba dos protecciones distintas, corregido por Johnny): el `top` de la caja de texto NO usa `usable_zone`/`SAFE_PRACTICAL` (vertical) en 9:16. `SAFE_PRACTICAL` (vertical, boton de suscripcion / caption de Reels) aplica a portadas sin excepcion -- es lo que compite con esa UI de descubrimiento antes de que alguien abra el video/pieza. `doble_marco` es un layout de cuerpo -- el contenido individual solo se ve una vez abierta la pieza.

Verificacion importante (30-oct-2026): el criterio de "es cuerpo, no portada" por si solo NO basta para descartar SAFE_PRACTICAL -- lo que importa es un hecho fisico (si el elemento cae o no dentro de la zona que la UI real tapa), no la categoria del layout. Se calculo que esta caja (top=5px a ~488px = 0.3%-25.4% del canvas) invade teoricamente la franja de riesgo de SAFE_PRACTICAL (0-20%/384px). Pero Johnny publico la pieza real como Reel y como TikTok (capturas verificadas, 30-oct-2026) y el texto se ve completo, sin que ningun elemento real de UI (rail de iconos, perfil, barra de estadisticas) lo tape -- el riesgo teorico no se materializo en ninguna de las dos plataformas con este contenido. Se mantiene top=5px sin SAFE_PRACTICAL en doble_marco 9:16 por evidencia real de plataforma, no solo por el argumento de categoria. Si una pieza futura con texto_pie mas largo (3+ lineas, por ejemplo) empuja la caja mas arriba del 20%, reverificar visualmente en plataforma real antes de asumir que sigue estando bien.

(Nota aparte, no aplicada a este layout: `SAFE_PRACTICAL_X`, horizontal, protege contra el rail de iconos lateral -- esa SI se usa en algunos layouts de cuerpo en 9:16, como ventana_texto/solo_texto en base.py, porque el rail lateral esta presente en toda reproduccion, no solo en portada. Son dos protecciones independientes -- no confundirlas de nuevo.)

Cada imagen de escena se recorta (crop-to-fill, con 2% de overscan para evitar bordes blancos en las esquinas) al tamano de su ventana YA reescalada (ver arriba) SIN rotar, luego se rota al angulo real, y se pega centrada en (cx', cy'). El marco de madera reescalado (con alpha real) va encima, tapando cualquier sobrante.

Nota de historial: la primera generacion 9:16 de este layout salio con el interior de ambos marcos en negro solido en vez de transparente -- corregido en v2 (el archivo referenciado arriba). Verificar siempre alpha real antes de dar por buena una entrega.

---

## 13. Marco cuadrado (portada de reel/video 9:16) -- NUEVO 30-ago-2026

Asset: FYR_ASSET_marco-cuadrado_9x16_v1.png (solo 9:16, no existe version 4:5 -- el 4:5 usa el marco_grande normal via marco_grande_portada)
Ubicacion en Drive: 01_Brand_Assets/C12_Frames/
Rol narrativo: portada estandar de reel/video, con vid y hoja decorativas ya integradas en el asset.
Activador: cualquier tema, es el formato de portada por defecto para 9:16 (decision de consistencia de marca: 4:5 vertical / 9:16 cuadrado).

El asset es un LIENZO COMPLETO (1080x1920, no solo el marco recortado) con la vid y la hoja ya en su posicion final de diseno -- se pega fijo en (0,0), sin ningun escalado dinamico.

| | Valor medido (9:16) |
|---|---|
| Ventana interior (para la imagen de escena) | x=179.4, y=320.3, ancho=722.0, alto=727.8 -- casi cuadrada, angulo de rotacion practicamente 0 (confirmado sin rotacion real). **Imagen a pedir en Gemini: 1:1** (11-oct-2026) |

**CORREGIDO 29/30-oct-2026 (reemplaza por completo la version anterior de esta tabla, que tenia Y superior del titulo = 1234.0, un valor stale medido cuando este layout todavia llevaba subtitulo debajo del titulo).**

El subtitulo se elimino de este layout: `marco_grande_cuadrado` (portada 9:16) es **titulo solo**, centrado entre las dos vides decorativas que ya vienen pintadas en el asset del marco. El titulo YA NO se ancla a un Y fijo -- se centra dinamicamente en el hueco real entre vides:

| | Valor medido (9:16) |
|---|---|
| Fin de la vid grande (borde inferior) | y = 1209 px |
| Inicio de la vid chica (borde superior) | y = 1599 px |
| Hueco disponible para el titulo | 390 px (1209 a 1599) |
| Colchon vertical reservado (arriba y abajo) | 24 px cada lado (48 px total) -- para que el titulo NUNCA toque las vides sin importar si son 2, 3 o 4 lineas |
| Margen horizontal (zona segura, ver Seccion 15) | **13% de cada lado** del canvas (1080px) -- NO 11%, ver nota abajo |
| Ancho util del bloque de titulo (9:16) | **799 px** (1080 - 2×140.4, redondeado) -- DISTINTO del ancho de la portada 4:5 (898px, `marco_grande_portada`, mas ancho porque ese layout no tiene la restriccion de safe-zone de video) |
| Tamano de fuente del titulo (9:16) | **85px** (rol de tipografia `titulo_cuadrado` en `layout_specs.py`, separado del rol `titulo` de 93px que usa la portada 4:5) |

**Por que 13% y no 11% (29-oct-2026):** el margen horizontal se midio directo del telefono real de Johnny (iPhone, UI de TikTok/Reels superpuesta) y el rail derecho de controles mide ~11.68% del ancho en el peor caso. 13% deja colchon sobre esa medicion real; 11% la pisa y vuelve a tapar el titulo. No reducir por debajo de 13% aunque parezca que "sobra espacio" en la vista de edicion -- el espacio que importa es el que queda libre en el telefono real, no en el canvas limpio.

**Por que 85px y no 93 ni 75px (30-oct-2026):** se probaron los tres. A 93px (tamano original, heredado de la portada 4:5) frases de 3+ palabras no entran en una linea sin cortes torpes. A 75px el ancho ya no es problema, pero en la grilla real del feed (miniatura pequena) el texto se ve chico y el hueco entre vides se ve vacio -- confirmado visualmente por Johnny en captura de perfil real. 85px es el balance: mas grande y legible en grilla, pero ya no le entra a la mayoria de fragmentos de 3+ palabras sin pensar el corte a mano (ver regla de fragmentacion abajo).

**Regla de fragmentacion del titulo (obligatoria, reemplaza cualquier wrap automatico como fuente de verdad semantica):** a 85px y 799px de ancho, una linea cabe con holgura hasta ~2-3 palabras cortas o ~12-14 caracteres; frases mas largas casi siempre exceden. El motor de ensamblado SI balancea automaticamente el ancho de las lineas dentro de cada segmento separado por `\n` (evita que quede una palabra huerfana sola), pero **no tiene ninguna nocion semantica** -- no sabe que "THAT ACTUALLY" es una unidad que no debe partirse, ni que "5-YEAR-OLD CAN" va junto. Por eso **quien redacta `texto_titulo` (el Paso 2/3 de este skill, abajo) debe declarar los `\n` el mismo, pensando linea por linea contra el ancho de 799px**, NO dejarselo al balanceador automatico ni escribir la frase corrida de un tiron. Reglas practicas:
- Nunca separar un modificador de su sustantivo, un pronombre de su verbo, un verbo compuesto (ej. "SHOULD HAVE", "ORDERED IN") o un parentesis de lo que califica.
- Para un titulo de 4+ palabras que no entra en 2 lineas, usar 3-4 lineas cortas en vez de forzar menos lineas mas largas -- mejor "WHAT I SHOULD / HAVE ORDERED / IN JANUARY" (3 lineas limpias) que "WHAT I SHOULD HAVE / ORDERED IN JANUARY" (2 lineas, la primera excede el ancho y el balanceador automatico la vuelve a partir en un punto sin sentido).
- Verificar contra el ancho real antes de dar el titulo por bueno: una linea de ~85px cabe en 799px hasta aprox 13-14 caracteres incluyendo espacios; por encima de eso, dividir.
- Esta regla aplica SOLO a la portada 9:16 (`marco_grande_cuadrado`, rol `titulo_cuadrado`, 799px). La portada 4:5 (`marco_grande_portada`, rol `titulo`, 93px, 898px de ancho) tiene mas margen y tolera frases un poco mas largas por linea -- no aplicar el mismo limite de caracteres ahi sin volver a medir.

---


## 14. Lockup de cierre -- NUEVO 11-oct-2026

**Asset:** `assets/brand/lockups-vertical/FYR_C14_lockup-vertical_1x1_v1.png` (identidad de marca versionada en el repo, no en Drive).
**Rol narrativo:** cierre de marca. En el carrusel 4:5 es la **última slide**; en video 9:16 es un recurso **opcional**, solo cuando el guion nombra la marca y hace falta que el espectador la reconozca.

| | Especificación |
|---|---|
| Fondo | Parchment sólido, sin texto ni imagen |
| Lockup | Vertical (símbolo + wordmark Playfair Display Bold), 620 px de ancho, centrado en la zona usable, Root Black |

---

## Proporciones de imagen a pedir a Gemini (11-oct-2026)

La proporción a pedir se elige según el hueco que la imagen va a ocupar en el slide, de modo que se vea completa:

| Layout | Hueco de la imagen | Pedir | Resultado |
|---|---|---|---|
| Portada 4:5 (`marco_grande_portada`) | ventana del marco | la de la ventana (sección 1) | llena el marco |
| Portada 9:16 (`marco_grande_cuadrado`) | 722×728 | **1:1** | llena la ventana |
| Marco grande 4:5 | 963×1232 | **0.78:1** (NO 4:5 — ver nota) | llena la ventana exacta, sin recorte |
| Marco grande 9:16 | 938×1788 | 9:16 | llena la ventana (recorte mínimo) |
| Doble marco | dos ventanas de ~440×590, ratio ~0.74–0.77 | recorte mínimo con 4:5 (ver nota) | aceptable, el motor ya recorta/rota |
| Full-bleed 4:5 | 1080×1350 | 4:5 | llena exacto, sin margen |
| Full-bleed 9:16 | 1080×1920 | 9:16 | llena exacto, sin margen |
| Ventana+texto 4:5 | 1080×900 (6:5) | 4:5 | 720×900 centrada, 180 px de parchment por lado (ninguna proporción estándar llena 6:5) |
| Ventana+texto 9:16 | 1080×1440 | 3:4 | llena exacto, sin margen |
| Texto+lateral (4:5 y 9:16) | 540×960 | 9:16 | llena exacto |

### Ratio real del hueco vs. 4:5 genérico — marcos de madera (16-oct-2026)

**Hallazgo (piloto PZA_1.2):** con borde de grosor uniforme en los 4 lados, un marco cuyo lienzo exterior es 4:5 (1080×1350) **nunca** puede tener un hueco interior también 4:5 exacto — es geometría, no error de medición ni de generación. Restar el mismo margen `m` a 1080 y a 1350 reduce proporcionalmente más el ancho que el alto, así que el ratio del hueco sube por encima de 0.800 con cualquier `m > 0` (se demostró algebraicamente: la única solución de `(1080-2m)/(1350-2m) = 4/5` es `m = 0`).

Por eso, para `marco_grande` (grosor de borde ~59px, hueco real 963×1232 = **ratio 0.781**), **la imagen de escena debe pedirse directamente en 0.78:1, nunca en 4:5 (0.800)**. Pedirla en 4:5 fuerza al compositor a recortar la imagen para encajarla en el hueco, y ese recorte automático fue la causa del "borde doble"/espacio visible detectado en PZA_1.2 slide 3 — sumado a que, por separado, la imagen de escena traía su propio paspartú pintado (ver nota siguiente).

`doble_marco` tiene el mismo efecto geométrico pero más marcado (ventanas rotadas con ratio ~0.74–0.77): como son dos ventanas por slide y de tamaño variable, no es práctico pedir el ratio exacto por generación — ese layout sigue dependiendo del recorte+rotación automático del compositor (`_paste_rotated_scene`), igual que hoy.

**El marco de madera actual (`FYR_ASSET_marco-madera_4x5_v1.png`) no se regenera por esto** — su color y estilo ya están aprobados; el ajuste es solo en qué ratio se le pide a Gemini para la imagen de escena que va adentro, de aquí en adelante.

### Regla "sin marco propio" — reforzada (16-oct-2026)

El bloque de composición obligatorio (más abajo) ya pide *"no drawn frame, border, vignette, margins or visible paper edge"*, pero el banco de imágenes existente muestra que Gemini no siempre lo respeta (ver PZA_1.2 slides 3 y 5 — imágenes con un paspartú/borde de mapa pintado dentro de la propia ilustración). Esto es un defecto distinto al del ratio del hueco, y compone mal con cualquier layout que ya tenga marco de madera real (se ve como doble borde). No se corrige retroactivamente en el banco ya generado, pero toda generación nueva para un layout con marco interno debe reforzar esta instrucción en el prompt, no asumir que el bloque base alcanza.

### Relleno de espacios y tolerancia de ratio (11-oct-2026)

El motor rellena siempre el espacio de la imagen. Gemini no entrega el ratio exacto (4:5 → 928×1152 = 0.806; 9:16 → 768×1376 = 0.558), por eso `full_bleed`, `ventana_texto` y `texto_lateral` aplican una tolerancia de **2 %**: dentro de ella se recorta lo mínimo y no quedan bandas; fuera de ella la imagen se contiene entera y el motor emite `RATIO:` (regenerar con la proporción correcta, no recortar a la fuerza). Los ratios esperados son los de la tabla de arriba; `ventana_texto` espera 4:5 en 4:5 (se centra a 720×900, ver tabla) y 3:4 en 9:16.

### Bloque de composición para prompts de Gemini (obligatorio en todo prompt)

Se añade al bloque de estilo base (`FYR_Asset_Governance_Policy.md` §4), **después** de la línea de output obligatoria (`Output <ancho>x<alto>px, {RATIO}, JPG format, maximum quality.` — ver Governance Policy §4, "Línea de output obligatoria"; el formato JPG (corrección 30-oct-2026, solo imágenes de escena nuevas, nunca assets de marca) y el {RATIO} correcto por layout se declaran ahí, no aquí). Este bloque de composición se rellena según el layout y la marca `fondo` del slide en el brief:

```
Aspect ratio: exactly {RATIO}. Edge-to-edge composition: the artwork fills the whole canvas to every edge — no drawn frame, border, vignette, margins or visible paper edge. Keep the key subjects at least 5% of the width away from the left and right edges.
{FONDO}
```

- `{RATIO}`: el de la tabla anterior para el layout y el aspecto del slide (1:1, 4:5, 3:4 o 9:16).
- `fondo: pergamino` → `{FONDO}` = "Background: plain flat warm parchment paper, uniform color #F5ECD7 reaching every edge — no gradient, no darker corners, no shadow at the edges." Es obligatorio cuando la imagen queda suelta sobre el pergamino del slide (`ventana_texto`, `texto_lateral`), porque ahí el borde de la imagen se ve si el tono no coincide.
- `fondo: color_completo` → `{FONDO}` = "Fully painted scene filling the whole canvas, no unpainted parchment margins." Para paisajes, huertos u otras composiciones a todo color. En `ventana_texto`/`texto_lateral` el rectángulo de borde duro es parte del diseño: no se difumina.
- `full_bleed` y los layouts con marco (`marco_grande`, portadas, `doble_marco`): cualquier fondo, porque la imagen ocupa todo el slide o la tapa el marco. Sigue valiendo el ratio.
- Gemini aproxima el color hex, no lo clava: el fondo saldrá cercano a #F5ECD7, no idéntico. Verificar a ojo en la corrida; las imágenes ya generadas con un papel algo más claro se dan por buenas.

---

## 15. Safe zones por plataforma de destino — NUEVO 29-oct-2026

**Por qué existe esta sección:** hasta hoy el motor componía un único layout por pieza y lo reutilizaba para todas las plataformas de salida (TikTok, Reels, Shorts, Feed de Instagram, Pinterest). Cada plataforma tapa con su propia interfaz una zona DISTINTA del lienzo — un título bien centrado para TikTok queda bajo los iconos en Reels, y bajo el nombre de cuenta en Pinterest. Confirmado el 29-oct-2026 al detectar texto tapado en un video ya publicado.

**Metodología:** para video (TikTok/Reels/Shorts) no existe spec oficial pública de safe zone para contenido orgánico — solo para anuncios. Las cifras de abajo son consenso de industria (agencias de diseño/marketing, 2025-2026), consistentes entre sí pero no verificadas por declaración oficial de cada plataforma. Pinterest sí publica cifras oficiales de safe zone (vía sus specs de creative/ads, aplicables también a Pin orgánico). Si se necesita más precisión en el futuro, validar con capturas reales de cada app antes de confiar ciegamente en estos porcentajes.

### TikTok — video 9:16 (1080×1920)

| Zona | Ubicación | % del lienzo | Qué la ocupa |
|---|---|---|---|
| Top | 0–190px aprox. | ~8-13% superior | Barra "Siguiendo/Para ti" |
| Right rail | ~120-150px de ancho | ~11-14% del ancho derecho | Perfil, like, comentar, guardar, compartir |
| Bottom | ~300-400px inferior | ~16-21% inferior | @usuario, caption, disco de sonido |
| Lados | 60-90px c/lado | ~6-8% | Margen de seguridad general |
| **Safe zone** | centrado | **x: ~6-14% a 86-94% / y: ~8-13% a 79-87%** | Zona recomendada para texto/título crítico |

### Instagram Reels — video 9:16 (1080×1920)

| Zona | Ubicación | % del lienzo | Qué la ocupa |
|---|---|---|---|
| Top | ~270px | ~14% superior | @usuario, etiqueta de audio |
| Right rail | ~84-230px de ancho | ~8-21% del ancho derecho | Like, comentar, compartir, guardar, perfil |
| Bottom | ~670-770px inferior | **~35-40% inferior (consenso de industria)** | Caption + nav inferior de la app + iconos, todo apilado — el margen inferior MÁS GRANDE de los tres formatos de video |
| Lados | ~65-85px c/lado | ~6-8% | Margen de gestos |
| **Safe zone** | centrado | **x: ~6-14% a 86-94% / y: ~14% a 63-73% (teórico)** | **Decisión de Johnny (29-oct-2026): el motor NO usa este 35-40%.** Adoptarlo íntegro deja la pieza usando menos de la mitad de la pantalla (~45%), con aspecto vacío — contrario a la intención de diseño de ocupar todo el lienzo. Se fija un tope de **25% inferior** (bottom del motor = 0.75, no 0.65), calibrado contra la medición real de Johnny en TikTok (peor caso ~27%). Si el margen real de Reels termina siendo mayor a 25% en la práctica, se acepta la posibilidad de que el caption/nav de Reels se superponga al texto en el peor caso — riesgo asumido consciente, no un descuido de medición. |

### YouTube Shorts — video 9:16 (1080×1920)

| Zona | Ubicación | % del lienzo | Qué la ocupa |
|---|---|---|---|
| Top | 180-380px | ~9-20% superior | Barra de título, nombre de canal (variable, hay A/B testing de layout) |
| Right rail | ~120-160px | ~11-15% del ancho derecho | Like, dislike, comentar, compartir, suscribirse |
| Bottom | 380-480px inferior | ~20-25% inferior | Nombre de canal, título del short, botón de suscripción, música |
| Left | 60px | ~5-6% | Margen mínimo |
| **Safe zone** | centrado, leve sesgo a la izquierda | **x: ~5-15% a 90-95% / y: ~9-20% a 75-80%** | El margen superior más grande de los tres — hay más variabilidad reportada acá que en TikTok/Reels |

### Instagram Feed / Carrusel — imagen estática 4:5 (1080×1350)

A diferencia del video, en el feed normal la barra de acciones (like/comentar/compartir/guardar) y el @usuario quedan FUERA del lienzo (arriba/abajo del post, no superpuestos) — en el momento en que alguien ve el carrusel en su feed, prácticamente el 100% de la imagen es segura.

El riesgo real está en el **grid de perfil**: Instagram está migrando el grid de 1:1 a 4:5 (rollout gradual, no universal a oct-2026). Una cuenta que todavía ve grid 1:1 recorta el 4:5 a 1080×1080 centrado, perdiendo ~270px combinados arriba+abajo (~20% del alto, repartido en ambos extremos).

| | Especificación |
|---|---|
| Safe zone en feed (scroll normal) | ~100% del lienzo |
| Safe zone pensando en grid legacy | Mantener título/logo/cara dentro del cuadro central 1080×1080 (el 80% vertical central del lienzo 4:5) |

### Pinterest — Pin de imagen, 2:3 (1000×1500)

**Pinterest ya NO tiene formato carrusel en 2026** (deprecó los Idea Pins) — esta tabla aplica a Pin de imagen única, que es el único formato de imagen vigente. Ver SKILL.md para el flujo de publicación (2 pines por pieza).

| Zona | Píxeles (sobre 1000×1500) | % del lienzo | Qué la ocupa |
|---|---|---|---|
| Top | 270px | 18% superior | Overlay de guardar, menú "···" |
| Left | 65px | 6.5% izquierda | Margen general |
| Right | 195px | 19.5% derecha | Botón de guardar/compartir |
| Bottom (standard) | 790px | **52.7% inferior** | Nombre de cuenta/board + título del Pin — reserva casi la mitad inferior del lienzo |
| **Safe zone (standard)** | x: 65-805, y: 270-710 | **~74% ancho × ~29% alto, top-weighted** | El título va en el **tercio superior-centro**, NO centrado verticalmente como en video vertical — es la geometría más distinta de las cinco |

### Resumen operativo

No existe una safe zone universal entre plataformas — pero Johnny decidió (29-oct-2026) que el motor **no** persigue el peor caso teórico de las tres a la vez, porque hacerlo (top 20% + bottom 35-40%) deja solo ~45% del lienzo utilizable y la pieza se ve vacía. En vez de eso, el motor usa un **tope fijo y deliberado de 25% inferior** (más 20% superior por el lado de Shorts), que cubre la medición real de Johnny en TikTok y deja ~55% de alto útil. Esto implica que, en el peor caso de Reels específicamente, el caption/nav pueda superponerse al texto — riesgo aceptado a cambio de que el contenido ocupe la pantalla como se pretende, no un valor sin revisar. Implementado en `production/scripts/assemble/layout_specs.py` (`SAFE_PRACTICAL = {"top": 0.20, "bottom": 0.75}`).

---

## Regla de variedad (recordatorio, ya en SKILL.md)

Con 6 layouts de cuerpo disponibles (marco grande, doble marco, full-bleed, ventana+texto, solo texto, texto+lateral), ninguno se repite más de 2 veces en la misma pieza. Las portadas y el lockup de cierre quedan fuera de la cuenta.

## Proporción imagen/texto por función del slide (recordatorio, ya en SKILL.md)

Apertura de loop = 85-90% imagen / 10-15% texto. Desarrollo/agitación = 60-75% / 25-40%. Giro/revelación = 50-65% / 35-50%. Cierre/CTA = 70-85% / 15-30%.

---

## 16. Contrato tipográfico — jerarquía, roles y líneas garantizadas — NUEVO 30-oct-2026

Rediseño completo del sistema de roles tipográficos, motivado por un bug real de truncamiento (PZA_6.5 S3, `doble_marco`: "Same plant. Different calendar. / Both thriving." se cortaba a 1 línea en el render real). El diagnóstico mostró que el problema no era el texto — era que ningún layout tenía documentado **cuántas líneas garantiza su caja**, así que cada caja se calculaba como "lo que sobra", no desde la función retórica del rol que iba a vivir ahí. Esta sección es la regla permanente para que eso no se repita: antes de escribir un `texto_pie`/`texto_titulo`/`texto_cuerpo` más largo de lo habitual en un brief, o antes de agregar un layout nuevo, consultar esta tabla.

### Principio rector

El tamaño de un rol tipográfico debe reflejar **cuánto peso retórico tiene esa frase**, no cuánto espacio sobraba en su layout. Y cada caja de texto debe dimensionarse desde el **contrato de líneas** de su rol — cuántas líneas se espera que tenga, medidas con la altura de tinta real (`text_renderer._altura_tinta_real`, no la aproximación tipográfica) — nunca a ojo ni como residuo geométrico.

### Escalera de jerarquía (de mayor a menor peso)

| Orden | Rol | Tamaño | Fuente | Función retórica | Dónde vive | Líneas garantizadas |
|---|---|---|---|---|---|---|
| 1 | `titulo` / `titulo_cuadrado` | 93px / 85px | SourceSerifPro, dorado con borde | El gancho — para el scroll, se lee en 1 segundo | Portadas (`marco_grande_portada`, `marco_grande_cuadrado`) | 1-3 |
| 2 | **`veredicto`** (nuevo) | 56px | Lora-BoldItalic | Nombra la tensión entre DOS escenas — la línea que se screenshotea | `doble_marco` (`texto_pie`) | **2 fijas** |
| 3 | `subtitulo` | 42px (bajado de 47px) | Lora-BoldItalic | Ancla UNA escena ya mostrada — refuerzo, no revelación | `marco_grande` (`texto_pie`); subtítulo de `marco_grande_cuadrado` | 1-2 |
| 4 | `cuerpo` | 40px | Lora regular | Argumenta, agita, revela — carga la idea completa | `ventana_texto`, `solo_texto`, `texto_lateral` | 2-4 |
| 5 | `cta` | 32px | DMSans | Cierre de marca, el más discreto | `lockup_cierre` | 1 |

**Por qué `veredicto` es más grande que `subtitulo`, invirtiendo el orden anterior:** antes `subtitulo` (47px) pesaba más que `cuerpo` (40px) sin ninguna razón retórica — era simplemente el tamaño que calzaba bien en `marco_grande`, heredado por analogía superficial a `doble_marco` ("ambos tienen marco, ambos tienen texto"). Pero la función no es la misma: `subtitulo` **ancla** (refuerza una imagen que el ojo ya interpretó), mientras que el texto de `doble_marco` **nombra una comparación** — es casi un titular, no un pie de foto. Por eso mereció rol propio (`veredicto`), con más peso que `subtitulo`, ocupando el peldaño inmediatamente debajo del título.

### Por qué cada caja mide lo que mide (contrato verificado, no estimado)

Todas las alturas de caja de esta tabla fueron verificadas renderizando con `text_renderer.py` real (PIL, `draw.textbbox`, auto-shrink hasta 70% del tamaño base incluido) — no son estimaciones a ojo.

| Layout | Rol | Caja (4:5) | Caja (9:16) | Nota |
|---|---|---|---|---|
| `marco_grande_portada` | `titulo` | ~252px (frame_bottom a canvas_h, padding 24px c/lado, centrado por tinta real) | — (usa `marco_grande_cuadrado`) | Corregido 30-oct-2026 — bug real de centrado, ver Sección 1 |
| `marco_grande_cuadrado` | `titulo_cuadrado` | — | Entre vines, centrado por tinta real | Sin cambios en esta ronda |
| `doble_marco` | `veredicto` | ~130px (antes 62px fijo — insuficiente incluso al mínimo de auto-shrink) | ~165px (antes la fórmula daba una caja NEGATIVA, nunca se disparó en producción porque ninguna pieza publicada usa `doble_marco` en 9:16) | Ver Sección 7 para el detalle completo del fix (`DOBLE_MARCO_SHRINK`) |
| `marco_grande` | `subtitulo` | Proporcional a `porcentaje_imagen` del slide — mínimo real documentado 107px (caso más apretado, 90% imagen) | Igual, proporcional | Ya era correcto, solo cambia el tamaño de fuente (47→42px) |
| `ventana_texto` / `solo_texto` / `texto_lateral` | `cuerpo` | Franjas grandes, calculadas por `zona_contenido` o espacio sobrante de imagen | Igual | Sin problema detectado — ya diseñado con margen generoso |

### Regla para briefs futuros

Al escribir `texto_pie` en `doble_marco`, el contrato es **2 líneas, siempre caben a tamaño completo** — no hay que acortar el texto por miedo a que trunque (ese era precisamente el bug que esto corrige). Si una frase futura necesitara 3 líneas en ese layout, eso ya rompe el contrato de diseño del rol `veredicto` y hay que traerlo a revisión antes de generar el brief, no descubrirlo en el render final.
