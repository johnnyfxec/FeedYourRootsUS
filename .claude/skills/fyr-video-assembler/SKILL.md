---
name: fyr-video-assembler
description: Capa de ejecución de video de FYR. Toma un brief de video ya aprobado (generado por fyr-content) y produce el pieza_X.json (guion narrado con marcas de pausa/énfasis, imágenes, voz) y ejecuta el render del MP4 9:16 (voz con Google TTS y subtítulos palabra por palabra) en GitHub Actions, subiendo el resultado a Drive. Usar cuando el usuario diga "arma el video de PZA_X", "genera el JSON de video", "prepara el render", "crea la variante B del video" o "compara cierre A y B". No decide contenido, hooks ni CTA: eso ya viene en el brief.
---

# FYR Video Assembler

Skill de **ejecución**, no de contenido. `fyr-content` decide qué se dice; esta skill lo convierte en archivos y comandos que producen el MP4. Se comunican solo a través de Airtable (`Content_Pieces`) y de los archivos del repo; nunca se invocan entre sí.

**Fuente de verdad de las reglas:** `knowledge/FYR_Protocolo_Edicion_Video.md`. Léelo completo antes de producir. Si este SKILL.md y el Protocolo difieren, gana el Protocolo y se avisa a Johnny para corregir la skill. Nunca cambies un valor marcado VALIDADO (voz, subtítulos, tabla de pausas, tiempos) sin una prueba nueva que lo supere.

## Cuándo NO usar esta skill
- Carruseles o slides estáticos → `assemble.py` (ver `FYR_Motor_Ensamblado_Arquitectura_v1.md`).
- Video generado por IA (clips animados) → fuera de alcance.
- Escribir el guion, elegir hook o CTA → `fyr-content`. Si el brief no existe o no está aprobado, detenerse y decirlo; no inventar contenido.

## Entradas requeridas (verificar, no suponer)
1. **Brief de video aprobado** de la pieza: slides con texto narrado, Hook usado, CTA, fase, assets. Fuente: `production/pieces/PZA_[tema]/brief.md` del repo y el registro en Airtable (`Content_Pieces`, base `appMy5aOwifSbBLPR`). Si el entorno no puede leerlo, pedirlo a Johnny.
2. **Imágenes** de cada slide, con nombre de asset en Drive/Airtable (`asset`) y archivo local previsto (`imagen`). El slide 1 es la portada (portada compuesta por Claude con `marco_grande_cuadrado`, ver `knowledge/FYR_Rutas_De_Produccion.md` Ruta B, paso B8; o la plantilla `TPL-video-cover-framed.png`).
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
- **A (frase cortada):** la última frase queda sin terminar, sin punto final, y la primera frase del video la completa; render con `FYR_TAIL_LAST=0.05`.
- Verificar leyendo en voz alta: última frase + primera frase del video deben sonar como una sola idea. Si no, reescribir el cierre antes de entregar.
- Para comparar A y B: preparar dos versiones del texto del slide final y avisar que cada cierre necesita su propio `tts.mjs` porque cambia el audio del último slide.

