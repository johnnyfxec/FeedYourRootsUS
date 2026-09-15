# Feed Your Roots — Brand Mark Specification
**Version 1.0 — September 2026**
**Fuente:** `FYR_C14_logo-frasco_1x1_v1.svg` (trazado desde el original de Johnny, no rediseñado)
**Manual completo (PDF, para lectura humana):** `knowledge/reference_assets/FYR_Brand_Mark_Specification_v1.pdf`

Este documento es la versión en texto plano del manual, para que Claude Code y cualquier agente puedan leer las reglas sin abrir un PDF.

---

## 01 — El símbolo

Un frasco conteniendo un árbol. "A jar holding an orchard — enough, held."

Silueta única, un solo color, sin detalle interior recortado (nada de manzanas, ramas sueltas ni huecos pequeños) — eso es lo que lo hace sobrevivir a tamaño de favicon.

## 02 — Construcción y espacio de protección

**X = altura de la tapa del frasco = 15.6% de la altura total del símbolo.**
Medido en el archivo fuente: la tapa mide 145 de las 931 unidades de altura total del symbol.

Espacio de protección: X en los cuatro lados. Ningún texto, regla, imagen o borde puede entrar en esa zona.

## 03 — Tamaño mínimo

- **32 px** es el mínimo general de uso.
- **Excepción única: favicon de navegador**, donde el sistema operativo impone 16 px. A ese tamaño el símbolo se lee como silueta, no como dibujo — se acepta. Publicar assets en 16, 32 y 48 px para favicon.
- **20 mm** es el tamaño mínimo de impresión, medido sobre la altura total del símbolo.

## 04 — Variantes de color

| Variante | Símbolo / Fondo | Uso |
|---|---|---|
| Root Black sobre Parchment | `#0A0A0A` / `#F5ECD7` | Primario. Todo impreso y documentos. |
| Forest sobre Parchment | `#4A7C59` / `#F5ECD7` | Cabeceras web, empaque, portadas editoriales. |
| Terra sobre Parchment | `#D4732A` / `#F5ECD7` | Solo sellos y estampas de un color. |
| Parchment sobre Forest (invertido) | `#F5ECD7` / `#4A7C59` | Fondos oscuros, ropa, avatares sociales. |

El símbolo siempre es un solo color. Harvest Gold y Story Brown nunca se usan en el símbolo.

## 05 — Lockups aprobados

**Horizontal** (`FYR_C14_lockup-horizontal_16x5_v1`) — símbolo a la izquierda, wordmark "Feed Your Roots" en Playfair Display Bold a la derecha, una sola línea. El gap entre símbolo y wordmark es X. La línea base del wordmark alinea con la base del frasco.

**Vertical** (`FYR_C14_lockup-vertical_4x5_v1`) — símbolo arriba, wordmark centrado debajo.
⚠️ **Pendiente v1.1:** el gap actual en el archivo es 142px; la regla dice que debe ser X (99.5px en este archivo). No corregido aún — ver sección "Pendientes" abajo.

**Solo símbolo** — obligatorio para avatares, favicons y cualquier aplicación bajo 120 px. El wordmark nunca se coloca dentro del frasco.

## 06 — Usos prohibidos

- Nunca estirar. Proporción fija: **1 : 1.405** (ancho : alto).
- Nunca rotar. El frasco va siempre a nivel, 0°.
- Nunca agregar sombra, glow, bisel o degradado.
- Nunca separar el color: frasco y árbol son siempre idénticos.
- Nunca colocar sobre imagen con mucho detalle. Usar fondo plano.
- Nunca encerrar en una insignia, anillo o marco ajeno.

## 07 — Aplicación

- **Avatar circular:** el símbolo se centra y escala de forma que el espacio X lo separe del borde del círculo en su punto más cercano.
- **Favicon:** Root Black a 16px. Publicar 16, 32 y 48px.
- **Esquina de portada PDF:** esquina superior derecha, con inset de una altura de tapa (X) desde ambos bordes.
- **Cabecera de sitio:** Forest a 32px, lockup horizontal, alineado a la izquierda.

---

## Piezas retiradas — no usar

- **Badge FYR** (monograma con brote): retirado por completo. No está en Drive, repo ni Airtable.
- **Tree of Life** (`FYR_C01_logo-tree-canopy`): reclasificado como ilustración insignia de marca, NO es el logo/símbolo activo. Se sigue usando como imagen destacada en portadas y hero, pero nunca como favicon, avatar o símbolo de identidad.
- **Wordmark en Satisfy:** Satisfy queda reservada para *Fun Fact headers* y acentos manuscritos (Brand Bible). El wordmark de marca usa **Playfair Display**.

## Pendientes para v1.1

1. Gap del lockup vertical: cambiar `translate(94.685 1192.465)` a `translate(94.685 1149.965)` en los 4 SVG verticales (`FYR_C14_lockup-vertical*_4x5_v1.svg`) para que el gap sea exactamente X.
2. Proporción del wordmark respecto al símbolo (hoy ~17% de la altura del símbolo) no está escrita como regla — definir tras ver el lockup en uso real (cabecera del sitio, portada).
3. El PDF v1.0 cita `FYR_C14_logo-frasco_1x1_v2.svg` en el bloque de versión de la página 1 — el archivo real es `v1`. Corregir en la próxima revisión del PDF.

## Archivos fuente (Drive: `01_Brand_Assets/C14_Brand_Mark/`)

- `FYR_C14_logo-frasco_1x1_v1.svg` — símbolo maestro + 4 variantes de color + 8 tamaños PNG
- `FYR_C14_lockup-horizontal_16x5_v1.svg` — + 4 variantes de color, SVG y PNG
- `FYR_C14_lockup-vertical_4x5_v1.svg` — + 4 variantes de color, SVG y PNG
- `favicon.ico` — pendiente de despliegue en rama web (ver Protocolo de Trabajo, Estrategia de ramas)
