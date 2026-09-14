# FYR - Principios de Composicion para el Motor de Ensamblado
Version 1.0 - 31 de agosto 2026
Proposito: reglas verificables por codigo que le permiten a Claude Code (u otra sesion) tomar decisiones de tamano, posicion y combinacion de layouts de forma AUTONOMA, sin aprobacion pieza por pieza -- con el mismo criterio que un compositor humano experimentado aplicaria, pero codificado como logica explicita.

Este documento existe porque durante la construccion de assemble.py (24-31 ago 2026), varias piezas de prueba salieron con errores de composicion reales (elementos decorativos usados como contenido principal, layouts sin sentido narrativo combinados entre si) que el codigo no podia prevenir porque no existia una capa de decision -- solo ejecucion de coordenadas fijas. Este documento es esa capa de decision, en forma de reglas.

---

## 0. El problema que este documento resuelve

Antes de este documento: cada slide de un brief se armaba eligiendo un layout de una lista, sin ningun criterio que verificara si esa eleccion tenia sentido compositivo. Resultado real observado: etiqueta_colgante usada como el contenido UNICO de un slide entero (se ve vacia y sin peso), migas_progreso combinado con full_bleed generico (sin relacion narrativa entre ambos), texto de portada creciendo sin limite hasta invadir otro elemento.

Despues de este documento: cada slide de un brief declara su rol narrativo explicito, y el motor de composicion usa ese rol -- no el layout elegido a ciegas -- para determinar tamano, posicion, y que combinaciones son validas.

---

## 1. Los 4 roles narrativos

Todo slide de una pieza (carrusel o reel) cumple exactamente uno de estos 4 roles. El brief JSON debe declararlo explicitamente en el campo rol_narrativo -- el motor NO lo infiere del largo del texto, lo infiere de la importancia narrativa que quien arma el brief le asigna.

| Rol | Funcion | % de canvas que ocupa el elemento principal | Ejemplos de uso |
|---|---|---|---|
| protagonista | El mensaje central del slide -- lo que abre o cierra un loop narrativo | 60-90% | Portada, hook de apertura, revelacion clave, resultado final |
| acompanante | Desarrolla o sostiene la narrativa, comparte espacio con una imagen real | 30-60% (el texto), imagen ocupa el resto | Texto sobre full_bleed, texto_lateral, cuerpo de doble_marco con anclaje |
| dato_al_margen | Informacion complementaria -- nunca es el contenido unico de un slide | 15-35%, siempre superpuesto sobre otro elemento ya protagonista | etiqueta_colgante, nota_esquina (ver Seccion 3, reclasificacion) |
| cierre | CTA + refuerzo de identidad de marca | Variable, pero SIEMPRE incluye un elemento de marca (logo, sello, frase ancla) ademas del texto | Ultimo slide del carrusel/reel |

Regla dura: ningun slide puede tener rol_narrativo "dato_al_margen" sin que exista una imagen de fondo en el mismo slide (ver Seccion 3). Si config_loader.py detecta esta combinacion, es un error de validacion -- fail loudly, no se procesa.

---

## 2. Matriz de combinacion valida (layout + acento + rol)

No todas las combinaciones de layout y acento tienen sentido narrativo, aunque tecnicamente el codigo pueda componerlas sin error. Esta tabla es la fuente de verdad de que combinaciones estan permitidas.

| Layout | Acento valido | Acento INVALIDO (nunca combinar) | Motivo |
|---|---|---|---|
| full_bleed | ninguno (correccion 13-sep-2026: full_bleed es SOLO imagen, sin texto -- un acento de progreso sin texto que lo narre no comunica secuencia real) | cualquiera | Sin texto que establezca la secuencia, ningun acento tiene contexto narrativo que reflejar |
| ventana_texto | migas_progreso (solo si el slide es parte de una secuencia tipo lista/countdown real, con estado de progreso correcto -- layout nuevo 13-sep-2026, reemplaza el uso con texto que antes vivia en full_bleed; migas_progreso en si mismo sigue sin terminar de implementarse, ver Arquitectura Seccion 7) | migas_progreso generico sobre imagen sin relacion de secuencia | El acento debe reflejar progreso REAL, no decorar una imagen aislada |
| solo_texto | cordel_guia (solo si el slide conecta visualmente con el siguiente/anterior en una secuencia real) | cordel_guia sobre texto centrado sin continuidad | El cordel es un conector de secuencia, no decoracion de un slide aislado |
| marco_grande_portada / marco_grande_cuadrado | (no lleva acentos, ya tiene su propia decoracion integrada) | cualquiera | Ya satura visualmente con marco + vid + hoja + texto |
| doble_marco | Texto de anclaje corto (ver Seccion 4) | -- | Sin texto, dos imagenes sin contexto no comunican nada (aprendizaje del 31-ago) |

