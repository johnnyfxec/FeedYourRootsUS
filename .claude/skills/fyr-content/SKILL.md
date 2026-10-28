---
name: fyr-content
description: Motor de producción de contenido FYR. Genera briefs de carrusel/video desde el banco de temas (Malla semilla de 61 + temas nuevos extraídos de los PDFs; Airtable registra los que se producen), aplicando el Sistema CRS (fases de embudo, 20 hooks verbales, loops abiertos) y la voz del Brand Bible. Output triple — brief .md legible, config JSON de pieza (carrusel: assemble.py; video: pipeline de video), registro en Airtable. Usar cuando el usuario pida "genera el siguiente", "dame el brief del tema X.Y", "produce N piezas" o "kit de afiliado para [creador]".
---

# FYR Content Engine

## Principio rector

Cada pieza existe para vender desde la autoridad. El hook no es el intro: es la razón por la que alguien deja de scrollear. La respuesta va al final, siempre. Ninguna pieza se escribe sin pasar el Question Test primero.

---

## 1. Infraestructura (IDs verificados — NO adivinar, NO reconstruir de nombres)

**Base Airtable:** `appMy5aOwifSbBLPR` (Feed Your Roots US Data Sheets)

### Tabla `Themes` — `tblRggZtw1E38ZQJs`
**Rediseño 28-oct-2026 (Route B):** `Themes` guarda solo la definición del tema, no la ejecución de ninguna pieza concreta. Se eliminaron los campos que eran de ejecución (Formato, Medio, Título Portada, Subtítulo, Prompt Imagen, Fase Embudo, Fecha de uso, Fecha de Publicación, los 5 `Link Publicación X`), el campo `Estado` (Pendiente/Usado, eliminado — era redundante con el link `Content_Pieces`, ver abajo) y el campo `Performance` de `Themes` (distinto del `Performance` de `Content_Pieces`, que sí existe); todos migraron o quedan cubiertos en `Content_Pieces`, o se responden cruzando `Content_Pieces.Performance`/`Tema Relacionado`. Detalle completo en `knowledge/FYR_Rutas_De_Produccion.md` §0.8, "Corrección 2".

**Corrección 27-oct-2026 — `Bundle Relacionado` y los 2 campos `Señales` faltaban en esta tabla por error propio** (verificado contra `get_table_schema` en vivo tras una pregunta de Johnny sobre si la documentación arrastraba huecos): estos 3 campos SÍ existen en `Themes` hoy, Route B nunca los tocó — se habían omitido de esta lista sin que ningún gate lo detectara (`check_field_coverage.py` no valida este archivo). `Bundle Relacionado` (`Themes`, singleSelect) y `CTA Sugerido` (`Content_Pieces`, texto libre) son dos campos reales y DISTINTOS que coexisten — uno no es el nombre viejo del otro.

| Campo | fieldId | Tipo |
|---|---|---|
| Número (primary) | `fld6BnujxYXzxfmOb` | number (ej. 1.1, 11.8) |
| Pilar | `fldBPnwVI3SuxXa7m` | singleSelect |
| Dolor/Deseo | `fldfdZoX3D1oIlakE` | multilineText |
| Bundle Relacionado | `fldT0UBdIsexJIT4i` | singleSelect (Starter/Family/Core/Homestead/Homestead Complete) — **Corrección 28-oct-2026 (consenso con Johnny): campo opcional/condicional, no obligatorio.** No todo tema debe estar ligado a un bundle específico. Se llena SOLO si el Pilar tiene un mapeo obvio a un bundle (ver guía en `FYR_Rutas_De_Produccion.md` §0.8); si no hay mapeo claro, queda vacío a propósito — vacío no es un hueco ni un error. Si se llena, es al crear el tema; no se reescribe después salvo corrección explícita. Distinto de `Content_Pieces.CTA Sugerido` (texto libre, por pieza) |
| Prioridad | `fld9t1dYpz4AfB1vJ` | singleSelect |
| Hook Asignado | `fldZwv8371fG270a7` | singleSelect ("01 Negativo"…"20 Revelación") — propuesta inicial para el tema; lo que de verdad se usó en cada pieza va en `Content_Pieces.Hook Usado` |
| Content_Pieces | `fldTOvVnXFjnT0SLk` | link inverso (múltiple) — **fuente de verdad de si el tema ya se produjo**: vacío = disponible; 1+ piezas vinculadas = ya trabajado. Reemplaza al antiguo campo `Estado` |
| Señales (Pilar Relacionado) | `fld9G0l383qnrch4J` | link inverso a `Trend_Signals.Pilar_Relacionado` — vacío en todo tema que no nació de una señal de `trend-scout` (normal, no es un hueco) |
| Señales (Tema Vinculado) | `fldIKJfDK1T3kECpv` | link inverso a `Trend_Signals.Tema_Vinculado` — misma nota que arriba |

