# PZA_4.2 — primera prueba de video (manual, en la PC)

Voz (Google TTS) + subtítulos palabra por palabra + render (Clipkit local). Dos variantes de subtítulo para comparar.

## 0. Dónde poner la carpeta
Copia `pza-4.2` DENTRO de la carpeta de la PC que ya tiene `node_modules` con
`@clipkit/renderer` y `@google-cloud/text-to-speech` (en cualquier nivel por debajo; Node los encuentra solo).
Abre PowerShell dentro de `pza-4.2`. Comprueba que las credenciales siguen puestas:

    echo $env:GOOGLE_APPLICATION_CREDENTIALS

## 1. Las 6 imágenes → carpeta `img/` con ESTOS nombres
| Archivo destino | Asset | Drive |
|---|---|---|
| img/01_portada.png | TPL-video-cover-framed.png | https://drive.google.com/file/d/1HEzwHQVBWNG0x9qaEweQTW7RO5NzXqBn/view |
| img/02_seed-tray.png | STOCK-child-hands-seed-tray_9x16_v1.png | https://drive.google.com/file/d/1DYpF8U-z7xQh-CsGiOGdasIOokkgb7io/view |
| img/03_riego.png | STOCK-watering-seedling-tray_9x16_v1.png | https://drive.google.com/file/d/1PP6fiw5_FLNL6UQZM8NUVCJJP0y4Nuhk/view |
| img/04_semillas.png | STOCK-planting-labeled-seeds_9x16_v1.png | https://drive.google.com/file/d/1iVgeAF6v9S-kbGzO9qb796WvFL8f7nOQ/view |
| img/05_tomate.png | STOCK-hands-picking-cherry-tomato_9x16_v1.png | https://drive.google.com/file/d/1UjTalomj04p5b6_0vHfJ7FHmUPQbgmTA/view |
| img/06_canasta.png | STOCK-child-harvest-basket-doorway_9x16_v1.png | https://drive.google.com/file/d/152m9l2XICJo7WSiL_5wHv9v0vFq_74cC/view |

## 2. Fuente de los subtítulos (opcional pero recomendado)
Copia `DMSans-Bold.ttf` a `fonts/`. Para encontrarla en el repo clonado:

    Get-ChildItem -Recurse -Filter "DMSans*Bold*.ttf" E:\RUTA-DEL-REPO | Select-Object -First 3 FullName

Sin ella, el render usa la fuente por defecto y avisa.

## 3. Elegir la voz (importante: solo sirven las que devuelven marcas de palabra)
    node tts.mjs --probe

Imprime una tabla: cada voz con "OK" devuelve el tiempo de cada palabra. Deja WAV de muestra en `build/probe/` para escucharlos.
Por defecto el guion usa `en-US-Neural2-F`; para cambiarla: `node tts.mjs --voice en-US-Neural2-H` (o edita `voz.name` en `pieza_4.2.json`).

## 4. Generar la voz de los 6 slides
    node tts.mjs

Crea `build/audio/slide_N.wav` y `build/timings.json`. Si algún slide dice "fallback-proporcional", esa voz no dio marcas: prueba otra.

## 5. Renderizar
    node render.mjs                 # A y B-e14
    node render.mjs B-e18 B-e10-nm  # otras variantes

Los videos salen en `salida/PZA_4.2__sub<VARIANTE>.mp4`. Con `--dry` solo escribe el JSON de Clipkit sin renderizar.

### Variantes
- **A** — subtítulo nativo de Clipkit: grupos de palabras, la palabra activa se resalta en dorado.
- **B** — una palabra a la vez; las palabras con `*énfasis*` salen más grandes y doradas.
- Modificadores: `-e14` tamaño del énfasis (1.0 / 1.4 / 1.8 → `-e10`, `-e14`, `-e18`) · `-nm` sin movimiento de cámara · `-up` MAYÚSCULAS.
- Reglas de la pieza: slide 1 (portada) sin subtítulos; subtítulos al centro del video (52 % de alto); sin numerales; crossfade de 0.25 s entre slides; zoom lento 1.00→1.07 en los slides 2–6.

## Qué traerme de vuelta
1. La tabla de `--probe` (copiada).
2. El resultado de `node tts.mjs` (líneas por slide).
3. Los MP4 (o una captura de pantalla de cada variante) y qué ves bien o mal: legibilidad sobre las ilustraciones claras, tamaño del énfasis, ritmo, la pausa antes de la pregunta final.
