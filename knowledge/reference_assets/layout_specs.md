# FYR — Especificaciones técnicas de layouts

Medidas reales extraídas de los assets aprobados (no teóricas). Cualquier imagen de fondo generada para estos layouts debe pedirse a Gemini exactamente en las dimensiones de "ventana de contenido" indicadas, para calzar sin hueco ni desbordamiento.

**Ambos aspectos completos: 1080×1350px (4:5, carrusel) y 1080×1920px (9:16, video).** Los assets 9:16 se generaron reescalando el canvas de los assets 4:5 ya aprobados (mismo objeto, mismo trazo, solo más espacio de fondo alrededor) — no son interpretaciones nuevas, así que ambos aspectos son visualmente el mismo elemento en proporciones distintas.

---

## 1. Marco grande (imagen enmarcada)

**Assets:** `FYR_ASSET_marco-madera_4x5_v1.png`, `FYR_ASSET_marco-madera_9x16_v1.png`
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

**Assets:** `FYR_LAYOUT_etiqueta-colgante_4x5_v1.png`, `FYR_LAYOUT_etiqueta-colgante_9x16_v1.png`
**Rol narrativo:** copy corto e íntimo, sensación de nota personal.
**Activador:** 04 Storytelling, 06 Secreto.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 555–931 (51%-86%) / y: 160–1141 (12%-85%) | x: 541–987 (50%-91%) / y: 344–1515 (18%-79%) |
| Zona de texto disponible | Dentro del cuerpo de la etiqueta, aprox. x: 580-910, y: 480-1050 | Dentro del cuerpo de la etiqueta, proporcional a la posición de arriba |

---

## 6. Nota-kraft en esquina

**Assets:** `FYR_LAYOUT_nota-esquina_4x5_v1.png`, `FYR_LAYOUT_nota-esquina_9x16_v1.png`
**Rol narrativo:** aside/comentario que no interrumpe la escena principal.
**Activador:** 06 Secreto, 20 Revelación, 12 Curiosidad.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 410–924 (38%-86%) / y: 581–1189 (43%-88%) | x: 390–986 (36%-91%) / y: 854–1556 (44%-81%) |
| Zona de texto disponible | Sobre la cara visible de la nota, aprox. x: 430-880, y: 620-1120 | Proporcional, dentro de la cara visible de la nota |

---

## 7. Doble marco superpuesto

**Assets:** `FYR_LAYOUT_doble-marco_4x5_v1.png`, `FYR_LAYOUT_doble-marco_9x16_v1.png`
**Rol narrativo:** antes/después en un solo slide, sin repetir Marco grande dos veces.
**Activador:** 07 Contraste/Versus (uso primario, alternativa a Marco grande ×2).

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 58–1011 (5%-94%) / y: 86–1273 (6%-94%) | x: 54–1021 (5%-95%) / y: 368–1556 (19%-81%) |
| Marco trasero (rotado -6°) | Posición superior-izquierda | Posición superior |
| Marco frontal (rotado +4°) | Posición inferior-derecha, superpuesto con sombra | Posición inferior, superpuesto con sombra |
| Imágenes a pedir en Gemini | Dos escenas (antes/después), sin marco propio, recortadas a la ventana interior de cada marco individual — medir cada ventana por separado antes de usar en producción | Igual, proporciones verticales |

**Nota de historial:** la primera generación 9:16 de este layout salió con el interior de ambos marcos en negro sólido en vez de transparente — corregido en v2 (el archivo referenciado arriba). Verificar siempre alpha real antes de dar por buena una entrega.

---

## 8. Palabra-acuarela (referencia de estilo — NO asset reutilizable)

**Archivos:** `FYR_LAYOUT_palabra-acuarela_4x5_v1.png`, `FYR_LAYOUT_palabra-acuarela_9x16_v1.png`
**Rol narrativo:** una palabra clave como portada/hook visual dominante.
**Activador:** 11 Mito, 01 Negativo, 14 Advertencia.

**Cómo se usa (distinto a los demás):** este NO es un asset con hueco a rellenar. Cuando el brief necesite este layout, la skill genera un prompt NUEVO en Gemini con la palabra real del hook (ej. "MYTH", "WARNING"), usando este archivo únicamente como referencia de estilo visual (textura de acuarela, paleta, flourishes decorativos alrededor de las letras) — nunca reutilizado directamente.

