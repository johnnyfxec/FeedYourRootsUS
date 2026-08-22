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
| `knowledge/Feed-Your-Roots-Brand-Bible.md` | Voz, paleta, tipografía, banned words, regla de diversidad |
| `FYR_Asset_Governance_Policy.md` (v2.0+) | Nomenclatura, ubicación de archivos, estructura `Content_Pieces/PZA_[tema]/[fecha]/`, y principio de duplicados semánticos en Themes |

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

### Paso 3 — Cuerpo (4-7 slides, cadena de loops)
- Slide 1: hook (loop 1 abierto). Slides intermedios: agitación y valor en pedazos, abrir loop nuevo antes de cerrar el anterior. Último slide: cierre de todos los loops + CTA único basado en la transformación del Bundle Relacionado.
- Decidir por slide si lleva asset de fondo o solo texto sobre fondo de marca (Parchment #F5ECD7): el criterio es si la imagen añade tensión/credibilidad al loop. Nunca imagen decorativa por rellenar.
- Voz del Brand Bible: cálida, directa, sin banned words. Todo el copy final en **inglés** (mercado US), títulos de portada en el formato ya definido en la Malla.

### Paso 4 — Selección de assets
Buscar en `Assets` por Tags relacionados al pilar/tema. Referenciar por nombre de archivo exacto + Link Drive. Si ningún asset calza para un slide clave, incluir en el brief un prompt de generación nuevo (bloque de estilo del Brand Bible + regla de diversidad) marcado como `[GENERAR EN GEMINI]` — no bloquear la pieza por eso.

### Paso 5 — Outputs y flujo temporal (5 sub-pasos, en este orden — NUNCA saltarse ni fusionar)

1. **Brief** → `production/briefs/FYR_Brief_[Número]_[slug].md`: tema, fase, hook (nombre + Question Test), tabla slide-por-slide (texto exacto | asset o fondo | nota de intención), CTA. El brief YA indica, por slide, si el asset existe en el banco o necesita generarse (`[GENERAR EN GEMINI]`) — esa evaluación se hace aquí, no después.
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
- **Sin texto en ilustraciones** salvo objetos cuya narrativa lo exige (recibos, portadas de libro).
- **Plan antes de ejecutar:** en modo batch ("produce 5 piezas"), mostrar la lista de temas seleccionados y esperar OK antes de generar. Pieza única: generar directo (la aprobación ocurre al revisar el brief).
- **Fail loudly:** ID no encontrado, archivo faltante, conteo que no cuadra → detenerse y reportar. Nunca aplicar un cambio silenciosamente incorrecto.
- **Un paso a la vez:** nunca pedir al usuario múltiples acciones manuales en un solo mensaje.
