# FYR — Fase D: Producción recurrente en Claude Code (diseño)
**Versión 1.0 — 16 de octubre 2026**
**Estado: implementado (16-oct-2026). Skill `fase-d-planner` creada en `.claude/skills/fase-d-planner/SKILL.md`. Trigger semanal activo (lunes 8:46 AM ET). Pendiente de probar con la primera corrida real — esa corrida calibra el tamaño definitivo del lote (§2.3).**

**Propósito:** llevar la producción de FYR de "una pieza a la vez, conversacional, en este sandbox" a "lotes semanales en Claude Code, con Johnny presente pero concentrando su revisión en 5 paradas en vez de aprobar cada paso de cada pieza". Este documento es el contrato de diseño — se edita in-place cuando algo cambie, no se le agregan entradas tipo changelog.

**Contexto previo necesario:** este diseño se apoya en la arquitectura ya descrita en `FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` (las 3 skills, por qué nunca se invocan entre sí, el módulo de conexión trend-scout→fyr-content ya escrito en el Paso 0 de `fyr-content`). Fase D no reemplaza esa arquitectura — la activa a escala semanal y le agrega la fuente de actualidad, que hoy no existe.

---

## 1. Por qué existe este documento

Los dos pilotos (PZA_1.2 carrusel, PZA_4.2 video) probaron que el pipeline técnico funciona de punta a punta: brief → assets → ensamblado → Drive → Airtable. Lo que no existe todavía es el proceso de **producir a volumen sin que Johnny tenga que estar aprobando cada paso de cada pieza** — con el patrón actual (4 pausas por pieza), 20 piezas significan ~80 aprobaciones en una sesión. Fase D resuelve esto con dos cambios: (a) una capa de planificación semanal que decide QUÉ producir y POR QUÉ antes de producir nada, y (b) agrupar las aprobaciones por lote en vez de por pieza.

---

## 2. Planificación semanal — qué se produce y por qué (Parada 0)

### 2.1 Las 3 fuentes de contenido, y qué rol cumple cada una

| Fuente | Responde a | Qué aporta | Peso en la mezcla semanal |
|---|---|---|---|
| **Banco de temas** (Malla de 61 + temas nuevos extraídos de los PDFs) | "Qué sabemos que funciona / qué cubre el método completo" | Autoridad, vende el producto directamente, es evergreen | La columna vertebral — mayoría del lote |
| **`trend-scout`** (viralidad) | "Qué está funcionando AHORA en el algoritmo" | Alcance — atrae audiencia nueva que el banco solo no alcanzaría | Minoría deliberada, oportunista |
| **Actualidad** | "Qué está pasando en el mundo que conecta con el nicho" | Relevancia/timing — el canal se siente vivo, no solo evergreen | Oportunista, no planificable de antemano (reacciona a eventos reales) |

Ninguna fuente reemplaza a las otras. Un lote 100% banco se siente estático; un lote 100% tendencia pierde la columna vertebral de autoridad que vende el producto. La mezcla es deliberada, no un azar de "¿qué hago hoy?".

**Punto de partida de referencia** (ajustable con datos reales, no una regla rígida): de un lote de N piezas, ~70-80% banco de temas, ~10-20% trend-scout, el resto actualidad si algo relevante surgió esa semana. Este reparto se recalibra según lo que uno vaya aprendiendo en `performance-lens` cuando exista (ver §6 de `FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` — no se construye hasta tener ~10 piezas publicadas con datos reales).

### 2.2 Disparo: automático, todos los lunes

Un trigger programado arranca la sesión de planificación cada lunes (hora a definir con Johnny al implementar). Esa sesión:

1. Corre `trend-scout` para traer señales vigentes (`Estado=Aprobada`, `Fecha_Expiracion >= hoy` en `Trend_Signals`).
2. Revisa si hubo algo de actualidad relevante para el nicho esa semana (búsqueda puntual, no un feed automatizado — esto es nuevo, no existía antes de Fase D).
3. Propone una lista de temas para el lote, con la fuente de cada uno marcada (banco / tendencia / actualidad) y la fase de embudo que cubre cada uno.
4. **Se detiene y espera la aprobación de Johnny antes de generar un solo brief.** Johnny puede aprobar tal cual, pedir cambios puntuales ("quita el 7, agrega algo de X"), o aplazar la semana completa.

Esto es la Parada 0: nada se produce hasta que la lista de temas de la semana está aprobada.

### 2.3 Tamaño del lote: no fijo, se calibra con la primera corrida real

No se fija un número arbitrario de piezas por semana de antemano. El tamaño real lo determina cuánto le toma a Johnny revisar la Parada 3 (revisión visual final) completa en una sesión razonable — si 20 piezas resultan demasiado para revisar de una sentada, el lote baja; si sobra margen, sube. La primera corrida real de Fase D es, en sí misma, el experimento que calibra este número — se documenta el resultado en este archivo una vez medido.

---