### Tabla `Content_Pieces` — `tblevmNSbGTzdjuDF`
| Campo | fieldId | Tipo |
|---|---|---|
| ID Pieza (primary) | `fld1g5OjdT2BlFdmr` | texto (formato `PZA_[tema]`, ej. `PZA_3.1` — mismo identificador que la carpeta de Drive) |
| Tipo de Pieza | `fld7zgQouWTYgQdJ3` | singleSelect (Carrusel/Video) |
| Fecha de Generación | `fldqWpBbCOSaD2gE7` | date |
| Número de Slides | `fldu0xeW00aYT29So` | number |
| Duración | `fldmv5v2wcnu0zxZ3` | number (segundos, solo video) |
| Copy Completo | `fldYXJcdumHdu9du6` | multilineText |
| Ruta .md | `fldSvPv8f3z58iUQS` | texto |
| Estado Producción | `fldqEyriByKYZ0t3n` | singleSelect (Brief Generado → Assets en Drive → Ensamblado → Publicado; verificadas en vivo 10-oct-2026) |
| Performance | `fldGxHIuckHi9yp4P` | singleSelect (Alto/Medio/Bajo/Sin datos) |
| Tema Relacionado | `fldgHOLLy8s3tr3Dh` | link → Themes (single) |
| Assets Usados | `fldT4ifnqw6Fz8a3v` | link → Assets (múltiple) |
| Audiencia | `fldXC1j4yq3ITULYz` | singleSelect (Propia/Afiliado) |
| Hook Usado | `fldmaZNxsUpRxBGmC` | singleSelect, nombre completo ("01 Negativo"…"20 Revelación", igual que `Hook Asignado`); las opciones sueltas "04", "07", "17" son restos, no usar |
| Carpeta Drive | `fldpu7xim0PtA1tJS` | url (subcarpeta de fecha en `Content_Pieces`) |
| Plataformas Destino | `fldoL0WzNyw2X8xHx` | multipleSelects (Instagram/Facebook/Pinterest/YouTube/TikTok; añadido 27-oct-2026 para `fyr-publisher`) |
| Estado IG | `flddWeWxcaWk0t3x2` | singleSelect (No aplica/Pendiente/Publicado/Fallido; añadido 27-oct-2026) |
| Estado FB | `fldS2HHRyr6UpdzSr` | singleSelect (mismas opciones que Estado IG; añadido 27-oct-2026) |
| Estado Pinterest | `fldzqxnaZ6DrurRHh` | singleSelect (mismas opciones; añadido 27-oct-2026) |
| Estado YouTube | `fldgZJ6eZ05oxPe7H` | singleSelect (mismas opciones; añadido 27-oct-2026) |
| Estado TikTok | `fldOM7Y83b4QAWTS7` | singleSelect (mismas opciones; añadido 27-oct-2026) |
| Post ID IG | `fld9MaAJxssTiUT7p` | texto (ID del media/post publicado, para auditar o borrar después; añadido 27-oct-2026) |
| Post ID FB | `fldA6Naoeg9je6uZb` | texto (añadido 27-oct-2026) |
| Post ID Pinterest | `fldMCih6SCcaadTKU` | texto (añadido 27-oct-2026) |
| Post ID YouTube | `fld0pgXfKXLhiUdj8` | texto (añadido 27-oct-2026) |
| Post ID TikTok | `fldublvHckaVEsYNs` | texto (añadido 27-oct-2026) |
| Fecha Publicación Programada | `fldrMl8gQKUBa7j1T` | date (fecha en que `fyr-publisher` debe publicar la pieza — distinta de `Fecha de Generación`, que es cuando se generó el brief; añadido 27-oct-2026) |
| Formato | `fldQvG5T4NkambfVK` | singleSelect (Countdown/Antes-Después/POV/Storytime; añadido 28-oct-2026, migrado desde `Themes`) |
| Título Portada | `fldR5k4mI7UWDrDsY` | multilineText (añadido 28-oct-2026, migrado desde `Themes`) |
| Subtítulo | `fld1iK04YprHgEU6A` | multilineText (añadido 28-oct-2026, migrado desde `Themes`) |
| Prompt Imagen | `fldE9R35NZzVTrP58` | multilineText (añadido 28-oct-2026, migrado desde `Themes`) |
| CTA Sugerido | `fldkxIDePMy7FxI3y` | multilineText (añadido 28-oct-2026, migrado desde `Themes`) |
| Fase Embudo | `fldVTuJvItUgc2LYK` | singleSelect (F1-F4; añadido 28-oct-2026, migrado desde `Themes`) |
| Fecha de Publicación | `fldzLDKI8biRw0uHZ` | dateTime (añadido 28-oct-2026, migrado desde `Themes`) |
| Link Publicación IG | `fldu6AfhLCgiP7fJS` | url (añadido 28-oct-2026, migrado desde `Themes`) |
| Link Publicación Pinterest | `fldbRm70Tldl2uUDq` | url (añadido 28-oct-2026, migrado desde `Themes`) |
| Link Publicación FB | `fldwjD1AKiJYW9mM0` | url (añadido 28-oct-2026, migrado desde `Themes`) |
| Link Publicación YouTube | `fldTGJPY0YBEGrE9U` | url (añadido 28-oct-2026, migrado desde `Themes`) |
| Link Publicación TikTok | `fldsTZkJA9jW8mb8W` | url (añadido 28-oct-2026, migrado desde `Themes`) |

**Nota de rediseño (28-oct-2026):** los 11 campos marcados "migrado desde `Themes`" son el resultado de mover a `Content_Pieces` todo lo que describe la ejecución concreta de una pieza, en vez de la definición general del tema (que se quedó en `Themes`, ver tabla arriba). Antes, cuando se producía una segunda pieza del mismo tema, estos valores se sobrescribían en `Themes` sin dejar registro de la primera pieza — ver `knowledge/FYR_Rutas_De_Produccion.md` §0.8 "Corrección 2" para el análisis completo (el documento de análisis previo a esta migración vivió temporalmente en el Proyecto de claude.ai y se borró el 27-oct-2026 tras cumplir su función, ya no existe en ningún lado). `Medio` no se migró como campo separado: ya existe `Tipo de Pieza` (Carrusel/Video) cumpliendo la misma función.

**Nota de solape con `fyr-publisher` (27-oct-2026, sigue vigente):** los `Post ID X` son el ID crudo de la plataforma (lo que devuelve la API al publicar, para borrar o verificar status), distinto de `Link Publicación X` (el link público legible). Ambos viven ahora en `Content_Pieces`.

### Tabla `Assets` — `tblkzOtjS4KK5B2Xn`
Campos clave: `Nombre de archivo` (`fldX3gsT4b6dkzIvg`), `Link Drive` (`fldMWMX97UDujzVgB`), `Tags` (`fldvq3RMSkUIR1Od4`), `Reutilizable en` (`fldxD7IhRHFI7f2XJ`). ~240 registros con link Drive verificado.

**Regla de propiedad de Airtable:** Claude hace TODAS las escrituras (crear, actualizar, borrar registros y campos) en el paso que corresponde de cada skill; Johnny no edita Airtable a mano.

**Campos de video en `Content_Pieces`:** `Ruta JSON` (`flduZXIO9iQ89U6Kt`, texto) ya existe; `ID de variante` (`fldnCOYKQf6SscuMz`, texto; formato `voz|subtítulo|cierre`, ej. `Neural2-J|B-e14|cierreB`) también existe (ver `knowledge/FYR_Protocolo_Edicion_Video.md` Secciones 8 y 10).

**Regla:** para singleSelect/multipleSelects escribir el nombre de la opción como string y usar `typecast: true` cuando la opción pueda no existir aún (crea la opción automáticamente).

---

