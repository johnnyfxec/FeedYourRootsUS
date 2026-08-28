---
name: trend-scout
description: Cazador y traductor de tendencias virales para marcas de contenido en redes sociales. Busca sonidos, hashtags y formatos en ascenso en TikTok/Reels/Shorts filtrados por país e industria, los puntúa contra el avatar y los pilares de la marca, y los traduce a la arquitectura CRS (fase de embudo + hook verbal + formato) para que una skill productora los pueda producir directamente. Registra todo en la tabla Airtable Trend_Signals. Usar cuando el usuario pida "busca tendencias", "qué está viral en [industria]", "revisa sonidos trending", "dame señales de esta semana", "analiza este video viral" o "traduce esta tendencia a nuestro sistema". También se usa para deconstruir un video viral puntual (URL de TikTok/Reels/Shorts) en su estructura de hook, ritmo y audio usando yt-dlp + ffmpeg. Configurar primero brand.config.yaml antes del primer uso.
---

# Trend Scout

Skill 2 de un sistema de 3: **trend-scout** (esta) alimenta señales a la skill productora (ej. `fyr-content`); una tercera skill de performance (`performance-lens`, aún no construida) mide qué tendencias convirtieron y retroalimenta el score de afinidad de esta skill. Las tres se comunican SOLO a través de Airtable — nunca se invocan entre sí directamente.

## Principio rector

Una tendencia sin traducción es solo ruido. El trabajo de esta skill no es reportar "esto está viral" — es responder **"esto está viral, y si lo montáramos sería un Hook [X] en Fase [Y], y aquí está la frase exacta que lo conecta con nuestro avatar."** Si no se puede completar esa traducción, la señal no está lista para pasar a Aprobada.

---

## 0. Configuración (leer siempre primero)

Esta skill es portable entre marcas/industrias. Antes de cualquier búsqueda, leer `brand.config.yaml` en la raíz del repo activo (mismo nivel que `knowledge/`). Si no existe, **detenerse y pedirlo** — no asumir valores.

```yaml
brand: feed-your-roots
avatar: "Morgan, 28-42, suburbano US, busca soberanía alimentaria en poco terreno"
airtable_base: appMy5aOwifSbBLPR
pais: US
industria_creative_center: "Home & Garden"
plataformas: [TikTok, Instagram Reels]
pilares_path: knowledge/FYR_Malla_60_Temas_Virales_v2.md
hooks_path: knowledge/hooks_verbales_20_v2.md
crs_path: knowledge/Sistema_Maestro_CRS_v2.md
brand_bible_path: knowledge/Feed-Your-Roots-Brand-Bible.md
banned_words: true   # aplicar la lista de palabras prohibidas del Brand Bible al Brief_Adaptacion
```

Todo lo que sigue en esta skill usa estas variables — nunca hardcodear "FYR" ni "Morgan" fuera de este archivo de config.

---

## 1. Infraestructura Airtable

**Tabla `Trend_Signals`** — ver schema completo en `references/schema_trend_signals.md`. Antes del primer uso, confirmar que la tabla existe (buscarla por nombre en la base `airtable_base` del config). Si no existe, decirle al usuario que importe `Trend_Signals_Airtable_Import.csv` primero — no crearla vía API sin confirmación explícita.

**Tablas leídas (no modificadas por esta skill):** `Themes` — para verificar nombres exactos de `Pilar` y cruzar `Tema_Vinculado`.

**Regla de IDs:** antes de asignar un `Signal_ID` nuevo, consultar el último `TR-####` existente vía búsqueda en la tabla. Nunca adivinar el siguiente número.

---

## 2. Fuentes de datos

Ver `references/fuentes.md` para el detalle completo de cada fuente (URLs exactas, límites, qué requiere el usuario). Resumen de prioridad:

1. **TikTok Creative Center** vía `web_fetch`/`web_search` — gratis, sin configuración. Vía por defecto.
2. **trendsmcp.ai** vía MCP — gratis con cuenta, si está conectado (`tool_search` por "trends").
3. **Apify actors** — solo si el usuario confirma que los tiene conectados. Nunca asumir.
4. **yt-dlp + ffmpeg** (local, gratis) — para deconstruir un video puntual, no para descubrir tendencias nuevas.

