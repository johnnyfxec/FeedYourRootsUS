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
| Campo | fieldId | Tipo |
|---|---|---|
| Número (primary) | `fld6BnujxYXzxfmOb` | number (ej. 1.1, 11.8) |
| Pilar | `fldBPnwVI3SuxXa7m` | singleSelect |
| Dolor/Deseo | `fldfdZoX3D1oIlakE` | multilineText |
| Formato | `fldT5oVcwdPIbUtUs` | singleSelect (POV/Antes-Después/Countdown/Storytime) |
| Medio | `fldTenGEKEdNeXZvK` | singleSelect (Video/Carrusel) |
| Título Portada | `fldCVVfapSEX9W91G` | multilineText |
| Subtítulo | `fldDMjUCQPjWQuloZ` | multilineText |
| Prompt Imagen | `fldaDHMXne92KYFxV` | multilineText |
| Estado | `fldzY0QnfpqGQ3430` | singleSelect (Pendiente/Usado/Descartado) |
| Fecha de uso | `fld4kEWvpINR87HIG` | dateTime |
| CTA Sugerido | `fld1NGli5eaExrV99` | multilineText |
| Bundle Relacionado | `fldT0UBdIsexJIT4i` | singleSelect |
| Plataforma | `fldTHMGY0eb93rtqA` | multipleSelects |
| Prioridad | `fld9t1dYpz4AfB1vJ` | singleSelect |
| Hook Asignado | `fldZwv8371fG270a7` | singleSelect ("01 Negativo"…"20 Revelación") |
| Fase Embudo | `fld46rAo9PUiyXTRF` | singleSelect (F1-F4) |
| Content_Pieces | `fldTOvVnXFjnT0SLk` | link inverso |

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
| Hook Usado | `fldmaZNxsUpRxBGmC` | singleSelect ("01"…"20") |

### Tabla `Assets` — `tblkzOtjS4KK5B2Xn`
Campos clave: `Nombre de archivo` (`fldX3gsT4b6dkzIvg`), `Link Drive` (`fldMWMX97UDujzVgB`), `Tags` (`fldvq3RMSkUIR1Od4`), `Reutilizable en` (`fldxD7IhRHFI7f2XJ`). ~206 registros con link Drive verificado.

**Regla de propiedad de Airtable:** Claude hace TODAS las escrituras (crear, actualizar, borrar registros y campos) en el paso que corresponde de cada skill; Johnny no edita Airtable a mano.

**Campos de video en `Content_Pieces`:** `Ruta JSON` (`flduZXIO9iQ89U6Kt`, texto) ya existe; `ID de variante` (`fldnCOYKQf6SscuMz`, texto; formato `voz|subtítulo|cierre`, ej. `Neural2-J|B-e14|cierreB`) también existe (ver `knowledge/FYR_Protocolo_Edicion_Video.md` Secciones 8 y 10).

**Regla:** para singleSelect/multipleSelects escribir el nombre de la opción como string y usar `typecast: true` cuando la opción pueda no existir aún (crea la opción automáticamente).

---

## 2. Fuentes de conocimiento (leer, no duplicar)

Rutas relativas a la raíz del repo (`~/FeedYourRootsUS`). Si un archivo no existe → **fallar con mensaje claro** indicando qué archivo copiar a `knowledge/`, nunca inventar su contenido.

