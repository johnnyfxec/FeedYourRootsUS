# Feed Your Roots — Política de Gestión de Assets
**Versión 1.0 — 22 de agosto 2026**
**Propósito:** que cualquier persona o agente que cree, nombre, ubique o registre un asset nuevo lo haga sin tener que reconstruir esta lógica desde cero.

---

## 1. Principio rector

Todo asset se clasifica por **una sola pregunta**: ¿es identidad de marca reutilizable, o es contenido de marketing para publicar?

- **Identidad de marca** (`01_Brand_Assets`, `02_Decorative_Elements`, `03_Seed_Library`) → piezas atómicas sin fecha de caducidad, reutilizables en cualquier pieza futura.
- **Marketing** (`05_Marketing_Assets`) → contenido producido para un canal específico, con propósito de publicación.
- **Producto** (`04_Producto_Finalizado`) → lo que se vende. Incluye también sus portadas de venta (Covers), porque son la cara oficial del producto Y un asset reutilizable de marketing a la vez.
- **Materia prima narrativa** (`06_Narrative_Stock`) → escenas completas, sin espacio reservado para overlay, listas para usarse tal cual en video, post individual o carrusel.

Cuando algo no encaje limpio en una categoría, la pregunta correcta no es "¿dónde cabe mejor?" sino "¿para qué se va a usar realmente?" — la función define la ubicación, no la apariencia.

---

## 2. Estructura de carpetas (Google Drive — `FYR/`)

```
FYR/
├── 00_Brand_Bible_Reference/
│   ├── Book_Elements/              (QR, DYK boxes — piezas reutilizables del libro)
│   └── Cover_Drafts_Archive/       (borradores históricos, no usar en producción)
├── 01_Brand_Assets/
│   ├── C01-C03_Logo_Concepts/
│   ├── C04-C05_Patterns/
│   ├── C06_Texture/
│   ├── C07-C08_Icon_Sets/
│   └── Corners/
├── 02_Decorative_Elements/          (E01-E36+, clip-art suelto 1:1, fondo transparente)
├── 03_Seed_Library/
│   └── WObg/                        (L01-L101, fondo transparente — única versión en uso)
├── 04_Producto_Finalizado/
│   ├── RGBc/                        (PDFs finales, no catalogados en Airtable)
│   ├── CMYK/                        (PDFs finales, no catalogados en Airtable)
│   └── Covers/
│       ├── Cuadradas_1x1/
│       ├── Verticales_2x3/
│       └── Horizontales_3x2/
├── 05_Marketing_Assets/
│   ├── Social_Media/
│   │   ├── TikTok_Covers/
│   │   ├── IG_Square/
│   │   ├── IG_Story/
│   │   ├── Pinterest_Pins/
│   │   └── Video_Cover_Templates/
│   ├── Ad_Creatives/
│   │   ├── Meta/
│   │   ├── Hooks/
│   │   └── Lifestyle/
│   ├── Web_Site/
│   │   └── Blog_Journal_Headers/
│   └── Video_Production/            (carpeta de trabajo activo, no banco de recursos)
├── 06_Narrative_Stock/               (escenas 9:16 sin overlay, fuente de b-roll para cualquier canal)
└── 07_Influencer_Outreach/           (solo la lista fuente; el registro de comunicación vive en Airtable)
```

**Regla de creación de carpetas nuevas:** antes de crear una carpeta, verificar si ya existe una que cumpla la misma función. Si aparece un tipo de asset nuevo sin casa clara, detenerse y decidir conscientemente (no crear "por si acaso").

---

## 3. Convención de nombres de archivo

```
[PREFIJO]_[categoría][número]_[slug-descriptivo]_[aspecto]_v[versión].[ext]
```

| Prefijo | Uso |
|---|---|
| `FYR_B##` | Social Media (Categoría B del Brand Bible) |
| `FYR_C##` | Brand Assets (Categoría C) |
| `FYR_D##` | Ad Creatives (Categoría D) |
| `E##` | Decorative Elements |
| `L##` | Seed Library (sufijo `-wobg` = fondo transparente) |
| `WEB-` | Banners y headers de sitio web |
| `TPL-` | Templates reutilizables (no assets terminados) |
| `STOCK-` | Narrative Stock |
| `COVER-` | Portadas de producto |
| `FYR_EXTRA_` | Asset aprobado sin categoría asignada al momento de crearlo |

