# FYR — Protocolo de Edición de Video
**Versión 1.0 — 10 de octubre de 2026**
**Propósito:** que cualquier sesión de Claude (chat o Claude Code) o cualquier persona pueda producir un video 9:16 de FYR —voz, subtítulos palabra por palabra, movimiento y render— sin reconstruir las decisiones tomadas en el piloto PZA_4.2. Se edita en su sitio cuando algo cambia (se reescribe la sección afectada, nunca se anexan entradas al final).

**Cómo leer los estados:** cada regla lleva un estado. **VALIDADO** = probado de punta a punta en el piloto y aprobado por Johnny. **EN PRUEBA** = decidido como variable a comparar, sin resultado todavía. **PENDIENTE** = identificado, no construido. Nada marcado VALIDADO se cambia sin una prueba nueva que lo supere.

**Alcance:** videos hechos de imágenes fijas 9:16 + voz narrada (cuenta regresiva, storytime, POV narrado). No cubre video generado por IA (clips animados) ni carruseles estáticos (ver `FYR_Motor_Ensamblado_Arquitectura_v1.md`).

---

## 1. Arquitectura del pipeline (VALIDADO)

```
brief aprobado (fyr-content)
   └─► pieza_X.json  (guion narrado + imágenes + voz)
          └─► tts.mjs     Google Cloud TTS (SSML con marcas) ─► build/audio/slide_N.wav + build/timings.json
                 └─► render.mjs   Clipkit renderer (self-hosted, Node) ─► salida/PZA_X__sub<VARIANTE>.mp4
                        └─► revisión (con loop activado) ─► Drive ─► Airtable
```

- **Dónde corre:** GitHub Actions (workflow `Render video`, `.github/workflows/render-video.yml`), sobre la carpeta `production/scripts/video/pza-[tema]/`. Las dependencias (`@clipkit/renderer`, `@google-cloud/text-to-speech`) se instalan en el runner con `npm ci`. No hay PC en el flujo (retirada el 14-oct-2026).
- **Qué NO se versiona** (`.gitignore` de la carpeta): `node_modules/`, `build/`, `salida/`, `img/*.png|jpg`, `fonts/*.ttf|otf`. Las credenciales de Google (`GOOGLE_APPLICATION_CREDENTIALS`, archivo JSON fuera del repo) **nunca** se commitean.
- **Flujo de archivos:** scripts y configuración por repo (Claude → push a `main`); imágenes y video por Google Drive (el workflow baja las imágenes por ID y sube el MP4 a `Content_Pieces`). Paso a paso: `knowledge/FYR_Rutas_De_Produccion.md`, Ruta B.
- **Costo de render:** cero (minutos gratuitos de Actions en un repo público). El piloto tardó ~37 s de render en local; en Actions la corrida completa (instalación, voz y render) toma unos minutos.
- **Limitación actual:** `tts.mjs` y `render.mjs` leen `pieza_4.2.json` fijo; para otra pieza se copia la carpeta y se renombra el JSON. PENDIENTE: motor único con `--pieza`.

---

## 2. Anatomía de una pieza de video

La unidad de trabajo es el **slide-beat**: una imagen 9:16 + una línea de narración + subtítulos + un movimiento de cámara. (Ver `FYR_Principios_De_Composicion.md` Sección 7, Fase 4.)

| Regla | Estado |
|---|---|
| **Slide 1 = portada** (`TPL-video-cover-framed.png`): estática, sin subtítulos, sin zoom. Es el único slide donde importan las zonas seguras de plataforma. | VALIDADO |
| **Slides 2–N:** imagen `full_bleed` al 100 % de intensidad (nunca atenuada) con zoom lento y subtítulos. | VALIDADO |
| **Cuenta regresiva** (5→1): se narra ("Number five…") pero **no se muestran numerales** en pantalla. | VALIDADO |
| **Texto horneado en la imagen** (carteles, etiquetas dentro de la escena) es decorativo y está permitido. | VALIDADO |
| **Resolución:** las imágenes narrativas llegan de Gemini en 768×1376 y se reescalan ~1.4× al canvas 1080×1920 (se ven bien en el piloto). Ideal: ≥1080×1920. `render.mjs` avisa si una imagen no es 9:16. | PENDIENTE (mejorar nitidez) |
| **Canvas:** 1080×1920, 30 fps, fondo parchment `#F5ECD7`. | VALIDADO |

