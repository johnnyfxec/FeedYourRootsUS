# FYR — Arquitectura del Motor de Ensamblado (assemble.py)
**Versión 1.0 — 24 de agosto 2026**
**Propósito:** especificación completa de los 6 dominios que debe resolver el motor de ensamblado local (Pillow, sin Canva) para producir slides finales sin margen de error. Este documento se lee ANTES de escribir o modificar `assemble.py` — es el contrato que el código debe cumplir, no una sugerencia.

---

## 0. El hallazgo que reorganiza todo: los 12 layouts NO se comportan igual

Intentar tratar los 12 layouts con una sola lógica de "imagen + texto" es la raíz de los huecos que fueron apareciendo uno por uno. La realidad es que hay **4 comportamientos distintos**, y cada layout pertenece a exactamente uno:

| Tipo | Comportamiento | Layouts |
|---|---|---|
| **A — Contenedor Escalable** | El asset (marco) se REDIMENSIONA dinámicamente según el % imagen/texto del slide (Sección 3, tabla de proporción). Imagen detrás, marco encima, texto debajo del marco en el espacio restante. | Marco grande, Doble marco superpuesto (×2 ventanas) |
| **B — Contenedor Fijo** | El asset (etiqueta, nota) se usa a escala fija (~90-100% de su tamaño medido), posicionado en su bbox ya medido. El texto vive DENTRO del cuerpo del asset, no debajo. No usa la tabla de proporción — su tamaño no depende de cuánto texto lleve el slide. | Etiqueta colgante, Nota-kraft en esquina, Ventana Polaroid |
| **C — Generado Completo** | Gemini ya entregó el slide completo (texto + fondo horneados juntos, usando el archivo de referencia de estilo). El script NO compone nada — solo verifica tamaño/zona segura y coloca el PNG tal cual. | Palabra-acuarela, Tachado/corrección |
| **D — Acento Superpuesto** | No es un layout independiente — es una decoración que se agrega ENCIMA de un layout Tipo A o de Full-bleed ya resuelto. Nunca aparece solo. | Cordel guía, Migas de progreso |

Los 3 layouts "base" que no están en la tabla de arriba (Full-bleed, Solo texto+acento, Texto+imagen lateral) son variantes propias sin asset fijo — se documentan en la Sección 2.5 con su propia regla de composición.

Esta clasificación es la que faltaba — sin ella, el script intentaría aplicar "redimensionar según %" a una etiqueta colgante (que debe mantenerse fija) o esperaría texto separado en un Tipo C (que ya no lo necesita).

---

## 1. Dominio: Geometría del canvas

| | 4:5 (carrusel) | 9:16 (video) |
|---|---|---|
| Canvas total | 1080×1350 | 1080×1920 |
| Zona segura — límite duro (nunca cruzar) | top: 12.5% (169px) / bottom: 83.3% (1125px) | top: 12.5% (240px) / bottom: 83.3% (1600px) |
| Margen práctico de diseño (estándar real, Plantilla A) | top: 15.2% (205px) / bottom: 86.5% (1168px) | top: 15.2% (292px) / bottom: 86.5% (1661px) |

**Regla:** todo contenido esencial (texto, rostro, elemento que comunica el hook) vive dentro del margen práctico. La zona entre el margen práctico y el límite duro es aire de seguridad adicional, no zona de contenido activo.

---

## 2. Dominio: Geometría por layout — las 4 categorías en detalle

### 2.1 — Tipo A: Contenedor Escalable (Marco grande, Doble marco)

El tamaño del marco NO es fijo — se deriva del % imagen/texto asignado al slide (ya existe en `SKILL.md` Sección "Proporción imagen/texto por función del slide").

**Algoritmo:**
```
usable_height = margen_practico_bottom - margen_practico_top
image_zone_height = usable_height * (%imagen / 100)
text_zone_height = usable_height * (%texto / 100)

# El marco se escala manteniendo su proporción interna real (medida en Layout_Specs),
# ajustado para que su ALTO TOTAL (marco+ventana) quepa en image_zone_height
frame_scale = image_zone_height / alto_original_del_asset_marco
frame_width_final = ancho_original_del_asset_marco * frame_scale

# Centrado horizontal
frame_x = (canvas_width - frame_width_final) / 2
frame_y = margen_practico_top

# La ventana interior (para la imagen de escena) se escala con el mismo frame_scale
ventana_x = frame_x + (ventana_x_original * frame_scale)
ventana_y = frame_y + (ventana_y_original * frame_scale)
ventana_w = ventana_w_original * frame_scale
ventana_h = ventana_h_original * frame_scale

texto_y_inicio = frame_y + (alto_original_del_asset_marco * frame_scale) + 20px_margen
```