**Regla de versión:** un archivo solo sube de número de versión (`v2`, `v3`...) **después** de que la versión anterior ya fue subida a Drive y confirmada. Nunca versionar en el nombre antes de tener la anterior archivada — evita huecos de versión sin sentido.

**Regla de aspecto:** siempre en formato `AxB` (ej. `9x16`, `1x1`, `4x5`, `2x3`, `3x2`) — nunca mezclar con formatos tipo `16:9` en el nombre de archivo (los dos puntos rompen compatibilidad con algunos sistemas de archivo).

---

## 4. Reglas de estilo de marca (para prompts de generación)

**Bloque de estilo base — usar siempre como punto de partida:**
```
Hand-drawn storybook illustration in the tradition of Beatrix Potter, modernized with the flat, confident color sensibility of contemporary Oatly packaging. Fine ink linework: delicate, slightly imperfect 1–2pt lines with visible hand tremor, precise on subjects, looser at edges. Color applied as soft watercolor washes that bleed gently past the linework, layered over a warm parchment background (#F5ECD7) — never pure white. Palette limited to forest green (#4A7C59), terracotta orange (#D4732A), warm brown (#8B5E3C), harvest gold (#F0C040). Light paper grain, dry-brush edges, occasional pencil under-sketch showing through. Compositions breathe: at least 30% negative parchment space. NEVER include: photorealism, 3D rendering, neon or saturated primary colors, digital gradients, text or lettering, human faces, sci-fi or fantasy elements, plastic objects, hard black outlines, pure white backgrounds.
```

**Excepciones aprendidas (cuándo desviarse conscientemente del bloque base):**
- **Patrones tileables (C4-C5):** el fondo debe pedirse **perfectamente plano, sin textura de papel**, o el patrón no repetirá sin costuras. La textura de papel es incompatible con seamless tiling.
- **Stickers decorativos con color botánico real (ej. semilla partida, corona de trigo):** cuando el propósito es destacar y ser memorable, el color botánico honesto (verde-musgo, ámbar de abeja) puede superar a la paleta estricta de 2 colores. Se decide caso por caso, nunca por defecto.
- **Recibos, carteles, objetos cuya identidad depende de tener texto:** la regla "no text" no aplica cuando el texto es parte de la narrativa del objeto (ej. un recibo de supermercado). Si el texto es decorativo/rotulado, sí se prohíbe.

**Regla de diversidad étnica (no negociable):** toda figura humana (manos, personas parciales) debe representar diversidad de tonos de piel a través del conjunto de contenido — nunca default a piel clara como estándar.

---

## 5. Errores conocidos de generación (Gemini/Nano Banana) — verificar antes de aprobar

| Problema | Cómo se manifiesta | Corrección |
|---|---|---|
| Contenido de jars/frascos | Interpreta líquidos genéricos en vez del contenido pedido (miel opaca sale como té translúcido) | Describir textura física exacta + acción física reconocible (ej. "miel espesa goteando de cuchara") |
| Escala de manos | Manos de niño salen con proporción de adulto | Especificar "noticeably smaller and pudgier than an adult hand, proportioned like a toddler" |
| Simetría en composiciones circulares | Elementos se concentran en un lado (ej. moras solo a la derecha) | Exigir explícitamente que ambas mitades contengan la mezcla completa de elementos |
| Texto no solicitado | Aparecen letras/números en objetos sin pedirlo | Añadir "no legible text, no readable numbers" si el objeto no necesita texto para su identidad |
| Patrones no tileable | Costura visible al repetir en mosaico | Pedir fondo perfectamente plano sin textura; **verificar con mosaico 2x2/3x3 antes de aprobar**, nunca asumir |
| "Logo" con exceso de detalle vectorial | Sale como ícono de app genérico, sin conexión a la marca | Para piezas de marca "logo", usar el bloque de estilo completo (acuarela, no línea vectorial limpia) salvo que se pida explícitamente minimalismo |

