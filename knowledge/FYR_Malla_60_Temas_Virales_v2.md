# Feed Your Roots US — Malla Programática de 61 Temas Virales (v2) — banco semilla

**Sistema (actualizado 10-oct-2026):** skills `fyr-content` (briefs) y `fyr-video-assembler` (video) + Gemini (imágenes) + `assemble.py` local (carruseles, ver `FYR_Motor_Ensamblado_Arquitectura_v1.md`) + pipeline de video local (voz Google Cloud TTS + render Clipkit, ver `FYR_Protocolo_Edicion_Video.md`) + publicación manual. El stack original de esta Malla (`/generate` + KIE.ai para clips de video IA + Canva para plantillas + Blotato para publicar) no es el flujo real: Canva ya no se usa en ninguna parte; KIE.ai y Blotato siguen como ideas no implementadas.
**Versión anterior:** v1 (temas y prompts de imagen). Esta v2 añade: sistema de plantillas visuales validado, tipografía final, columna de Medio (Video/Carrusel), y título+subtítulo de portada por cada uno de los 60 temas.

---

## 🎨 Sistema de plantillas de marca (validado)

### Plantilla A — Portada tipo "capítulo de libro" (frame de apertura, 1.5-2s)
*Hoy se produce con el layout `marco_grande_cuadrado` (9:16) / `marco_grande_portada` (4:5) de `assemble.py`; en video es el slide 1 estático y sin subtítulos (`TPL-video-cover-framed.png`).*
- Canvas 1080×1920px, fondo parchment (#F5ECD7) con textura de papel envejecido, edge to edge
- Marco de imagen: **1:1** (cuadrado), imagen ilustrada dentro con marco de madera fina y envejecida (ver prompt de marco más abajo)
- Debajo del marco: un solo divisor de enredadera/hojas en forest green
- Título: 2 líneas, **Source Serif Pro**, color gold (#E8B84B) con contorno grueso brown (#5C3A1E)
- Subtítulo: 1-2 líneas itálicas, **Lora**, color brown (#5C3A1E)
- Pequeño ornamento de hoja al final
- Todo el bloque (marco + divisor + título + subtítulo + ornamento) debe estar centrado y contenido dentro del rango vertical seguro (ver zonas seguras abajo), ligeramente desplazado hacia arriba para que el thumbnail cuadrado de perfil (TikTok/Instagram) también muestre marco + inicio del título

### Plantilla B — Cierre / sello de marca (frame final, 1-2s)
- Franja parchment semi-transparente en la parte inferior
- Sello circular con el símbolo oficial de marca (C14, frasco con árbol; reglas en `FYR_Brand_Mark_Spec_v1.md`). El "brote + FYR en Satisfy" original quedó reemplazado. En el piloto de video PZA_4.2 no se usó sello de cierre: el cierre es narrado (CTA + frase en loop)
- Nombre del recurso mostrado en DM Sans, junto al sello

### Prompt reutilizable — Marco de madera envejecida (para aislar y reutilizar como asset de layout)
> A thin, delicate old wooden picture frame, viewed straight-on/flat (front-facing, no perspective angle), isolated on a solid flat white background for easy background removal. Vertical square 1:1 inner proportions, thin width (not chunky), aged weathered wood with visible grain, small natural cracks, warm brown tone (#5C3A1E) with honey-brown highlights. Simple, slightly rounded corners, minimal and rustic, not ornate. Inside completely empty/hollow. Soft even studio lighting, sharp focus on wood texture. Watercolor and ink illustration style, hand-painted look. High resolution, clean edges for isolation.

### Zonas seguras de plataforma (TikTok/Instagram, canvas 1080×1920)
- **Recorte de thumbnail de perfil (3:4):** se corta ~240px arriba y ~240px abajo — todo lo esencial debe caber entre y=240 y y=1680
- **UI de reproducción completa:** ~150-200px tapados arriba (usuario/sonido), ~250-320px tapados abajo (caption/botones), ~150px tapados a la derecha (like/comentar/compartir)
- **Zona segura combinada recomendada:** contenido esencial entre **y=240 y y=1600**, dejando margen lateral derecho libre de ~150px

### Tipografía final (corrección post-pruebas)
- **Título de portada:** Source Serif Pro (reemplaza a Playfair Display — mejor legibilidad en thumbnail pequeño, mantiene el tono editorial)
- **Subtítulo de portada:** Lora (ya validada, buena legibilidad a tamaño chico)
- Playfair Display se mantiene únicamente para piezas grandes fuera de video (landing page, portadas de libro impresas)

---

## 🎥 Video vs 🖼️ Carrusel — criterio de asignación

No todos los temas requieren animación. Se asigna **Medio** por afinidad de formato:

| Formato | Medio por defecto | Razón |
|---|---|---|
| Countdown | **Carrusel** | cada punto = un slide, cero necesidad de movimiento |
| Antes/Después | **Carrusel** | 2 imágenes fijas ya cuentan la historia completa |
| POV | Video | la inmersión en primera persona pierde fuerza sin movimiento |
| Storytime | Video | la narrativa se beneficia de sentirse "vivida", no solo leída |

**Nota estratégica:** el carrusel no está penalizado por el algoritmo, pero tiene techo de alcance viral más bajo que el video de gran escala; a cambio, suele generar más guardados/compartidos en contenido educativo. Esto describía el video como clips animados por IA (Qwen/KIE.ai, 5 s por clip, con costo). Con el pipeline de imágenes fijas + zoom + voz narrada (piloto PZA_4.2, un tema Countdown producido como video, 10-oct-2026) el video no gasta animación: su costo es la voz (dentro del tier gratuito de Google) y el render local. Los defaults de la tabla de arriba quedan como criterio creativo, ya no como restricción de costo; la decisión de cambiarlos depende de medir retención carrusel vs video con datos reales.

---

## 🗓️ Nota: Serie diaria ("365 Días de Homestead") — NO es un pilar

Aclaración importante: la idea de una pieza diaria de contenido (una tarea del Action Plan / Quick Calendar / Planting Calendar por cada día del año) **no se suma como pilar 12**. Es un **formato/cadencia de publicación** que cruza varios pilares a la vez (9, 2 y 6 principalmente), no un recurso nuevo con su propio dolor/CTA.

Se clasifica como la **capa de ejecución de la Fase 3** del pipeline de extracción masiva ya planeado (extracción atómica → scoring → generación de guión). Es el motor de volumen que correrá en paralelo a estos 60 temas curados, cuando se construya el skill/agente de producción y publicación. Usará el formato de Plantilla A (portada con ilustración diaria), sin necesidad de gancho/CTA de dolor tan elaborado como los 60 temas curados.

---

## Regla de diversidad (aplica a TODO el contenido)

Todos los personajes humanos (niños, padres, adultos) deben representar tonos de piel y etnias diversas a través del set de contenido — nunca por defecto blanco/rubio. Esta regla aplica a cada prompt de imagen y video generado para FYR, no solo a temas específicos. Se recomienda rotar el personaje protagonista entre temas distintos (mismo niño/familia dentro de un solo video para continuidad, pero variando entre videos del catálogo completo).

---

## Cómo está organizada esta malla

61 temas repartidos en **11 pilares**, uno por cada recurso ya producido de FYR (P5 tiene 4, P11 tiene 8). **Esta malla es el banco semilla, no una lista cerrada ni una carga en Airtable:** un tema entra a la tabla `Themes` cuando se produce, y los temas nuevos se extraen de los PDFs de cada pilar (ver `fyr-content`, sección 3). El archivo conserva "60" en el nombre por historia.

**Distribución de formato (61 total, contada del archivo):** POV 22 · Antes/Después 14 · Countdown 12 · Storytime 13
**Distribución de medio resultante (contada):** 34 Video · 27 Carrusel

**Estructura de cada tema:**
- **Gancho / título interno** (referencia de trabajo)
- **Ángulo de dolor/deseo**
- **Recurso FYR / CTA visual**
- **Formato** (POV / Antes-Después / Countdown / Storytime)
- **Medio** (Video / Carrusel)
- **Título de portada** (Source Serif Pro, 2 líneas) + **Subtítulo** (Lora, itálico)

**CORREGIDO 30-oct-2026:** este banco ya NO incluye un campo "Prompt de imagen" por tema — redactar el prompt visual de una escena es competencia exclusiva de `fyr-content` al armar el brief de cada pieza (Paso 3/4), siguiendo el bloque de estilo de `Feed-Your-Roots-Brand-Bible.md` y las reglas de `FYR_Asset_Governance_Policy.md`. La Malla es solo el banco de *qué contar* (dolor/deseo, formato, hook); nunca de *cómo dibujarlo*. Se eliminaron los ~75 prompts que este archivo traía antes porque varios usaban lenguaje de cámara fotográfica ("soft morning light", "blurred background") que compite contra el bloque de estilo del Brand Bible y puede producir salidas foto-realistas en vez de ilustradas (ver hallazgo real, sesión 30-oct-2026, PZA_1.1) — mantenerlos aquí, desincronizados de la única fuente de verdad de estilo, era el riesgo real, no solo el texto en sí.

---

## PILAR 1 — Half-Acre Blueprint (Core Bundle, $37)
*Dolor ancla: "no sé por dónde empezar / creo que necesito una granja grande"*

### 1.1 — "Empecé con media acre y un lápiz"
- **Dolor/deseo:** abrumado por la idea de que autosuficiencia = mucho terreno y dinero
- **CTA visual:** Core Bundle — plano del libro abierto en la mesa
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I STARTED WITH HALF AN ACRE AND A PENCIL" · **Subtítulo:** *Every homestead begins on paper.*

### 1.2 — "Mi vecino tiene 5 acres y cosecha menos que yo"
- **Dolor/deseo:** envidia/comparación con quienes tienen más terreno
- **CTA visual:** vista aérea ilustrada de un lote pequeño productivo
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "5 ACRES VS HALF AN ACRE" · **Subtítulo:** *It's never about the size of the land.*

### 1.3 — "Todo homestead empieza igual: en papel, en invierno"
- **Dolor/deseo:** nostalgia de simplicidad, deseo de un plan claro
- **CTA visual:** Core Bundle, capítulo de planeación
- **Formato:** POV · **Medio:** Video
- **Título portada:** "EVERY HOMESTEAD STARTS THE SAME WAY" · **Subtítulo:** *On paper, in winter.*

### 1.4 — "La cosa que nadie te dice del primer huerto"
- **Dolor/deseo:** miedo a fracasar / vergüenza de no saber
- **CTA visual:** libro abierto en capítulo de errores comunes
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT NO ONE TELLS YOU ABOUT YOUR FIRST GARDEN" · **Subtítulo:** *It's not supposed to look perfect.*

### 1.5 — "Convertí mi patio trasero en esto en un año"
- **Dolor/deseo:** deseo de resultado visible / prueba social
- **CTA visual:** libro + jardín real de fondo
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY BACKYARD, ONE YEAR LATER" · **Subtítulo:** *From bare grass to a half-acre blueprint.*

---

## PILAR 2 — Half-Acre Quick Calendar (Starter Bundle, $47)
*Dolor ancla: "no sé cuándo sembrar nada, siempre lo hago tarde"*

### 2.1 — "Sembré tomates en el mes equivocado (otra vez)"
- **Dolor/deseo:** miedo a desperdiciar tiempo/dinero por mal timing
- **CTA visual:** calendario visual desplegado
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I PLANTED TOMATOES AT THE WRONG TIME (AGAIN)" · **Subtítulo:** *Timing is everything in a garden.*

### 2.2 — "5 señales de que estás sembrando en la fecha equivocada"
- **Dolor/deseo:** ansiedad de estar haciendo algo mal sin saberlo
- **CTA visual:** calendario, columna de ventana de siembra
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOU'RE PLANTING AT THE WRONG TIME" · **Subtítulo:** *Your calendar might be the problem.*

### 2.3 — "Mi abuela nunca necesitó una app para saber cuándo sembrar"
- **Dolor/deseo:** nostalgia de sabiduría ancestral perdida
- **CTA visual:** calendario impreso, look vintage
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "GRANDMA NEVER NEEDED AN APP TO KNOW WHEN TO PLANT" · **Subtítulo:** *Some wisdom just gets passed down.*

### 2.4 — "36 plantas, un solo vistazo, cero adivinanzas"
- **Dolor/deseo:** deseo de simplicidad y control
- **CTA visual:** tabla completa del Quick Calendar
- **Formato:** POV · **Medio:** Video
- **Título portada:** "36 PLANTS, ONE GLANCE, ZERO GUESSING" · **Subtítulo:** *Everything you need to know, at once.*

### 2.5 — "Antes vs después de tener un calendario de siembra"
- **Dolor/deseo:** caos vs orden
- **CTA visual:** calendario resolviendo el caos
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "BEFORE AND AFTER A PLANTING CALENDAR" · **Subtítulo:** *Chaos in, order out.*

---

## PILAR 3 — Seed Library Kit (Starter Bundle, $47)
*Dolor ancla: "compro semillas sin saber si combinan / se me pierden"*

### 3.1 — "Mi caja de semillas era un desastre hasta esto"
- **Dolor/deseo:** desorganización, culpa de desperdicio
- **CTA visual:** kit de semillas ilustrado con 101 especies
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY SEED BOX WAS A DISASTER UNTIL THIS" · **Subtítulo:** *Order changes everything.*

### 3.2 — "101 plantas que sí puedes cultivar sin ser experto"
- **Dolor/deseo:** sentirse intimidado por la jardinería
- **CTA visual:** hoja ilustrada de la seed library
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "101 PLANTS YOU CAN GROW WITHOUT BEING AN EXPERT" · **Subtítulo:** *No green thumb required.*

### 3.3 — "Le enseñé a mi hija a distinguir semillas por categoría"
- **Dolor/deseo:** deseo de transmitir conocimiento a los hijos
- **CTA visual:** seed library + niño de espaldas ayudando
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I TAUGHT MY DAUGHTER TO SORT SEEDS BY CATEGORY" · **Subtítulo:** *Small hands, big lessons.*

### 3.4 — "Guardé semillas de mi propio jardín este año"
- **Dolor/deseo:** deseo de autosuficiencia total, no depender de comprar cada año
- **CTA visual:** sobre de semillas etiquetado a mano
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I SAVED SEEDS FROM MY OWN GARDEN THIS YEAR" · **Subtítulo:** *One step closer to self-sufficiency.*

### 3.5 — "Lo que compraba en semillas antes vs ahora"
- **Dolor/deseo:** ahorro económico
- **CTA visual:** comparación de gasto anual implícita
- **Formato:** Storytime · **Medio:** Carrusel
- **Título portada:** "WHAT I USED TO SPEND ON SEEDS VS NOW" · **Subtítulo:** *One library instead of a dozen packets.*

---

## PILAR 4 — Family Homestead Skill Map (Family Bundle, $67)
*Dolor ancla: "quiero involucrar a mis hijos pero no sé qué pueden hacer a su edad"*

### 4.1 — "Qué puede hacer tu hijo de 5 años en el huerto (y qué no)"
- **Dolor/deseo:** miedo a sobre-exigir o subestimar a los niños
- **CTA visual:** skill map con columnas de edad
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT YOUR 5-YEAR-OLD CAN (AND CAN'T) DO" · **Subtítulo:** *Every age has its own tasks.*

### 4.2 — "5 tareas de huerto que hasta un niño de 3 años puede hacer" ✅ *(en producción — ver ejemplo trabajado en este chat)*
- **Dolor/deseo:** deseo de involucrar a toda la familia sin frustración
- **CTA visual:** skill map, columna toddler
- **Formato:** Countdown (narrativo, microhistoria) · **Medio:** Video
- **Título portada:** "5 THINGS EVEN A 3-YEAR-OLD CAN DO" · **Subtítulo:** *The garden doesn't ask for grown-up hands.*

### 4.3 — "Mi esposo pensó que esto era solo cosa mía"
- **Dolor/deseo:** deseo de que la pareja se involucre, sentirse sola en el proyecto
- **CTA visual:** skill map compartido en la mesa
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "MY HUSBAND THOUGHT THIS WAS JUST MY THING" · **Subtítulo:** *Until the table proved him wrong.*

### 4.4 — "De juguetes a herramientas reales: la transición"
- **Dolor/deseo:** deseo de que los hijos crezcan con propósito, no solo pantallas
- **CTA visual:** skill map, progresión de edades
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "FROM TOYS TO REAL TOOLS" · **Subtítulo:** *Watching a kid grow into the garden.*

### 4.5 — "Lo que mis hijos aprenden en el huerto que la escuela no enseña"
- **Dolor/deseo:** deseo de educación práctica/valores tradicionales
- **CTA visual:** skill map, categoría "planning & learning"
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT MY KIDS LEARN THAT SCHOOL DOESN'T TEACH" · **Subtítulo:** *Some lessons only grow outdoors.*

---

## PILAR 5 — Kids' Roots Activity Pack (Family Bundle, $67)
*Dolor ancla: "necesito algo educativo sin pantallas para mis hijos"*

### 5.1 — "El bingo de cosecha que mis hijos piden jugar cada semana"
- **Dolor/deseo:** deseo de actividades familiares repetibles y sin pantallas
- **CTA visual:** Harvest Bingo ilustrado
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE HARVEST BINGO MY KIDS ASK FOR EVERY WEEK" · **Subtítulo:** *Screen-free and they still beg for more.*

### 5.2 — "Mi hija llevó su propio diario de jardín por primera vez"
- **Dolor/deseo:** orgullo, deseo de que los hijos desarrollen responsabilidad
- **CTA visual:** garden journal página con dibujo infantil
- **Formato:** Storytime · **Medio:** Carrusel
- **Título portada:** "MY DAUGHTER KEPT HER OWN GARDEN JOURNAL" · **Subtítulo:** *Her first entry, in her own words.*

### 5.3 — "De la huerta a la mesa: la receta que inventó mi hijo"
- **Dolor/deseo:** deseo de conexión familiar através de la comida
- **CTA visual:** página "Garden to Table" del activity pack
- **Formato:** POV · **Medio:** Video
- **Título portada:** "GARDEN TO TABLE: THE RECIPE MY SON INVENTED" · **Subtítulo:** *Proof he was paying attention.*

### 5.4 — "5 actividades de huerto para un día lluvioso"
- **Dolor/deseo:** necesidad de opciones cuando no se puede salir
- **CTA visual:** activity pack completo
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 GARDEN ACTIVITIES FOR A RAINY DAY" · **Subtítulo:** *No mud required.*

---

## PILAR 6 — Half-Acre Planting Calendar (Homestead Bundle, $97)
*Dolor ancla: "tengo demasiadas plantas y ninguna certeza de fechas exactas por zona"*

### 6.1 — "Por fin entendí en qué zona USDA vivo (y por qué importa)"
- **Dolor/deseo:** confusión técnica, miedo a hacerlo mal
- **CTA visual:** calendario completo con columna de zonas
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I FINALLY UNDERSTOOD MY USDA ZONE" · **Subtítulo:** *And why it changes everything.*

### 6.2 — "101 plantas, cada una con su fecha exacta"
- **Dolor/deseo:** deseo de precisión y control total
- **CTA visual:** planting calendar, vista de página completa
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "101 PLANTS, EACH WITH ITS EXACT DATE" · **Subtítulo:** *No more guessing games.*

### 6.3 — "Dejé de perder cosechas por sembrar en la fecha equivocada"
- **Dolor/deseo:** frustración por pérdidas pasadas
- **CTA visual:** calendario resolviendo el problema
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I STOPPED LOSING HARVESTS TO BAD TIMING" · **Subtítulo:** *One calendar fixed it all.*

### 6.4 — "Lo que sembré en marzo cambió todo mi año"
- **Dolor/deseo:** deseo de un "antes de que sea tarde" / urgencia estacional
- **CTA visual:** calendario, mes de marzo resaltado
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT I PLANTED IN MARCH CHANGED MY WHOLE YEAR" · **Subtítulo:** *Small dates, big consequences.*

### 6.5 — "Zona 5 vs Zona 9: por qué tu vecino en Florida no debería darte consejos"
- **Dolor/deseo:** frustración de recibir consejos genéricos que no aplican
- **CTA visual:** comparación de columnas de zona
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "ZONE 5 VS ZONE 9" · **Subtítulo:** *Why your Florida neighbor's advice won't work.*

### 6.6 — "El error de sembrar todo el mismo día"
- **Dolor/deseo:** ansiedad por sobre-simplificar el proceso
- **CTA visual:** calendario, ventanas escalonadas
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE MISTAKE OF PLANTING EVERYTHING THE SAME DAY" · **Subtítulo:** *Stagger it, and everything changes.*

---

## PILAR 7 — Homestead Preservation Log (Homestead Bundle, $97)
*Dolor ancla: "cultivo mucho pero se me echa a perder / no sé si lo hice bien"*

### 7.1 — "Mi primer tarro de conservas que sí selló bien"
- **Dolor/deseo:** miedo a hacerlo mal / inseguridad técnica
- **CTA visual:** preservation log, canning log
- **Formato:** POV · **Medio:** Video
- **Título portada:** "MY FIRST JAR THAT ACTUALLY SEALED RIGHT" · **Subtítulo:** *That little pop meant everything.*

### 7.2 — "5 señales de que tu conserva NO selló correctamente"
- **Dolor/deseo:** miedo a intoxicación / desperdicio
- **CTA visual:** canning log, columna "sealed"
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOUR JAR DIDN'T SEAL RIGHT" · **Subtítulo:** *Better to know now than later.*

### 7.3 — "Antes tiraba la mitad de mi cosecha, ahora nada se pierde"
- **Dolor/deseo:** culpa por desperdicio, deseo de aprovechar todo
- **CTA visual:** pantry inventory completo y organizado
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I USED TO WASTE HALF MY HARVEST" · **Subtítulo:** *Now nothing goes to waste.*

### 7.4 — "Cómo mi abuela conservaba comida sin refrigerador (y funciona hoy)"
- **Dolor/deseo:** nostalgia, deseo de resiliencia ante crisis
- **CTA visual:** preservation log, sección fermentación
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "HOW GRANDMA PRESERVED FOOD WITHOUT A FRIDGE" · **Subtítulo:** *And it still works today.*

### 7.5 — "Mi congelador organizado por primera vez en años"
- **Dolor/deseo:** caos doméstico, deseo de control
- **CTA visual:** freezing log
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY FREEZER, ORGANIZED FOR THE FIRST TIME IN YEARS" · **Subtítulo:** *One log page changed everything.*

### 7.6 — "Lo que un apagón de 3 días me enseñó sobre mi despensa"
- **Dolor/deseo:** miedo a crisis / emergencia, deseo de preparación
- **CTA visual:** pantry inventory como red de seguridad
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT A 3-DAY BLACKOUT TAUGHT ME ABOUT MY PANTRY" · **Subtítulo:** *We never went hungry.*

---

## PILAR 8 — Half-Acre Master Layout (Complete Bundle, $150)
*Dolor ancla: "no sé cómo distribuir mi terreno sin desperdiciar espacio"*

### 8.1 — "Así se ve media acre bien aprovechada"
- **Dolor/deseo:** deseo de ver el resultado final posible
- **CTA visual:** master layout, vista aérea del modelo
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THIS IS WHAT A WELL-USED HALF ACRE LOOKS LIKE" · **Subtítulo:** *Every corner has a purpose.*

### 8.2 — "Cuarto de acre también alcanza (aquí el plano)"
- **Dolor/deseo:** ansiedad de "no tengo suficiente terreno"
- **CTA visual:** master layout, versión cuarto de acre
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "A QUARTER ACRE IS ENOUGH" · **Subtítulo:** *Here's the exact layout.*

### 8.3 — "Por qué mi colmena mira hacia el este (y la tuya debería también)"
- **Dolor/deseo:** deseo de hacer las cosas técnicamente correctas
- **CTA visual:** master layout, ubicación de colmena
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHY MY BEEHIVE FACES EAST" · **Subtítulo:** *And yours probably should too.*

### 8.4 — "El error de poner el invernadero en el lugar equivocado"
- **Dolor/deseo:** miedo a cometer errores de diseño costosos
- **CTA visual:** master layout, orientación sur del invernadero
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "THE MISTAKE OF PLACING YOUR GREENHOUSE WRONG" · **Subtítulo:** *Orientation is everything.*

### 8.5 — "6 elementos que todo homestead necesita, en orden de prioridad"
- **Dolor/deseo:** abrumado por no saber qué construir primero
- **CTA visual:** master layout, leyenda numerada
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "6 THINGS EVERY HOMESTEAD NEEDS FIRST" · **Subtítulo:** *In the right order.*

### 8.6 — "De este patio vacío a este plano en una tarde"
- **Dolor/deseo:** deseo de rapidez y claridad en la planeación
- **CTA visual:** master layout, plantilla personalizable
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "FROM EMPTY YARD TO FULL LAYOUT IN ONE AFTERNOON" · **Subtítulo:** *The plan made it possible.*

---

## PILAR 9 — First & Second Year Action Plan (Complete Bundle, $150)
*Dolor ancla: "quiero empezar pero no sé qué hacer en qué orden, me paralizo"*

### 9.1 — "Semana 1 de mi homestead: esto fue lo único que hice"
- **Dolor/deseo:** parálisis por análisis, necesidad de un primer paso simple
- **CTA visual:** action plan, semana 1 de enero
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WEEK ONE OF MY HOMESTEAD" · **Subtítulo:** *This was the only thing I did.*

### 9.2 — "576 tareas para no perderme en mi primer año"
- **Dolor/deseo:** deseo de un mapa completo y confiable
- **CTA visual:** action plan, vista de página mensual completa
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "576 TASKS SO I NEVER GOT LOST" · **Subtítulo:** *A full year, mapped out.*

### 9.3 — "Lo que debí ordenar en enero y no lo hice"
- **Dolor/deseo:** miedo a llegar tarde a fechas críticas (pollos, abejas, semillas)
- **CTA visual:** action plan, notas de "order now"
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT I SHOULD HAVE ORDERED IN JANUARY" · **Subtítulo:** *And didn't.*

### 9.4 — "Año 1 caótico vs Año 2 con un plan"
- **Dolor/deseo:** deseo de dejar atrás el caos del primer intento
- **CTA visual:** action plan resolviendo el caos
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "CHAOTIC YEAR ONE VS PLANNED YEAR TWO" · **Subtítulo:** *Same land, different outcome.*

### 9.5 — "5 tareas de infraestructura que debes hacer antes de marzo"
- **Dolor/deseo:** urgencia estacional, miedo a quedarse atrás
- **CTA visual:** action plan, categoría infra/repair
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 INFRASTRUCTURE TASKS BEFORE MARCH" · **Subtítulo:** *Do these before the season starts.*

### 9.6 — "Cómo se ve un plan de dos años bien hecho"
- **Dolor/deseo:** deseo de visión a largo plazo, no solo supervivencia
- **CTA visual:** action plan, vista general year 1 vs year 2
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT A WELL-MADE TWO-YEAR PLAN LOOKS LIKE" · **Subtítulo:** *Vision beyond just surviving.*

---

## PILAR 10 — Shopping & Sourcing Guide (Complete Bundle, $150)
*Dolor ancla: "no sé cuánto cuesta esto de verdad ni dónde comprarlo sin que me estafen"*

### 10.1 — "Cuánto me costó realmente mi primer año de homestead"
- **Dolor/deseo:** miedo al costo oculto / sorpresas financieras
- **CTA visual:** shopping guide, tabla de presupuesto año 1
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT MY FIRST HOMESTEAD YEAR REALLY COST" · **Subtítulo:** *The real numbers, no filter.*

### 10.2 — "5 cosas que debes comprar localmente antes que en línea"
- **Dolor/deseo:** deseo de ahorrar y apoyar comunidad local
- **CTA visual:** shopping guide, sección "buy local first"
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 THINGS TO BUY LOCAL BEFORE ONLINE" · **Subtítulo:** *Your community has what you need.*

### 10.3 — "El mes en que se agotan las semillas raras (y cómo no perdértelo)"
- **Dolor/deseo:** miedo a quedarse sin opciones / FOMO estacional
- **CTA visual:** shopping guide, calendario mensual de compras
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "THE MONTH RARE SEEDS SELL OUT" · **Subtítulo:** *Don't miss the window.*

### 10.4 — "Gasté de más en mi gallinero por no comparar precios"
- **Dolor/deseo:** arrepentimiento financiero, deseo de evitar el mismo error
- **CTA visual:** shopping guide, rango de precios por categoría
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I OVERPAID FOR MY COOP" · **Subtítulo:** *Because I didn't compare prices.*

### 10.5 — "El presupuesto real para empezar (no el que ves en redes)"
- **Dolor/deseo:** desconfianza hacia contenido "aspiracional" poco realista
- **CTA visual:** shopping guide, rango bajo vs alto
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE REAL STARTING BUDGET" · **Subtítulo:** *Not the one you see on social media.*

---

## PILAR 11 — Homestead Troubleshooting Field Guide (Complete Bundle, $150)
*Dolor ancla: "algo le pasa a mi planta/gallina y no sé qué ni cómo arreglarlo"*

### 11.1 — "Por qué mis tomates tienen esa mancha oscura"
- **Dolor/deseo:** frustración, sensación de estar perdiendo la cosecha
- **CTA visual:** troubleshooting guide, entrada de antracnosis
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHY MY TOMATOES HAVE THAT DARK SPOT" · **Subtítulo:** *One page told me exactly why.*

### 11.2 — "5 señales de que tu suelo está enfermo"
- **Dolor/deseo:** miedo a un problema invisible que arruina todo
- **CTA visual:** troubleshooting guide, sección salud del suelo
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOUR SOIL IS SICK" · **Subtítulo:** *The problem you can't always see.*

### 11.3 — "Encontré gusanos verdes gigantes en mis tomates"
- **Dolor/deseo:** asco/sorpresa, urgencia de resolver ya
- **CTA visual:** troubleshooting guide, entrada de gusano cachón
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "I FOUND GIANT GREEN WORMS ON MY TOMATOES" · **Subtítulo:** *Here's what they actually were.*

### 11.4 — "Diagnostiqué mis gallinas antes de que fuera tarde"
- **Dolor/deseo:** miedo a perder animales por no saber identificar señales
- **CTA visual:** troubleshooting guide, sección aves/gallinero
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I DIAGNOSED MY HENS BEFORE IT WAS TOO LATE" · **Subtítulo:** *One page, caught in time.*

### 11.5 — "Antes tiraba mis plantas sin saber qué les pasaba"
- **Dolor/deseo:** culpa retrospectiva, deseo de haber sabido antes
- **CTA visual:** troubleshooting guide resolviendo el problema
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I USED TO THROW AWAY PLANTS I DIDN'T UNDERSTAND" · **Subtítulo:** *Now I know exactly what to fix.*

### 11.6 — "131 problemas de homestead, todos con solución en una página"
- **Dolor/deseo:** deseo de sentirse preparado ante cualquier imprevisto
- **CTA visual:** troubleshooting guide, vista general del libro
- **Formato:** POV · **Medio:** Video
- **Título portada:** "131 HOMESTEAD PROBLEMS, ALL SOLVED IN ONE BOOK" · **Subtítulo:** *Whatever goes wrong, it's in here.*

### 11.7 — "Mi compost olía mal hasta que encontré la razón"
- **Dolor/deseo:** vergüenza doméstica, frustración con lo básico que "debería funcionar solo"
- **CTA visual:** troubleshooting guide, sección infraestructura
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "MY COMPOST SMELLED BAD UNTIL I FOUND OUT WHY" · **Subtítulo:** *One fix, no more smell.*

### 11.8 — "5 plagas que arruinan tu huerto en verano (y cómo pararlas)"
- **Dolor/deseo:** ansiedad estacional, miedo a perder toda la cosecha de verano
- **CTA visual:** troubleshooting guide, sección pests & insects
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 PESTS THAT RUIN YOUR SUMMER GARDEN" · **Subtítulo:** *And how to stop them.*

---

## Checklist de producción rápida

1. Imagen de portada: marco 1:1 con madera envejecida, bloque completo entre y=240 y y=1600, título Source Serif Pro + subtítulo Lora
2. Imágenes de escena: 1080×1920 exacto para clips animados, o 1:1 si van dentro del marco de portada
3. Sin texto no intencional en la imagen (salvo gpt-image-2 a propósito)
4. Personaje narrador SIEMPRE en POV — nunca rostro frontal; familiares secundarios permitidos de cuerpo/rostro completo
5. Diversidad de piel/etnia rotada entre temas del catálogo — nunca por defecto blanco/rubio
6. Countdown/Antes-Después → Carrusel por defecto; POV/Storytime → Video (el video de imágenes fijas + voz no gasta animación; un Countdown puede salir como video, ver el piloto PZA_4.2)
7. Prompt de animación (cuando aplique): una sola micro-acción, cámara sutil ("barely drifting"), línea obligatoria "no distortion / no extra fingers / no facial warping", línea "preserve the watercolor and ink illustration texture"
8. Si se usa animación IA (clips): confirmar costo cotizado por el skill `/generate` antes de aprobar. No aplica al video de imágenes fijas + voz
9. Cuenta social "calentada" (actividad manual diaria) antes de automatizar la publicación (hoy es manual; Blotato sigue sin conectar)

---

**Resumen numérico:** 61 temas · 11 pilares · 22 POV / 14 Antes-Después / 12 Countdown / 13 Storytime · 34 Video / 27 Carrusel · Costo estimado de generación de video (solo la porción en Video, sin descartes): ~$22–24 USD a $0.75–0.80/clip. La porción en Carrusel no requiere gasto de animación. (Esa cifra es para clips IA; el video de imágenes fijas + voz cuesta ≈ $0 mientras la voz esté en el tier gratuito de Google.)