## 2. Fuentes de conocimiento (leer, no duplicar)

Rutas relativas a la raíz del repo (`~/FeedYourRootsUS`). Si un archivo no existe → **fallar con mensaje claro** indicando qué archivo copiar a `knowledge/`, nunca inventar su contenido.

| Archivo | Uso |
|---|---|
| `knowledge/FYR_Malla_60_Temas_Virales_v2.md` | Banco semilla de 61 temas (no está cargado en Airtable; un tema entra a `Themes` al producirse). Marcar aquí el estado de un tema NO es necesario: manda `Themes` |
| `knowledge/Sistema_Maestro_CRS_v2.md` | **Solo Partes 1–6** (Estrategia/fases de embudo, Selección de hook, Arquitectura/Question Test/loops, Ejecución, Distribución, Optimización) — es la base de conocimiento personal de Johnny para su otro negocio (trading/JIFU), compartida aquí solo por la ciencia que contiene. **Nunca usar la Parte 8** ("Temas por Fase", banco de 30 temas en trading sin traducir — usar la Malla de FYR en su lugar) **ni la Parte 9** ("Sistema de DMs": flujos de prospección e inscripción de JIFU, cero aplicación a FYR, que no vende por DM uno a uno) |
| `knowledge/hooks_verbales_20_v2.md` | Los 20 hooks: principio psicológico, estructura, reglas de uso. Es un documento compartido con otro negocio de Johnny — sus "5 ejemplos" por hook están en el avatar de trading, no se traducen aquí |
| `knowledge/FYR_Cierres_CTA_v1.md` | Las 3 familias de cierre (Venta / Engagement / Loop-retención) y el mapeo obligatorio Fase Embudo → tipo de cierre — leer SIEMPRE antes de escribir el último slide (Paso 3), reemplaza la gradación "CTA siempre de venta, solo cambia la intensidad" |
| `.claude/skills/fyr-content/references/hooks_ejemplos_morgan.md` | 2 ejemplos ya traducidos al avatar Morgan por cada uno de los 20 hooks — leer junto con el de arriba al construir un hook (Paso 2), para no traducir de memoria ni arriesgar que se filtre vocabulario del dominio equivocado |
| `knowledge/Feed-Your-Roots-Brand-Bible.md` | Voz, paleta, tipografía, banned words, regla de diversidad, excepcion de rostros en escenas narrativas (v2) |
| `knowledge/FYR_Asset_Governance_Policy.md` (v2.3+) | Nomenclatura, ubicación de archivos, estructura `Content_Pieces/PZA_[tema]/[fecha]/`, estructura `01_Brand_Assets/C01-C13` (incluye C12_Frames y C13_Layout_Elements), y principio de duplicados semánticos en Themes |
| `knowledge/reference_assets/FYR_Layout_Specs_v1.md` | Medidas exactas (bbox, ventanas de contenido) de los layouts vigentes en 4:5 y 9:16, con ruta de Drive de cada asset — consultar SIEMPRE antes de generar un prompt de imagen que use un layout con marco/asset fijo |
| `knowledge/FYR_Brand_Mark_Spec_v1.md` | Simbolo oficial de marca (frasco+arbol): espacio de proteccion, tamano minimo, variantes de color, lockups aprobados, usos prohibidos, proporcion fija 1:1.405 — consultar SIEMPRE antes de usar/reproducir el simbolo o el wordmark en cualquier pieza |
| `knowledge/FYR_Motor_Ensamblado_Arquitectura_v1.md` | Contrato de `assemble.py` (carruseles/slides estáticos): tipos de layout, tipografía, schema del config JSON — leer antes de escribir el config de un carrusel |
| `knowledge/FYR_Protocolo_Edicion_Video.md` | Pipeline de video (voz TTS, subtítulos palabra por palabra, pausas, cierre en loop A/B, contrato del JSON de pieza, procedimiento de render en Actions) — leer SIEMPRE cuando `Medio = Video`, antes del Paso 3 |
| `knowledge/FYR_Rutas_De_Produccion.md` | **Paso a paso de cada formato** (Ruta A carrusel, Ruta B video): quién actúa, qué se escribe en Airtable en cada etapa, destinos de cada imagen, reglas de memoria de uso. Es la guía de ejecución del Paso 5 — leer SIEMPRE antes de abrir una pieza |
| `knowledge/FYR_Plan_Reutilizacion_y_Serie_Botanica.md` | Inventario del banco de assets, informe de cobertura Malla vs banco, serie "Conoce la planta" y orden de ejecución — consultar al elegir tema y al buscar assets (Paso 4): primero el banco |
| `knowledge/FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` | Arquitectura del sistema completo de 3 skills (trend-scout, fyr-content, performance-lens), como se comunican vía Airtable, y el schema real de `Trend_Signals` — leer antes de tocar cualquier logica relacionada a tendencias o performance |

**Adaptación obligatoria del CRS:** el sistema fue escrito para el avatar de trading/libertad financiera. Al aplicarlo, traducir SIEMPRE al avatar Morgan (28-42, patio suburbano, busca soberanía alimentaria): el dolor no es "depender de un sueldo", es "depender del supermercado / no saber qué come su familia / sentir que la autosuficiencia es para gente con 5 acres". La ciencia (loops, fases, hooks) se conserva; el contenido se traduce. Para el hook específico del Paso 2, usar `references/hooks_ejemplos_morgan.md` (2 ejemplos ya traducidos por hook) en vez de traducir los ejemplos de trading de `hooks_verbales_20_v2.md` de memoria en cada sesión.

---

## 3. Banco de temas y alta de temas

**Dos lugares, dos funciones (no confundirlos):**
- **Banco de temas** = la Malla (`knowledge/FYR_Malla_60_Temas_Virales_v2.md`, 61 temas semilla `X.Y`) + los temas nuevos que se extraigan de los PDFs. Es donde se *elige* qué producir. NO está cargado en Airtable y no se carga en bloque.
- **Tabla `Themes`** = solo los temas que ya se han producido (o están en producción). Guarda únicamente la definición del tema (Número, Pilar, Dolor/Deseo, Prioridad, Hook Asignado) — desde 28-oct-2026 ya no guarda estado de uso, fechas ni datos de ninguna pieza concreta; eso vive en `Content_Pieces` (ver Paso 5.6 y Paso 5 sub-paso 4). Un tema entra a `Themes` en el momento de producirlo (Paso 5.6), nunca antes.

