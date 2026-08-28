---
name: fyr-content
description: Motor de producción de contenido FYR. Genera briefs de carrusel/video desde la Malla de 61 temas en Airtable, aplicando el Sistema CRS (fases de embudo, 20 hooks verbales, loops abiertos) y la voz del Brand Bible. Output triple — brief .md legible, fila CSV para Canva Bulk Create, registro en Airtable. Usar cuando el usuario pida "genera el siguiente", "dame el brief del tema X.Y", "produce N piezas" o "kit de afiliado para [creador]".
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
| Tipo de Pieza | `fld7zgQouWTYgQdJ3` | singleSelect (Carrusel/Video/Imagen única) |
| Fecha de Generación | `fldqWpBbCOSaD2gE7` | date |
| Número de Slides | `fldu0xeW00aYT29So` | number |
| Duración | `fldmv5v2wcnu0zxZ3` | number (segundos, solo video) |
| Copy Completo | `fldYXJcdumHdu9du6` | multilineText |
| Ruta .md | `fldSvPv8f3z58iUQS` | texto |
| Estado Producción | `fldqEyriByKYZ0t3n` | singleSelect (Brief Generado/En Canva o Edición/Publicado) |
| Performance | `fldGxHIuckHi9yp4P` | singleSelect (Alto/Medio/Bajo/Sin datos) |
| Tema Relacionado | `fldgHOLLy8s3tr3Dh` | link → Themes (single) |
| Assets Usados | `fldT4ifnqw6Fz8a3v` | link → Assets (múltiple) |
| Audiencia | `fldXC1j4yq3ITULYz` | singleSelect (Propia/Afiliado) |
| Hook Usado | `fldmaZNxsUpRxBGmC` | singleSelect ("01"…"20") |

### Tabla `Assets` — `tblkzOtjS4KK5B2Xn`
Campos clave: `Nombre de archivo` (`fldX3gsT4b6dkzIvg`), `Link Drive` (`fldMWMX97UDujzVgB`), `Tags` (`fldvq3RMSkUIR1Od4`), `Reutilizable en` (`fldxD7IhRHFI7f2XJ`). ~206 registros con link Drive verificado.

**Regla:** para singleSelect/multipleSelects escribir el nombre de la opción como string y usar `typecast: true` cuando la opción pueda no existir aún (crea la opción automáticamente).

---

## 2. Fuentes de conocimiento (leer, no duplicar)

Rutas relativas a la raíz del repo (`~/FeedYourRootsUS`). Si un archivo no existe → **fallar con mensaje claro** indicando qué archivo copiar a `knowledge/`, nunca inventar su contenido.

| Archivo | Uso |
|---|---|
| `knowledge/FYR_Malla_60_Temas_Virales_v2.md` | Fuente de los 61 temas (solo para migración inicial; después Airtable manda) |
| `knowledge/Sistema_Maestro_CRS_v2.md` | Fases de embudo, arquitectura de loops, Question Test, framework 6 pasos |
| `knowledge/hooks_verbales_20_v2.md` | Los 20 hooks: principio psicológico, estructura, reglas de uso |
| `knowledge/Feed-Your-Roots-Brand-Bible.md` | Voz, paleta, tipografía, banned words, regla de diversidad, excepcion de rostros en escenas narrativas (v2) |
| `knowledge/FYR_Asset_Governance_Policy.md` (v2.2+) | Nomenclatura, ubicación de archivos, estructura `Content_Pieces/PZA_[tema]/[fecha]/`, estructura `01_Brand_Assets/C01-C13` (incluye C12_Frames y C13_Layout_Elements), y principio de duplicados semánticos en Themes |
| `knowledge/reference_assets/FYR_Layout_Specs_v1.md` | Medidas exactas (bbox, ventanas de contenido) de los 12 layouts en 4:5 y 9:16, con ruta de Drive de cada asset — consultar SIEMPRE antes de generar un prompt de imagen que use un layout con marco/asset fijo |
| `knowledge/FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` | Arquitectura del sistema completo de 3 skills (trend-scout, fyr-content, performance-lens), como se comunican vía Airtable, y el schema real de `Trend_Signals` — leer antes de tocar cualquier logica relacionada a tendencias o performance |

**Adaptación obligatoria del CRS:** el sistema fue escrito para el avatar de trading/libertad financiera. Al aplicarlo, traducir SIEMPRE al avatar Morgan (28-42, patio suburbano, busca soberanía alimentaria): el dolor no es "depender de un sueldo", es "depender del supermercado / no saber qué come su familia / sentir que la autosuficiencia es para gente con 5 acres". La ciencia (loops, fases, hooks) se conserva; el contenido se traduce.

---