| Archivo | Uso |
|---|---|
| `knowledge/FYR_Malla_60_Temas_Virales_v2.md` | Banco semilla de 61 temas (no está cargado en Airtable; un tema entra a `Themes` al producirse). Marcar aquí el estado de un tema NO es necesario: manda `Themes` |
| `knowledge/Sistema_Maestro_CRS_v2.md` | Fases de embudo, arquitectura de loops, Question Test, framework 6 pasos |
| `knowledge/hooks_verbales_20_v2.md` | Los 20 hooks: principio psicológico, estructura, reglas de uso |
| `knowledge/Feed-Your-Roots-Brand-Bible.md` | Voz, paleta, tipografía, banned words, regla de diversidad, excepcion de rostros en escenas narrativas (v2) |
| `knowledge/FYR_Asset_Governance_Policy.md` (v2.3+) | Nomenclatura, ubicación de archivos, estructura `Content_Pieces/PZA_[tema]/[fecha]/`, estructura `01_Brand_Assets/C01-C13` (incluye C12_Frames y C13_Layout_Elements), y principio de duplicados semánticos en Themes |
| `knowledge/reference_assets/FYR_Layout_Specs_v1.md` | Medidas exactas (bbox, ventanas de contenido) de los layouts vigentes en 4:5 y 9:16, con ruta de Drive de cada asset — consultar SIEMPRE antes de generar un prompt de imagen que use un layout con marco/asset fijo |
| `knowledge/FYR_Brand_Mark_Spec_v1.md` | Simbolo oficial de marca (frasco+arbol): espacio de proteccion, tamano minimo, variantes de color, lockups aprobados, usos prohibidos, proporcion fija 1:1.405 — consultar SIEMPRE antes de usar/reproducir el simbolo o el wordmark en cualquier pieza |
| `knowledge/FYR_Motor_Ensamblado_Arquitectura_v1.md` | Contrato de `assemble.py` (carruseles/slides estáticos): tipos de layout, tipografía, schema del config JSON — leer antes de escribir el config de un carrusel |
| `knowledge/FYR_Protocolo_Edicion_Video.md` | Pipeline de video (voz TTS, subtítulos palabra por palabra, pausas, cierre en loop A/B, contrato del JSON de pieza, procedimiento en la PC) — leer SIEMPRE cuando `Medio = Video`, antes del Paso 3 |
| `knowledge/FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` | Arquitectura del sistema completo de 3 skills (trend-scout, fyr-content, performance-lens), como se comunican vía Airtable, y el schema real de `Trend_Signals` — leer antes de tocar cualquier logica relacionada a tendencias o performance |

**Adaptación obligatoria del CRS:** el sistema fue escrito para el avatar de trading/libertad financiera. Al aplicarlo, traducir SIEMPRE al avatar Morgan (28-42, patio suburbano, busca soberanía alimentaria): el dolor no es "depender de un sueldo", es "depender del supermercado / no saber qué come su familia / sentir que la autosuficiencia es para gente con 5 acres". La ciencia (loops, fases, hooks) se conserva; el contenido se traduce.

---

## 3. Banco de temas y alta de temas

**Dos lugares, dos funciones (no confundirlos):**
- **Banco de temas** = la Malla (`knowledge/FYR_Malla_60_Temas_Virales_v2.md`, 61 temas semilla `X.Y`) + los temas nuevos que se extraigan de los PDFs. Es donde se *elige* qué producir. NO está cargado en Airtable y no se carga en bloque.
- **Tabla `Themes`** = solo los temas que ya se han producido (o están en producción). Es el registro: estado, fecha, hook, piezas. Un tema entra a `Themes` en el momento de producirlo (Paso 5.6), nunca antes.

**Temas nuevos desde los PDFs (la fuente de contenido es ilimitada).** Cada parte de un recurso (sección, tabla, lista, error común, caso del PDF) puede convertirse en un tema que impulse recordación o ventas:
1. Leer el PDF del pilar en el Proyecto (los 10 recursos de la carpeta de producto; el Core Bundle y los demás bundles están en la lista de archivos del Proyecto) y elegir un fragmento concreto: una cifra, un error, una tabla, un procedimiento.
2. Convertirlo en tema con la misma estructura de la Malla: Dolor/deseo (traducido al avatar Morgan), CTA visual (el recurso), Formato, Medio, Título de portada + Subtítulo, Prompt de imagen.
3. **Numeración:** el tema pertenece al pilar del PDF y toma el siguiente número libre de ese pilar, mirando AMBOS lugares (la Malla y `Themes`). Ejemplo: P4 llega hasta 4.5 en la Malla, el tema nuevo es 4.6. Nunca reutilizar un número.
4. **Duplicado semántico:** antes de crearlo, comparar su dolor/deseo contra los temas de la Malla del mismo pilar y contra `Themes`; si ya está cubierto en otras palabras, usar el existente.
5. Asignar **Fase Embudo** (dolor sin mencionar el producto → F1; mostrar alternativa → F2; destruir objeción → F3; resultado/demostración del recurso → F4; verificar que la mezcla mensual se acerque a 40/27/20/13) y **Hook Asignado** (Fase + Formato con la tabla de compatibilidad del CRS, Parte 2; el hook Mito (11) es el de mayor conversión para creencias arraigadas como "autosuficiencia = mucho terreno y dinero").
6. Mostrar el tema nuevo al usuario y esperar su OK antes de continuar al Paso 1.