**Temas nuevos desde los PDFs (la fuente de contenido es ilimitada).** Cada parte de un recurso (sección, tabla, lista, error común, caso del PDF) puede convertirse en un tema que impulse recordación o ventas:
1. Leer el PDF del pilar en el Proyecto (los 10 recursos de la carpeta de producto; el Core Bundle y los demás bundles están en la lista de archivos del Proyecto) y elegir un fragmento concreto: una cifra, un error, una tabla, un procedimiento.
2. Convertirlo en tema con la misma estructura de la Malla: Dolor/deseo (traducido al avatar Morgan), CTA visual (el recurso), Formato, Medio, Título de portada + Subtítulo, Prompt de imagen.
3. **Numeración:** el tema pertenece al pilar del PDF y toma el siguiente número libre de ese pilar, mirando AMBOS lugares (la Malla y `Themes`). Ejemplo: P4 llega hasta 4.5 en la Malla, el tema nuevo es 4.6. Nunca reutilizar un número.
4. **Duplicado semántico:** antes de crearlo, comparar su dolor/deseo contra los temas de la Malla del mismo pilar y contra `Themes`; si ya está cubierto en otras palabras, usar el existente.
5. Asignar **Fase Embudo** (dolor sin mencionar el producto → F1; mostrar alternativa → F2; destruir objeción → F3; resultado/demostración del recurso → F4; verificar que la mezcla mensual se acerque a 40/27/20/13) y **Hook Asignado** (Fase + Formato con la tabla de compatibilidad del CRS, Parte 2; el hook Mito (11) es el de mayor conversión para creencias arraigadas como "autosuficiencia = mucho terreno y dinero").
6. Mostrar el tema nuevo al usuario y esperar su OK antes de continuar al Paso 1.

**Alta en `Themes` (Paso 5.6):** si el tema no existe en `Themes`, crearlo SOLO con sus campos propios (Número, Pilar, Dolor/Deseo, Prioridad, Hook Asignado) y `typecast: true`. **`Bundle Relacionado` se incluye en esta escritura SOLO si el Pilar tiene un mapeo obvio a un bundle** (ver guía en `FYR_Rutas_De_Produccion.md` §0.8) — si no hay mapeo claro, se omite y queda vacío a propósito (no todo tema debe estar ligado a un bundle específico; corrección 28-oct-2026, consenso con Johnny). **Si ya existe, no se toca** — desde 28-oct-2026, `Themes` nunca se actualiza con datos de una pieza concreta (Formato, Medio, Título Portada, Subtítulo, Prompt Imagen, Fase Embudo, CTA Sugerido, Plataforma viven en `Content_Pieces`, ver Paso 5 sub-paso 4). Verificar antes de crear que el Número no exista ya (fail loudly si hay duplicado). Ver `FYR_Rutas_De_Produccion.md` §0.8 "Corrección 2" para el porqué de este rediseño.

## 4. Flujo de producción por pieza