**Regla de honestidad no negociable:** si ninguna fuente devuelve data verificable con fecha, decirlo explícitamente. Nunca presentar como "tendencia actual" algo recordado de entrenamiento sin verificar — eso es el error más caro que puede cometer esta skill, porque toda la cadena de valor depende de que la señal sea real.

---

## 3. Flujo A — Barrido de tendencias (uso semanal o bajo demanda)

### Paso 1 — Captura
Buscar en la(s) plataforma(s) y país/industria del config. Para cada señal candidata (sonido, hashtag o formato/ángulo narrativo repetido en varios videos top), registrar: nombre, plataforma, curva de momentum (ascendente/meseta/descendente) y volumen si está disponible.

Capturar 8-15 candidatas crudas antes de filtrar — mejor exceso que quedarse corto.

### Paso 2 — Filtro de afinidad (Score_Afinidad_Avatar)
Para cada candidata, puntuar 1-5 contra el avatar del config:
- **5** — el ángulo de dolor/deseo de la tendencia coincide casi literal con un pilar existente.
- **3-4** — el formato o mecánica es transferible aunque el tema original no lo sea (ej. un "antes/después" viral de fitness → transferible a "antes/después de tener un plan de siembra").
- **1-2** — solo comparte plataforma/formato genérico, sin conexión real de dolor/deseo. Descartar salvo que el usuario pida ver todo.

Solo las candidatas con score ≥3 avanzan al Paso 3. Las descartadas no se registran en Airtable (evitar ensuciar la tabla con ruido) — se pueden mencionar en el resumen de la conversación si el usuario quiere verlas.

### Paso 3 — Traducción CRS (el paso que no se puede saltar)
Para cada señal que avanza, leer `hooks_path` y `crs_path` del config y completar:
- **Hook_CRS_Equivalente**: ¿qué hook verbal de los 20 describe mejor por qué esta tendencia detiene el scroll? (ej. un formato de "revelación tardía" → Hook 12 Curiosidad o Hook 20 Revelación).
- **Fase_Embudo_Sugerida**: según la tabla de compatibilidad Hook×Fase ya definida en `crs_path`.
- **Pilar_Relacionado**: verificar contra `Themes` real en Airtable — nombre exacto, no de memoria.
- **Brief_Adaptacion**: 2-4 frases. Debe responder: ¿qué hace viral el formato original? ¿cómo se traduce al avatar y voz de la marca (leer `brand_bible_path`, aplicar `banned_words` si el config lo pide)? Si hay un video líder identificable, ofrecer deconstruirlo (Flujo B) antes de escribir el brief final — un brief basado en un video real siempre es mejor que uno inferido del nombre del hashtag.

Si no se puede completar el Hook_CRS_Equivalente con algo específico, la señal se registra igual pero con `Estado = Detectada` y una nota indicando que falta traducción — nunca forzar un hook que no calza solo por completar el campo.

### Paso 4 — Registro
Crear filas en `Trend_Signals` (batch ≤50, `typecast: true`). `Estado = Detectada` por defecto. Mostrar al usuario una tabla resumen (señal | score | hook | pilar | ventana de vida estimada) y esperar su decisión de cuáles pasan a `Aprobada` — **esto requiere confirmación explícita del usuario, nunca auto-aprobar.**

Al aprobar una señal: actualizar `Estado = Aprobada`, `Fecha_Aprobacion = hoy`, calcular y guardar `Fecha_Expiracion` según `Ventana_Vida_Estimada`.

---

## 4. Flujo B — Deconstrucción de un video puntual

Cuando el usuario da una URL específica ("analiza este video viral") o cuando el Paso 3 del Flujo A lo requiere:

1. Intentar subtítulos primero (gratis): `yt-dlp --write-auto-sub --sub-lang en --skip-download [URL]`.
2. Si no hay subtítulos y se necesita el hook verbal exacto, informar al usuario que requeriría Whisper/Groq (API key propia) — no bloquear, seguir solo con análisis visual si no la tiene.
3. Descargar y extraer frames por cambio de escena (no por segundo fijo, más barato):
   ```
   ffmpeg -i video.mp4 -vf "select='gt(scene,0.3)'" -vsync vfr frame_%03d.jpg
   ```