---

## 6. Flujo de aprobación (cómo se decide qué se sube)

1. **Generar** con prompt basado en el bloque de estilo + brief específico.
2. **Revisar contra el brief original** — ¿cumple composición, mood, elementos pedidos?
3. **Verificar reglas técnicas** (tiling si aplica, diversidad si hay personas, ausencia de texto no deseado).
4. Si falla: **ajustar el prompt de forma quirúrgica** (una variable a la vez) — no regenerar desde cero sin diagnóstico.
5. Si pasa 2-3 intentos sin lograrlo: pausar y repensar el enfoque en vez de seguir iterando a ciegas.
6. **Aprobado** → nombrar según convención (Sección 3) → subir a la carpeta correcta (Sección 2) → registrar en Airtable (Sección 7).

---

## 7. Registro en Airtable — tabla `Assets`

**Base:** Feed Your Roots US Data Sheets (`appMy5aOwifSbBLPR`)
**Tabla:** `Assets` (`tblkzOtjS4KK5B2Xn`)

| Campo | Tipo | Notas |
|---|---|---|
| Nombre de archivo | Texto | Debe coincidir exacto con el nombre en Drive |
| Categoría | Selección única | Social Media / Ad Creative / Brand Asset / Elemento Decorativo / Web / Narrative Stock / Producto Finalizado |
| Subcategoría/Uso | Selección única | TikTok Cover, IG Square, Hook, Blog Header, etc. |
| Aspecto | Selección única | 1:1, 9:16, 4:5, 2:3, 3:2, 16:9 |
| Link Drive | URL | **Obligatorio** — sin esto el registro no sirve para nada |
| Carpeta Drive | Selección única | Ruta legible, debe coincidir con Sección 2 |
| Descripción breve | Texto largo | Una línea de contenido, suficiente para buscar por concepto |
| Fecha de creación | Fecha | |
| Tags | Selección múltiple | Palabras sueltas de búsqueda libre — el campo más importante para recuperación real |
| Proyecto/Producto | Selección única | Hoy solo "Feed Your Roots US"; reservado para expansión LATAM/España futura |
| Reutilizable en | Selección múltiple | Redes sociales / Blog / Libro / Publicidad / Web / Video / Marca |

**Regla de oro:** ningún asset se considera "terminado" hasta que tiene su fila en Airtable **con el Link Drive real** (no un placeholder). Un asset sin link es un asset invisible para cualquier agente futuro.

**Cómo obtener el link correcto sin errores:** listar la carpeta de Drive completa (`search_files` con `parentId`), nunca escribir un link de memoria o adivinado. Cruzar por nombre de archivo exacto, nunca por posición o suposición de orden.

---

## 8. Producción en lote — lecciones de eficiencia

- **Listar carpetas completas > buscar archivo por archivo.** Una llamada que trae 20-100 resultados es más segura y más barata que 20-100 llamadas individuales.
- **Lotes de Airtable:** máximo 50 registros por llamada de creación/actualización. Para más, dividir en sub-lotes.
- **Verificar antes de asumir:** cuando algo parece automático (ej. tiling nativo de Gemini), comprobarlo con evidencia (mosaico de prueba) antes de aplicar postproceso innecesario.
- **Un error de nombre corrompe silenciosamente.** Nombres parecidos (`E86-rutabaga` vs `E87-rutabaga`, `B01` vs `B02`) requieren doble verificación antes de escribir en lote.

---

## 9. Qué NO está automatizado todavía (honestidad operativa)

- Generación de imagen en Gemini/Nano Banana — sigue siendo un paso manual de Johnny.
- Ensamblaje de carrusel en Canva — Canva MCP puede ayudar, pero requiere plantilla base con placeholders ya definida.
- Publicación/programación en redes sociales — no hay conector de publicación directa disponible; sigue siendo manual.
- Producción de copy/guión — puede generarse por Claude a partir de la Malla de 60 Temas + este documento, pero requiere revisión humana antes de publicar.

---

*Este documento se actualiza cada vez que se descubre una regla nueva, un error recurrente, o se ajusta la estructura. No es un documento estático — es la memoria operativa del sistema.*