## 3. Formato por pieza: carrusel o video, según el contenido — no por plataforma

Decisión explícita (16-oct-2026): **no se fuerza todo a un formato único para cubrir YouTube.** El formato lo decide qué cuenta mejor esa historia:

- **Carrusel** cuando el valor está en poder releer/pausar en un dato concreto: listas, comparaciones, antes/después, pasos numerados.
- **Video narrado** cuando el valor está en el arco emocional y el ritmo de revelación: storytelling, resultados/transformación — el loop de curiosidad de los hooks verbales no se replica igual en estático.

Esto ya es la lógica de afinidad Hook→Layout que existe en `fyr-content` (Paso 2) — Fase D no la cambia, solo la hereda tal cual para decidir el formato de cada tema de la semana.

**YouTube se puebla como efecto secundario, no como objetivo forzado.** Con la mezcla natural de hooks, una fracción significativa del lote (estimado ~40-60%, a confirmar con datos reales) termina siendo video 9:16 — el mismo MP4 que ya se sube para TikTok/Reels se publica también en YouTube Shorts sin producción adicional. Si con el tiempo los datos muestran que vale la pena producir específicamente para YouTube, se revisita esta decisión con evidencia, no antes.

---

## 4. Las 4 paradas de producción (después de la Parada 0)

Una vez aprobada la lista de temas de la semana, el lote avanza por 4 paradas de aprobación en bloque, no una por pieza:

### Parada 1 — Briefs
Se generan TODOS los briefs del lote (temas, hooks, copy) de una sola vez, usando `fyr-content` para cada tema (montado sobre la señal de trend-scout cuando aplique, vía el Paso 0 que ya existe). Se presentan juntos — una tabla o resumen del lote completo, no un mensaje por pieza. Johnny aprueba en bloque o señala piezas puntuales a corregir; el resto del lote sigue avanzando mientras esas se ajustan.

### Parada 2 — Assets
Se resuelven todos los assets necesarios para el lote completo: reutilización del banco primero (según `FYR_Plan_Reutilizacion_y_Serie_Botanica.md`), y una lista única y consolidada de lo que falta generar en Gemini (si algo falta), en vez de pedir imágenes una por una a lo largo del proceso.

### Parada 3 — Revisión visual final
Se ensamblan todos los carruseles y se renderizan todos los videos del lote. Se presentan juntos para revisión — esta es la parada donde más vale la pena que Johnny mire cada pieza con cuidado, porque es el producto terminado, pero sigue siendo una sola sesión de revisión del lote, no interrupciones repartidas a lo largo de días.

**Manejo de fallos puntuales (clave para volumen):** si una pieza específica falla en cualquier punto (un asset no cuadra, un render de Actions falla, una validación no pasa), esa pieza se marca como "necesita atención" y el resto del lote sigue su curso normal — no se detiene el lote completo por un problema aislado. Esto es automático, no una decisión que Johnny deba tomar cada vez que algo falla.

### Parada 4 — Publicación y cierre
Confirmación de que todo lo aprobado en Parada 3 está subido a Drive, registrado en Airtable (`Estado Producción = Publicado`), y lista de qué quedó pendiente de la semana (piezas marcadas "necesita atención" que no se resolvieron a tiempo pasan a la cola de la semana siguiente, no se descartan).

---

## 5. Lo que Fase D NO resuelve todavía (deliberadamente fuera de alcance)

- **Alertas/notificaciones de fallos sin supervisión** (lo que iba a ser "Fase C"): mientras el modo de trabajo siga siendo síncrono (Johnny presente durante la producción del lote), un fallo se ve en el momento. Esto se retoma cuando el patrón cambie a disparar trabajo en paralelo/background sin nadie mirando activamente — probablemente cuando el volumen semanal crezca más allá de lo que una sesión síncrona puede cubrir cómodamente.
- **Verificación de la app OAuth en Google para salir de "Testing"** (lo que iba a ser "Fase B"): descartada — cada proyecto/marca nace con su propio client OAuth y su propio test user, el límite de 1 test user por app nunca se vuelve cuello de botella en ese modelo.
- **`performance-lens`**: no se construye hasta tener ~10 piezas publicadas con datos reales de performance (regla ya establecida en `FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md` §6). Fase D produce el volumen que eventualmente da esos datos, pero no incluye la skill de medición en sí.
- **Separación motor/config de marca para white-label**: mencionada como visión de largo plazo en sesiones anteriores, explícitamente fuera del alcance de Fase D. Se retoma después de que el modelo de lote semanal esté probado y estable con FYR.

---

## 6. Próximo paso

Implementar esto en Claude Code: el trigger semanal de planificación, y el flujo de las 4 paradas operando sobre un lote real (tamaño a determinar en la primera corrida, ver §2.3). La primera corrida real de Fase D sirve además como la prueba de volumen que Johnny pidió — "varios temas con imágenes y videos para ver cuál es el orden óptimo".