### Contrato del JSON de pieza (`pieza_X.json`)

```json
{
  "pieza_id": "PZA_4.2", "medio": "Video", "aspecto": "9:16",
  "canvas": { "w": 1080, "h": 1920 }, "tema": "4.2",
  "voz": { "name": "en-US-Neural2-J", "speakingRate": 0.92, "pitch": -4 },
  "fuente_subtitulos": { "family": "DM Sans", "weight": "700", "file": "fonts/DMSans.ttf" },
  "slides": [
    { "n": 1, "layout": "full_bleed", "asset": "TPL-video-cover-framed.png",
      "imagen": "img/01_portada.png", "subtitulos": false, "movimiento": false,
      "texto_narrado": "Even a *three-year-old* can do five things in the garden." },
    { "n": 2, "layout": "full_bleed", "asset": "STOCK-…_9x16_v1.png",
      "imagen": "img/02_….png", "texto_narrado": "Number *five*: …" }
  ]
}
```
`asset` es el nombre exacto en Drive/Airtable (trazabilidad); `imagen` es la ruta local. Claude escribe este JSON, nunca coordenadas ni tiempos: los tiempos salen de `timings.json`.

---

## 3. Guion narrado

**Marcas dentro de `texto_narrado`** (VALIDADO):

| Marca | Efecto |
|---|---|
| `*palabra*` | Énfasis: el subtítulo sale más grande (×1.4). No cambia la voz. |
| `//` pegado al final de una palabra | Pausa extra de +450 ms (ej. `bio.//`). |
| `…` al final de una palabra | Pausa larga (+500 ms) y se lee como coma. |

**Tabla de pausas** (`PAUSE` en `lib.mjs`, en ms, se suman a la pausa natural de la voz): fin de oración 380 · dos puntos 200 · coma 100 · puntos suspensivos 500 · extra (`//`) 450. Se ajustan en una sola línea. Antes del cambio (120/80/0/300) la narración sonaba apresurada; ahora suena a libro para niños. VALIDADO.

**Ritmo:** `speakingRate` **0.92**. El 95 % todavía se sentía apresurado. VALIDADO.

**Reglas de redacción:**
- Todo en inglés (mercado US), voz del Brand Bible, sin banned words. El Question Test del Sistema CRS sigue siendo bloqueante.
- Un único CTA. Va **antes** de la línea de cierre en loop, separado por pausa (`link in bio.//`), nunca pegado con conectores tipo "So…".
- Longitud de referencia: ~525 caracteres de texto (~35 s de video) con 6 slides.
- Hook 17 (Resultados) exige resultados reales; no se inventan.

---

## 4. Cierre en loop (variable "tipo de cierre")

La última frase del video se diseña para que, al reiniciarse la reproducción, las primeras palabras del video sean su respuesta o su continuación. Decisión de Johnny: es el default de los videos FYR y se alterna entre dos formas para medir cuál retiene más.

| Tipo | Qué es | Ejemplo (PZA_4.2) | Estado |
|---|---|---|---|
| **B — Pregunta** | La última frase es una pregunta cuya respuesta son las primeras palabras del video. | "…Family guide, link in bio.// **Wait, how early can a kid really start gardening?**" → reinicia: "Even a three-year-old can do five things in the garden." | EN PRUEBA |
| **A — Frase cortada** | La última frase queda sin terminar y el inicio la completa. Sin puntuación final; cola de silencio mínima (`FYR_TAIL_LAST=0.05`). | "…Family guide, link in bio.// **Because the truth is**" → reinicia: "Even a three-year-old can do five things in the garden." | EN PRUEBA |

**Regla aprendida (10-oct-2026):** la pregunta **no debe repetir la respuesta**. La primera versión ("who says a *three-year-old* is too small…?") ya contenía "three-year-old"; al reiniciar no había hueco que llenar y la pregunta sonaba pegada. La pregunta abre el hueco; el inicio del video lo llena.