**Doble marco:** mismo algoritmo pero aplicado 2 veces (una por cada uno de los 2 marcos que trae el asset), usando el bbox individual de cada marco ya medido dentro del PNG compuesto. Dos imágenes de escena distintas, dos ventanas.

### 2.2 — Tipo B: Contenedor Fijo (Etiqueta, Nota, Polaroid)

Usa el asset a escala fija — no depende del % imagen/texto del slide (estos layouts casi siempre combinan con un Full-bleed de fondo, así que "imagen" ya está resuelta por el fondo, no por el asset).

| Layout | Escala de uso | Zona de texto (dentro del cuerpo del asset, % relativo al bbox del asset) |
|---|---|---|
| Etiqueta colgante | 100% (tamaño nativo del asset) | Centro del rectángulo kraft, ~65% del ancho del cuerpo, ~50% del alto del cuerpo |
| Nota-kraft esquina | 100% | Centro de la cara visible de la nota, ~80% ancho, ~70% alto |
| Ventana Polaroid | 100% | La ventana interior YA medida en Layout_Specs recibe la IMAGEN (no texto) — el texto de este layout (si existe) va como caption debajo del Polaroid, centrado, en el 10% inferior del canvas |

**Regla de posición del asset en canvas:** se coloca en la posición relativa donde fue medido originalmente (bbox de Layout_Specs, convertido a % del canvas) — no se re-centra ni se mueve, porque su composición interna (sombra, ángulo) ya fue diseñada para esa posición.

### 2.3 — Tipo C: Generado Completo (Palabra-acuarela, Tachado)

Sin composición. El script:
1. Verifica que el PNG recibido mida exactamente el canvas objetivo (1080×1350 o 1080×1920) — si no, es un error de generación, fail loudly, no intentar corregir con estiramiento.
2. Coloca el PNG completo como el slide final, sin más capas encima.
3. Excepción: si el brief pide un elemento Tipo D (acento) combinado, ese sí se agrega encima (ver 2.4).

### 2.4 — Tipo D: Acento Superpuesto (Cordel, Migas)

Se agregan como capa final, encima de cualquier slide ya resuelto (Tipo A, B, C, o Full-bleed).

| Acento | Posición | Escala |
|---|---|---|
| Cordel guía | Esquina a esquina (bbox ya medido, atraviesa el canvas) | 100% del canvas, sin reescalar — ya está diseñado a tamaño completo |
| Migas de progreso | Franja horizontal centro-baja (bbox ya medido) | 100%, posición fija relativa |

**Regla:** el JSON de un slide puede declarar `"acento": "cordel_guia"` opcionalmente además de su `layout` principal — nunca un acento sin layout base.

### 2.5 — Layouts sin asset fijo (Full-bleed, Solo texto+acento, Texto+lateral)

| Layout | Composición |
|---|---|
| **Full-bleed** | Imagen de escena ocupa 100% canvas (crop-to-fill si no calza exacto) → franja overlay parchment semi-transparente (alpha 90-95%) en el tercio inferior → texto centrado sobre la franja |
| **Solo texto+acento** | Fondo parchment sólido → texto centrado en el 100% del área de contenido (sin ventana de imagen) → acento botánico opcional (pequeño, no listado en Layout_Specs porque usa el banco de 130+ ilustraciones sueltas, no un asset de layout fijo) |
| **Texto+lateral** | Fondo parchment sólido → imagen de escena sin marco, 40-60% del ancho, en el lado declarado por el brief (izquierda/derecha) → texto en el lado opuesto, alineado hacia el borde exterior (no hacia el centro) |

---

## 3. Dominio: Tipografía — tabla de roles

Ningún texto se renderiza con tamaño "a ojo" — cada ROL tiene fuente, tamaño base, color y comportamiento de overflow ya decididos.