### Paso 0 — Selección de tema
**Chequeo previo, siempre primero (opcional, nunca bloqueante):** consultar `Trend_Signals` (tabla `tblxdaRsgEy8CHvV9`) filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`. Si hay resultados, ofrecer al usuario producir la pieza montada sobre esa señal — usando su `Hook_CRS_Equivalente`, `Formato_Sugerido` y `Brief_Adaptacion` como punto de partida del Paso 1 en vez de partir de cero. Si el usuario acepta, al completar el Paso 5 escribir el `PZA_[tema]` resultante de vuelta en `Content_Piece_Generada` de esa fila. Si no hay señales aprobadas vigentes, o el usuario declina, continuar normal con los 3 caminos de siempre:
- Usuario pide tema específico (`X.Y`) → buscar primero en `Themes`; si no está, tomarlo de la Malla (banco semilla) tal cual. Si el número no existe en ninguno de los dos, decirlo y detenerse. Nunca seleccionar un tema que ya tiene al menos una `Content_Pieces` vinculada (ver `Themes.Content_Pieces`) sin confirmación explícita.
- Usuario pide "el siguiente" → elegir del banco (Malla + temas nuevos) los temas que NO tengan ninguna `Content_Pieces` vinculada en `Themes.Content_Pieces` (desde 28-oct-2026 ya no existe el campo `Estado`; el link a `Content_Pieces` es la fuente de verdad de si un tema ya se produjo). **Cola de arranque** (primeras 8 piezas): selección deliberadamente diversa, un pilar distinto cada vez y cubriendo las 4 fases, para tener señal real de qué convierte antes de escalar. Después de 8 piezas: priorizar por performance de lo ya publicado (`Content_Pieces.Performance`) y por la mezcla de fases del mes cerca de 40/27/20/13.
- Usuario pide un tema nuevo "desde el PDF de [pilar]" o describe un ángulo libremente, SIN número → **búsqueda semántica obligatoria, siempre, sin excepción**: comparar su dolor/deseo contra los temas de la Malla del mismo pilar y contra `Dolor/Deseo` + `Título Portada` de todo `Themes`, evaluando conceptualmente (no por texto exacto). Coincidencia real → usar el existente y avisar cuál y por qué. Sin coincidencia → crear el tema nuevo siguiendo la Sección 3 (numeración, Fase, Hook) y esperar el OK del usuario antes de continuar.
- El estado de un tema lo decide el link `Themes.Content_Pieces`, no la Malla: un tema de la Malla que no está en `Themes`, o que está sin ninguna pieza vinculada, está disponible.
- **Cobertura del banco (regla de reutilización, 11-oct-2026):** al proponer o confirmar un tema, calcular cuántos de sus slides pueden salir de escenas ya existentes en `Assets` (libres, sin `En descanso`) y decirlo. Si dos temas empatan, preferir el de mayor cobertura. Camino alterno, "desde el banco": si el usuario lo pide o el banco tiene escenas sin usar, partir de los assets con `Veces usado` bajo y proponer temas de la Malla (o nuevos desde los PDFs) que los aprovechen. El inventario y el informe de cobertura viven en `knowledge/FYR_Plan_Reutilizacion_y_Serie_Botanica.md`.

### Paso 1 — Question Test (bloqueante)
Completar: *"Cuando Morgan vea los primeros 3 segundos, la pregunta exacta en su cabeza será: ______"*. Si no sale una pregunta específica, el hook no está listo — iterar antes de escribir nada más.

### Paso 2 — Construcción del hook
- Leer la ficha del hook asignado en la guía de 20 (principio, estructura, regla de uso). Se permite cambiar de hook si el Question Test lo exige — registrar el cambio en `Hook Usado`.
- Fórmula de contexto: [contexto que ubica a Morgan] + [elemento que desafía/sorprende dentro de ese contexto].
- Alineación visual-verbal: el asset/imagen del slide 1 NUNCA debe resolver el loop que abre el texto.

**Afinidad Hook -> Layout de apertura del cuerpo (slide 2):** al elegir el layout del primer slide del cuerpo, usar esta afinidad natural en vez de un criterio generico. Layouts vigentes (poda del 11-oct-2026): de cuerpo, Marco grande, Doble marco superpuesto, Full-bleed solo imagen, Ventana+texto, Solo texto, Texto + imagen lateral; ademas, las portadas (4:5 `marco_grande_portada`, 9:16 `marco_grande_cuadrado`) y el Lockup de cierre. Assets, ventanas y la proporcion de imagen a pedir a Gemini en knowledge/reference_assets/FYR_Layout_Specs_v1.md. IMPORTANTE (correccion 13-sep-2026): Full-bleed NUNCA lleva texto -- si el hook necesita mensaje verbal sobre la imagen, usar Ventana+texto, no Full-bleed. El texto bajo un Marco grande o Doble marco va en el campo `texto_pie` (estilo subtitulo); el titulo dorado es solo de portadas.
- 03 Numerico, 13 Lista -> Solo texto
- 07 Contraste/Versus -> Doble marco superpuesto (preferido, un solo slide) o Marco grande dos veces (si el anterior no calza)
- 04 Storytelling, 10 Dolor/Frustracion -> Ventana+texto (inmersion emocional con mensaje)
- 06 Secreto, 20 Revelacion, 12 Curiosidad -> Texto + imagen lateral
- 11 Mito, 05 Error Comun -> Solo texto
- 17 Resultados/Transformacion, 19 Demostracion -> Marco grande (necesita evidencia visual clara)
- 01 Negativo, 14 Advertencia, 09 Prediccion -> Ventana+texto
- 02 Pregunta, 08 Autoridad, 15 Oportunidad, 16 Desafio, 18 Sorpresa -> libre segun el tema especifico, sin afinidad estructural fuerte

**Regla de variedad ampliada:** con 6 layouts de cuerpo disponibles, ningun layout se repite mas de 2 veces en la misma pieza (antes era 'nunca consecutivo'; ahora ademas se limita la repeticion total).

**Proporcion imagen/texto por funcion del slide** (aplica sin importar cual de los layouts se use): Apertura de loop (hook fuerte) = 85-90% imagen / 10-15% texto. Desarrollo/agitacion = 60-75% imagen / 25-40% texto. Giro/revelacion = 50-65% imagen / 35-50% texto. Cierre/CTA = 70-85% imagen / 15-30% texto. Esta proporcion se declara como campo `% imagen` en la tabla slide-por-slide del brief (Paso 5).

### Paso 3 — Cuerpo (numero de slides segun Fase Embudo, cadena de loops)
- **Numero de slides por Fase** (reemplaza el rango generico anterior): F1 Baja conciencia = 4-5 slides (incomodar es rapido, alargar diluye el golpe); F2 Media conciencia = 5-6 (necesita espacio para mostrar la alternativa sin apurar); F3 Alta conciencia = 6-7 (destruir objecion requiere mas desarrollo argumental, es la fase mas larga); F4 Autoridad = 4-5 (el resultado habla solo, exceso de slides diluye el impacto).
- **Regla de longitud real (27-oct-2026 — corrige el patrón de caer siempre al mínimo del rango):** el rango por Fase es un límite, no un objetivo — la decisión de cuántos slides usar depende de cuánto material de Valor real (ver regla de valor real arriba) tiene el tema, nunca de tomar el número más bajo por default. Antes de fijar el número de slides: listar cuántos puntos de Valor distintos puede dar el tema (mecanismos, criterios, pasos, datos que Morgan no tenía). Si hay 4+ puntos de valor reales y el rango de la Fase lo permite, usar el extremo alto del rango — un tema que da para más no se debe comprimir a 5 slides solo por costumbre. Si el tema genuinamente solo da para 2-3 puntos de valor, usar el extremo bajo en vez de rellenar con Agitación repetida para llegar al número. La longitud sigue al contenido, no al revés.
- Slide 1: hook (loop 1 abierto). Slides intermedios: agitación y valor en pedazos, abrir loop nuevo antes de cerrar el anterior.
- **Regla de valor real (27-oct-2026 — corrige el patrón "lista de síntomas sin explicar nada"):** agitación y valor NO son intercambiables. Agitación = nombrar o enumerar el problema/síntoma sin explicar por qué pasa ni qué hacer. Valor = explicar el mecanismo (por qué pasa), dar el dato/criterio que la persona no tenía, o mostrar la acción correcta — algo que Morgan se lleva aunque nunca compre nada. **Mínimo por pieza: al menos la mitad de los slides intermedios (redondeando hacia arriba) deben ser Valor, no solo Agitación.** Ejemplo del error real encontrado en auditoría (PZA_11.2, "5 SIGNS YOUR SOIL IS SICK"): los 3 slides intermedios solo listan síntomas ("agua se queda estancada", "huele a huevo podrido") sin decir una sola vez por qué eso indica suelo compactado/sin oxígeno ni qué hacer al respecto — los 3 son Agitación, 0 son Valor. Antes de cerrar el brief del Paso 5, marcar cada slide intermedio como `[Agitación]` o `[Valor]` en la tabla slide-por-slide; si no se cumple el mínimo, reescribir antes de continuar.
- **Ultimo slide (cierre, sin plantilla fija):** cierre de todos los loops + UN cierre único, cuyo tipo (no solo su intensidad) se decide por Fase Embudo siguiendo `knowledge/FYR_Cierres_CTA_v1.md` — leer ese documento completo antes de escribir el cierre, siempre, no solo la primera vez. Resumen (el documento tiene el detalle, los principios psicológicos y los ejemplos completos; no reconstruir de memoria):
  - **F1 → Cierre B (Engagement):** invita a comentar/compartir su propia experiencia, relatable y no competitivo ("seguro no soy el único", nunca "cuéntame cuál fue el peor"). Cero mención de Bundle. Es el default — no la excepción.
  - **F2 → mitad B, mitad A suave:** puede nombrar el recurso sin presión de urgencia (p. ej. "Shopping & Sourcing Guide, real price ranges included") o puede ser puramente de engagement — decidir según si el tema ya resolvió una objeción concreta.
  - **F3 → Cierre A (Venta directa):** nombra el recurso que resuelve la objeción que la pieza acaba de destruir — el `CTA Sugerido` de la pieza si el brief especificó uno más preciso que el canónico, o el `Bundle Relacionado` del tema si no. Puede combinarse con una pregunta de engagement si el tema se presta.
  - **F4 → Cierre A (venta de resultado) o C (loop/retención):** invita a replicar el resultado, con o sin venta explícita.
  - El campo `CTA Sugerido` de la pieza (el recurso/bundle que resuelve la objeción del tema) es la OPCIÓN de venta disponible para cierres A — no una instrucción de usarla siempre. En piezas F1 no se consulta para el cierre.
  El layout del cierre se elige libremente entre los layouts de cuerpo vigentes (ver Paso 2) segun que sirva mejor a esa resolucion especifica — nunca un layout de marca fijo tipo catalogo.
- **Regla de loop visual (obligatoria en el cierre):** el prompt de imagen del slide de cierre debe citar textualmente un elemento especifico del prompt de portada (objeto, color dominante, o composicion) e instruir que se repita transformado — mismo objeto, estado distinto. Esto invita a redeslizar desde el inicio, aumentando el watch-time/replay. Ejemplo: portada = "caja de zapatos desordenada"; cierre = "la misma caja, ahora organizada y cerrada con lazo".
- Decidir por slide si lleva asset de fondo o solo texto sobre fondo de marca (Parchment #F5ECD7): el criterio es si la imagen añade tensión/credibilidad al loop. Nunca imagen decorativa por rellenar.
- **Gate de presupuesto de texto (27-oct-2026 — bloqueante, solo carrusel):** la regla de valor real arriba empuja a escribir más por slide (mecanismo + síntoma, no solo síntoma); eso solo es seguro si el layout asignado a ese slide tiene espacio real para ello. Antes de cerrar el brief, para CADA slide con texto, verificar su layout contra `FYR_Layout_Specs_v1.md`:
  - `Full-bleed` → **0 texto permitido, nunca** (regla dura del documento). Si el slide necesita texto, el layout está mal elegido — cambiar a `Ventana+texto` o `Texto+lateral`, no forzar el texto encima.
  - `Marco grande` / `Doble marco` → el texto va en `texto_pie`, una franja de subtítulo (Lora 47px) **una sola línea corta** — no es espacio para explicar un mecanismo completo. Si el punto de Valor necesita más de una línea corta, ese slide no puede ser Marco grande/Doble marco: pasarlo a `Ventana+texto`, `Texto+lateral` o `Solo texto`.
  - `Ventana+texto` → franja sólida dedicada (tercio inferior en 4:5, equivalente en 9:16) — cabe una o dos oraciones cortas.
  - `Texto+lateral` → columna de 410px dedicada — la más generosa de las que combinan imagen, cabe un párrafo breve.
  - `Solo texto` → todo el slide es texto, sin límite de layout (el límite es el de legibilidad general, no de espacio).
  - Si un punto de Valor no cabe en el layout que el Paso 2 le asignó por afinidad Hook→Layout, no se recorta el contenido a la fuerza ni se cambia de layout sin criterio: se decide explícitamente — partir el punto en dos slides, o moverlo a un layout con más espacio de texto — y se declara en el brief, nunca se descubre al momento de ensamblar.
- Voz del Brand Bible: cálida, directa, sin banned words. Todo el copy final en **inglés** (mercado US), títulos de portada en el formato ya definido en la Malla.
- **Si `Medio = Video`** (leer `knowledge/FYR_Protocolo_Edicion_Video.md` completo antes de escribir): la unidad es el slide-beat (imagen 9:16 + una línea narrada). Reglas del piloto PZA_4.2:
  - Slide 1 = portada (`TPL-video-cover-framed.png`, estática, sin subtítulos); slides 2–N = imagen `full_bleed` con la línea narrada en `texto_narrado`. El Paso 2 (afinidad Hook→Layout) NO aplica al cuerpo del video: todos son `full_bleed` solo imagen; el texto lo ponen los subtítulos.
  - Cuenta regresiva narrada ("Number five: …"), **sin numerales en pantalla**.
  - Marcas en `texto_narrado`: `*palabra*` = énfasis (subtítulo más grande), `//` al final de una palabra = pausa extra, `…` = pausa larga. Longitud de referencia ~525 caracteres (~35 s, 6 slides).
  - **Cierre en loop de replay por defecto, alternando A y B:** B = pregunta cuya respuesta son las primeras palabras del video; A = frase cortada que el inicio completa. El CTA único va antes, separado con `//`. Registrar el tipo de cierre en el brief (es una variable a medir).
  - **Regla crítica (19-oct-2026, corregida tras hallazgo en TTS real):** tanto en A como en B, la frase de cierre **nunca puede compartir 3+ palabras seguidas con la frase de apertura, ni repetir su idea completa** — eso suena a error de guion al escucharlo, no a loop. "Frase cortada" (tipo A) significa gramaticalmente incompleta (termina en dos puntos, conector o idea sin cerrar), nunca "la misma frase con distinto final". El corte debe sonar como alguien hablando, no como fórmula de copywriting: preferir conectores cortos y naturales como "And honestly?", "Because, real talk—", "So yeah—" (la prohibición anterior de "So…" como conector era excesiva y se retira — el problema real nunca fue la palabra "So", fue la repetición de contenido).
  - Las imágenes narrativas deben ser 9:16; verificar el tamaño real (Gemini suele entregar 768×1376, ver Policy v2.4 Sección 5).