Regla dura: migas_progreso y cordel_guia NUNCA se aplican como acento de un slide rol_narrativo "protagonista" aislado -- su funcion es de continuidad entre piezas de una secuencia, no de decoracion de un momento unico.

---

## 3. Reclasificacion: etiqueta_colgante y nota_esquina

Decision del 31-ago-2026: estos dos layouts dejan de poder usarse como contenido UNICO de un slide. Su asset (rectangulo kraft rotado, medido con medidor_esquinas.html) se compone siempre ENCIMA de una imagen de fondo real (full_bleed u otra escena), nunca sobre parchment vacio.

Justificacion (verificada visualmente el 31-ago): en pruebas reales, un slide con solo la etiqueta/nota flotando sobre fondo vacio se percibe sin peso narrativo -- el elemento fue disenado como un "post-it" que puntua una imagen, no como el mensaje completo de un slide.

Implicacion de codigo (pendiente de implementar, Fase 1 de este roadmap): config_loader.py debe exigir imagen_escena como campo obligatorio para estos dos layouts (hoy no lo exige). tipo_b.py debe recibir una imagen de fondo, componerla primero (mismo crop-to-fill que full_bleed), y DESPUES aplicar el rectangulo rotado con el texto encima -- dos pasos, no uno.

---

## 4. doble_marco -- anclaje de texto (pendiente de implementar)

Decision del 31-ago-2026: dos imagenes sin ninguna palabra no comunican una comparacion real -- el usuario ve "dos fotos de jardin" sin saber que esta cambiando entre ellas. doble_marco gana la capacidad de llevar un texto corto de anclaje.

Alcance a definir en Fase 1: el texto va como titulo unico debajo de ambos marcos, o como etiqueta corta en cada mitad (tipo BEFORE/AFTER)? Esto requiere medicion visual antes de implementar -- no se asume, se mide con medidor_esquinas.html o editor_posicion_texto.html sobre un mockup real primero.

---

## 5. Relacion entre largo de texto y tamano de fuente (NO es el criterio de rol)

Aclaracion importante, para no confundir con la Seccion 1: el rol_narrativo determina el tamano del ESPACIO asignado al elemento (el % de canvas). Dentro de ese espacio ya asignado, el sistema de fit_text existente (reduccion automatica + limite minimo, ver text_renderer.py) sigue siendo el mecanismo correcto para ajustar el tamano de fuente al largo real del texto -- eso no cambia. Lo que cambia es que el ESPACIO ya no es una coordenada fija ciega, sino una funcion del rol narrativo declarado.

---

## 6. Checklist de auto-verificacion (Fase 3 del roadmap, pendiente)

Antes de que el sistema de una pieza por terminada sin supervision humana, debe poder confirmar:

1. Ningun slide con rol_narrativo "dato_al_margen" existe sin imagen de fondo? (validable hoy en config_loader.py una vez implementada la Seccion 3)
2. Ninguna combinacion de layout+acento de la tabla de la Seccion 2 esta en la lista de "INVALIDO"? (validable con una funcion nueva, validar_combinaciones(cfg))
3. Ningun bloque de texto se superpone con otro? (requiere una verificacion geometrica real -- no existe todavia, es la pieza mas dificil de este roadmap: comparar bounding boxes de cada elemento de texto renderizado)
4. El slide de cierre incluye un elemento de identidad de marca, no solo texto? (validable en config_loader.py: si rol_narrativo == "cierre", exigir un campo nuevo elemento_marca)

Estado actual: ninguno de estos 4 checks existe todavia en codigo. Este documento es la especificacion; la implementacion es el trabajo de las Fases 1-3 del roadmap (ver FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 8 para el registro de la sesion que origino esta necesidad).

---

## 7. Roadmap de implementacion (fases, no todo de una sesion)