## 3. Primer run — Migración de los 61 temas

Si `Themes` está vacía (verificar con una búsqueda antes de asumir):

1. Parsear la Malla. Cada tema es un bloque `### X.Y — "Título"` con bullets: Dolor/deseo, CTA visual, Formato, Medio, Título portada, Subtítulo, Prompt. **Son 61 temas, no 60** (P5 tiene 4, P11 tiene 8) — verificar el conteo tras parsear y fallar si no da 61.
2. Durante el parseo, asignar a cada tema:
   - **Fase Embudo**, según el ángulo de dolor: incomodar sin que sepan del producto → F1; mostrar alternativa → F2; destruir objeción → F3; resultado/demostración del recurso → F4. Al terminar, verificar que la mezcla global aproxime 40/27/20/13 y ajustar los casos límite.
   - **Hook Asignado**, cruzando Fase + Formato con la tabla de compatibilidad del CRS (Parte 2). Nota v2 del sistema: el hook Mito (11) es el de mayor conversión para avatares con creencias arraigadas — Morgan cree que "autosuficiencia = mucho terreno y dinero"; usarlo generosamente en F2/F3.
3. Crear registros en lotes de ≤50 vía MCP con `typecast: true`, `Estado = Pendiente`.
4. Verificar: contar registros creados == 61 antes de declarar éxito. Mostrar resumen de distribución (temas por fase, por hook) para aprobación del usuario.

La migración corre UNA vez. En runs posteriores, Airtable es la única fuente de verdad de los temas.

---

## 4. Flujo de producción por pieza

