# PZA_4.2 — video de piloto (manual, en la PC)

Voz (Google Cloud TTS) + subtítulos palabra por palabra + render local (Clipkit).
La política completa vive en `knowledge/FYR_Protocolo_Edicion_Video.md`; este archivo es solo el recordatorio de comandos de esta carpeta.

Estado: voz `en-US-Neural2-J` (pitch -4, velocidad 0.92) y subtítulo `B-e14` validados. Cierre A vs B en prueba.

## 0. Preparar (Git Bash en VSCodium)
Desde la raíz del repo:

    cd production/scripts/video/pza-4.2
    git pull
    npm install                       # solo la primera vez
    echo $GOOGLE_APPLICATION_CREDENTIALS   # debe imprimir la ruta del JSON (fuera del repo)

Si `git pull` se queja de cambios locales en `lib.mjs` o `pieza_4.2.json`, son los parches hechos a mano en la PC: ya están incorporados en el repo. Descártalos con `git checkout -- lib.mjs pieza_4.2.json` y vuelve a hacer `git pull`.

## 1. Imágenes → carpeta `img/` con ESTOS nombres
| Archivo destino | Asset | Drive |
|---|---|---|
| img/01_portada.png | TPL-video-cover-framed.png | https://drive.google.com/file/d/1HEzwHQVBWNG0x9qaEweQTW7RO5NzXqBn/view |
| img/02_seed-tray.png | STOCK-child-hands-seed-tray_9x16_v1.png | https://drive.google.com/file/d/1DYpF8U-z7xQh-CsGiOGdasIOokkgb7io/view |
| img/03_riego.png | STOCK-watering-seedling-tray_9x16_v1.png | https://drive.google.com/file/d/1PP6fiw5_FLNL6UQZM8NUVCJJP0y4Nuhk/view |
| img/04_semillas.png | STOCK-planting-labeled-seeds_9x16_v1.png | https://drive.google.com/file/d/1iVgeAF6v9S-kbGzO9qb796WvFL8f7nOQ/view |
| img/05_tomate.png | STOCK-hands-picking-cherry-tomato_9x16_v1.png | https://drive.google.com/file/d/1UjTalomj04p5b6_0vHfJ7FHmUPQbgmTA/view |
| img/06_canasta.png | STOCK-child-harvest-basket-doorway_9x16_v1.png | https://drive.google.com/file/d/152m9l2XICJo7WSiL_5wHv9v0vFq_74cC/view |

## 2. Fuente de los subtítulos
`fonts/DMSans.ttf` (fuente variable DM Sans, se usa en Bold). El repo la trae en `production/fonts/DMSans.ttf`; cópiala a `fonts/` si falta. Sin ella el render usa la fuente por defecto y avisa.

## 3. Voz (una sola vez por guion)

    node tts.mjs

Crea `build/audio/slide_N.wav` y `build/timings.json`. Cada slide debe decir `marks`; si dice `fallback-proporcional`, esa voz no devolvió marcas de palabra y los subtítulos saldrían desfasados. Cambiar de voz: edita `voz.name` en `pieza_4.2.json` o usa `node tts.mjs --voice en-US-Neural2-J`.

## 4. Render

    node render.mjs B-e14                      # cierre B (pregunta), el que trae el JSON
    FYR_TAIL_LAST=0.15 node render.mjs B-e14   # cierre A (frase cortada): ver nota abajo
    node render.mjs B-e14 B-e14-gold           # varias variantes seguidas

Salida: `salida/PZA_4.2__sub<VARIANTE>.mp4`. Cada render sobrescribe el anterior: **renombra o copia el MP4 antes de renderizar otra versión**. Con `--dry` solo escribe el JSON de Clipkit.

Para el cierre A, además de la variable de entorno cambia el final de la última línea de `texto_narrado` (slide 6) por: `link in bio.// Because the truth is` (sin punto final) y vuelve a correr `node tts.mjs`.

## 5. Variantes de subtítulo
- **B** — una palabra a la vez; `*énfasis*` sale más grande. Es la base (`B-e14`).
- **A** — caption nativo de Clipkit por grupos de palabras (deprioritizado).
- Modificadores: `-e10` / `-e14` / `-e18` tamaño del énfasis · `-nm` sin zoom · `-up` MAYÚSCULAS · `-gold` énfasis dorado.
- Reglas fijas: portada sin subtítulos; subtítulos al centro (52 % de alto); sin numerales en pantalla; crossfade 0.25 s; zoom 1.00→1.07 en slides 2–6.

## 6. Qué no se commitea
`node_modules/`, `build/`, `salida/`, `img/*.png`, `fonts/*.ttf`, credenciales. Commit con rutas explícitas (`git add archivo`), nunca `git add .`.

## 7. Qué revisar en el video
Con repetición activada: la unión del final con el inicio (¿la pregunta/frase cortada engancha?), que ningún subtítulo se salga del cuadro, el ritmo de las pausas, y nitidez de las imágenes.
