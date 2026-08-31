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

**Nota de estilo:** la imagen de fondo puede o no incluir su propia vid decorativa integrada — ambas variantes son válidas (ver Sección 6, Regla de variedad). No usar el marco de ReportLab/Canva ENCIMA de una imagen que ya trae su propio marco pintado — es doble-marco, error confirmado en iteración previa.

---

## 2. Full-bleed con overlay

**Asset:** ninguno — la imagen generada ES el fondo completo.
**Rol narrativo:** inmersión emocional, momento de tensión.
**Activador:** 04 Storytelling, 10 Dolor/Frustración, 01 Negativo, 14 Advertencia, 09 Predicción.

| | Especificación |
|---|---|
| Imagen de fondo a pedir en Gemini | Exactamente 1080×1350px (4:5) o 1080×1920px (9:16) — edge-to-edge, sin marco ni vid propia |
| Franja de texto | Overlay semi-transparente (parchment #F5ECD7, alpha ~90-95%) sobre el tercio inferior de la imagen |

---

## 3. Solo texto + acento

**Asset:** ninguno obligatorio; opcionalmente 1-2 elementos del banco de 130+ ilustraciones botánicas como acento suelto.
**Rol narrativo:** tensión pura, dato numérico, pregunta que sostiene el loop.
**Activador:** 03 Numérico, 13 Lista, 11 Mito, 05 Error Común.

| | Especificación |
|---|---|
| Fondo | Parchment sólido (#F5ECD7), sin imagen |
| Texto | Centrado, tipografía grande, jerarquía título+subtítulo |
| Acento (opcional) | Hoja o semilla suelta del banco, 1-2 elementos, nunca decoración densa |

---

## 4. Texto + imagen lateral

**Asset:** ninguno — imagen recortada sin marco.
**Rol narrativo:** explicación breve con apoyo visual.
**Activador:** 06 Secreto, 20 Revelación, 12 Curiosidad.

| | Especificación |
|---|---|
| Imagen de fondo a pedir en Gemini | 40-60% del ancho del canvas, sin marco ni vid |
| Posición | Lateral (izquierda o derecha), texto ocupa el lado opuesto |

---

## 5. Etiqueta colgante

Assets: FYR_LAYOUT_etiqueta-colgante_4x5_v1.png, FYR_LAYOUT_etiqueta-colgante_9x16_v1.png
Ubicacion en Drive: 01_Brand_Assets/C13_Layout_Elements/
Rol narrativo: copy corto e intimo, sensacion de nota personal.
Activador: 04 Storytelling, 06 Secreto.

ACTUALIZADO 30-ago-2026: el rectangulo kraft esta ROTADO en el asset real (no alineado a ejes como se asumia antes). Medido con medidor_esquinas.html (4 esquinas reales).

| | 4:5 (1080x1350) | 9:16 (1080x1920) |
|---|---|---|
| Centro del rectangulo (rotado) | cx=742.2, cy=898.7 | cx=762.4, cy=1233.3 |
| Ancho x Alto (del rectangulo, sin rotar) | 275.4 x 347.9 | 330.9 x 411.3 |
| Angulo de rotacion | 11.98 grados | 10.77 grados |
| Zona de texto | 85% del ancho, 85% del alto del rectangulo medido -- ya excluye el ojal/cordel (la medicion empezo justo debajo de esa zona), es 100% zona segura | igual criterio |

El texto se renderiza en un lienzo aparte y se rota al mismo angulo antes de pegarse centrado en (cx, cy) -- ver render_text_block_rotated en text_renderer.py.

---

## 6. Nota-kraft en esquina

Assets: FYR_LAYOUT_nota-esquina_4x5_v1.png, FYR_LAYOUT_nota-esquina_9x16_v1.png
Ubicacion en Drive: 01_Brand_Assets/C13_Layout_Elements/
Rol narrativo: aside/comentario que no interrumpe la escena principal.
Activador: 06 Secreto, 20 Revelacion, 12 Curiosidad.

ACTUALIZADO 30-ago-2026: mismo hallazgo que etiqueta colgante -- rotada en el asset real.

| | 4:5 (1080x1350) | 9:16 (1080x1920) |
|---|---|---|
| Centro del rectangulo (rotado) | cx=666.6, cy=928.0 | cx=690.7, cy=1257.3 |
| Ancho x Alto (del rectangulo, sin rotar) | 337.0 x 327.7 | 412.8 x 373.8 |
| Angulo de rotacion | 12.08 grados | 11.66 grados |
| Zona de texto | 85% del ancho, 85% del alto del rectangulo medido | igual criterio |

---

## 7. Doble marco superpuesto

Assets: FYR_LAYOUT_doble-marco_4x5_v1.png, FYR_LAYOUT_doble-marco_9x16_v1.png
Ubicacion en Drive: 01_Brand_Assets/C13_Layout_Elements/
Rol narrativo: antes/despues en un solo slide, sin repetir Marco grande dos veces.
Activador: 07 Contraste/Versus (uso primario, alternativa a Marco grande x2).

ACTUALIZADO 30-ago-2026: pendiente resuelto -- ambas ventanas medidas por separado con medidor_esquinas.html (4 esquinas reales de cada una).

| | 4:5 -- trasero | 4:5 -- frontal | 9:16 -- trasero | 9:16 -- frontal |
|---|---|---|---|---|
| Ancho x Alto | 434.8 x 584.4 | 448.0 x 588.0 | 439.9 x 598.1 | 451.8 x 589.3 |
| Angulo | -8.47 grados | 10.89 grados | -8.70 grados | 10.93 grados |
| Centro (cx, cy) | 349.1, 441.8 | 702.6, 907.6 | 347.7, 721.3 | 704.0, 1193.1 |

Cada imagen de escena se recorta (crop-to-fill, con 2% de overscan para evitar bordes blancos en las esquinas) al tamano de su ventana SIN rotar, luego se rota al angulo real, y se pega centrada en (cx, cy). El marco de madera (con alpha real) va encima, tapando cualquier sobrante.

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
| Ventana interior (para la imagen de escena) | x=179.4, y=320.3, ancho=722.0, alto=727.8 -- casi cuadrada, angulo de rotacion practicamente 0 (confirmado sin rotacion real) |
| Y superior del titulo | 1234.0 (medido con editor_posicion_texto.html) |
| Ancho del bloque de titulo | 898px, sin subtitulo en este layout aplica el mismo ancho a la portada 4:5 (marco_grande_portada) |
| Y superior del subtitulo | 1454.0 |
| Ancho del bloque de subtitulo | 584px (65% del ancho del titulo) |

Ambas posiciones Y son ABSOLUTAS, medidas independientemente -- no se calculan de forma encadenada (titulo + espacio -> subtitulo), ver Seccion 8 de FYR_Motor_Ensamblado_Arquitectura_v1.md para el porque.

---


## 8. Palabra-acuarela (referencia de estilo — NO asset reutilizable)

**Archivos:** `FYR_LAYOUT_palabra-acuarela_4x5_v1.png`, `FYR_LAYOUT_palabra-acuarela_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C13_Layout_Elements/Style_References/`
**Rol narrativo:** una palabra clave como portada/hook visual dominante.
**Activador:** 11 Mito, 01 Negativo, 14 Advertencia.

**Cómo se usa (distinto a los demás):** este NO es un asset con hueco a rellenar. Cuando el brief necesite este layout, la skill genera un prompt NUEVO en Gemini con la palabra real del hook (ej. "MYTH", "WARNING"), usando este archivo únicamente como referencia de estilo visual (textura de acuarela, paleta, flourishes decorativos alrededor de las letras) — nunca reutilizado directamente.

**Nota de tamaño:** el archivo de referencia 4:5 llegó en 928×1152px, no 1080×1350px — el 9:16 sí llegó correcto en 1080×1920px. Al regenerar para producción, pedir siempre el tamaño exacto del canvas objetivo.

---

## 9. Tachado/corrección (referencia de estilo — NO asset reutilizable)

**Archivos:** `FYR_LAYOUT_tachado_4x5_v1.png`, `FYR_LAYOUT_tachado_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C13_Layout_Elements/Style_References/`
**Rol narrativo:** visualiza la transformación directamente en el texto.
**Activador:** 07 Contraste/Versus (alternativa a Doble marco, más verbal que visual).

**Cómo se usa:** igual que Palabra-acuarela — referencia de estilo, se regenera con las palabras reales de cada tema (ej. "MESSY" tachado → "ORGANIZED").

**Márgenes medidos del ejemplo real (4:5):** la línea diagonal llega hasta 84.5% del ancho, dejando 15.5% de margen libre al borde derecho. Al recortar/regenerar, mantener margen de aire de al menos 8-10% en los 4 lados alrededor de las palabras y la línea — ni pegado al borde ni excesivamente centrado. La versión 9:16 reescala el mismo texto con más aire arriba/abajo, mismo margen lateral relativo.

---

## 10. Cordel guía

**Assets:** `FYR_LAYOUT_cordel-guia_4x5_v1.png`, `FYR_LAYOUT_cordel-guia_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C13_Layout_Elements/`
**Rol narrativo:** continuidad visual entre slides consecutivos — no depende de un hook específico, es un conector.
**Activador:** cualquiera, cuando se quiera dar continuidad fuerte a la secuencia.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 0–1079 (0%-100%) / y: 0–1296 (0%-96%) | x: 0–1079 (0%-100%) / y: 158–1749 (8%-91%) |

Atraviesa el canvas de esquina a esquina en ambos aspectos.

---

## 11. Migas de progreso

**Assets:** `FYR_LAYOUT_migas-progreso_4x5_v1.png`, `FYR_LAYOUT_migas-progreso_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C13_Layout_Elements/`
**Rol narrativo:** slides tipo lista/countdown con conteo visible — 3 de 5 elementos completos, 2 pendientes (plantilla de ejemplo; ajustar cantidad de "completos" según el slide real).
**Activador:** 13 Lista, 03 Numérico.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 95–984 (9%-91%) / y: 608–759 (45%-56%) | x: 74–1002 (7%-93%) / y: 890–1047 (46%-55%) |
| Posición | Franja horizontal centro-baja del canvas | Igual, franja horizontal centrada verticalmente |

---

## 12. Ventana Polaroid

**Assets:** `FYR_LAYOUT_ventana-polaroid_4x5_v1.png`, `FYR_LAYOUT_ventana-polaroid_9x16_v1.png`
**Ubicación en Drive:** `01_Brand_Assets/C13_Layout_Elements/`
**Rol narrativo:** momento de foco/revelación con fondo ambiental desenfocado.
**Activador:** 20 Revelación, 18 Sorpresa.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Canvas | Fondo desenfocado ocupa 100%, es parte opaca del asset | Igual |
| Ventana interior transparente (marco Polaroid) | x: 358–728 (370px ancho) / y: 453–831 (378px alto) — casi cuadrada | x: 333–746 (413px ancho) / y: 702–1122 (420px alto) — casi cuadrada |
| Imagen de fondo a pedir en Gemini | Exactamente 370×378px, recortada/generada cuadrada | Exactamente 413×420px |

**Nota:** la ventana es intencionalmente casi 1:1 (formato Polaroid clásico) — la imagen que se inserte ahí debe generarse o recortarse a proporción cuadrada, no al aspect ratio del canvas completo.

---

## Regla de variedad (recordatorio, ya en SKILL.md)

Con 12 layouts disponibles, ningún layout se repite más de 2 veces en la misma pieza.

## Proporción imagen/texto por función del slide (recordatorio, ya en SKILL.md)

Apertura de loop = 85-90% imagen / 10-15% texto. Desarrollo/agitación = 60-75% / 25-40%. Giro/revelación = 50-65% / 35-50%. Cierre/CTA = 70-85% / 15-30%.