### Paso 0 — Selección de tema
**Chequeo previo, siempre primero (opcional, nunca bloqueante):** consultar `Trend_Signals` (tabla `tblxdaRsgEy8CHvV9`) filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`. Si hay resultados, ofrecer al usuario producir la pieza montada sobre esa señal — usando su `Hook_CRS_Equivalente`, `Formato_Sugerido` y `Brief_Adaptacion` como punto de partida del Paso 1 en vez de partir de cero. Si el usuario acepta, al completar el Paso 5 escribir el `PZA_[tema]` resultante de vuelta en `Content_Piece_Generada` de esa fila. Si no hay señales aprobadas vigentes, o el usuario declina, continuar normal con los 3 caminos de siempre:
- Usuario pide tema específico (`X.Y`) que ya existe en `Themes` → usarlo directo, sin búsqueda.
- Usuario pide "el siguiente" → **cola de arranque** (primeras 8 piezas): selección deliberadamente diversa, un pilar distinto cada vez y cubriendo las 4 fases, para tener señal real de qué convierte antes de escalar. Después de 8 piezas: priorizar `Prioridad = Alta` + `Estado = Pendiente`, manteniendo la mezcla de fases del mes cerca de 40/27/20/13.
- Usuario describe un ángulo/tema libremente, SIN número de tema exacto → **búsqueda semántica obligatoria, siempre, sin excepción**: leer `Dolor/Deseo` + `Título Portada` de todo `Themes` y evaluar conceptualmente (no por texto exacto) si algún tema existente ya cubre ese mismo dolor del avatar en palabras distintas. Si hay coincidencia real → usar el tema existente, avisar al usuario cuál es y por qué. Si no hay coincidencia → crear el tema nuevo con el mismo criterio de Fase Embudo + Hook Asignado del proceso de migración (Sección 3), y recién ahí continuar el flujo.
- Nunca seleccionar un tema `Usado` sin confirmación explícita.

### Paso 1 — Question Test (bloqueante)
Completar: *"Cuando Morgan vea los primeros 3 segundos, la pregunta exacta en su cabeza será: ______"*. Si no sale una pregunta específica, el hook no está listo — iterar antes de escribir nada más.

### Paso 2 — Construcción del hook
- Leer la ficha del hook asignado en la guía de 20 (principio, estructura, regla de uso). Se permite cambiar de hook si el Question Test lo exige — registrar el cambio en `Hook Usado`.
- Fórmula de contexto: [contexto que ubica a Morgan] + [elemento que desafía/sorprende dentro de ese contexto].
- Alineación visual-verbal: el asset/imagen del slide 1 NUNCA debe resolver el loop que abre el texto.

**Afinidad Hook -> Layout de apertura del cuerpo (slide 2):** al elegir el layout del primer slide del cuerpo, usar esta afinidad natural en vez de un criterio generico. Catalogo completo: 4 layouts base (Marco grande, Full-bleed con overlay, Solo texto + acento, Texto + imagen lateral) + 8 layouts expandidos (L6 Etiqueta colgante, L7 Nota-kraft en esquina, L8 Doble marco superpuesto, L9 Palabra-acuarela, L10 Tachado/correccion, L11 Cordel guia, L12 Migas de progreso, L13 Ventana Polaroid) — assets y ventanas de cada uno en knowledge/reference_assets/FYR_Layout_Specs_v1.md.
- 03 Numerico, 13 Lista -> Solo texto + acento, o L12 Migas de progreso si el conteo es el eje central
- 07 Contraste/Versus -> L8 Doble marco superpuesto (preferido, un solo slide) o L10 Tachado/correccion (alternativa, mas verbal) o Marco grande dos veces (si ninguno de los anteriores calza)
- 04 Storytelling, 10 Dolor/Frustracion -> Full-bleed con overlay (inmersion emocional)
- 06 Secreto, 20 Revelacion, 12 Curiosidad -> Texto + imagen lateral, o L7 Nota-kraft en esquina, o L13 Ventana Polaroid (revelacion con foco)
- 11 Mito, 05 Error Comun -> Solo texto + acento, o L9 Palabra-acuarela (la creencia como palabra dominante)
- 17 Resultados/Transformacion, 19 Demostracion -> Marco grande (necesita evidencia visual clara)
- 01 Negativo, 14 Advertencia, 09 Prediccion -> Full-bleed con overlay, o L9 Palabra-acuarela (palabra de alerta dominante)
- 02 Pregunta, 08 Autoridad, 15 Oportunidad, 16 Desafio, 18 Sorpresa -> libre segun el tema especifico, sin afinidad estructural fuerte
- L6 Etiqueta colgante -> copy corto e intimo, cualquier hook que necesite sensacion de nota personal
- L11 Cordel guia -> no depende de hook, es conector entre slides consecutivos — usar cuando se quiera dar continuidad visual fuerte a la secuencia

**Regla de variedad ampliada:** con 12 layouts disponibles, ningun layout se repite mas de 2 veces en la misma pieza (antes era 'nunca consecutivo'; ahora ademas se limita la repeticion total).

**Proporcion imagen/texto por funcion del slide** (aplica sin importar cual de los 12 layouts se use): Apertura de loop (hook fuerte) = 85-90% imagen / 10-15% texto. Desarrollo/agitacion = 60-75% imagen / 25-40% texto. Giro/revelacion = 50-65% imagen / 35-50% texto. Cierre/CTA = 70-85% imagen / 15-30% texto. Esta proporcion se declara como campo `% imagen` en la tabla slide-por-slide del brief (Paso 5).

### Paso 3 — Cuerpo (numero de slides segun Fase Embudo, cadena de loops)
- **Numero de slides por Fase** (reemplaza el rango generico anterior): F1 Baja conciencia = 4-5 slides (incomodar es rapido, alargar diluye el golpe); F2 Media conciencia = 5-6 (necesita espacio para mostrar la alternativa sin apurar); F3 Alta conciencia = 6-7 (destruir objecion requiere mas desarrollo argumental, es la fase mas larga); F4 Autoridad = 4-5 (el resultado habla solo, exceso de slides diluye el impacto).
- Slide 1: hook (loop 1 abierto). Slides intermedios: agitación y valor en pedazos, abrir loop nuevo antes de cerrar el anterior.
- **Ultimo slide (cierre, sin plantilla fija):** cierre de todos los loops + CTA unico, graduado segun Fase (F1 implicito/sin mencionar Bundle, F2 suave nombrando el recurso gratuito, F3 directo nombrando el Bundle que resuelve la objecion, F4 de autoridad invitando a replicar el resultado). El layout del cierre se elige libremente entre los 12 layouts activos (ver catalogo completo arriba en Paso 2) segun que sirva mejor a esa resolucion especifica — nunca un layout de marca fijo tipo catalogo.
- **Regla de loop visual (obligatoria en el cierre):** el prompt de imagen del slide de cierre debe citar textualmente un elemento especifico del prompt de portada (objeto, color dominante, o composicion) e instruir que se repita transformado — mismo objeto, estado distinto. Esto invita a redeslizar desde el inicio, aumentando el watch-time/replay. Ejemplo: portada = "caja de zapatos desordenada"; cierre = "la misma caja, ahora organizada y cerrada con lazo".
- Decidir por slide si lleva asset de fondo o solo texto sobre fondo de marca (Parchment #F5ECD7): el criterio es si la imagen añade tensión/credibilidad al loop. Nunca imagen decorativa por rellenar.
- Voz del Brand Bible: cálida, directa, sin banned words. Todo el copy final en **inglés** (mercado US), títulos de portada en el formato ya definido en la Malla.

### Paso 4 — Selección de assets
Dos búsquedas distintas en `Assets`, según qué necesita el slide:
- **Imagen de escena** (contenido del tema): buscar por Tags relacionados al pilar/tema. Referenciar por nombre de archivo exacto + Link Drive.
- **Elemento de layout fijo** (marco, etiqueta, nota, doble-marco, cordel, migas, polaroid — cuando el Paso 2 asignó uno de los 12 layouts): buscar por nombre `FYR_LAYOUT_[nombre-layout]_[aspecto]_v1.png` o `FYR_ASSET_marco-madera_[aspecto]_v1.png` en `Assets` — NO por tags de tema, son reutilizables entre piezas. Consultar `knowledge/reference_assets/FYR_Layout_Specs_v1.md` para la ventana exacta de cada uno antes de dimensionar la imagen de fondo a generar. Si el layout es Palabra-acuarela o Tachado (referencias de estilo, NO reutilizables), el brief debe indicar `[GENERAR EN GEMINI, usar de referencia [nombre-archivo]]` con la palabra/texto real del tema — nunca reutilizar el archivo de muestra directo.

Si ningún asset calza para un slide clave, incluir en el brief un prompt de generación nuevo (bloque de estilo del Brand Bible + regla de diversidad) marcado como `[GENERAR EN GEMINI]` — no bloquear la pieza por eso.

### Paso 5 — Outputs y flujo temporal (5 sub-pasos, en este orden — NUNCA saltarse ni fusionar)

1. **Brief** → `production/briefs/FYR_Brief_[Número]_[slug].md`: tema, fase, hook (nombre + Question Test), tabla slide-por-slide (texto exacto | layout asignado segun Paso 2/3 | asset o fondo | nota de intencion), CTA. El numero de slides y el layout de cada uno ya vienen decididos por las reglas de los Pasos 2 y 3 — el brief los documenta, no los reinventa. El campo CTA puede quedar vacio o decir "ninguno (F1)" cuando la Fase Embudo asignada al tema es F1, segun la gradacion del Paso 3. El brief YA indica, por slide, si el asset existe en el banco o necesita generarse (`[GENERAR EN GEMINI]`) — esa evaluacion se hace aqui, no despues.
2. **Fila CSV** → append a `production/canva_bulk_queue.csv`. Crear con header si no existe. Schema fijo:
   ```
   pieza_id,tema,hook_titulo,hook_sub,s2_txt,s3_txt,s4_txt,s5_txt,s6_txt,cta_txt,img1,img2,img3,img4,img5,img6,img7
   ```
   Columnas de slides no usados = cadena vacía. `img*` = nombre de archivo exacto del asset. Escapar comas con comillas dobles estándar CSV.
3. **PAUSA — Aprobación del usuario.** El brief puede cambiar aquí (el usuario edita texto, pide otro hook, etc.) — si cambia, se hace patch quirúrgico del `.md`, nunca regenerar desde cero. Solo se avanza al paso 4 cuando el usuario confirma explícitamente que el brief está listo para producirse.
4. **Creación de carpeta (Drive MCP, automática al aprobar).** Verificar primero si `FYR/05_Marketing_Assets/Social_Media/Content_Pieces/PZA_[tema]/` ya existe (ese tema pudo producirse antes en otra fecha). Si no existe, crear ambos niveles; si existe, crear solo la subcarpeta `[fecha-YYYY-MM-DD]/` de hoy dentro. Esto ocurre sin importar si la pieza necesita generar imágenes nuevas o reutiliza 100% assets existentes — el criterio es "la pieza está lista para ensamblarse", no "ya terminé de generar en Gemini".
5. **Generación manual + espera.** Si el brief marcó slides pendientes, el usuario genera en Gemini usando los prompts del brief (bloque de estilo del Brand Bible + regla de diversidad) y sube los archivos a la carpeta de fecha ya creada, nombrados según convención: `FYR_PZA_[tema]_S[n]_[slug]_[aspecto]_v[version].png`. La skill NO continúa hasta que el usuario confirma que ya subió.
6. **Registro Airtable** → crear fila en `Content_Pieces` (ID `PZA_[tema]`, ej. `PZA_3.1` — mismo nombre que la carpeta de Drive, nunca un consecutivo genérico), linkear `Tema Relacionado` y `Assets Usados` con record IDs reales, `Estado Producción = Publicado en Drive`, `Hook Usado`, `Audiencia`. Luego actualizar el tema: `Estado = Usado`, `Fecha de uso = ahora`.

**Verificación final de cada pieza:** brief existe en disco + fila CSV parseable + carpeta de Drive con archivos + registro Airtable con links poblados. Reportar los cuatro checks al usuario. Si cualquiera falla, decirlo — nunca declarar éxito parcial como éxito.

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