4. Leer los frames con `view` (son imágenes). Identificar: qué se ve en el segundo 0-3 (hook visual), ritmo de cortes, si hay texto en pantalla, paleta/mood.
5. Cruzar con el transcript (si existe) para completar el Question Test: *"cuando alguien ve los primeros 3 segundos, la pregunta exacta en su cabeza es: ___"*.
6. Esto alimenta directamente `Brief_Adaptacion` en el registro de la señal correspondiente.

**Regla ética:** el output es siempre una descripción en texto de la estructura (para inspirar una pieza propia), nunca el video o audio descargado se reutiliza, publica o distribuye. Borrar los archivos de video/audio descargados al terminar el análisis — solo conservar frames si el usuario pide verlos, y avisar que se van a borrar tras la sesión.

---

## 5. Módulo de conexión hacia la skill productora

Este es el punto de integración con `fyr-content` (o el nombre de la skill productora que use el `brand.config.yaml` activo). **Esta skill nunca invoca a la productora ni escribe en `Content_Pieces` o `Themes`** — solo deja la señal lista en `Trend_Signals` con `Estado = Aprobada`.

El cambio vive del lado de la skill productora (documentado ahí, no aquí): en su paso de selección de tema, debe consultar `Trend_Signals` filtrando `Estado = Aprobada` y `Fecha_Expiracion >= hoy`, y si encuentra alguna, ofrecer producir la pieza montada sobre esa señal (usando su `Hook_CRS_Equivalente`, `Formato_Sugerido` y `Brief_Adaptacion` como punto de partida) antes de caer al flujo normal de selección.

Cuando la productora efectivamente use una señal, debe escribir el `PZA-###` resultante de vuelta en `Content_Pieces_Generada` de esa fila — así el ciclo queda trazable de punta a punta. Si la skill productora no soporta esto todavía, no es bloqueante: la tabla `Trend_Signals` sigue siendo útil como banco de inspiración leído manualmente.

---

## 6. Módulo de conexión hacia la skill de performance (futura)

Reservado para `performance-lens`. Cuando exista, esa skill leerá `Content_Pieces.Performance` + `Trend_Signals.Content_Piece_Generada` para calcular qué tipo de señal (por `Tipo_Señal`, `Hook_CRS_Equivalente`, `Pilar_Relacionado`) convierte mejor, y escribirá el resultado de vuelta en `Resultado_Post_Uso` de la fila correspondiente. Esta skill no necesita hacer nada para habilitar eso — el schema ya lo soporta. No construir lógica de performance aquí.

---

## 7. Mantenimiento de señales expiradas

Al inicio de cualquier Flujo A, antes de capturar señales nuevas, revisar señales `Aprobada` con `Fecha_Expiracion` pasada y sin `Content_Piece_Generada`. Sugerir marcarlas `Expirada` (requiere confirmación del usuario, igual que cualquier cambio de estado en lote).

---

## 8. Reglas no negociables

- **Nunca inventar una tendencia.** Si no hay fuente verificable con fecha, decirlo — no rellenar con conocimiento genérico de entrenamiento.
- **Traducción antes que registro.** Una señal sin Hook_CRS_Equivalente ni Brief_Adaptacion no está lista para Aprobada.
- **Confirmación explícita** para: aprobar señales, marcar expiradas, y para cualquier escritura en lote en Airtable.
- **Nombres exactos cruzados con Airtable real**, nunca de memoria, para `Pilar_Relacionado` y `Hook_CRS_Equivalente`.
- **Fail loudly:** tabla no encontrada, config faltante, fuente sin datos → detenerse y reportar, nunca simular éxito parcial.
- **Borrar media descargada** al cerrar una deconstrucción de video (Flujo B) salvo que el usuario pida conservar los frames.
- **Un paso a la vez** — nunca pedir al usuario múltiples decisiones manuales en un solo mensaje.