**Nota de tamaño:** el archivo de referencia 4:5 llegó en 928×1152px, no 1080×1350px — el 9:16 sí llegó correcto en 1080×1920px. Al regenerar para producción, pedir siempre el tamaño exacto del canvas objetivo.

---

## 9. Tachado/corrección (referencia de estilo — NO asset reutilizable)

**Archivos:** `FYR_LAYOUT_tachado_4x5_v1.png`, `FYR_LAYOUT_tachado_9x16_v1.png`
**Rol narrativo:** visualiza la transformación directamente en el texto.
**Activador:** 07 Contraste/Versus (alternativa a Doble marco, más verbal que visual).

**Cómo se usa:** igual que Palabra-acuarela — referencia de estilo, se regenera con las palabras reales de cada tema (ej. "MESSY" tachado → "ORGANIZED").

**Márgenes medidos del ejemplo real (4:5):** la línea diagonal llega hasta 84.5% del ancho, dejando 15.5% de margen libre al borde derecho. Al recortar/regenerar, mantener margen de aire de al menos 8-10% en los 4 lados alrededor de las palabras y la línea — ni pegado al borde ni excesivamente centrado. La versión 9:16 reescala el mismo texto con más aire arriba/abajo, mismo margen lateral relativo.

---

## 10. Cordel guía

**Assets:** `FYR_LAYOUT_cordel-guia_4x5_v1.png`, `FYR_LAYOUT_cordel-guia_9x16_v1.png`
**Rol narrativo:** continuidad visual entre slides consecutivos — no depende de un hook específico, es un conector.
**Activador:** cualquiera, cuando se quiera dar continuidad fuerte a la secuencia.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 0–1079 (0%-100%) / y: 0–1296 (0%-96%) | x: 0–1079 (0%-100%) / y: 158–1749 (8%-91%) |

Atraviesa el canvas de esquina a esquina en ambos aspectos.

---

## 11. Migas de progreso

**Assets:** `FYR_LAYOUT_migas-progreso_4x5_v1.png`, `FYR_LAYOUT_migas-progreso_9x16_v1.png`
**Rol narrativo:** slides tipo lista/countdown con conteo visible — 3 de 5 elementos completos, 2 pendientes (plantilla de ejemplo; ajustar cantidad de "completos" según el slide real).
**Activador:** 13 Lista, 03 Numérico.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Bbox del contenido opaco | x: 95–984 (9%-91%) / y: 608–759 (45%-56%) | x: 74–1002 (7%-93%) / y: 890–1047 (46%-55%) |
| Posición | Franja horizontal centro-baja del canvas | Igual, franja horizontal centrada verticalmente |

---

## 12. Ventana Polaroid

**Assets:** `FYR_LAYOUT_ventana-polaroid_4x5_v1.png`, `FYR_LAYOUT_ventana-polaroid_9x16_v1.png`
**Rol narrativo:** momento de foco/revelación con fondo ambiental desenfocado.
**Activador:** 20 Revelación, 18 Sorpresa.

| | 4:5 (1080×1350) | 9:16 (1080×1920) |
|---|---|---|
| Canvas | Fondo desenfocado ocupa 100%, es parte opaca del asset | Igual |
| Marco Polaroid (interior transparente) | Aproximadamente centrado, cuadrado — ventana interior exacta pendiente de medir en pasada separada | Igual, pendiente de medir ventana interior específica |

**Pendiente:** ambos aspectos necesitan una segunda pasada de medición enfocada solo en el rectángulo blanco interior del marco Polaroid (no el bbox general del asset, que incluye el fondo desenfocado completo) antes de usarse en producción real.

---

## Regla de variedad (recordatorio, ya en SKILL.md)

Con 12 layouts disponibles, ningún layout se repite más de 2 veces en la misma pieza.

## Proporción imagen/texto por función del slide (recordatorio, ya en SKILL.md)

Apertura de loop = 85-90% imagen / 10-15% texto. Desarrollo/agitación = 60-75% / 25-40%. Giro/revelación = 50-65% / 35-50%. Cierre/CTA = 70-85% / 15-30%.
