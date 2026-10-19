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

### 2.1 Señales de tendencia vigentes
Consultar `Trend_Signals` filtrando `Estado=Aprobada` y `Fecha_Expiracion >= hoy`. Listar las disponibles con su `Hook_CRS_Equivalente` y `Fase_Embudo_Sugerida`. Si no hay ninguna vigente, la fuente "tendencia" queda en 0% para este lote.

### 2.2 Actualidad relevante
Hacer una búsqueda web acotada: ¿hubo algún evento noticiable esta semana relacionado con soberanía alimentaria, jardines urbanos, cadenas de suministro alimentario o precios de supermercado en US? Si sí, proponer un tema de actualidad con su ángulo CRS (dolor/deseo traducido al avatar Morgan, Fase de Embudo, Hook sugerido). Si no hay nada relevante, esta fuente queda en 0% para el lote.

### 2.3 Propuesta de temas
Construir una tabla con todos los temas propuestos para el lote. Por cada tema:

| # | Tema (Número.Pilar) | Fuente | Fase Embudo | Hook sugerido | Señal TR (si aplica) | % cobertura assets |
|---|---|---|---|---|---|---|
| 1 | [número] — [título] | Banco / Tendencia / Actualidad | F1/F2/F3/F4 | [##] [nombre] | TR-#### o — | ~N% |

**Selección del banco:** consultar `Themes` para excluir los ya `Usado`. Preferir temas con mayor cobertura de assets existentes en `Assets` (calcular antes de proponer). Mantener la mezcla de fases cercana a 40/27/20/13. No repetir pilar en dos piezas consecutivas de la tabla.

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

---

## 6. Parada 4 — Publicación y cierre

Por cada pieza aprobada en Parada 3:

1. Verificar que el archivo final está en Drive en `Content_Pieces/PZA_[tema]/[fecha]/` con el nombre correcto.
2. Actualizar `Content_Pieces.Estado Producción` → `Publicado`.
3. Actualizar `Themes.Estado` → `Usado` + `Fecha de uso` → hoy.
4. Si la pieza usó una señal de tendencia: buscar en `Content_Pieces` el registro cuyo `ID Pieza = PZA_[tema]` para obtener su `recXXXXXXXXXXXXXX`; escribir ese record ID en `Trend_Signals.Content_Piece_Generada` de la fila correspondiente (`multipleRecordLinks` — nunca el string visible). Cambiar `Estado` → `Usada`. Ver `trend-scout/references/schema_trend_signals.md` para la regla completa sobre campos Link.

**Cierre del lote — presentar resumen:**

| Resultado | Piezas | Detalle |
|---|---|---|
| ✓ Publicadas | N | Lista de PZAs |
| ⚠ Necesita atención | N | Lista de PZAs con razón → pasan a cola semana siguiente |

Documentar el **tamaño del lote** y el **tiempo aproximado de la Parada 3** en `knowledge/FYR_Fase_D_Produccion_Recurrente_v1.md` §2.3 si es la primera corrida real.

### 6.1 ⛔ PARADA 4 — Confirmación final de Johnny

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