**Regla aprendida (19-oct-2026, hallazgo en TTS real — lote de 4 videos, Parada 3):** la misma trampa existe en el tipo A y ahí es peor, porque es más fácil caer en ella sin darse cuenta al escribir el brief. "Frase cortada" significa que la frase de cierre queda GRAMATICALMENTE INCOMPLETA y el inicio la termina — **no significa que el cierre repita las palabras del inicio**. En el primer lote real, 3 de 4 briefs de video (PZA_5.3, 7.1, 9.3) escribieron el cierre A como una repetición casi o totalmente textual de la frase de apertura (ej. cierre = "Careful what you skip ordering in January." / inicio = "Careful what you skip ordering in January — some of it..."). Al escucharlo en TTS real sonó como un error de guion, no como un loop — exactamente el mismo síntoma que la regla de arriba ya identificó para el tipo B. **Checklist antes de aprobar un cierre tipo A:** (1) la frase de cierre, leída sola, debe terminar en un punto gramaticalmente abierto (dos puntos, conector, oración sin completar — nunca punto final ni la misma idea ya dicha); (2) no debe compartir ninguna palabra clave con la frase de apertura (si comparte 3+ palabras seguidas, es repetición, no corte); (3) el corte debe sonar como alguien hablando de forma natural, nunca como fórmula de copywriting ("Because here's the thing nobody tells you about:" suena a anuncio; "And honestly?" o "Because, real talk—" suena a conversación — preferir lo segundo).

**Cierre visual** (regla de loop visual de `SKILL.md`, Paso 3): el último slide puede repetir transformado un elemento de la portada. NO probado en video todavía.

**Marca en video (decisión de Johnny, 11-oct-2026):** el video 9:16 no lleva icono en ningún slide (la interfaz de las plataformas lo tapa en cualquier posición). El **lockup vertical** (`lockup_cierre` del motor de ensamblado: `assets/brand/lockups-vertical/FYR_C14_lockup-vertical_1x1_v1.png`, centrado) es un recurso **opcional**: se usa solo cuando el guion nombra la marca y hace falta que el espectador la reconozca. Por defecto NO sustituye la última imagen del loop: el cierre en loop pierde fuerza si el último slide no conecta con la imagen que se ve. Si se prueba, va como variante (una variable a la vez). EN PRUEBA.

**Veredicto del piloto (10-oct-2026):** a Johnny le gustaron ambos cierres, así que se mantiene la alternancia A/B (no se descarta ninguno). Dos ajustes pedidos: (1) la **espera entre el final y el reinicio se recorta a la mitad** (ver `TAIL_LAST` en §7); (2) la **pregunta B debe sonar más orgánica**: registro hablado y casual, con un arranque conversacional corto (tipo "Wait, …" / "Ever wonder …"), no una pregunta de manual. Se renderiza de nuevo y se juzga por oído; el ganador final se mide después con datos reales de publicación (retención y replays).

---

## 5. Voz

**Decisión (VALIDADO por oído):** `en-US-Neural2-J`, tono **-4** semitonos, velocidad 0.92. Fue la favorita 1 entre 14 muestras (Neural2, WaveNet, Standard y Chirp 3 HD) para un narrador masculino grave tipo documental; superó a `en-GB-Neural2-O` en la comparación directa. Las primeras pruebas (voz femenina Neural2-F, ~60 % robótica) se descartaron.

**Por qué Neural2 y no otra:** `tts.mjs` usa la API v1beta1 con `enableTimePointing: ['SSML_MARK']`, que devuelve el instante exacto de cada palabra (base de los subtítulos sincronizados). Esas marcas funcionan en Neural2, WaveNet y Standard; **no** en Studio ni Journey (error) y **Chirp 3 HD** acepta solo texto plano, sin marcas. El tono (`pitch`) solo se aplica en Neural2/WaveNet/Standard.

**Costos** (página de precios de Google, verificada 10-oct-2026; los precios cambian, reverificar antes de escalar):

| Motor | Gratis/mes | Después | ≈ por video de 35 s |
|---|---|---|---|
| Standard / WaveNet | 4 M caracteres | $4 / M | ~$0.004 |
| **Neural2** (elegido) | 1 M | $16 / M | ~$0.017 |
| Chirp 3 HD | 1 M | $30 / M | ~$0.016 |
| Gemini 2.5 Flash TTS | ninguno | tokens: $10 / M de audio (25 tokens/s) | ~$0.009 |
| Gemini 2.5 Pro TTS | ninguno | $20 / M de audio | ~$0.018 |

Los tags SSML cuentan como caracteres (excepto `<mark>`): un video usa ~1,000 caracteres facturables → ~1,000 videos gratis al mes con Neural2. El audio se genera **una vez por pieza**; las variantes de subtítulo reutilizan los WAV sin costo. PENDIENTE: Johnny crea una alerta de presupuesto en Google Cloud (~$5).

