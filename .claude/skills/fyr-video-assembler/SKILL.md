---
name: fyr-video-assembler
description: Capa de ejecución de video de FYR. Toma un brief de video ya aprobado (generado por fyr-content) y produce el pieza_X.json (guion narrado con marcas de pausa/énfasis, imágenes, voz) más los bloques de comandos Git Bash para generar la voz con Google TTS y renderizar el MP4 9:16 con subtítulos palabra por palabra en la PC. Usar cuando el usuario diga "arma el video de PZA_X", "genera el JSON de video", "prepara el render", "crea la variante B del video" o "compara cierre A y B". No decide contenido, hooks ni CTA: eso ya viene en el brief.
---

# FYR Video Assembler

Skill de **ejecución**, no de contenido. `fyr-content` decide qué se dice; esta skill lo convierte en archivos y comandos que producen el MP4. Se comunican solo a través de Airtable (`Content_Pieces`) y de los archivos del repo; nunca se invocan entre sí.

**Fuente de verdad de las reglas:** `knowledge/FYR_Protocolo_Edicion_Video.md`. Léelo completo antes de producir. Si este SKILL.md y el Protocolo difieren, gana el Protocolo y se avisa a Johnny para corregir la skill. Nunca cambies un valor marcado VALIDADO (voz, subtítulos, tabla de pausas, tiempos) sin una prueba nueva que lo supere.

## Cuándo NO usar esta skill
- Carruseles o slides estáticos → `assemble.py` (ver `FYR_Motor_Ensamblado_Arquitectura_v1.md`).
- Video generado por IA (clips animados) → fuera de alcance.
- Escribir el guion, elegir hook o CTA → `fyr-content`. Si el brief no existe o no está aprobado, detenerse y decirlo; no inventar contenido.

## Entradas requeridas (verificar, no suponer)
1. **Brief de video aprobado** de la pieza: slides con texto narrado, Hook usado, CTA, fase, assets. Fuente: `production/briefs/` del repo o el registro en Airtable (`Content_Pieces`, base `appMy5aOwifSbBLPR`). Si el entorno no puede leerlo, pedirlo a Johnny.
2. **Imágenes** de cada slide, con nombre de asset en Drive/Airtable (`asset`) y archivo local previsto (`imagen`). El slide 1 es la portada (`TPL-video-cover-framed.png` u otra portada marcada).
3. **Tipo de cierre** (A cortada / B pregunta) si el brief lo indica; si no, B por defecto y se propone A como variante a comparar.

## Procedimiento

### Paso 1 — Leer
Leer el Protocolo de Edición de Video y el brief. Confirmar: nº de slides, que el slide 1 es portada, que no hay numerales de cuenta regresiva para mostrar en pantalla, que el texto está en inglés.

### Paso 2 — Escribir `pieza_[tema].json`
Ruta: `production/scripts/video/pza-[tema]/pieza_[tema].json` (copiar la carpeta `pza-4.2` como base mientras no exista el motor con `--pieza`). Usar exactamente el contrato del Protocolo §2:

- `voz`: `{ "name": "en-US-Neural2-J", "speakingRate": 0.92, "pitch": -4 }` salvo que Johnny pida probar otra voz (entonces una sola variable cambia).
- `fuente_subtitulos`: DM Sans 700, `fonts/DMSans.ttf`.
- Slide 1: `subtitulos: false`, `movimiento: false`. Slides 2–N: `layout: "full_bleed"`.
- `texto_narrado`: copiar del brief y aplicar solo las marcas del Protocolo §3: `*palabra*` énfasis (1–2 por slide, en la palabra clave), `//` pausa extra donde el brief separa ideas o antes de la línea de cierre, `…` pausa larga. Sin numerales ni símbolos; los números se escriben en letras.
- Nunca escribir coordenadas, tiempos ni duraciones: salen de `timings.json`.