### Paso 4 — Selección de assets
Dos búsquedas distintas en `Assets`, según qué necesita el slide:
- **Imagen de escena** (contenido del tema): buscar por Tags relacionados al pilar/tema. Referenciar por nombre de archivo exacto + Link Drive.
- **Elemento de layout fijo** (marcos: marco grande, doble marco y las portadas — cuando el Paso 2 asignó uno de ellos): buscar por nombre `FYR_LAYOUT_doble-marco_[aspecto]_v1.png`, `FYR_ASSET_marco-madera_[aspecto]_v1.png` o `FYR_ASSET_marco-cuadrado_9x16_v1.png` en `Assets` — NO por tags de tema, son reutilizables entre piezas. Consultar `knowledge/reference_assets/FYR_Layout_Specs_v1.md` para la ventana exacta y la proporcion de imagen que se pide a Gemini (4:5, 9:16, 3:4 o 1:1 segun el hueco) antes de generar la imagen de escena. **Todo prompt de Gemini lleva el bloque de composicion** (Layout_Specs, "Bloque de composicion para prompts"): ratio exacto del hueco, composicion a sangre sin marcos ni margenes, y la marca `fondo` por slide en el brief: `pergamino` (fondo liso #F5ECD7, obligatorio si la imagen queda suelta en `ventana_texto`/`texto_lateral`) o `color_completo` (escena a todo color; se usa tal cual).

**Primero el banco (11-oct-2026).** Para cada slide que pide imagen de escena, buscar antes en `Assets` (por Tags, `Descripción breve` y `Aspecto`) y usar lo que calce. Se descartan los assets con `En descanso` marcado (una escena no se repite en dos piezas seguidas) y se prefiere el de menor `Veces usado`; plantillas y marcos están exentos. El brief declara "X de N slides salen del banco". Las ilustraciones botánicas de fondo transparente (Seed Library L01–L101, 1:1) entran directo a la portada 9:16 (`marco_grande_cuadrado`, ventana 1:1); en slides secundarias requieren el layout `ficha_planta` (pendiente de construir).

Solo lo que falte lleva un prompt de generación nuevo marcado como `[GENERAR EN GEMINI]` — no bloquear la pieza por eso. Lo que se genere debe poder reutilizarse: sin texto horneado en la imagen salvo que la escena lo exija, y se registra en `Assets` con tags pensados para reuso.

**Fuente única del bloque de estilo (corrección 18-oct-2026 — error detectado: el lote PZA_3.1–PZA_9.3 escribió prompts con la frase obsoleta "watercolor and ink illustration, vintage nature-journal style" en vez del bloque real):** el bloque de estilo base vive SOLO en `FYR_Asset_Governance_Policy.md` §4 ("Bloque de estilo base") — citarlo ahí, textual, nunca parafrasearlo ni reconstruirlo de memoria. Cada prompt de Gemini se compone pegando, en este orden: (1) el bloque de estilo base completo tal cual aparece en Governance Policy §4, (2) la **línea de output obligatoria** (`Output <ancho>x<alto>px, <ratio>, PNG format.` — Governance Policy §4, "Línea de output obligatoria"; PNG siempre, y el ratio según el layout real del slide en `FYR_Layout_Specs_v1.md`, nunca el 4:5 genérico cuando el layout pide otro — ej. `marco_grande` es 0.78:1 real), (3) el bloque de composición por layout de `FYR_Layout_Specs_v1.md` (ratio + `fondo` del slide), (4) el texto específico de la escena (sujeto, encuadre, mood, regla de diversidad si hay manos/personas) **aplicando siempre la Regla de narrativa visual de Governance Policy §4** (ángulo con presencia implícita, contexto de uso real, variación de desgaste, detalle conectado a la intención del slide) — nunca una descripción mínima de una línea. Esta regla es un estándar de calidad obligatorio para toda generación de aquí en adelante, detectado al comparar dos generaciones de la misma escena (PZA_3.1 S1): la versión con bloque de estilo correcto pero descripción mínima salió plana/cenital; la versión vieja, aunque desviada de paleta, tenía vida real por el contexto y el ángulo. El objetivo es la paleta correcta CON ese nivel de vida.

**Regla de separación prompt-copiable / nota humana (corrección 19-oct-2026 — error detectado en PZA_6.5 S3a/S3b: una nota operacional quedó dentro del texto citado del prompt):** el texto que se copia literalmente a Gemini (lo que va dentro de las comillas del prompt) contiene SOLO instrucciones técnicas de generación — nunca una nota editorial/operacional para Johnny o el ensamblado (ej. "va dentro de la ventana del marco", "el compositor ajusta...", "recorte mínimo aceptable"). Ese tipo de nota puede hacer que Gemini interprete palabras como "marco"/"ventana"/"video" como elementos a dibujar. Cualquier nota de ese tipo se escribe SIEMPRE fuera de las comillas del prompt — en el texto descriptivo de la entrada o como "*(Nota para Johnny: ...)*" aparte. Ver Governance Policy §4 para el texto completo de esta regla.

**Separación prefacio/específico al escribir el brief:** en la tabla slide-por-slide del brief.md y en el campo `prompt` del config JSON de la pieza, NO repetir el bloque de estilo base completo en cada slide — anotar una sola vez al inicio del brief que todos los prompts usan el bloque base de Governance Policy §4, y que el campo `prompt` de cada slide contiene SOLO la línea de output (PNG + ratio del layout) + el bloque de composición + lo específico de esa escena. Esto es lo que la Mesa de Producción (herramienta de apoyo visual de Fase D) espera para poder concatenar prefacio + línea de output + bloque de composición + específico en un solo botón de copiar por slide.

### Paso 5 — Outputs y flujo temporal (en este orden — NUNCA saltarse ni fusionar)

**La ejecución detallada vive en `knowledge/FYR_Rutas_De_Produccion.md`** (Ruta A = carrusel, nunca toca Actions; Ruta B = video, el render solo en Actions). Las dos rutas no se mezclan. Resumen de cómo se corresponden con estos sub-pasos:

1. **Brief** → `production/pieces/PZA_[tema]/brief.md` (en Git; `production/briefs/` ya no existe): tema, fase, hook (nombre completo + Question Test), tabla slide-por-slide (texto exacto | layout según Pasos 2/3 | `% imagen` | imagen: record de Assets + ID de Drive + nombre, o `[GENERAR EN GEMINI]` con nombre final `STOCK-[slug]_[aspecto]_v1.png`, prompt y `fondo` | nota de intención), CTA (vacío o "ninguno (F1)" si la fase es F1) y caption. El brief ya indica por slide si el asset existe en el banco o hay que generarlo.
2. **Config de la pieza** (reemplaza al CSV de Canva). Claude escribe solo qué layout, qué texto y qué imagen —nunca coordenadas ni tiempos—:
   - **Carrusel:** `production/pieces/PZA_[tema]/config.json` (schema de `FYR_Motor_Ensamblado_Arquitectura_v1.md` §6) + `imagenes.json` (nombre de la imagen → ID de Drive; `null` mientras la imagen no exista).
   - **Video:** `production/scripts/video/pza-[tema]/pieza_[tema].json` (contrato de `FYR_Protocolo_Edicion_Video.md` §2) + `production/pieces/PZA_[tema]/portada_config.json` + `imagenes.json` de la imagen 1:1 de la portada.
   Si el brief cambia en la pausa del sub-paso 3, el config se parchea con el brief; nunca queda desfasado.
3. **PAUSA — Aprobación del usuario.** El brief puede cambiar aquí; si cambia, patch quirúrgico, nunca regenerar desde cero. Solo se avanza cuando el usuario confirma explícitamente.
4. **Apertura de la pieza (Claude, automática al aprobar):** crear en Drive `Content_Pieces/PZA_[tema]/[fecha]/` (verificando si `PZA_[tema]/` ya existe); crear el tema en `Themes` SOLO si no existe (Número, Pilar, Dolor/Deseo, Prioridad, Hook Asignado, y `Bundle Relacionado` solo si el Pilar tiene mapeo obvio — opcional, no se fuerza) — si ya existe, no se toca; crear la fila en `Content_Pieces` (`Estado Producción = Brief Generado`, `Tema Relacionado`, `Assets Usados` del banco, `Hook Usado` con nombre completo, `Formato`, `Fase Embudo`, `Título Portada`, `Subtítulo`, `Prompt Imagen`, `CTA Sugerido`, `Audiencia`, `Carpeta Drive`, `Ruta .md`, `Ruta JSON`; video: `Tipo de Pieza = Video`, `ID de variante`, tipo de cierre al inicio de `Copy Completo`) y aplicar la memoria de uso en `Assets` (`Veces usado` +1, `Último uso`, `En descanso` marcado; desmarcar los que ya descansaron). Claude hace estas escrituras.
5. **Generación manual + espera.** Solo si el brief marcó `[GENERAR]`: el usuario genera en Gemini con el prompt del brief (un prompt a la vez), lo exporta a `06_Narrative_Stock/` **con el nombre exacto** y avisa. Claude lista la carpeta, cruza por nombre exacto, descarga, mide la proporción real, crea la fila en `Assets` (campos exactos en `FYR_Rutas_De_Produccion.md` §0.6), la linkea en `Assets Usados`, completa `imagenes.json` y pone `Estado Producción = Assets en Drive`. La skill NO continúa hasta que el usuario confirma que ya subió.
6. **Producción del archivo final** — según la Ruta A (carrusel: descargar con el conector → `run_pieza.py importar` y `ensamblar` → revisión visual y aprobación → `run_pieza.py subir` y mover con el conector a `Content_Pieces` → `Ensamblado`) o la Ruta B (video: portada compuesta → verificación → push de la cola → Actions → revisión → `Ensamblado`). Al publicar (desde 28-oct-2026, todo en `Content_Pieces`, ya no en `Themes`): `Estado Producción = Publicado`, `Fecha de Publicación`, `Último uso` de los assets corregido a la fecha de publicación, y el link en el campo `Link Publicación [red]` de `Content_Pieces` que corresponda a dónde se publicó (`IG`/`TikTok`/`Pinterest`/`FB`/`YouTube` — campos separados por red, no un único "link"; si se publica en varias redes, llenar cada campo correspondiente).

**Verificación final de cada pieza:** brief y config en el repo + config válido (carrusel: `config_loader.py` lo acepta; video: JSON válido y cada escena existe en `Assets`) + carpeta de Drive con los archivos terminados (cuenta y checksum) + registro Airtable con `Carpeta Drive`, `Assets Usados`, `Hook Usado` y estado correctos. Reportar los cuatro checks al usuario. Si cualquiera falla, decirlo — nunca declarar éxito parcial como éxito.

---

## 5. Modo afiliado (`Audiencia = Afiliado`)

Cuando el usuario pida un "kit para [creador]": mismo flujo, con estos cambios:
- El CTA apunta al link de afiliado del creador (pedirlo si no se conoce; el formato es `feedyourroots.us/?aff=CODE` o su link Hotmart directo — no inventar códigos).
- El copy se escribe en primera persona DEL CREADOR (su historia con el recurso), no de FYR.
- Los briefs van a `production/affiliate_kits/[handle]/`.
- Registrar `Audiencia = Afiliado` y anotar el handle del creador al inicio de `Copy Completo`.
- El tema usado en un kit de afiliado NO se marca `Usado` para la cuenta propia — el mismo tema puede vivir en ambas audiencias. Anotar en el registro, no en el tema.

---

## 6. Reglas no negociables

- **Diversidad étnica** en toda figura humana de prompts nuevos — nunca default a piel clara.
- **Rostros:** prohibidos en assets de marca/iconos/decorativos; permitidos con expresion completa en escenas narrativas POV/emocionales de piezas de Content_Pieces (ver Brand Bible v2 y Policy v2.2).
- **Texto en ilustraciones:** solo cuando el objeto narrado lo exige (etiquetas de semillero, recibos, portadas de libro, carteles dentro de la escena) — nunca texto decorativo suelto ni titulos superpuestos fuera de la escena misma.
- **Plan antes de ejecutar:** en modo batch ("produce 5 piezas"), mostrar la lista de temas seleccionados y esperar OK antes de generar. Pieza única: generar directo (la aprobación ocurre al revisar el brief).
- **Fail loudly:** ID no encontrado, archivo faltante, conteo que no cuadra → detenerse y reportar. Nunca aplicar un cambio silenciosamente incorrecto.
- **Un paso a la vez:** nunca pedir al usuario múltiples acciones manuales en un solo mensaje.
- **Video:** un video de FYR cierra en loop de replay (A/B alternados) y nunca muestra numerales en una cuenta regresiva; el detalle y su estado de validación viven en `knowledge/FYR_Protocolo_Edicion_Video.md`.