| Rol | Fuente | Tamaño base (4:5) | Color | Uso |
|---|---|---|---|---|
| Título de portada/cierre | SourceSerifPro-Regular.ttf | 93px (medido, cap-height=61px) | `#E8B84B` (Gold) con contorno `#5C3A1E` 6px (medido) | Marco grande en slide 1/cierre |
| Subtítulo | Lora.ttf, weight Italic | 28px | `#5C3A1E` (Brown) | Debajo del título |
| Texto de cuerpo (slides intermedios) | Lora.ttf, weight Regular | 36-44px (ver regla de ajuste abajo) | `#5C3A1E` o `#D4732A` (Terra) según énfasis del brief | Full-bleed, Solo texto, Texto+lateral |
| CTA de cierre | DMSans.ttf, weight Bold | 32px | `#5C3A1E` | Última línea del cierre |
| Palabra dominante (dentro de imagen Tipo C) | — ya horneada por Gemini, el script no la toca | — | — | Palabra-acuarela |

**Tamaño base para 9:16:** mismo valor en px que 4:5 (NO se escala proporcional al alto mayor) — el canvas es más alto pero el texto debe seguir siendo legible al mismo tamaño físico relativo a la pantalla del celular, que es igual en ambos formatos.

### Regla de ajuste automático (overflow)

1. Calcular el ancho disponible de la zona de texto (según el layout, Sección 2).
2. Envolver el texto (word-wrap) al tamaño base.
3. Si el bloque de texto resultante excede el alto disponible de su zona: reducir tamaño en pasos de 2px y repetir, hasta un mínimo de 70% del tamaño base.
4. Si aún al mínimo no cabe: truncar con "…" al final de la última línea que sí cabe, y registrar advertencia en el log de ensamblado (no falla el proceso completo, pero se reporta al usuario al final).

---

## 4. Dominio: Reglas de recorte de imagen (crop-to-fill)

Toda imagen de escena que entra a una ventana (Tipo A o B) o a full-bleed usa el mismo algoritmo, estándar "cover" (igual al `object-fit: cover` de CSS ya usado en los mockups HTML de hoy):

```
scale = max(ventana_ancho / imagen_ancho, ventana_alto / imagen_alto)
imagen_reescalada = imagen.resize(imagen_ancho * scale, imagen_alto * scale)
recorte_x = (imagen_reescalada.ancho - ventana_ancho) / 2   # ancla: centro
recorte_y = (imagen_reescalada.alto - ventana_alto) / 2      # ancla: centro
resultado = imagen_reescalada.crop(recorte_x, recorte_y, ventana_ancho, ventana_alto)
```

**Ancla por defecto: centro.** Si una imagen específica necesita otra ancla (ej. mantener la cabeza de una persona visible si el recorte central la corta), el JSON de esa pieza puede declarar `"ancla_recorte": "top"` para ese slide — pero el default siempre es centro, sin excepción salvo declaración explícita.

---

## 5. Dominio: El motor de ensamblado — contrato del script

### 5.1 — Entrada
Un archivo `PZA_[tema]_config.json` (Sección 6 define su schema exacto).

### 5.2 — Módulos internos (modularidad real, no monolito)

```
assemble.py
├── config_loader.py       → lee y VALIDA el JSON contra el schema (Sección 6) antes de tocar nada
├── layout_specs_reader.py → lee FYR_Layout_Specs_v1.md, expone las coordenadas como diccionario Python
├── layout_classifier.py   → dado un nombre de layout, retorna su Tipo (A/B/C/D) y su función de composición
├── compositors/
│   ├── tipo_a.py           → lógica de la Sección 2.1
│   ├── tipo_b.py           → lógica de la Sección 2.2
│   ├── tipo_c.py           → lógica de la Sección 2.3
│   └── acentos.py          → lógica de la Sección 2.4
├── text_renderer.py       → aplica la Sección 3 completa (fuente, overflow, color)
├── image_fetcher.py       → descarga/cachea desde Drive (assets fijos cacheados permanentemente, escenas por pieza)
└── main.py                → orquesta: lee config → por cada slide, clasifica layout → compone → renderiza texto → exporta PNG
```

**Por qué modular y no un solo archivo:** cada compositor se puede probar aisladamente contra un slide de prueba sin correr el pipeline completo — y si mañana se agrega un layout 13, solo se toca `layout_classifier.py` + un nuevo archivo en `compositors/`, nada más se reescribe.

### 5.3 — Manejo de errores (fail loudly, consistente con el resto del sistema)