### Paso 3 — Cierre en loop
Aplicar el Protocolo §4. El CTA va antes de la línea final y separado por `//` (`link in bio.//`), sin conectores como "So…".
- **B (pregunta):** la última frase es una pregunta cuya respuesta son las primeras palabras del video. La pregunta **no debe contener la respuesta**.
- **A (frase cortada):** la última frase queda sin terminar, sin punto final, y la primera frase del video la completa; render con `FYR_TAIL_LAST=0.15`.
- Verificar leyendo en voz alta: última frase + primera frase del video deben sonar como una sola idea. Si no, reescribir el cierre antes de entregar.
- Para comparar A y B: preparar dos versiones del texto del slide final y avisar que cada cierre necesita su propio `tts.mjs` porque cambia el audio del último slide.

### Paso 4 — Entregar los comandos (Git Bash en la PC)
Dar bloques cortos y pegables, uno por acción, en este orden (Protocolo §9):

    cd /e/Mis-Repositorios/FeedYourRootsUS/production/scripts/video/pza-[tema]
    git pull
    node tts.mjs
    node render.mjs B-e14

Indicar siempre: qué imágenes bajar de Drive y con qué nombres; que cada slide debe imprimir `marks` en `tts.mjs` (si dice `fallback-proporcional`, detenerse: esa voz no dio marcas); que `salida/` se sobrescribe y hay que renombrar el MP4 antes del siguiente render; para el cierre A, `FYR_TAIL_LAST=0.15 node render.mjs B-e14`.
- Si hay que parchear archivos en la PC, seguir la regla CRLF del Protocolo §9 (Python con `newline=''`, verificar cada conteo antes de escribir, sin `!` en heredocs). Si el parche es largo, preferir editar el archivo en el repo (rama de Claude) y pedir `git pull`.
- Nunca pedir ni escribir credenciales de Google; solo comprobar `echo $GOOGLE_APPLICATION_CREDENTIALS`.

### Paso 5 — Revisión (la hace Johnny)
Pedir que revise con repetición activada: unión final→inicio, subtítulos que caben (palabras largas), ritmo de pausas, nitidez. Registrar su veredicto; si cambia una regla VALIDADO o resuelve un EN PRUEBA, **editar la sección correspondiente del Protocolo en su sitio** (no anexar al final) y actualizar el `CHANGELOG.md`.

### Paso 6 — Registro
Tras aprobar: MP4 a `Content_Pieces/PZA_[tema]/[fecha]/` en Drive con nombre `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4`; en Airtable `Tipo de Pieza = Video`, `Duración`, `Assets Usados`, `Estado Producción = En Edición` → `Publicado` al subir. Los WAV y `timings.json` no se suben. Los campos `ID de variante` y `Ruta JSON` aún no existen: Johnny los crea a mano; mientras tanto, anotar la variante en Notas. Marcar el tema como `Usado` en `Themes` solo cuando la pieza se publique.

## Reglas no negociables
1. No decidir ni modificar hook, CTA, fase o promesa del brief. Solo aplicar marcas de pausa/énfasis y ajustar el cierre bajo las reglas del §4; si el cierre cambia el sentido, avisar.
2. No inventar resultados, cifras ni testimonios (Hook 17 exige datos reales).
3. Un solo CTA por video.
4. Cambiar una variable por prueba (cierre, voz, subtítulo, ritmo).
5. Fallar de forma visible: si falta una imagen, el brief no está aprobado, las marcas no se generan o un archivo no coincide con el contrato, decirlo y detenerse; no rellenar con suposiciones.
6. Repo = fuente de verdad. Trabajar en rama `claude/<nombre>`, nunca en `main`; no commitear `node_modules/`, `build/`, `salida/`, `img/`, fuentes ni credenciales.
7. No decir "funciona" de nada que no se haya renderizado y revisado: el video lo valida Johnny.

## Pendientes conocidos (no resolver por cuenta propia)
Motor único con `--pieza`; alineación en la nube si se adopta Chirp 3 HD o Gemini-TTS; mejora de resolución de imágenes (768×1376); cierre visual en loop; subtítulo que desaparece al terminar la palabra. Ver Protocolo §11.