### Paso 4 — Preparar y disparar el render (Claude, sin PC)
Seguir la **Ruta B** de `knowledge/FYR_Rutas_De_Produccion.md` (pasos B8 a B10). Resumen:
1. **Portada (B8):** descargar la imagen 1:1 con el conector → `run_pieza.py importar` + `ensamblar --config portada_config.json --portada` → `drive_client.py upload`, subiendo directo a `video_production_folder(pieza_id)` (la resuelve sola, creándola si falta — ya no se sube a la raíz ni se mueve después con el conector) → escribir su ID en el slide 1 del JSON (`asset`, `drive_id`).
2. **Verificación previa (B9):** cada `drive_id` del JSON existe en Drive (`get_file_metadata`), es PNG y pesa > 0; ninguno es `null`; el guion está completo. Si algo falla, no se dispara el render.
3. **Disparo (B10):** Claude resuelve `content_pieces_folder(pieza_id, fecha)` para obtener el `parent_id` de destino y lo pone en `production/queue/pza-[tema].env` junto con `PIEZA`, `VARIANTE`, `TAIL_LAST` (cierre B 0.35, cierre A 0.05). Commit a `main` de ese `.env` y del JSON. El push dispara "Render video". El workflow sube el MP4 directo a `Content_Pieces/PZA_[tema]/[fecha]/` (ese `parent_id`, nunca `Video_Production/`) y deja el registro (con el enlace) en `production/runs/` — ya no hace falta mover nada después con el conector.
4. Esperar el registro de la corrida; si falla, leer el log, corregir la causa y repetir (máximo 3 intentos, luego reportar). Si hay que comparar cierres A y B, un archivo `.env` por variante, uno a la vez (cada cierre cambia el audio).
- Nunca pedir ni escribir credenciales; viven en secretos de GitHub y en el entorno de la sesión.

### Paso 5 — Revisión
Claude descarga el MP4 de Drive y comprueba duración, 1080×1920, audio y fotogramas de cada slide. Luego Johnny revisa con repetición activada: unión final→inicio, subtítulos que caben (palabras largas), ritmo de pausas, nitidez. Registrar su veredicto; si cambia una regla VALIDADO o resuelve un EN PRUEBA, **editar la sección correspondiente del Protocolo en su sitio** (no anexar al final) y actualizar el `CHANGELOG.md`.

### Paso 6 — Registro
Tras aprobar (el MP4 ya está en `Content_Pieces/PZA_[tema]/[fecha]/` con nombre `FYR_PZA_[tema]_VIDEO_[variante]_9x16_v[n].mp4`, subido por el workflow; las versiones anteriores se mandan a la papelera): en Airtable `Tipo de Pieza = Video`, `Duración`, `Assets Usados`, `Ruta JSON`, `ID de variante` y `Estado Producción = Ensamblado` (MP4 aprobado y en Drive); `Publicado` solo cuando sale a la red. Los WAV y `timings.json` no se suben. Claude hace estas escrituras en Airtable; Johnny no las hace a mano. Al publicar (desde 28-oct-2026, todo en `Content_Pieces`, ya no en `Themes` — ver migración Route B en `fyr-content/SKILL.md`): `Estado Producción = Publicado`, `Content_Pieces.Fecha de Publicación`, y el `Link Publicación [red]` de `Content_Pieces` correspondiente a dónde se publicó. `Themes` ya no tiene campo `Estado`; el tema se crea una sola vez al aprobar el brief (si no existía) y no se vuelve a tocar — el link `Themes.Content_Pieces` es la señal de que ya se produjo.

## Reglas no negociables
1. No decidir ni modificar hook, CTA, fase o promesa del brief. Solo aplicar marcas de pausa/énfasis y ajustar el cierre bajo las reglas del §4; si el cierre cambia el sentido, avisar.
2. No inventar resultados, cifras ni testimonios (Hook 17 exige datos reales).
3. Un solo CTA por video.
4. Cambiar una variable por prueba (cierre, voz, subtítulo, ritmo).
5. Fallar de forma visible: si falta una imagen, el brief no está aprobado, las marcas no se generan o un archivo no coincide con el contrato, decirlo y detenerse; no rellenar con suposiciones.
6. Repo = fuente de verdad. Commits a `main` (no hay PC que sincronizar); nunca `--force`; no commitear `node_modules/`, `build/`, `salida/`, `img/`, fuentes ni credenciales.
7. No decir "funciona" de nada que no se haya renderizado y revisado: el video lo valida Johnny tras la revisión de Claude.

## Pendientes conocidos (no resolver por cuenta propia)
Motor único con `--pieza`; alineación en la nube si se adopta Chirp 3 HD o Gemini-TTS; mejora de resolución de imágenes (768×1376); cierre visual en loop; subtítulo que desaparece al terminar la palabra. Ver Protocolo §11.
