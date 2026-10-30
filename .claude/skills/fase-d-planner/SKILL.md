---
name: fase-d-planner
description: Orquestador de producción semanal en lote para FYR. Implementa las 5 paradas de Fase D (Parada 0 planificación + Paradas 1-4 de producción): propone la lista de temas del lote, agrupa las 4 aprobaciones de Johnny en bloque en vez de pieza por pieza, y maneja fallos aislados sin detener el lote. Usar cuando arranque la sesión semanal de planificación (disparo automático los lunes) o cuando Johnny diga "arranca el lote", "planifica la semana", "parada [N]" o "continúa el lote".
---

# FYR Fase D — Orquestador de producción semanal

## Principio rector

Un lote semanal tiene 5 paradas de aprobación de Johnny, no una por pieza. Nada se produce hasta que la lista de temas de la Parada 0 esté aprobada. Cada parada produce su output completo y espera aprobación en bloque antes de avanzar. Un fallo aislado no detiene el lote — la pieza se marca "necesita atención" y el resto sigue.

---

## 1. Infraestructura heredada

Todo lo definido en `.claude/skills/fyr-content/SKILL.md` (IDs de tablas Airtable, rutas de archivos, estados de `Content_Pieces`) es válido aquí y no se duplica. Leer ese archivo antes de cualquier operación sobre Airtable o el repo.

**Base Airtable:** `appMy5aOwifSbBLPR`
**Tabla `Trend_Signals`:** `tblxdaRsgEy8CHvV9`. Schema completo en `knowledge/FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` §5.

**Mezcla de fuentes objetivo (punto de partida, ajustable con datos reales):**
- ~70-80% banco de temas (Malla + temas nuevos de PDFs)
- ~10-20% `trend-scout` (señales aprobadas vigentes en `Trend_Signals`)
- Resto: actualidad, si algo relevante surgió esa semana (oportunista, puede ser 0%)

---

## 2. Parada 0 — Planificación semanal (la sesión arranca aquí)

Esta parada es el único output del disparo automático de los lunes. Nada más corre hasta que Johnny la apruebe.

### 2.0 ⛔ Gate obligatorio, antes de proponer ningún tema: cobertura de campos

**Correr primero, siempre, antes de cualquier otra cosa de esta Parada:**

```
AIRTABLE_API_KEY=<token> python3 production/scripts/governance/check_field_coverage.py
```

**Por qué va aquí y no al cierre del lote:** el incidente real que motivó esta regla (`Bundle Relacionado` vacío en 6 filas de `Themes`, 19-oct-2026) se detectó recién en una auditoría manual al final del lote completo — el hueco viajó sin detectarse durante Paradas enteras porque ninguna fila "buena" del mismo lote existía para compararla (ver §9 abajo y su límite estructural documentado ahí). Corriendo este chequeo **antes** de registrar la primera fila del lote, un campo real sin cobertura documentada detiene el lote en el primer segundo, no después de producir 7 piezas.

**Si el script termina con exit code ≠ 0:** el lote NO arranca. Reportar a Johnny la lista exacta de campos que imprimió el script (huérfanos reales = Airtable tiene un campo que ningún documento nombra; huérfanos documentados = un documento nombra un campo que ya no existe así en Airtable) y esperar instrucción — normalmente actualizar `knowledge/FYR_Rutas_De_Produccion.md` (prosa en §0.8 + el bloque `<!-- CAMPOS-DOCUMENTADOS -->` en su Sección 3) antes de continuar.

**Qué NO cubre este gate (para no sobre-confiar en él):** valida que todo campo real esté *nombrado* en la documentación — no valida que una fila específica de este lote lo haya *llenado* correctamente. Esa segunda verificación sigue siendo la auditoría dinámica de §9, que no se reemplaza, se complementa.