**Alternativas evaluadas y estado:**
- **Chirp 3 HD** (favoritas 2–4: Enceladus GB, Iapetus US, Sadaltager): más natural, pero sin marcas → exigiría un paso de alineación en la nube (Google Speech-to-Text con tiempos por palabra, emparejado con el guion). PENDIENTE, solo si Neural2-J deja de convencer.
- **Gemini-TTS** (modelos 2.5 Flash/Pro): admite petición de estilo en lenguaje natural y etiquetas `[sigh]`, `[whispering]`, `[short pause]`, `[curious]`; tiene las mismas voces masculinas (Charon, Enceladus, Iapetus, Sadaltager, Algenib, Orus…). La documentación no menciona tiempos por palabra → misma necesidad de alineación. Las etiquetas están en preview y en-GB está en preview (en-US es GA). EN INVESTIGACIÓN.
- **Modelos locales** (Kokoro, Piper): descartados, la PC del piloto no los soporta. **edge-tts:** no oficial, inadecuado para una marca comercial.

---

## 6. Subtítulos (VALIDADO)

Variante por defecto: **`B-e14`** — una palabra a la vez.

| Propiedad | Valor |
|---|---|
| Posición | Centro del video (`y` 52 %, el "ombligo"); las zonas seguras NO aplican a subtítulos |
| Fuente | DM Sans Bold (`fonts/DMSans.ttf`; el repo tiene solo `DMSans.ttf`) |
| Tamaño base | 104 px; palabras con énfasis ×1.4 |
| Color | Blanco puro `#FFFFFF`, **sin contorno**, sombra de dos capas (offset_y 4/blur 4 y offset_y 8/blur 22, opacidad .55) |
| Entrada | Escala 0.78→1 en 0.14 s, `ease-out-back` (con keyframes; los presets de animación no corren con stroke) |
| **Autoajuste de ancho** | tamaño = mín(tamaño, 900 / (letras × 0.58)); 0.66 si va en mayúsculas. Evita que palabras largas con guion ("three-year-old", 14 letras) se salgan del cuadro. Bug detectado y corregido el 10-oct-2026. |
| Sincronía | Tiempos exactos de las marcas SSML |
| Slide 1 | Sin subtítulos |

**Modificadores de variante:** `-e10`/`-e14`/`-e18` (tamaño del énfasis), `-nm` (sin zoom), `-up` (mayúsculas), `-gold` (énfasis dorado). **Descartados por Johnny:** `-so` (contorno marrón) y `-dim` (atenuar imágenes). **Variante `A`** (caption nativo de Clipkit por grupos de palabras): disponible, deprioritizada; Johnny prefiere una palabra a la vez.

**A vigilar:** la palabra queda en pantalla hasta la siguiente marca, también durante las pausas largas. Si molesta, hacer que desaparezca al terminar de pronunciarse. PENDIENTE de opinión.

---

## 7. Línea de tiempo y movimiento (VALIDADO)

| Parámetro | Valor |
|---|---|
| Silencio antes de la voz por slide (`HEAD`) | 0.15 s |
| Silencio después de la voz (`TAIL`) | 0.65 s (antes 0.40: más aire entre slides) |
| Cola del último slide (`TAIL_LAST`) | 0.35 s por defecto (cierre B); se cambia con la variable de entorno `FYR_TAIL_LAST` (cierre A: 0.05). Era 0.90 y 0.15: Johnny pidió recortar a la mitad la espera entre el final y el reinicio del loop (10-oct). EN PRUEBA |
| Transición entre slides | Crossfade de 0.25 s (`fade-in` ease-out) |
| Movimiento | Zoom lineal 1.00→1.07 en los slides 2–N; portada estática |
| Voz | Entra en `inicio del slide + HEAD`; cada slide tiene su propio WAV |

---

## 8. Variantes y experimentación

Cada video publicado lleva un **ID de variante** que combina: estilo de subtítulo (`B-e14`), tipo de cierre (`A`/`B`) y voz. Reglas: se cambia **una variable a la vez**; el audio se genera una sola vez por combinación voz+guion; las variantes de render reutilizan los WAV.

