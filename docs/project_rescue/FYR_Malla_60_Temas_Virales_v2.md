# Feed Your Roots US — Malla Programática de 60 Temas Virales (v2)

**Sistema:** Claude `/generate` skill + KIE.ai (video) + Canva (plantillas) + Gemini (imágenes) + Blotato (publicación)
**Versión anterior:** v1 (temas y prompts de imagen). Esta v2 añade: sistema de plantillas visuales validado, tipografía final, columna de Medio (Video/Carrusel), y título+subtítulo de portada por cada uno de los 60 temas.

---

## 🎨 Sistema de plantillas de marca (validado)

### Plantilla A — Portada tipo "capítulo de libro" (frame de apertura, 1.5-2s)
- Canvas 1080×1920px, fondo parchment (#F5ECD7) con textura de papel envejecido, edge to edge
- Marco de imagen: **1:1** (cuadrado), imagen ilustrada dentro con marco de madera fina y envejecida (ver prompt de marco más abajo)
- Debajo del marco: un solo divisor de enredadera/hojas en forest green
- Título: 2 líneas, **Source Serif Pro**, color gold (#E8B84B) con contorno grueso brown (#5C3A1E)
- Subtítulo: 1-2 líneas itálicas, **Lora**, color brown (#5C3A1E)
- Pequeño ornamento de hoja al final
- Todo el bloque (marco + divisor + título + subtítulo + ornamento) debe estar centrado y contenido dentro del rango vertical seguro (ver zonas seguras abajo), ligeramente desplazado hacia arriba para que el thumbnail cuadrado de perfil (TikTok/Instagram) también muestre marco + inicio del título

### Plantilla B — Cierre / sello de marca (frame final, 1-2s)
- Franja parchment semi-transparente en la parte inferior
- Sello circular con el **logo real de FYR** (brote + "FYR" en Satisfy script)
- Nombre del recurso mostrado en DM Sans, junto al sello

### Prompt reutilizable — Marco de madera envejecida (para aislar y reutilizar en Canva)
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

**Nota estratégica:** el carrusel no está penalizado por el algoritmo, pero tiene techo de alcance viral más bajo que el video de gran escala; a cambio, suele generar más guardados/compartidos en contenido educativo. Mientras no haya presupuesto de animación, priorizar carrusel en Countdown/Antes-Después, y reservar el video (Qwen gratis, clips de 5s) para 1-2 piezas semanales en POV/Storytime donde el gancho depende del movimiento.

---

## 🗓️ Nota: Serie diaria ("365 Días de Homestead") — NO es un pilar

Aclaración importante: la idea de una pieza diaria de contenido (una tarea del Action Plan / Quick Calendar / Planting Calendar por cada día del año) **no se suma como pilar 12**. Es un **formato/cadencia de publicación** que cruza varios pilares a la vez (9, 2 y 6 principalmente), no un recurso nuevo con su propio dolor/CTA.

Se clasifica como la **capa de ejecución de la Fase 3** del pipeline de extracción masiva ya planeado (extracción atómica → scoring → generación de guión). Es el motor de volumen que correrá en paralelo a estos 60 temas curados, cuando se construya el skill/agente de producción y publicación. Usará el formato de Plantilla A (portada con ilustración diaria), sin necesidad de gancho/CTA de dolor tan elaborado como los 60 temas curados.

---

## Regla de diversidad (aplica a TODO el contenido)

Todos los personajes humanos (niños, padres, adultos) deben representar tonos de piel y etnias diversas a través del set de contenido — nunca por defecto blanco/rubio. Esta regla aplica a cada prompt de imagen y video generado para FYR, no solo a temas específicos. Se recomienda rotar el personaje protagonista entre temas distintos (mismo niño/familia dentro de un solo video para continuidad, pero variando entre videos del catálogo completo).

---

## Cómo está organizada esta malla

60 temas repartidos en **11 pilares**, uno por cada recurso ya producido de FYR.

**Distribución de formato (60 total):** POV 30 · Antes/Después 10 · Countdown 10 · Storytime 10
**Distribución de medio resultante:** ~30 Video · ~30 Carrusel (aprox., ver detalle por tema)

**Estructura de cada tema:**
- **Gancho / título interno** (referencia de trabajo)
- **Ángulo de dolor/deseo**
- **Recurso FYR / CTA visual**
- **Formato** (POV / Antes-Después / Countdown / Storytime)
- **Medio** (Video / Carrusel)
- **Título de portada** (Source Serif Pro, 2 líneas) + **Subtítulo** (Lora, itálico)
- **Prompt de imagen (Gemini/Nano Banana)**

---

## PILAR 1 — Half-Acre Blueprint (Core Bundle, $37)
*Dolor ancla: "no sé por dónde empezar / creo que necesito una granja grande"*

### 1.1 — "Empecé con media acre y un lápiz"
- **Dolor/deseo:** abrumado por la idea de que autosuficiencia = mucho terreno y dinero
- **CTA visual:** Core Bundle — plano del libro abierto en la mesa
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I STARTED WITH HALF AN ACRE AND A PENCIL" · **Subtítulo:** *Every homestead begins on paper.*
- **Prompt:** First-person POV, watercolor and ink illustration in a vintage nature-journal style, hands resting on a wooden kitchen table at dawn, an open illustrated book titled "Half-Acre Blueprint" showing a hand-drawn garden layout, soft morning light through a window, muted forest green and warm terracotta palette, parchment-colored pages with visible ink linework, cozy rustic kitchen blurred in background, vertical 9:16, 2K resolution, crisp linework on the book page.

### 1.2 — "Mi vecino tiene 5 acres y cosecha menos que yo"
- **Dolor/deseo:** envidia/comparación con quienes tienen más terreno
- **CTA visual:** vista aérea ilustrada de un lote pequeño productivo
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "5 ACRES VS HALF AN ACRE" · **Subtítulo:** *It's never about the size of the land.*
- **Prompt (ANTES):** Watercolor and ink illustration, aerial view of a small suburban backyard, half in shadow and neglected, patchy grass, one sad wilted planter box, muted brown and gray tones, vintage botanical journal style, vertical 9:16.
- **Prompt (DESPUÉS):** Same aerial angle, same small suburban backyard now transformed into a thriving half-acre-style homestead layout — raised beds, small greenhouse, chicken coop, fruit trees — lush forest green and terracotta color palette, warm golden-hour light, watercolor and ink vintage nature journal style, vertical 9:16.

### 1.3 — "Todo homestead empieza igual: en papel, en invierno"
- **Dolor/deseo:** nostalgia de simplicidad, deseo de un plan claro
- **CTA visual:** Core Bundle, capítulo de planeación
- **Formato:** POV · **Medio:** Video
- **Título portada:** "EVERY HOMESTEAD STARTS THE SAME WAY" · **Subtítulo:** *On paper, in winter.*
- **Prompt:** First-person POV, hand holding a pencil sketching a garden grid on graph paper next to an open illustrated homestead book, winter light from a frosted window, wool sweater sleeve visible, watercolor and ink illustration style, warm brown and parchment tones with a small terracotta accent, vertical 9:16, cozy winter atmosphere.

### 1.4 — "La cosa que nadie te dice del primer huerto"
- **Dolor/deseo:** miedo a fracasar / vergüenza de no saber
- **CTA visual:** libro abierto en capítulo de errores comunes
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT NO ONE TELLS YOU ABOUT YOUR FIRST GARDEN" · **Subtítulo:** *It's not supposed to look perfect.*
- **Prompt:** Watercolor and ink illustration, first-person POV kneeling in a small backyard garden bed, dirt-covered hands holding a wilted seedling, an open illustrated guidebook resting on the grass beside the bed opened to a helpful diagram, soft overcast daylight, muted forest green and warm brown palette, vintage nature journal aesthetic, vertical 9:16.

### 1.5 — "Convertí mi patio trasero en esto en un año"
- **Dolor/deseo:** deseo de resultado visible / prueba social
- **CTA visual:** libro + jardín real de fondo
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY BACKYARD, ONE YEAR LATER" · **Subtítulo:** *From bare grass to a half-acre blueprint.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV looking down at bare patchy backyard lawn, single empty flower pot, gray cloudy sky, muted desaturated tones, vintage journal style, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV angle one year later, lush illustrated raised bed garden filling the same yard, tomatoes and herbs growing, warm golden light, forest green and terracotta palette, watercolor and ink style, vertical 9:16.

---

## PILAR 2 — Half-Acre Quick Calendar (Starter Bundle, $47)
*Dolor ancla: "no sé cuándo sembrar nada, siempre lo hago tarde"*

### 2.1 — "Sembré tomates en el mes equivocado (otra vez)"
- **Dolor/deseo:** miedo a desperdiciar tiempo/dinero por mal timing
- **CTA visual:** calendario visual desplegado
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I PLANTED TOMATOES AT THE WRONG TIME (AGAIN)" · **Subtítulo:** *Timing is everything in a garden.*
- **Prompt:** First-person POV, hands unrolling an illustrated seasonal planting calendar chart on a wooden potting table, small terracotta pots and seed packets scattered nearby, soft spring morning light, watercolor and ink vintage nature-journal style, forest green and gold color accents, vertical 9:16.

### 2.2 — "5 señales de que estás sembrando en la fecha equivocada"
- **Dolor/deseo:** ansiedad de estar haciendo algo mal sin saberlo
- **CTA visual:** calendario, columna de ventana de siembra
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOU'RE PLANTING AT THE WRONG TIME" · **Subtítulo:** *Your calendar might be the problem.*
- **Prompt:** Watercolor and ink illustration, close-up POV of a hand pointing at a hand-illustrated planting calendar grid with small icons for sowing and harvest windows, warm parchment background, soft daylight, forest green ink linework, vertical 9:16, crisp legible chart detail.

### 2.3 — "Mi abuela nunca necesitó una app para saber cuándo sembrar"
- **Dolor/deseo:** nostalgia de sabiduría ancestral perdida
- **CTA visual:** calendario impreso, look vintage
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "GRANDMA NEVER NEEDED AN APP TO KNOW WHEN TO PLANT" · **Subtítulo:** *Some wisdom just gets passed down.*
- **Prompt:** Watercolor and ink illustration, first-person POV, weathered wooden hands (implying an elder) holding an illustrated seasonal calendar chart next to a windowsill with drying herbs, warm nostalgic golden light, sepia and forest green tones, vintage botanical journal style, vertical 9:16.

### 2.4 — "36 plantas, un solo vistazo, cero adivinanzas"
- **Dolor/deseo:** deseo de simplicidad y control
- **CTA visual:** tabla completa del Quick Calendar
- **Formato:** POV · **Medio:** Video
- **Título portada:** "36 PLANTS, ONE GLANCE, ZERO GUESSING" · **Subtítulo:** *Everything you need to know, at once.*
- **Prompt:** First-person POV, hands holding an illustrated wall chart covered in small botanical icons arranged in a monthly grid, kitchen wall in soft background blur, morning light, watercolor and ink style, forest green and terracotta palette, vertical 9:16.

### 2.5 — "Antes vs después de tener un calendario de siembra"
- **Dolor/deseo:** caos vs orden
- **CTA visual:** calendario resolviendo el caos
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "BEFORE AND AFTER A PLANTING CALENDAR" · **Subtítulo:** *Chaos in, order out.*
- **Prompt (ANTES):** Watercolor and ink illustration, cluttered kitchen counter with scattered seed packets, sticky notes, and a confused expression implied by messy handwriting, muted gray-brown tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same kitchen counter now tidy, a single open illustrated planting calendar chart neatly organizing the seed packets by month, warm forest green and gold tones, soft light, watercolor and ink style, vertical 9:16.

---

## PILAR 3 — Seed Library Kit (Starter Bundle, $47)
*Dolor ancla: "compro semillas sin saber si combinan / se me pierden"*

### 3.1 — "Mi caja de semillas era un desastre hasta esto"
- **Dolor/deseo:** desorganización, culpa de desperdicio
- **CTA visual:** kit de semillas ilustrado con 101 especies
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY SEED BOX WAS A DISASTER UNTIL THIS" · **Subtítulo:** *Order changes everything.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV looking down at a messy shoebox overflowing with unlabeled seed packets, dim indoor light, muted brown tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV, seed packets now neatly organized in labeled illustrated envelopes with hand-painted botanical icons, sorted by category, warm daylight, forest green and gold palette, watercolor and ink vintage style, vertical 9:16.

### 3.2 — "101 plantas que sí puedes cultivar sin ser experto"
- **Dolor/deseo:** sentirse intimidado por la jardinería
- **CTA visual:** hoja ilustrada de la seed library
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "101 PLANTS YOU CAN GROW WITHOUT BEING AN EXPERT" · **Subtítulo:** *No green thumb required.*
- **Prompt:** Watercolor and ink illustration, close-up POV of hands flipping through an illustrated seed library booklet with rows of hand-painted botanical illustrations — vegetables, herbs, flowers — soft natural light, parchment paper texture, forest green and terracotta accents, vertical 9:16.

### 3.3 — "Le enseñé a mi hija a distinguir semillas por categoría"
- **Dolor/deseo:** deseo de transmitir conocimiento a los hijos
- **CTA visual:** seed library + niño de espaldas ayudando
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I TAUGHT MY DAUGHTER TO SORT SEEDS BY CATEGORY" · **Subtítulo:** *Small hands, big lessons.*
- **Prompt:** First-person POV, looking down at a wooden table where a small child's hands (child seen from behind, no adult face) are sorting illustrated seed packets into category piles, warm afternoon light, watercolor and ink vintage nature-journal style, forest green and gold tones, vertical 9:16.

### 3.4 — "Guardé semillas de mi propio jardín este año"
- **Dolor/deseo:** deseo de autosuficiencia total, no depender de comprar cada año
- **CTA visual:** sobre de semillas etiquetado a mano
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I SAVED SEEDS FROM MY OWN GARDEN THIS YEAR" · **Subtítulo:** *One step closer to self-sufficiency.*
- **Prompt:** First-person POV, hands sealing a small illustrated hand-labeled seed envelope on a rustic table, dried seed heads and a pair of scissors nearby, golden hour light through a barn window, watercolor and ink style, warm brown and forest green palette, vertical 9:16.

### 3.5 — "Lo que compraba en semillas antes vs ahora"
- **Dolor/deseo:** ahorro económico
- **CTA visual:** comparación de gasto anual implícita
- **Formato:** Storytime · **Medio:** Carrusel
- **Título portada:** "WHAT I USED TO SPEND ON SEEDS VS NOW" · **Subtítulo:** *One library instead of a dozen packets.*
- **Prompt:** Watercolor and ink illustration, split-composition POV: left side shows a hand holding several separate store-bought seed packets with price tags, right side shows the same hand holding one organized illustrated seed library booklet, warm parchment background, forest green and gold palette, vertical 9:16.

---

## PILAR 4 — Family Homestead Skill Map (Family Bundle, $67)
*Dolor ancla: "quiero involucrar a mis hijos pero no sé qué pueden hacer a su edad"*

### 4.1 — "Qué puede hacer tu hijo de 5 años en el huerto (y qué no)"
- **Dolor/deseo:** miedo a sobre-exigir o subestimar a los niños
- **CTA visual:** skill map con columnas de edad
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT YOUR 5-YEAR-OLD CAN (AND CAN'T) DO" · **Subtítulo:** *Every age has its own tasks.*
- **Prompt:** First-person POV, adult hands (no face) guiding a small child's hands (child visible, seen from side/behind) watering a raised garden bed with a small watering can, warm afternoon light, watercolor and ink vintage nature-journal illustration, forest green and gold palette, vertical 9:16.

### 4.2 — "5 tareas de huerto que hasta un niño de 3 años puede hacer" ✅ *(en producción — ver ejemplo trabajado en este chat)*
- **Dolor/deseo:** deseo de involucrar a toda la familia sin frustración
- **CTA visual:** skill map, columna toddler
- **Formato:** Countdown (narrativo, microhistoria) · **Medio:** Video
- **Título portada:** "5 THINGS EVEN A 3-YEAR-OLD CAN DO" · **Subtítulo:** *The garden doesn't ask for grown-up hands.*
- **Prompts (5 escenas, mismo niño para continuidad):** ver detalle ya generado — bandeja de siembra, riego, semillas grandes, cosecha de frutas bajas, transporte de cosecha.

### 4.3 — "Mi esposo pensó que esto era solo cosa mía"
- **Dolor/deseo:** deseo de que la pareja se involucre, sentirse sola en el proyecto
- **CTA visual:** skill map compartido en la mesa
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "MY HUSBAND THOUGHT THIS WAS JUST MY THING" · **Subtítulo:** *Until the table proved him wrong.*
- **Prompt:** Watercolor and ink illustration, first-person POV at a kitchen table, an illustrated family skill chart spread open between two coffee mugs, a partner's hand (visible, no face) pointing at a task on the chart, warm evening light, forest green and brown palette, vintage nature-journal style, vertical 9:16.

### 4.4 — "De juguetes a herramientas reales: la transición"
- **Dolor/deseo:** deseo de que los hijos crezcan con propósito, no solo pantallas
- **CTA visual:** skill map, progresión de edades
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "FROM TOYS TO REAL TOOLS" · **Subtítulo:** *Watching a kid grow into the garden.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV of a child's hands (visible from behind) holding a tablet on a couch, dim indoor light, muted gray-blue tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same child now outdoors, hands holding a small trowel digging in a garden bed, warm golden sunlight, forest green and terracotta palette, watercolor and ink illustration, vertical 9:16.

### 4.5 — "Lo que mis hijos aprenden en el huerto que la escuela no enseña"
- **Dolor/deseo:** deseo de educación práctica/valores tradicionales
- **CTA visual:** skill map, categoría "planning & learning"
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT MY KIDS LEARN THAT SCHOOL DOESN'T TEACH" · **Subtítulo:** *Some lessons only grow outdoors.*
- **Prompt:** First-person POV, looking down at a wooden table where a child's hand (visible, no adult face) draws a garden layout on paper next to an illustrated family skill chart, warm afternoon light through a window, watercolor and ink vintage nature-journal style, forest green and gold tones, vertical 9:16.

---

## PILAR 5 — Kids' Roots Activity Pack (Family Bundle, $67)
*Dolor ancla: "necesito algo educativo sin pantallas para mis hijos"*

### 5.1 — "El bingo de cosecha que mis hijos piden jugar cada semana"
- **Dolor/deseo:** deseo de actividades familiares repetibles y sin pantallas
- **CTA visual:** Harvest Bingo ilustrado
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE HARVEST BINGO MY KIDS ASK FOR EVERY WEEK" · **Subtítulo:** *Screen-free and they still beg for more.*
- **Prompt:** First-person POV, looking down at a wooden table with an illustrated harvest bingo card covered in small hand-painted vegetable icons, a child's hand (visible from side) placing a marker on one square, warm kitchen light, watercolor and ink vintage style, forest green and terracotta palette, vertical 9:16.

### 5.2 — "Mi hija llevó su propio diario de jardín por primera vez"
- **Dolor/deseo:** orgullo, deseo de que los hijos desarrollen responsabilidad
- **CTA visual:** garden journal página con dibujo infantil
- **Formato:** Storytime · **Medio:** Carrusel
- **Título portada:** "MY DAUGHTER KEPT HER OWN GARDEN JOURNAL" · **Subtítulo:** *Her first entry, in her own words.*
- **Prompt:** Watercolor and ink illustration, first-person POV, an open illustrated garden journal page with a child's crayon-style drawing of a sunflower and simple handwriting, small hands (child visible from behind) holding a colored pencil, soft afternoon light, parchment paper texture, forest green and gold accents, vertical 9:16.

### 5.3 — "De la huerta a la mesa: la receta que inventó mi hijo"
- **Dolor/deseo:** deseo de conexión familiar através de la comida
- **CTA visual:** página "Garden to Table" del activity pack
- **Formato:** POV · **Medio:** Video
- **Título portada:** "GARDEN TO TABLE: THE RECIPE MY SON INVENTED" · **Subtítulo:** *Proof he was paying attention.*
- **Prompt:** First-person POV, kitchen counter with a small illustrated recipe card filled in by a child's handwriting, a bowl of freshly harvested vegetables beside it, a child's hands (visible, no face) stirring in a bowl, warm cozy kitchen light, watercolor and ink illustration style, terracotta and forest green tones, vertical 9:16.

### 5.4 — "5 actividades de huerto para un día lluvioso"
- **Dolor/deseo:** necesidad de opciones cuando no se puede salir
- **CTA visual:** activity pack completo
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 GARDEN ACTIVITIES FOR A RAINY DAY" · **Subtítulo:** *No mud required.*
- **Prompt:** Watercolor and ink illustration, POV of a wooden table by a rain-streaked window, an illustrated activity booklet open with seed-sorting and drawing pages, colored pencils scattered nearby, soft gray daylight with warm lamp glow, forest green and gold palette, vintage nature-journal style, vertical 9:16.

---

## PILAR 6 — Half-Acre Planting Calendar (Homestead Bundle, $97)
*Dolor ancla: "tengo demasiadas plantas y ninguna certeza de fechas exactas por zona"*

### 6.1 — "Por fin entendí en qué zona USDA vivo (y por qué importa)"
- **Dolor/deseo:** confusión técnica, miedo a hacerlo mal
- **CTA visual:** calendario completo con columna de zonas
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I FINALLY UNDERSTOOD MY USDA ZONE" · **Subtítulo:** *And why it changes everything.*
- **Prompt:** First-person POV, hands holding an illustrated detailed planting calendar booklet open to a page with color-coded USDA zone columns, small botanical icons per plant, warm desk lamp light, watercolor and ink vintage style, forest green and terracotta palette, vertical 9:16.

### 6.2 — "101 plantas, cada una con su fecha exacta"
- **Dolor/deseo:** deseo de precisión y control total
- **CTA visual:** planting calendar, vista de página completa
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "101 PLANTS, EACH WITH ITS EXACT DATE" · **Subtítulo:** *No more guessing games.*
- **Prompt:** Watercolor and ink illustration, close-up POV flipping through an illustrated planting calendar with rows of hand-painted plant icons and colored sowing/harvest bars, parchment texture, soft morning light, forest green and gold tones, vertical 9:16.

### 6.3 — "Dejé de perder cosechas por sembrar en la fecha equivocada"
- **Dolor/deseo:** frustración por pérdidas pasadas
- **CTA visual:** calendario resolviendo el problema
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I STOPPED LOSING HARVESTS TO BAD TIMING" · **Subtítulo:** *One calendar fixed it all.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV looking at a wilted, yellowed vegetable bed, overcast light, muted brown and gray tones, vintage journal style, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV angle, thriving vegetable bed full of ripe produce, an illustrated planting calendar booklet resting on the edge of the bed, warm golden light, forest green and terracotta palette, watercolor and ink style, vertical 9:16.

### 6.4 — "Lo que sembré en marzo cambió todo mi año"
- **Dolor/deseo:** deseo de un "antes de que sea tarde" / urgencia estacional
- **CTA visual:** calendario, mes de marzo resaltado
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT I PLANTED IN MARCH CHANGED MY WHOLE YEAR" · **Subtítulo:** *Small dates, big consequences.*
- **Prompt:** First-person POV, hands opening an illustrated planting calendar to a spring month page, seed packets and a trowel resting nearby on damp soil, early spring light, watercolor and ink vintage nature-journal style, forest green and gold accents, vertical 9:16.

### 6.5 — "Zona 5 vs Zona 9: por qué tu vecino en Florida no debería darte consejos"
- **Dolor/deseo:** frustración de recibir consejos genéricos que no aplican
- **CTA visual:** comparación de columnas de zona
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "ZONE 5 VS ZONE 9" · **Subtítulo:** *Why your Florida neighbor's advice won't work.*
- **Prompt:** Watercolor and ink illustration, split composition, left side a frost-covered garden bed in muted cold blue-gray tones, right side a sun-drenched garden bed in warm gold and terracotta tones, an illustrated zone map subtly visible between them, vintage nature-journal style, vertical 9:16.

### 6.6 — "El error de sembrar todo el mismo día"
- **Dolor/deseo:** ansiedad por sobre-simplificar el proceso
- **CTA visual:** calendario, ventanas escalonadas
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE MISTAKE OF PLANTING EVERYTHING THE SAME DAY" · **Subtítulo:** *Stagger it, and everything changes.*
- **Prompt:** First-person POV, hands holding a magnifying glass over an illustrated planting calendar page showing staggered sowing windows across weeks, warm desk light, watercolor and ink style, forest green and terracotta tones, vertical 9:16.

---

## PILAR 7 — Homestead Preservation Log (Homestead Bundle, $97)
*Dolor ancla: "cultivo mucho pero se me echa a perder / no sé si lo hice bien"*

### 7.1 — "Mi primer tarro de conservas que sí selló bien"
- **Dolor/deseo:** miedo a hacerlo mal / inseguridad técnica
- **CTA visual:** preservation log, canning log
- **Formato:** POV · **Medio:** Video
- **Título portada:** "MY FIRST JAR THAT ACTUALLY SEALED RIGHT" · **Subtítulo:** *That little pop meant everything.*
- **Prompt:** First-person POV, hands holding a sealed glass mason jar filled with preserved tomatoes, an illustrated canning log notebook open beside it on a rustic counter, steam rising from a canner in soft background blur, warm kitchen light, watercolor and ink vintage style, terracotta and forest green palette, vertical 9:16.

### 7.2 — "5 señales de que tu conserva NO selló correctamente"
- **Dolor/deseo:** miedo a intoxicación / desperdicio
- **CTA visual:** canning log, columna "sealed"
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOUR JAR DIDN'T SEAL RIGHT" · **Subtítulo:** *Better to know now than later.*
- **Prompt:** Watercolor and ink illustration, close-up POV of hands inspecting a row of sealed mason jars on a wooden shelf, an illustrated log page with checkmarks visible nearby, warm pantry light, forest green and gold tones, vintage nature-journal style, vertical 9:16.

### 7.3 — "Antes tiraba la mitad de mi cosecha, ahora nada se pierde"
- **Dolor/deseo:** culpa por desperdicio, deseo de aprovechar todo
- **CTA visual:** pantry inventory completo y organizado
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I USED TO WASTE HALF MY HARVEST" · **Subtítulo:** *Now nothing goes to waste.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV of a kitchen counter with wilted, rotting vegetables in a basket, dim light, muted brown tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same counter now replaced by a neatly organized pantry shelf full of labeled jars, dried herbs, and an illustrated inventory log, warm golden light, forest green and terracotta palette, watercolor and ink style, vertical 9:16.

### 7.4 — "Cómo mi abuela conservaba comida sin refrigerador (y funciona hoy)"
- **Dolor/deseo:** nostalgia, deseo de resiliencia ante crisis
- **CTA visual:** preservation log, sección fermentación
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "HOW GRANDMA PRESERVED FOOD WITHOUT A FRIDGE" · **Subtítulo:** *And it still works today.*
- **Prompt:** Watercolor and ink illustration, first-person POV, weathered hands packing sliced vegetables into a ceramic fermentation crock on a rustic wooden table, an illustrated preservation log open nearby, warm nostalgic light, sepia and forest green tones, vintage botanical journal style, vertical 9:16.

### 7.5 — "Mi congelador organizado por primera vez en años"
- **Dolor/deseo:** caos doméstico, deseo de control
- **CTA visual:** freezing log
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "MY FREEZER, ORGANIZED FOR THE FIRST TIME IN YEARS" · **Subtítulo:** *One log page changed everything.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV looking into a cluttered freezer with unlabeled frosty bags piled randomly, cool blue-gray tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same freezer POV now neatly organized with labeled bags in rows, an illustrated freezing log page visible taped to the door, warm accent lighting, forest green and gold tones, watercolor and ink style, vertical 9:16.

### 7.6 — "Lo que un apagón de 3 días me enseñó sobre mi despensa"
- **Dolor/deseo:** miedo a crisis / emergencia, deseo de preparación
- **CTA visual:** pantry inventory como red de seguridad
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT A 3-DAY BLACKOUT TAUGHT ME ABOUT MY PANTRY" · **Subtítulo:** *We never went hungry.*
- **Prompt:** Watercolor and ink illustration, first-person POV, candlelight illuminating a well-stocked pantry shelf full of canned goods and dried herbs, an illustrated inventory log resting on a nearby stool, warm flickering golden light, forest green and terracotta palette, vintage nature-journal style, vertical 9:16.

---

## PILAR 8 — Half-Acre Master Layout (Complete Bundle, $150)
*Dolor ancla: "no sé cómo distribuir mi terreno sin desperdiciar espacio"*

### 8.1 — "Así se ve media acre bien aprovechada"
- **Dolor/deseo:** deseo de ver el resultado final posible
- **CTA visual:** master layout, vista aérea del modelo
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THIS IS WHAT A WELL-USED HALF ACRE LOOKS LIKE" · **Subtítulo:** *Every corner has a purpose.*
- **Prompt:** Watercolor and ink illustration, aerial bird's-eye view of a half-acre homestead layout — raised beds, small greenhouse, chicken coop, beehive, herb spiral, fruit trees arranged in an organized grid, warm golden afternoon light, forest green and terracotta palette with gold accents, vintage botanical map illustration style, vertical 9:16.

### 8.2 — "Cuarto de acre también alcanza (aquí el plano)"
- **Dolor/deseo:** ansiedad de "no tengo suficiente terreno"
- **CTA visual:** master layout, versión cuarto de acre
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "A QUARTER ACRE IS ENOUGH" · **Subtítulo:** *Here's the exact layout.*
- **Prompt (ANTES):** Watercolor and ink illustration, aerial view of a small empty quarter-acre suburban lot, plain grass, muted gray-green tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same aerial view transformed into an organized small-scale homestead layout with compact raised beds, a mini greenhouse, and a small coop, warm forest green and terracotta palette, golden light, watercolor and ink illustration style, vertical 9:16.

### 8.3 — "Por qué mi colmena mira hacia el este (y la tuya debería también)"
- **Dolor/deseo:** deseo de hacer las cosas técnicamente correctas
- **CTA visual:** master layout, ubicación de colmena
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHY MY BEEHIVE FACES EAST" · **Subtítulo:** *And yours probably should too.*
- **Prompt:** First-person POV, standing in a garden looking toward a small illustrated beehive facing the morning sun, soft golden-hour light, herb spiral visible nearby, watercolor and ink vintage nature-journal style, forest green and gold tones, vertical 9:16.

### 8.4 — "El error de poner el invernadero en el lugar equivocado"
- **Dolor/deseo:** miedo a cometer errores de diseño costosos
- **CTA visual:** master layout, orientación sur del invernadero
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "THE MISTAKE OF PLACING YOUR GREENHOUSE WRONG" · **Subtítulo:** *Orientation is everything.*
- **Prompt:** Watercolor and ink illustration, first-person POV standing before a small south-facing greenhouse glowing with warm interior light at dusk, garden beds and rain barrels visible nearby, forest green and terracotta palette, vintage botanical illustration style, vertical 9:16.

### 8.5 — "6 elementos que todo homestead necesita, en orden de prioridad"
- **Dolor/deseo:** abrumado por no saber qué construir primero
- **CTA visual:** master layout, leyenda numerada
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "6 THINGS EVERY HOMESTEAD NEEDS FIRST" · **Subtítulo:** *In the right order.*
- **Prompt:** Watercolor and ink illustration, close-up POV of a hand tracing a numbered legend on an illustrated homestead layout map, small icons for beds, coop, hive, greenhouse, compost, and herb spiral, warm desk light, forest green and gold accents, vintage nature-journal style, vertical 9:16.

### 8.6 — "De este patio vacío a este plano en una tarde"
- **Dolor/deseo:** deseo de rapidez y claridad en la planeación
- **CTA visual:** master layout, plantilla personalizable
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "FROM EMPTY YARD TO FULL LAYOUT IN ONE AFTERNOON" · **Subtítulo:** *The plan made it possible.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV of a blank grid sheet on a table, empty and intimidating, muted parchment tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV, the grid now filled in by hand with a colorful custom homestead layout, colored pencils scattered around, warm afternoon light, forest green and terracotta palette, watercolor and ink illustration style, vertical 9:16.

---

## PILAR 9 — First & Second Year Action Plan (Complete Bundle, $150)
*Dolor ancla: "quiero empezar pero no sé qué hacer en qué orden, me paralizo"*

### 9.1 — "Semana 1 de mi homestead: esto fue lo único que hice"
- **Dolor/deseo:** parálisis por análisis, necesidad de un primer paso simple
- **CTA visual:** action plan, semana 1 de enero
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WEEK ONE OF MY HOMESTEAD" · **Subtítulo:** *This was the only thing I did.*
- **Prompt:** First-person POV, hands holding an illustrated action plan checklist page for "Week 1," pencil checking off a small box, a rough hand-drawn property map beside it, winter light through a window, watercolor and ink vintage style, forest green and terracotta palette, vertical 9:16.

### 9.2 — "576 tareas para no perderme en mi primer año"
- **Dolor/deseo:** deseo de un mapa completo y confiable
- **CTA visual:** action plan, vista de página mensual completa
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "576 TASKS SO I NEVER GOT LOST" · **Subtítulo:** *A full year, mapped out.*
- **Prompt:** Watercolor and ink illustration, close-up POV flipping through an illustrated year-long action plan booklet with color-coded task categories, checkboxes, and small icons for garden, bees, and livestock, warm desk light, forest green and gold tones, vintage nature-journal style, vertical 9:16.

### 9.3 — "Lo que debí ordenar en enero y no lo hice"
- **Dolor/deseo:** miedo a llegar tarde a fechas críticas (pollos, abejas, semillas)
- **CTA visual:** action plan, notas de "order now"
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "WHAT I SHOULD HAVE ORDERED IN JANUARY" · **Subtítulo:** *And didn't.*
- **Prompt:** First-person POV, hands writing in an illustrated action plan notebook at a kitchen table, a seed catalog and calendar visible nearby, morning winter light, watercolor and ink vintage style, forest green and brown palette, vertical 9:16.

### 9.4 — "Año 1 caótico vs Año 2 con un plan"
- **Dolor/deseo:** deseo de dejar atrás el caos del primer intento
- **CTA visual:** action plan resolviendo el caos
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "CHAOTIC YEAR ONE VS PLANNED YEAR TWO" · **Subtítulo:** *Same land, different outcome.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV of a cluttered desk with scattered sticky notes and a stressed, disorganized garden sketch, muted gray tones, vertical 9:16.
- **Prompt (DESPUÉS):** Same desk now organized with a single open illustrated action plan booklet, neat handwriting, a cup of tea, warm golden light, forest green and terracotta palette, watercolor and ink style, vertical 9:16.

### 9.5 — "5 tareas de infraestructura que debes hacer antes de marzo"
- **Dolor/deseo:** urgencia estacional, miedo a quedarse atrás
- **CTA visual:** action plan, categoría infra/repair
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 INFRASTRUCTURE TASKS BEFORE MARCH" · **Subtítulo:** *Do these before the season starts.*
- **Prompt:** Watercolor and ink illustration, POV of hands holding a small illustrated checklist card with tool and infrastructure icons, a toolbox and lumber visible in soft background blur, cool late-winter light, forest green and gold tones, vintage nature-journal style, vertical 9:16.

### 9.6 — "Cómo se ve un plan de dos años bien hecho"
- **Dolor/deseo:** deseo de visión a largo plazo, no solo supervivencia
- **CTA visual:** action plan, vista general year 1 vs year 2
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT A WELL-MADE TWO-YEAR PLAN LOOKS LIKE" · **Subtítulo:** *Vision beyond just surviving.*
- **Prompt:** First-person POV, hands holding two illustrated action plan booklets side by side labeled Year One and Year Two, warm desk lamp light, watercolor and ink vintage nature-journal style, forest green and terracotta palette, vertical 9:16.

---

## PILAR 10 — Shopping & Sourcing Guide (Complete Bundle, $150)
*Dolor ancla: "no sé cuánto cuesta esto de verdad ni dónde comprarlo sin que me estafen"*

### 10.1 — "Cuánto me costó realmente mi primer año de homestead"
- **Dolor/deseo:** miedo al costo oculto / sorpresas financieras
- **CTA visual:** shopping guide, tabla de presupuesto año 1
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHAT MY FIRST HOMESTEAD YEAR REALLY COST" · **Subtítulo:** *The real numbers, no filter.*
- **Prompt:** First-person POV, hands holding an illustrated budget guide page with a price table and small icons for seeds, tools, and coop, a calculator and coffee cup nearby, warm morning light, watercolor and ink vintage style, forest green and gold palette, vertical 9:16.

### 10.2 — "5 cosas que debes comprar localmente antes que en línea"
- **Dolor/deseo:** deseo de ahorrar y apoyar comunidad local
- **CTA visual:** shopping guide, sección "buy local first"
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 THINGS TO BUY LOCAL BEFORE ONLINE" · **Subtítulo:** *Your community has what you need.*
- **Prompt:** Watercolor and ink illustration, POV walking through a small local farmers market stall with baskets of seedlings and jars, an illustrated supplier guide booklet held in one hand, warm daylight, forest green and terracotta palette, vintage nature-journal style, vertical 9:16.

### 10.3 — "El mes en que se agotan las semillas raras (y cómo no perdértelo)"
- **Dolor/deseo:** miedo a quedarse sin opciones / FOMO estacional
- **CTA visual:** shopping guide, calendario mensual de compras
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "THE MONTH RARE SEEDS SELL OUT" · **Subtítulo:** *Don't miss the window.*
- **Prompt:** First-person POV, hands circling a date on an illustrated monthly shopping calendar page with a red pencil, seed catalogs stacked nearby, warm indoor light, watercolor and ink vintage style, forest green and gold tones, vertical 9:16.

### 10.4 — "Gasté de más en mi gallinero por no comparar precios"
- **Dolor/deseo:** arrepentimiento financiero, deseo de evitar el mismo error
- **CTA visual:** shopping guide, rango de precios por categoría
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I OVERPAID FOR MY COOP" · **Subtítulo:** *Because I didn't compare prices.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV holding an expensive-looking receipt beside a plain coop, muted gray tones with a hint of red frustration accent, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV, an illustrated sourcing guide open on a table showing a lower price range, a modest but well-built coop in warm background light, forest green and terracotta palette, watercolor and ink style, vertical 9:16.

### 10.5 — "El presupuesto real para empezar (no el que ves en redes)"
- **Dolor/deseo:** desconfianza hacia contenido "aspiracional" poco realista
- **CTA visual:** shopping guide, rango bajo vs alto
- **Formato:** POV · **Medio:** Video
- **Título portada:** "THE REAL STARTING BUDGET" · **Subtítulo:** *Not the one you see on social media.*
- **Prompt:** First-person POV, hands holding an illustrated budget comparison chart showing a low-cost DIY range next to a premium range, warm desk light, watercolor and ink vintage nature-journal style, forest green and gold palette, vertical 9:16.

---

## PILAR 11 — Homestead Troubleshooting Field Guide (Complete Bundle, $150)
*Dolor ancla: "algo le pasa a mi planta/gallina y no sé qué ni cómo arreglarlo"*

### 11.1 — "Por qué mis tomates tienen esa mancha oscura"
- **Dolor/deseo:** frustración, sensación de estar perdiendo la cosecha
- **CTA visual:** troubleshooting guide, entrada de antracnosis
- **Formato:** POV · **Medio:** Video
- **Título portada:** "WHY MY TOMATOES HAVE THAT DARK SPOT" · **Subtítulo:** *One page told me exactly why.*
- **Prompt:** First-person POV, hand holding a tomato with a dark sunken spot close to the camera, an illustrated troubleshooting field guide page open on the ground nearby showing a matching symptom illustration, warm afternoon garden light, watercolor and ink vintage style, forest green and terracotta palette, vertical 9:16.

### 11.2 — "5 señales de que tu suelo está enfermo"
- **Dolor/deseo:** miedo a un problema invisible que arruina todo
- **CTA visual:** troubleshooting guide, sección salud del suelo
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 SIGNS YOUR SOIL IS SICK" · **Subtítulo:** *The problem you can't always see.*
- **Prompt:** Watercolor and ink illustration, close-up POV of hands holding a clump of gray, compacted soil next to an illustrated field guide page with soil diagnostic icons, overcast light, muted brown and forest green tones, vintage nature-journal style, vertical 9:16.

### 11.3 — "Encontré gusanos verdes gigantes en mis tomates"
- **Dolor/deseo:** asco/sorpresa, urgencia de resolver ya
- **CTA visual:** troubleshooting guide, entrada de gusano cachón
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "I FOUND GIANT GREEN WORMS ON MY TOMATOES" · **Subtítulo:** *Here's what they actually were.*
- **Prompt:** First-person POV, kneeling in a tomato patch, hand pointing at a large green hornworm camouflaged on a leaf, an illustrated field guide page visible tucked under one arm, warm late-afternoon light, watercolor and ink vintage style, forest green tones, vertical 9:16.

### 11.4 — "Diagnostiqué mis gallinas antes de que fuera tarde"
- **Dolor/deseo:** miedo a perder animales por no saber identificar señales
- **CTA visual:** troubleshooting guide, sección aves/gallinero
- **Formato:** POV · **Medio:** Video
- **Título portada:** "I DIAGNOSED MY HENS BEFORE IT WAS TOO LATE" · **Subtítulo:** *One page, caught in time.*
- **Prompt:** First-person POV, standing in a chicken coop, hand gently checking a hen while holding an illustrated field guide open to a diagnostic page, warm dusty golden light filtering through wood slats, watercolor and ink vintage nature-journal style, terracotta and brown palette, vertical 9:16.

### 11.5 — "Antes tiraba mis plantas sin saber qué les pasaba"
- **Dolor/deseo:** culpa retrospectiva, deseo de haber sabido antes
- **CTA visual:** troubleshooting guide resolviendo el problema
- **Formato:** Antes/Después · **Medio:** Carrusel
- **Título portada:** "I USED TO THROW AWAY PLANTS I DIDN'T UNDERSTAND" · **Subtítulo:** *Now I know exactly what to fix.*
- **Prompt (ANTES):** Watercolor and ink illustration, POV looking at a wilted yellow plant being pulled from a bed and discarded, muted gray-brown tones, somber light, vertical 9:16.
- **Prompt (DESPUÉS):** Same POV, a healthy green plant thriving in the same spot, an illustrated field guide open on the ground showing the exact fix that worked, warm golden light, forest green and terracotta palette, watercolor and ink illustration style, vertical 9:16.

### 11.6 — "131 problemas de homestead, todos con solución en una página"
- **Dolor/deseo:** deseo de sentirse preparado ante cualquier imprevisto
- **CTA visual:** troubleshooting guide, vista general del libro
- **Formato:** POV · **Medio:** Video
- **Título portada:** "131 HOMESTEAD PROBLEMS, ALL SOLVED IN ONE BOOK" · **Subtítulo:** *Whatever goes wrong, it's in here.*
- **Prompt:** First-person POV, hands holding a thick illustrated field guide book with a worn cover, flipping rapidly through pages full of small diagnostic illustrations, warm barn light, watercolor and ink vintage nature-journal style, forest green and gold palette, vertical 9:16.

### 11.7 — "Mi compost olía mal hasta que encontré la razón"
- **Dolor/deseo:** vergüenza doméstica, frustración con lo básico que "debería funcionar solo"
- **CTA visual:** troubleshooting guide, sección infraestructura
- **Formato:** Storytime · **Medio:** Video
- **Título portada:** "MY COMPOST SMELLED BAD UNTIL I FOUND OUT WHY" · **Subtítulo:** *One fix, no more smell.*
- **Prompt:** First-person POV, standing over a compost bin holding a pitchfork, an illustrated field guide page visible resting on the bin's edge, steam rising faintly from the pile, warm late-afternoon light, watercolor and ink vintage style, brown and forest green palette, vertical 9:16.

### 11.8 — "5 plagas que arruinan tu huerto en verano (y cómo pararlas)"
- **Dolor/deseo:** ansiedad estacional, miedo a perder toda la cosecha de verano
- **CTA visual:** troubleshooting guide, sección pests & insects
- **Formato:** Countdown · **Medio:** Carrusel
- **Título portada:** "5 PESTS THAT RUIN YOUR SUMMER GARDEN" · **Subtítulo:** *And how to stop them.*
- **Prompt:** Watercolor and ink illustration, close-up POV of a hand inspecting the underside of a leaf covered in small aphids, an illustrated field guide page with pest icons visible in soft focus nearby, bright summer light, forest green and gold tones, vintage nature-journal style, vertical 9:16.

---

## Checklist de producción rápida

1. Imagen de portada: marco 1:1 con madera envejecida, bloque completo entre y=240 y y=1600, título Source Serif Pro + subtítulo Lora
2. Imágenes de escena: 1080×1920 exacto para clips animados, o 1:1 si van dentro del marco de portada
3. Sin texto no intencional en la imagen (salvo gpt-image-2 a propósito)
4. Personaje narrador SIEMPRE en POV — nunca rostro frontal; familiares secundarios permitidos de cuerpo/rostro completo
5. Diversidad de piel/etnia rotada entre temas del catálogo — nunca por defecto blanco/rubio
6. Countdown/Antes-Después → Carrusel por defecto (sin gasto de animación); POV/Storytime → Video
7. Prompt de animación (cuando aplique): una sola micro-acción, cámara sutil ("barely drifting"), línea obligatoria "no distortion / no extra fingers / no facial warping", línea "preserve the watercolor and ink illustration texture"
8. Confirmar costo cotizado por el skill `/generate` antes de aprobar animación
9. Cuenta social "calentada" (actividad manual diaria) antes de conectar Blotato en automático

---

**Resumen numérico:** 60 temas · 11 pilares · 30 POV / 10 Antes-Después / 10 Countdown / 10 Storytime · ~30 Video / ~30 Carrusel · Costo estimado de generación de video (solo la porción en Video, sin descartes): ~$22–24 USD a $0.75–0.80/clip. La porción en Carrusel no requiere gasto de animación.