### 2.1 Señales de tendencia vigentes
Consultar `Trend_Signals` filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`. Listar las disponibles con su `Hook_CRS_Equivalente` y `Fase_Embudo_Sugerida`. Si no hay ninguna vigente, la fuente "tendencia" queda en 0% para este lote.

### 2.2 Actualidad relevante
Hacer una búsqueda web acotada: ¿hubo algún evento noticiable esta semana relacionado con soberanía alimentaria, jardines urbanos, cadenas de suministro alimentario o precios de supermercado en US? Si sí, proponer un tema de actualidad con su ángulo CRS (dolor/deseo traducido al avatar Morgan, Fase de Embudo, Hook sugerido). Si no hay nada relevante, esta fuente queda en 0% para el lote.

### 2.3 Propuesta de temas
Construir una tabla con todos los temas propuestos para el lote. Por cada tema:

| # | Tema (Número.Pilar) | Fuente | Fase Embudo | Hook sugerido | Señal TR (si aplica) | % cobertura assets |
|---|---|---|---|---|---|---|
| 1 | [número] — [título] | Banco / Tendencia / Actualidad | F1/F2/F3/F4 | [##] [nombre] | TR-#### o — | ~N% |

**Selección del banco:** consultar `Themes` para excluir los que ya tienen al menos una `Content_Pieces` vinculada (`Themes.Content_Pieces`, link inverso — fuente de verdad desde el rediseño Route B del 28-oct-2026, reemplaza al antiguo campo `Estado`). Preferir temas con mayor cobertura de assets existentes en `Assets` (calcular antes de proponer). Mantener la mezcla de fases cercana a 40/27/20/13. No repetir pilar en dos piezas consecutivas de la tabla.

**Tamaño inicial del lote:** proponer 5-8 temas para la primera corrida. El número definitivo lo calibra lo que Johnny pueda revisar en Parada 3 en una sola sesión — documentar ese dato al cerrar el primer lote real y actualizar `knowledge/FYR_Fase_D_Produccion_Recurrente_v1.md` §2.3 con el número calibrado.

### 2.4 ⛔ PARADA 0 — Esperar aprobación de Johnny
Presentar la tabla, esperar respuesta. Johnny puede:
- **Aprobar tal cual** → continuar a Parada 1
- **Pedir cambios puntuales** ("quita el 3, agrega algo de X") → ajustar la tabla y re-presentar
- **Aplazar la semana** → confirmar y cerrar la sesión sin producir nada

**Nada se produce hasta que esta parada esté aprobada.**

---

## 3. Parada 1 — Briefs en bloque

Para cada tema aprobado en Parada 0, generar el brief completo siguiendo los **Pasos 1-5 de `fyr-content/SKILL.md`** (Question Test, construcción del hook, copy CRS, tabla slide-por-slide, formato + JSON de pieza). Completar TODO el lote antes de presentar nada.

**Output de esta parada:**
- Todos los archivos `production/pieces/PZA_[tema]/brief.md` escritos en el repo
- Todos los `production/pieces/PZA_[tema]/config.json` (carrusel) o `production/pieces/PZA_[tema]/pieza_[tema].json` (video) escritos
- Una tabla resumen del lote:

| # | PZA | Tipo | Hook | Formato | # slides / seg | Q-Test | Estado |
|---|---|---|---|---|---|---|---|
| 1 | PZA_X.Y | Carrusel/Video | 07 Contraste | Carrusel | 8 slides | ✓ | Listo |

**Manejo de fallos:** si para una pieza específica el Question Test no produce una pregunta clara, o el tema resulta inviable por falta de información, marcarla como `necesita atención — [razón]`. El resto del lote sigue.

Si el tema usa una señal de `Trend_Signals` (fuente=Tendencia), usar su `Hook_CRS_Equivalente`, `Formato_Sugerido` y `Brief_Adaptacion` como punto de partida del Paso 1, en vez de partir de cero.

### 3.1 ⛔ PARADA 1 — Esperar aprobación de Johnny
Presentar la tabla resumen. Johnny aprueba en bloque o señala piezas puntuales a corregir. Las piezas corregidas se re-presentan; el resto del lote sigue avanzando en paralelo.

Escribir en `Content_Pieces` (crear la fila si no existe) con `Estado Producción = Brief Generado` para cada pieza aprobada.

**Antes de cerrar esta Parada: auditoría obligatoria §9** sobre `Content_Pieces` (`Copy Completo`, `Ruta .md`/`Ruta JSON`, `CTA Sugerido` y el resto de campos de la Sección 3 de `fyr-content/SKILL.md`) y, si el tema es nuevo, también `Themes` (Número, Pilar, Dolor/Deseo, Prioridad, Hook Asignado — único rol de `Themes` desde el rediseño Route B del 28-oct-2026, ver `fyr-content/SKILL.md` §1). Reportar el resultado.

---

## 4. Parada 2 — Assets en bloque

Para todo el lote de una vez:

**4.1 Reutilización primero**
Para cada pieza, mapear qué slides pueden resolverse con assets ya existentes en `Assets` (sin `En descanso`). Calcular % de cobertura por pieza según `knowledge/FYR_Plan_Reutilizacion_y_Serie_Botanica.md`.

**4.2 Lista consolidada de gaps**
Un único listado de todas las imágenes que NO existen y deben generarse en Gemini. No generar aquí — solo producir la lista para aprobación:

| PZA | Slide # | Descripción del contenido | Prompt Gemini (listo para pegar) | Aspecto | Nombre de archivo destino |
|---|---|---|---|---|---|

Usar las convenciones de nomenclatura de `knowledge/FYR_Asset_Governance_Policy.md`. **El "Prompt Gemini (listo para pegar)" de cada fila debe cumplir las reglas de `fyr-content/SKILL.md` y de `FYR_Asset_Governance_Policy.md` §4** (bloque de estilo base textual, línea de output con PNG + ratio correcto por layout, nunca texto editorial/operacional dentro del prompt citado) — no reconstruir el prompt de memoria ni tomar como referencia un brief anterior sin verificar que ya tenga estas reglas aplicadas.

**Error real detectado (19-oct-2026, primer lote): la lista de gaps omitió las 4 portadas de video del lote.** Un video usa `marco_grande_cuadrado` (reutilizable) para su portada, pero ese marco solo trae la vid/hoja pintadas — tiene una ventana interior 1:1 (722×728) vacía que necesita su propia imagen de escena nueva, igual que cualquier otro beat. Confundir "el layout de portada ya existe" con "la imagen de la portada ya existe" dejó 4 piezas (todas las de video del lote) sin su gap de portada listado. **Regla:** al construir la tabla de gaps, leer la sección "Prompts nuevos a generar" de cada `brief.md` **completa, de inicio a fin** (incluida cualquier entrada marcada "Portada (beat 1, 1:1, ventana del marco...)") — nunca inferir desde el nombre del layout si una imagen de escena ya existe o no. Las imágenes de portada 1:1 se registran en `Assets` igual que cualquier escena nueva (misma carpeta `06_Narrative_Stock/`), pero NO se vinculan a `Content_Pieces` como "asset usado" de un slide normal — son insumo de la ventana del marco, no un beat narrativo independiente.

**4.3 Piezas con 0% de gaps** pasan directamente a "Assets resueltos" sin acción adicional.

**4.3-bis Verificación obligatoria contra la Mesa de Producción (incidente 19-oct-2026, ver `FYR_Asset_Governance_Policy.md` §6-bis):** antes de presentar la lista de gaps en la Puerta de Parada 2, para cada pieza cuyo `brief.md` haya sido tocado por un commit de OTRA sesión de Claude (distinto `Claude-Session:` en `git log`) después de que Johnny empezara a generar imágenes de esa pieza, **no asumir que `brief.md` refleja lo que Johnny realmente ve/generó** — pedir confirmación explícita (captura o descripción de la Mesa) antes de incluir esa pieza en la lista de gaps o de registrar nada en Airtable. Un `brief.md` internamente consistente no es evidencia de que esté sincronizado con la Mesa.

### 4.4 ⛔ PARADA 2 — Esperar aprobación de Johnny
Johnny confirma la lista de imágenes a generar (o las genera en ese momento con los prompts de la tabla). Una vez todas las imágenes existen en Drive y están registradas en `Assets` con su `Link Drive`, esta parada cierra.

Actualizar `Content_Pieces.Estado Producción` → `Assets en Drive` para cada pieza resuelta.

**Manejo de fallos:** si una imagen específica no se puede generar, marcar esa pieza como `necesita atención — [razón]` y continuar con las demás.

**Antes de cerrar esta Parada: auditoría obligatoria §9** sobre `Assets` — especialmente si el registro ocurrió en más de una pasada (ej. assets narrativos del cuerpo en una pasada, portadas 1:1 de video en otra). Verificar campo por campo que todas las filas nuevas o tocadas tengan el mismo patrón completo (`Content_Pieces`, `Veces usado`, `Último uso`, `En descanso`), no solo los campos descriptivos. Reportar el resultado.

---

## 5. Parada 3 — Revisión visual final

Con todos los assets resueltos, ensamblar todo el lote:

**Carruseles:** correr `assemble.py` con el `config.json` de cada pieza. Output: N PNGs en `production/pieces/PZA_[tema]/`.

**Videos:** disparar GitHub Actions (`render-video.yml`) con el `pieza_[tema].json` de cada video. No esperar de forma sincrónica — dejar correr, verificar que el MP4 llegó a Drive antes de cerrar la parada.

Subir todos los assets terminados a Drive (`Content_Pieces/PZA_[tema]/[fecha]/`). Actualizar `Content_Pieces.Estado Producción` → `Ensamblado` y `Content_Pieces.Carpeta Drive` → URL de la carpeta.

Presentar **una lista del lote con links a Drive** para que Johnny revise en una sola sesión:

| # | PZA | Tipo | Link Drive | Estado |
|---|---|---|---|---|
| 1 | PZA_X.Y | Carrusel | [link] | Listo para revisión |

**Manejo de fallos:** si un render falla o `assemble.py` devuelve error para una pieza, marcarla `necesita atención — [error exacto]` y continuar con el resto. No detener el lote.

### 5.1 ⛔ PARADA 3 — Esperar aprobación de Johnny
Esta es la parada de mayor atención — el producto terminado. Johnny revisa cada pieza en Drive y da OK o solicita correcciones. Piezas corregidas se re-ensamblan; el resto sigue.

**Antes de cerrar esta Parada: auditoría obligatoria §9**, con atención especial a cualquier archivo que haya cambiado de ruta durante el ensamblado (ej. de `production/pieces/` a `production/scripts/video/` para video) — la `Ruta .md`/`Ruta JSON` en Airtable se actualiza en el mismo momento del movimiento, y se verifica aquí que de verdad quedó así. Reportar el resultado.

---

## 6. Parada 4 — Cierre del lote (NO es publicación)

**Corrección 28-oct-2026 (Johnny):** esta Parada terminaba antes en "publicar" como si fuera un paso que `fase-d-planner` ejecuta — no lo es. Ninguna skill de FYR publica en redes sociales hoy, ni de forma automática ni manual: esa responsabilidad es de una skill futura (`fyr-publisher`, diseño en `knowledge/FYR_Plan_Publicacion_Automatizada_v1.md`/`v2.md`, no construida). `fase-d-planner` cierra el lote en `Ensamblado`, no en `Publicado`.

Por cada pieza aprobada en Parada 3:

1. Verificar que el archivo final está en Drive en `Content_Pieces/PZA_[tema]/[fecha]/` con el nombre correcto, y que `Content_Pieces.Estado Producción = Ensamblado` (ya escrito en Parada 3 — esta Parada no lo cambia).
2. **No tocar ninguno de estos campos:** `Estado Producción = Publicado`, `Fecha de Publicación`, `Fecha Publicación Programada`, `Estado IG/FB/Pinterest/YouTube/TikTok`, `Post ID [red]`, `Link Publicación [red]`. Pertenecen al dominio de `fyr-publisher`, que no existe todavía.
3. Si la pieza usó una señal de tendencia: buscar en `Content_Pieces` el registro cuyo `ID Pieza = PZA_[tema]` para obtener su `recXXXXXXXXXXXXXX`; escribir ese record ID en `Trend_Signals.Content_Piece_Generada` de la fila correspondiente (`multipleRecordLinks` — nunca el string visible). Cambiar `Estado` → `Usada` (esto registra que la señal se usó para producir, no que la pieza se publicó). Ver `trend-scout/references/schema_trend_signals.md` para la regla completa sobre campos Link.

**`Themes` no se toca en esta Parada** — desde el rediseño Route B (28-oct-2026), `Themes` ya no guarda estado de uso ni datos de ninguna pieza concreta (se eliminó el campo `Estado`). La señal de "este tema ya se produjo" es el link `Themes.Content_Pieces` (inverso), que se llena en el momento en que se crea la fila de `Content_Pieces` (Apertura de la pieza, Parada 1/2 al aprobar el brief) — nunca algo que Parada 4 deba poner o corregir.

**Cierre del lote — presentar resumen:**

| Resultado | Piezas | Detalle |
|---|---|---|
| ✓ Ensambladas, listas para publicar | N | Lista de PZAs |
| ⚠ Necesita atención | N | Lista de PZAs con razón → pasan a cola semana siguiente |

Documentar el **tamaño del lote** y el **tiempo aproximado de la Parada 3** en `knowledge/FYR_Fase_D_Produccion_Recurrente_v1.md` §2.3 si es la primera corrida real.

### 6.1 ⛔ PARADA 4 — Confirmación final de Johnny

**Antes de cerrar esta Parada (y el lote completo): auditoría obligatoria §9 final**, cubriendo TODAS las filas tocadas en TODAS las Paradas del lote — esta es la última oportunidad de detectar un hueco que haya pasado las auditorías parciales de Paradas anteriores. Reportar el resultado explícitamente antes de dar el lote por cerrado.

---

## 7. Recuperación de estado entre sesiones

Si la sesión de Claude Code se interrumpe entre paradas, reconstruir el estado así:
1. Consultar `Content_Pieces` filtrando `Fecha de Generación` de esta semana.
2. Leer `Estado Producción` de cada fila para saber en qué parada está cada pieza.
3. Retomar desde la parada más baja en común (si hay piezas en estados distintos, la parada del lote es la del más retrasado).
4. Avisar a Johnny: "Retomando lote — N piezas en [estado], continuando desde Parada [X]."

---

## 8. Reglas no negociables

- Nunca producir nada antes de Parada 0 aprobada.
- Fail loudly: tabla de Airtable no encontrada, config faltante, Drive no accesible → detenerse y reportarlo, nunca simular éxito parcial.
- Ningún asset nuevo entra a una pieza sin estar registrado en `Assets` con su `Link Drive`.
- Todo archivo que debe sobrevivir entre sesiones va a Git o Drive, nunca solo local (`production/pieces/PZA_[tema]/` en el repo para briefs y configs; Drive para imágenes y videos terminados).
- Esta skill no invoca a `trend-scout`, `fyr-content` ni `fyr-video-assembler` directamente — lee sus SKILL.md y sigue sus pasos, y se comunica con `trend-scout` únicamente leyendo `Trend_Signals` de Airtable.
- Un fallo aislado nunca detiene el lote — la pieza se marca "necesita atención" y el lote sigue.
- `typecast: true` en todas las escrituras a singleSelect/multipleSelects de Airtable.
- **Ningún hueco de documentación queda abierto al cerrar una Parada — ver §9, auditoría obligatoria.**

## 9. Auditoría obligatoria de Airtable al cierre de cada Parada (19-oct-2026, no negociable)

**Por qué existe esta regla:** en el primer lote real (7 piezas), una auditoría manual pedida por Johnny al final encontró 4 tipos de huecos que llevaban abiertos desde Parada 2/3: assets de portada sin `Content_Pieces`/`Veces usado`/`Último uso`/`En descanso`, `Copy Completo` vacío en las 7 piezas desde Parada 1, `Ruta JSON` apuntando a una ruta que dejó de existir tras mover archivos, y `Bundle Relacionado` vacío en las 6 filas de `Themes` nuevas. Causa raíz: cuando el registro de una pieza ocurre en más de una pasada (ej. Parada 2 para carruseles/assets narrativos y Parada 3 Ruta B para portadas de video, en momentos distintos), es fácil llenar los campos de esa pasada específica y olvidar replicar el patrón completo que sí se aplicó en la otra pasada. Esperar a una auditoría final de "todo el lote" significa que el hueco viaja sin detectarse durante Paradas enteras.

**No es una checklist fija — es un método.** Johnny (19-oct-2026): "una auditoría comprensiva de TODOS los campos recientemente utilizados en la pasada actual", no solo los 4 campos que fallaron la primera vez. Los campos de abajo (`Veces usado`, `Copy Completo`, `Ruta JSON`, `Bundle Relacionado`...) son el ejemplo concreto que motivó la regla, no la lista completa de lo que hay que mirar — si en un lote futuro se toca cualquier otro campo (`Performance`, `Hook Usado`, `Audiencia`, uno que no exista todavía), la auditoría lo cubre igual, porque el método no depende de nombrar el campo de antemano.

**Regla (método dinámico, aplica a cualquier campo, presente o futuro):** antes de dar CUALQUIER Parada por cerrada (no solo la última), para cada tabla de Airtable tocada en esa Parada (`Assets`, `Content_Pieces`, `Themes`, y cualquier otra que se use a futuro):

1. **Listar, de las filas tocadas en esta pasada, TODOS los campos que tienen al menos una fila con valor no vacío** — sin filtrar de antemano cuáles "importan". Ese listado es el patrón real que esta pasada usó.
2. **Para cada fila tocada, comparar contra ese patrón:** ¿tiene valor en todos los campos que el patrón dice que debería tener? Una fila con un campo vacío que SÍ está lleno en las demás filas del mismo tipo (misma tabla, mismo lote, mismo tipo de pieza — video vs. carrusel si aplica) es un hueco, sin importar qué campo sea.
3. **Atención especial cuando el registro de una pieza ocurrió en más de una pasada** (ej. assets del cuerpo en Parada 2, portada en Ruta B de Parada 3): comparar la fila de esa pasada tardía contra el patrón de la pasada temprana, no asumir que "ya se aplicó antes" solo porque el resto del lote lo tiene.
4. **Atención especial a rutas de archivo** (`Ruta .md`, `Ruta JSON`, `Link Drive`): si un archivo cambió de ubicación en cualquier commit posterior a su registro inicial, verificar que la ruta en Airtable sea la REAL en este momento, no la de cuando se escribió por primera vez. **Un campo de ruta "lleno" no es lo mismo que un campo correcto (corrección 30-oct-2026, hueco real encontrado en PZA_1.1 y PZA_4.2 — ver `CHANGELOG.md`):** el punto 2 de este método compara solo si el campo tiene *algún* valor, no si ese valor apunta a algo que existe de verdad. Para todo campo que sea una ruta de archivo o un `drive_id`/file id, verificar explícitamente que el archivo exista en ese momento (`Read`/`ls` para rutas del repo, `get_file_metadata` para IDs de Drive) — un campo "lleno" con una ruta que nunca se creó (no solo una que se movió) es el mismo tipo de hueco que un campo vacío, y pasa desapercibido si solo se mira "¿tiene texto o no?".
5. **Si la taxonomía de un campo (sus choices de singleSelect/multipleSelects) no cubre un valor real** (ej. un pilar nuevo sin opción de `Bundle Relacionado` equivalente en `Themes`, ver `fyr-content/SKILL.md` §1 — y `Bundle Relacionado` es un campo real y propio, DISTINTO de `Content_Pieces.CTA Sugerido`, corrección 27/28-oct-2026, no confundirlos): no aproximar a la opción más cercana en silencio — crear la opción correcta con `typecast: true` (reportando a Johnny qué opción se creó) o preguntar antes de aproximar.
6. **Reportar la auditoría explícitamente** en el cierre de la Parada, aunque no haya encontrado nada — nombrando qué tablas y qué patrón de campos se verificó, no solo "todo bien": nunca pasar a la siguiente Parada en silencio asumiendo que quedó completo.