| Variable | Opciones | Estado |
|---|---|---|
| Tipo de cierre | A (cortada) vs B (pregunta) | EN PRUEBA |
| Cierre visual | último slide repite la portada transformada vs no | PENDIENTE |
| Voz | Neural2-J (base) vs Chirp 3 HD / Gemini-TTS | PENDIENTE |
| Ritmo | tabla `PAUSE` actual vs más/menos pausa | base validada |
| Subtítulo | `B-e14` (base) vs `-gold` | base validada |

PENDIENTE: campo "ID de variante" en `Content_Pieces` (el conector de Airtable no crea campos; se crea a mano) para que `performance-lens` cruce retención contra variante.

---

## 9. Procedimiento (GitHub Actions, sin PC)

El paso a paso completo, con el registro en Airtable en cada etapa, está en `knowledge/FYR_Rutas_De_Produccion.md` (Ruta B). La parte de render:

1. **Preparar (Claude).** Imágenes de las escenas ya en `06_Narrative_Stock` y registradas en `Assets`; portada compuesta y alojada en `Video_Production/PZA_[tema]/`; el JSON de la pieza trae el `drive_id` de cada slide. Verificación previa con el conector de Drive.
2. **Disparar (Claude).** Commit a `main` de `pieza_[tema].json` y `production/queue/pza-[tema].env` (`PIEZA`, `VARIANTE`, `TAIL_LAST`). El push dispara el workflow; también se puede lanzar a mano desde la pestaña Actions.
3. **Render (Actions).** Baja las imágenes por ID, `node tts.mjs` (cada slide debe decir `marks`; si dice `fallback-proporcional`, esa voz no devolvió marcas y la corrida se revisa), `node render.mjs <variante>` (cierre A: `TAIL_LAST=0.05`), sube el MP4 a la raíz de Drive como `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4` (la versión sube sola, nunca sobrescribe) y Claude lo mueve a `Content_Pieces/PZA_[tema]/[fecha]/` con el conector de Drive y deja el registro en `production/runs/`. El MP4 queda además 7 días como artefacto.
4. **Revisar.** Claude descarga el MP4 y comprueba duración, tamaño y fotogramas; Johnny lo ve con repetición activada (unión final→inicio, subtítulos que caben, ritmo, nitidez).
5. **Aprobado** → registrar en Airtable (`Estado Producción = Ensamblado`, `Duración`, `ID de variante`, `Carpeta Drive`).
6. **Commit** solo de scripts y JSON (nunca `node_modules/`, `build/`, `salida/`, `img/`, credenciales).

## 10. Registro en el sistema

- **Drive:** el MP4 final vive junto a las imágenes de la pieza, en `Content_Pieces/PZA_[tema]/[fecha]/`. Los WAV y `timings.json` son intermedios regenerables: no se suben.
- **Airtable (`Content_Pieces`):** `ID Pieza = PZA_[tema]`, `Tipo de Pieza = Video`, `Duración` (segundos), `Assets Usados`, `Estado Producción` (`Brief Generado` → `Assets en Drive` → `Ensamblado` = MP4 renderizado y aprobado — este es el último estado que `fyr-video-assembler`/`fyr-content` escriben; `Publicado` es dominio de una skill de publicación que no existe todavía, ver `fyr-content/SKILL.md` Paso 5 sub-paso 6, corrección 28-oct-2026), `Ruta JSON` (ruta del `pieza_X.json` en el repo). `ID de variante` (`voz|subtítulo|cierre`). Todas las escrituras en Airtable las hace Claude en el paso correspondiente de la skill; Johnny no las hace a mano.
- **Skill:** `fyr-video-assembler` (`.claude/skills/fyr-video-assembler/SKILL.md`) guía a Claude para escribir el JSON de pieza y entregar los bloques de comandos de este procedimiento. Se comunica con `fyr-content` a través de Airtable y de los archivos del repo, nunca invocándola.

---

## 11. Pendientes honestos

1. Veredicto de Johnny sobre cierre A vs B (PZA_4.2) y sobre el ritmo con la nueva tabla de pausas.
2. Primera publicación real y medición de retención/replays: todo lo "EN PRUEBA" depende de eso.
3. Nitidez de imágenes (768×1376): decidir si se pide a Gemini mayor resolución o se aplica un reescalado previo.
4. Alerta de presupuesto en Google Cloud.
5. Motor único parametrizado (`--pieza`) en vez de copiar la carpeta por pieza.
6. Alineación en la nube si se adopta Chirp 3 HD o Gemini-TTS.
7. Cierre visual en loop y subtítulo que desaparece al terminar la palabra: sin probar.