**Alta en `Themes` (Paso 5.6):** si el tema no existe en `Themes`, crearlo con todos sus campos (Número, Pilar, Dolor/Deseo, Formato, Medio, Título Portada, Subtítulo, Prompt Imagen, Fase Embudo, Hook Asignado, CTA Sugerido, Plataforma) y `typecast: true`; si ya existe, actualizarlo. Verificar antes de crear que el Número no exista ya (fail loudly si hay duplicado).

## 4. Flujo de producción por pieza

### Paso 0 — Selección de tema
**Chequeo previo, siempre primero (opcional, nunca bloqueante):** consultar `Trend_Signals` (tabla `tblxdaRsgEy8CHvV9`) filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`. Si hay resultados, ofrecer al usuario producir la pieza montada sobre esa señal — usando su `Hook_CRS_Equivalente`, `Formato_Sugerido` y `Brief_Adaptacion` como punto de partida del Paso 1 en vez de partir de cero. Si el usuario acepta, al completar el Paso 5 escribir el `PZA_[tema]` resultante de vuelta en `Content_Piece_Generada` de esa fila. Si no hay señales aprobadas vigentes, o el usuario declina, continuar normal con los 3 caminos de siempre:
- Usuario pide tema específico (`X.Y`) → buscar primero en `Themes`; si no está, tomarlo de la Malla (banco semilla) tal cual. Si el número no existe en ninguno de los dos, decirlo y detenerse. Nunca seleccionar uno ya `Usado` sin confirmación explícita.
- Usuario pide "el siguiente" → elegir del banco (Malla + temas nuevos) los temas que NO estén en `Themes` como `Usado`. **Cola de arranque** (primeras 8 piezas): selección deliberadamente diversa, un pilar distinto cada vez y cubriendo las 4 fases, para tener señal real de qué convierte antes de escalar. Después de 8 piezas: priorizar por performance de lo ya publicado (`Performance`) y por la mezcla de fases del mes cerca de 40/27/20/13.
- Usuario pide un tema nuevo "desde el PDF de [pilar]" o describe un ángulo libremente, SIN número → **búsqueda semántica obligatoria, siempre, sin excepción**: comparar su dolor/deseo contra los temas de la Malla del mismo pilar y contra `Dolor/Deseo` + `Título Portada` de todo `Themes`, evaluando conceptualmente (no por texto exacto). Coincidencia real → usar el existente y avisar cuál y por qué. Sin coincidencia → crear el tema nuevo siguiendo la Sección 3 (numeración, Fase, Hook) y esperar el OK del usuario antes de continuar.
- El estado de un tema lo decide `Themes`, no la Malla: un tema de la Malla que no está en `Themes` está disponible.

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
- Slide 1: hook (loop 1 abierto). Slides intermedios: agitación y valor en pedazos, abrir loop nuevo antes de cerrar el anterior.
- **Ultimo slide (cierre, sin plantilla fija):** cierre de todos los loops + CTA unico, graduado segun Fase (F1 implicito/sin mencionar Bundle, F2 suave nombrando el recurso gratuito, F3 directo nombrando el Bundle que resuelve la objecion, F4 de autoridad invitando a replicar el resultado). El layout del cierre se elige libremente entre los 12 layouts activos (ver catalogo completo arriba en Paso 2) segun que sirva mejor a esa resolucion especifica — nunca un layout de marca fijo tipo catalogo.
- **Regla de loop visual (obligatoria en el cierre):** el prompt de imagen del slide de cierre debe citar textualmente un elemento especifico del prompt de portada (objeto, color dominante, o composicion) e instruir que se repita transformado — mismo objeto, estado distinto. Esto invita a redeslizar desde el inicio, aumentando el watch-time/replay. Ejemplo: portada = "caja de zapatos desordenada"; cierre = "la misma caja, ahora organizada y cerrada con lazo".
- Decidir por slide si lleva asset de fondo o solo texto sobre fondo de marca (Parchment #F5ECD7): el criterio es si la imagen añade tensión/credibilidad al loop. Nunca imagen decorativa por rellenar.
- Voz del Brand Bible: cálida, directa, sin banned words. Todo el copy final en **inglés** (mercado US), títulos de portada en el formato ya definido en la Malla.
- **Si `Medio = Video`** (leer `knowledge/FYR_Protocolo_Edicion_Video.md` completo antes de escribir): la unidad es el slide-beat (imagen 9:16 + una línea narrada). Reglas del piloto PZA_4.2:
  - Slide 1 = portada (`TPL-video-cover-framed.png`, estática, sin subtítulos); slides 2–N = imagen `full_bleed` con la línea narrada en `texto_narrado`. El Paso 2 (afinidad Hook→Layout) NO aplica al cuerpo del video: todos son `full_bleed` solo imagen; el texto lo ponen los subtítulos.
  - Cuenta regresiva narrada ("Number five: …"), **sin numerales en pantalla**.
  - Marcas en `texto_narrado`: `*palabra*` = énfasis (subtítulo más grande), `//` al final de una palabra = pausa extra, `…` = pausa larga. Longitud de referencia ~525 caracteres (~35 s, 6 slides).
  - **Cierre en loop de replay por defecto, alternando A y B:** B = pregunta cuya respuesta son las primeras palabras del video; A = frase cortada que el inicio completa. La pregunta NO puede contener las palabras de la respuesta. El CTA único va antes, separado con `//`, sin conectores tipo "So…". Registrar el tipo de cierre en el brief (es una variable a medir).
  - Las imágenes narrativas deben ser 9:16; verificar el tamaño real (Gemini suele entregar 768×1376, ver Policy v2.4 Sección 5).