| Situación | Comportamiento |
|---|---|
| JSON no valida contra el schema | Detener antes de descargar nada, listar exactamente qué campo falta |
| Imagen de escena no existe en Drive | Detener ese slide específico, reportar cuál, continuar con los demás slides de la pieza |
| Asset de layout no encontrado localmente ni en Drive | Detener todo el proceso — un asset de layout faltante no es recuperable por slide, es un problema de configuración |
| Texto no cabe ni al tamaño mínimo | Truncar + advertir, NO detener (ya definido en Sección 3) |
| Layout declarado en JSON no existe en el clasificador | Detener antes de procesar ese slide, error explícito de "layout desconocido: X" |

### 5.4 — Salida
Un PNG por slide, nombrado `FYR_PZA_[tema]_S[n]_v[version].png`, guardado localmente en `production/output/PZA_[tema]/`, y subido a la carpeta de fecha en Drive ya creada por el flujo existente.

---

## 6. Dominio: Contrato JSON (lo que Claude Code genera, lo que el script consume)

### 6.1 — Principio: Claude Code nunca escribe coordenadas

El JSON solo contiene: qué layout, qué texto, qué imagen, y (cuando el layout es Tipo A) el % imagen/texto ya decidido en el brief. Las coordenadas viven exclusivamente en `FYR_Layout_Specs_v1.md`, leídas por `layout_specs_reader.py`. Esto es lo que garantiza cero margen de error — un solo lugar de verdad para números, nunca duplicados ni reinventados por slide.

### 6.2 — Schema completo

```json
{
  "pieza_id": "PZA_3.1",
  "aspecto": "4:5",
  "slides": [
    {
      "numero": 1,
      "layout": "marco_grande",
      "porcentaje_imagen": 85,
      "imagen_escena": "S1_portada.png",
      "texto_titulo": "MY SEED BOX WAS A DISASTER UNTIL THIS",
      "texto_subtitulo": "Order changes everything.",
      "acento": null,
      "ancla_recorte": "center"
    },
    {
      "numero": 2,
      "layout": "full_bleed",
      "imagen_escena": "S2_antes.png",
      "texto_overlay": "Every seed packet just... thrown in.",
      "acento": null
    },
    {
      "numero": 3,
      "layout": "doble_marco",
      "imagen_escena_1": "S3a_antes.png",
      "imagen_escena_2": "S3b_despues.png",
      "texto_titulo": null,
      "acento": "cordel_guia"
    },
    {
      "numero": 4,
      "layout": "palabra_acuarela",
      "imagen_escena": null,
      "nota": "GENERADO COMPLETO en Gemini con la palabra real ya horneada, usando FYR_LAYOUT_palabra-acuarela_4x5_v1.png como referencia de estilo.",
      "imagen_final": "S4_palabra.png"
    }
  ]
}
```

**Campos obligatorios por Tipo de layout:**

| Tipo | Campos requeridos |
|---|---|
| A (marco_grande) | `layout`, `porcentaje_imagen`, `imagen_escena`, al menos uno de `texto_titulo`/`texto_subtitulo` |
| A (doble_marco) | `layout`, `porcentaje_imagen`, `imagen_escena_1`, `imagen_escena_2` |
| B (etiqueta/nota/polaroid) | `layout`, `imagen_escena` (fondo si aplica), `texto_cuerpo` |
| C (palabra_acuarela/tachado) | `layout`, `imagen_final` (el PNG ya generado completo) |
| Full-bleed / Solo-texto / Texto-lateral | `layout`, `imagen_escena` (excepto Solo-texto), texto correspondiente |

`config_loader.py` valida esta tabla exacta antes de dejar avanzar el proceso — es el "no adivinar" hecho código.

---

## 7. Lo que este documento NO resuelve todavía (honestidad operativa)

- Los valores exactos de zona de texto para Tipo B (Sección 2.2) son un **primer criterio razonable, no medido con precisión de píxel** como sí lo están las ventanas de imagen — deben verificarse contra el primer ensamblaje real y ajustarse si el texto se ve mal posicionado.
- La tabla de tipografía (Sección 3) usa tamaños base estimados a partir de lo que se vio bien en los mockups de hoy — no hay una medición formal de legibilidad en dispositivo real todavía.
- El comportamiento de `Texto+imagen lateral` cuando el brief no especifica izquierda/derecha no está definido — asumir alternancia (par=izquierda, impar=derecha) hasta que se decida lo contrario.