- Fase 0 (este documento): principios documentados. COMPLETO 31-ago-2026.
- Fase 1: config_loader.py exige rol_narrativo en el schema; etiqueta_colgante/nota_esquina exigen imagen de fondo; doble_marco gana campo de texto de anclaje (con medicion previa).
- Fase 2: motor de decision -- dado el rol_narrativo y el layout, calcular automaticamente tamano/posicion dentro de los rangos de la Seccion 1, en vez de coordenadas fijas por layout.
- Fase 3: checklist de auto-verificacion (Seccion 6) implementado como funcion que corre antes de que main.py de una pieza por exportada.
- Fase 4 (identificada 13-sep-2026, no iniciada): extender la Seccion 8 (Puentes narrativos) a video/reels. El tiempo aparece como variable nueva -- el Test de Silueta deja de ser solo composicion y se vuelve tambien de duracion (una imagen que necesita 3 segundos para leerse pero el clip solo la sostiene 2 rompe el loop por timing, no por diseno). En video el puente narrativo puede resolverse con una linea de narracion cayendo sobre la imagen existente (insercion temporal) en vez de un slide nuevo (insercion espacial) -- mecanismo distinto, no el mismo truco trasladado. La unidad atomica de planeacion en video probablemente deba ser el "beat" (imagen + duracion + linea de narracion + movimiento de camara + caption), no el "slide" -- FYR ya tiene un precedente de esto en el shot list de 13 beats documentado para "Video 1 (WHY)".

Cada fase se ataca como su propia sesion de trabajo, con verificacion visual real antes de pasar a la siguiente -- el mismo metodo que usamos para construir el resto de assemble.py, aplicado a esta capa nueva.

---

## 8. Puentes narrativos entre slides de imagen pura (13-sep-2026, decision de Johnny)

**Problema que resuelve:** una secuencia de slides full_bleed (imagen pura, sin texto -- ver Seccion 2) puede perder al espectador de baja capacidad de inferencia cuando el SUJETO o REGISTRO de la imagen cambia de un slide al siguiente, sin ningun texto que marque el giro. Confirmado con evidencia real en PZA_1.2: Slide 2 (ilustracion-journal comparando "mi media acre" vs "el vecino de 5 acres") pasa a Slide 3 (foto de un patio descuidado) sin que nada aclare de quien es ese patio -- podria leerse como mas detalle del vecino, o como el "antes" del narrador. El espectador pierde el hilo no por mal diseño de cada imagen, sino porque el salto entre ellas no esta anclado.

**Marco conceptual (dos principios de oficio narrativo, no inventados para FYR):**

1. **Test de Silueta** (principio de animacion clasica -- Disney/Pixar exigen que cada frame se lea solo, en 1-2 segundos, sin depender de contexto externo): aplicado a una imagen aislada, no explica si el sujeto es "yo" o "el otro", ni si es metafora o documento real, ese frame FALLA el test -- necesita anclaje.
2. **Apertura/cierre de loop narrativo** (ya documentado como arquitectura de hook en Sistema_Maestro_CRS_v2.md, Parte 3): un CIERRE de loop puede ser puramente visual -- el cerebro reconoce una resolucion sin que haga falta explicarla (ej. Slide 3 a Slide 4 en PZA_1.2, antes/despues del mismo espacio, el contraste cierra solo). Una APERTURA o GIRO de loop (una pregunta nueva que la imagen genera pero nadie formula en palabras) SIEMPRE necesita anclaje textual -- el cerebro no puede registrar una pregunta que nadie hizo.

**Regla de aplicacion:** entre dos slides full_bleed consecutivos, evaluar la transicion contra ambos principios:
- Si el segundo slide PASA el Test de Silueta por si solo (queda claro quien/que/por que sin ayuda externa) Y la transicion es un CIERRE de loop (resolucion, contraste, pago de una promesa ya hecha) -> no necesita puente.
- Si el segundo slide FALLA el Test de Silueta, O la transicion es una APERTURA/GIRO de loop (cambio de sujeto, cambio de "el otro" a "yo", cambio de metafora a documento real) -> insertar un slide `solo_texto` corto (una sola clausula, no un parrafo) entre ambos que nombre el giro.

**No es "cada full_bleed necesita texto"** -- eso contradiria la Seccion 2 (full_bleed es SOLO imagen, sin excepcion). La solucion nunca es agregarle texto a la imagen -- es insertar un slide puente nuevo entre las dos imagenes.

**Ejemplo real aplicado (PZA_1.2):** entre Slide 2 (journal) y Slide 3 (patio descuidado) se inserta un slide `solo_texto` nuevo con el texto "This is where my half acre started." -- resuelve el Test de Silueta (establece que el patio es del narrador, "my") y nombra la apertura del loop (un punto de partida, "started", antes de mostrar la transformacion en los slides siguientes).
