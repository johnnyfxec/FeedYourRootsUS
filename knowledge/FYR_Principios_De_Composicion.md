# FYR - Principios de Composicion para el Motor de Ensamblado
Version 1.1 - 11 de octubre 2026 (poda de layouts; v1.0: 31 de agosto 2026)
Proposito: reglas verificables por codigo que le permiten a Claude Code (u otra sesion) tomar decisiones de tamano, posicion y combinacion de layouts de forma AUTONOMA, sin aprobacion pieza por pieza -- con el mismo criterio que un compositor humano experimentado aplicaria, pero codificado como logica explicita.

Este documento existe porque durante la construccion de assemble.py (24-31 ago 2026), varias piezas de prueba salieron con errores de composicion reales (elementos decorativos usados como contenido principal, layouts sin sentido narrativo combinados entre si) que el codigo no podia prevenir porque no existia una capa de decision -- solo ejecucion de coordenadas fijas. Este documento es esa capa de decision, en forma de reglas.

---

## 0. El problema que este documento resuelve

Antes de este documento: cada slide de un brief se armaba eligiendo un layout de una lista, sin ningun criterio que verificara si esa eleccion tenia sentido compositivo. Resultado real observado: elementos decorativos usados como el contenido UNICO de un slide entero (se ve vacio y sin peso), acentos combinados con imagenes sin relacion narrativa entre ambos, texto de portada creciendo sin limite hasta invadir otro elemento. (11-oct-2026: esos elementos decorativos se eliminaron del sistema; ver Arquitectura Seccion 0.)

Despues de este documento: cada slide de un brief declara su rol narrativo explicito, y el motor de composicion usa ese rol -- no el layout elegido a ciegas -- para determinar tamano, posicion, y que combinaciones son validas.

---

## 1. Los 3 roles narrativos

Todo slide de una pieza (carrusel o reel) cumple exactamente uno de estos 3 roles. (v1.0 incluia un cuarto rol, `dato_al_margen`, retirado el 11-oct-2026 junto con los layouts que lo usaban.) El brief JSON debe declararlo explicitamente en el campo rol_narrativo -- el motor NO lo infiere del largo del texto, lo infiere de la importancia narrativa que quien arma el brief le asigna.

| Rol | Funcion | % de canvas que ocupa el elemento principal | Ejemplos de uso |
|---|---|---|---|
| protagonista | El mensaje central del slide -- lo que abre o cierra un loop narrativo | 60-90% | Portada, hook de apertura, revelacion clave, resultado final |
| acompanante | Desarrolla o sostiene la narrativa, comparte espacio con una imagen real | 30-60% (el texto), imagen ocupa el resto | Texto lateral, ventana_texto, cuerpo de doble_marco con anclaje |
| cierre | CTA + refuerzo de identidad de marca | Variable, pero SIEMPRE incluye un elemento de marca (logo, sello, frase ancla) ademas del texto | Ultimo slide del carrusel/reel |

---

## 2. Combinaciones de layout (sin acentos)

Desde el 11-oct-2026 no existen acentos ni el campo `acento`: cada slide se compone con un solo layout. Reglas vigentes:

| Layout | Regla |
|---|---|
| full_bleed | SOLO imagen, sin texto (13-sep-2026) |
| marco_grande_portada / marco_grande_cuadrado | Portadas: ya traen su decoracion integrada (marco, vid, hoja) y el titulo dorado con borde es exclusivo de ellas |
| marco_grande / doble_marco | El texto va en `texto_pie` (rol subtitulo), nunca en el estilo del titulo de portada |
| doble_marco | Conviene llevar `texto_pie` corto de anclaje: sin texto, dos imagenes sin contexto no comunican una comparacion real (aprendizaje del 31-ago; implementado como campo opcional el 11-oct-2026) |
| solo_texto, ventana_texto, texto_lateral | Llevan el icono C14 abajo al centro en 4:5 |
| lockup_cierre | Ultima slide del carrusel 4:5 (opcional en video 9:16) |

---

## 5. Relacion entre largo de texto y tamano de fuente (NO es el criterio de rol)

Aclaracion importante, para no confundir con la Seccion 1: el rol_narrativo determina el tamano del ESPACIO asignado al elemento (el % de canvas). Dentro de ese espacio ya asignado, el sistema de fit_text existente (reduccion automatica + limite minimo, ver text_renderer.py) sigue siendo el mecanismo correcto para ajustar el tamano de fuente al largo real del texto -- eso no cambia. Lo que cambia es que el ESPACIO ya no es una coordenada fija ciega, sino una funcion del rol narrativo declarado.

---

## 6. Checklist de auto-verificacion (Fase 3 del roadmap, pendiente)

Antes de que el sistema de una pieza por terminada sin supervision humana, debe poder confirmar:

1. Ningun slide combina un layout con una regla de la tabla de la Seccion 2 que prohiba? (validable con una funcion nueva, validar_combinaciones(cfg))
2. Ningun bloque de texto se superpone con otro? (requiere una verificacion geometrica real -- no existe todavia, es la pieza mas dificil de este roadmap: comparar bounding boxes de cada elemento de texto renderizado)
3. El slide de cierre incluye un elemento de identidad de marca, no solo texto? (validable en config_loader.py: si rol_narrativo == "cierre", exigir un campo nuevo elemento_marca)

Estado actual: ninguno de estos 3 checks existe todavia en codigo. Este documento es la especificacion; la implementacion es el trabajo de las Fases 1-3 del roadmap (ver FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 8 para el registro de la sesion que origino esta necesidad).

---

## 7. Roadmap de implementacion (fases, no todo de una sesion)

- Fase 0 (este documento): principios documentados. COMPLETO 31-ago-2026.
- Fase 1: config_loader.py exige rol_narrativo en el schema (el campo de texto de anclaje de doble_marco, `texto_pie`, ya se implemento el 11-oct-2026).
- Fase 2: motor de decision -- dado el rol_narrativo y el layout, calcular automaticamente tamano/posicion dentro de los rangos de la Seccion 1, en vez de coordenadas fijas por layout.
- Fase 3: checklist de auto-verificacion (Seccion 6) implementado como funcion que corre antes de que main.py de una pieza por exportada.
- Fase 4 (identificada 13-sep-2026; INICIADA 10-oct-2026 con el piloto de video PZA_4.2, ver `FYR_Protocolo_Edicion_Video.md`): extender la Seccion 8 (Puentes narrativos) a video/reels. El tiempo aparece como variable nueva -- el Test de Silueta deja de ser solo composicion y se vuelve tambien de duracion (una imagen que necesita 3 segundos para leerse pero el clip solo la sostiene 2 rompe el loop por timing, no por diseno). En video el puente narrativo puede resolverse con una linea de narracion cayendo sobre la imagen existente (insercion temporal) en vez de un slide nuevo (insercion espacial) -- mecanismo distinto, no el mismo truco trasladado. La unidad atomica de planeacion en video probablemente deba ser el "beat" (imagen + duracion + linea de narracion + movimiento de camara + caption), no el "slide" -- FYR ya tiene un precedente de esto en el shot list de 13 beats documentado para "Video 1 (WHY)".
  - Resultado del piloto (10-oct-2026): la unidad de planeación quedó como **slide-beat** (imagen 9:16 + línea narrada + zoom + subtítulos); la DURACIÓN de cada beat la fija la voz (TTS, `timings.json`), no el diseño, así que el Test de Silueta por timing se resuelve alargando o acortando la línea narrada. La narración cumple por diseño el rol de anclaje (cada imagen llega con su línea hablada). Sin probar todavía: un giro de loop sin anclaje en video.

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