### Paso 4 — Selección de assets
Dos búsquedas distintas en `Assets`, según qué necesita el slide:
- **Imagen de escena** (contenido del tema): buscar por Tags relacionados al pilar/tema. Referenciar por nombre de archivo exacto + Link Drive.
- **Elemento de layout fijo** (marcos: marco grande, doble marco y las portadas — cuando el Paso 2 asignó uno de ellos): buscar por nombre `FYR_LAYOUT_doble-marco_[aspecto]_v1.png`, `FYR_ASSET_marco-madera_[aspecto]_v1.png` o `FYR_ASSET_marco-cuadrado_9x16_v1.png` en `Assets` — NO por tags de tema, son reutilizables entre piezas. Consultar `knowledge/reference_assets/FYR_Layout_Specs_v1.md` para la ventana exacta y la proporcion de imagen que se pide a Gemini (4:5, 9:16, 3:4 o 1:1 segun el hueco) antes de generar la imagen de escena. **Todo prompt de Gemini lleva el bloque de composicion** (Layout_Specs, "Bloque de composicion para prompts"): ratio exacto del hueco, composicion a sangre sin marcos ni margenes, y la marca `fondo` por slide en el brief: `pergamino` (fondo liso #F5ECD7, obligatorio si la imagen queda suelta en `ventana_texto`/`texto_lateral`) o `color_completo` (escena a todo color; se usa tal cual).

Si ningún asset calza para un slide clave, incluir en el brief un prompt de generación nuevo (bloque de estilo del Brand Bible + regla de diversidad) marcado como `[GENERAR EN GEMINI]` — no bloquear la pieza por eso.

### Paso 5 — Outputs y flujo temporal (6 sub-pasos, en este orden — NUNCA saltarse ni fusionar)

1. **Brief** → `production/briefs/FYR_Brief_[Número]_[slug].md`: tema, fase, hook (nombre + Question Test), tabla slide-por-slide (texto exacto | layout asignado segun Paso 2/3 | asset o fondo (`pergamino` / `color_completo` para las imagenes a generar) | nota de intencion), CTA. El numero de slides y el layout de cada uno ya vienen decididos por las reglas de los Pasos 2 y 3 — el brief los documenta, no los reinventa. El campo CTA puede quedar vacio o decir "ninguno (F1)" cuando la Fase Embudo asignada al tema es F1, segun la gradacion del Paso 3. El brief YA indica, por slide, si el asset existe en el banco o necesita generarse (`[GENERAR EN GEMINI]`) — esa evaluacion se hace aqui, no despues.
2. **Config JSON de la pieza** (reemplaza al CSV de Canva, retirado). Claude escribe solo qué layout, qué texto y qué imagen —nunca coordenadas ni tiempos—:
   - **Carrusel / imagen:** `PZA_[tema]_config.json`, schema de `FYR_Motor_Ensamblado_Arquitectura_v1.md` Sección 6, junto al brief en `production/briefs/` (esa carpeta no va a Git). Lo consume `assemble.py`.
   - **Video:** `pieza_[tema].json`, contrato de `FYR_Protocolo_Edicion_Video.md` Sección 2, en `production/scripts/video/pza-[tema]/`. Lo consume el pipeline de video en la PC (skill `fyr-video-assembler`).
   Si el brief cambia en la pausa del sub-paso 3, el JSON se parchea con el brief; nunca queda desfasado.
3. **PAUSA — Aprobación del usuario.** El brief puede cambiar aquí (el usuario edita texto, pide otro hook, etc.) — si cambia, se hace patch quirúrgico del `.md`, nunca regenerar desde cero. Solo se avanza al paso 4 cuando el usuario confirma explícitamente que el brief está listo para producirse.
4. **Creación de carpeta (Drive MCP, automática al aprobar).** Verificar primero si `FYR/05_Marketing_Assets/Social_Media/Content_Pieces/PZA_[tema]/` ya existe (ese tema pudo producirse antes en otra fecha). Si no existe, crear ambos niveles; si existe, crear solo la subcarpeta `[fecha-YYYY-MM-DD]/` de hoy dentro. Esto ocurre sin importar si la pieza necesita generar imágenes nuevas o reutiliza 100% assets existentes — el criterio es "la pieza está lista para ensamblarse", no "ya terminé de generar en Gemini".
5. **Generación manual + espera.** Si el brief marcó slides pendientes, el usuario genera en Gemini usando los prompts del brief (bloque de estilo del Brand Bible + regla de diversidad) y sube los archivos a la carpeta de fecha ya creada, nombrados según convención: `FYR_PZA_[tema]_S[n]_[slug]_[aspecto]_v[version].png`. La skill NO continúa hasta que el usuario confirma que ya subió.
6. **Registro Airtable** → crear fila en `Content_Pieces` (ID `PZA_[tema]`, ej. `PZA_3.1` — mismo nombre que la carpeta de Drive, nunca un consecutivo genérico), linkear `Tema Relacionado` y `Assets Usados` con record IDs reales, `Estado Producción = Assets en Drive` (brief listo y assets en Drive, falta ensamblar/renderizar; pasa a `Ensamblado` cuando el carrusel o el MP4 está terminado y aprobado, y a `Publicado` solo cuando se publica en la red), `Hook Usado`, `Audiencia`, y para video `Tipo de Pieza = Video` y el tipo de cierre (A/B) anotado al inicio de `Copy Completo`. Luego dar de alta o actualizar el tema en `Themes` (Sección 3): `Estado = Usado`, `Fecha de uso = ahora`, con `Hook Asignado` y `Fase Embudo`.

**Verificación final de cada pieza:** brief existe en disco + config JSON válido (carrusel: `config_loader.py` lo acepta; video: es JSON válido y cada `asset` existe en `Assets`) + carpeta de Drive con archivos + registro Airtable con links poblados. Reportar los cuatro checks al usuario. Si cualquiera falla, decirlo — nunca declarar éxito parcial como éxito.

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
