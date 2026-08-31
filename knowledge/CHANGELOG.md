# FYR — Changelog de gobernanza

Registro legible de cambios a los documentos de `knowledge/` (fuente de
verdad del proyecto). Se actualiza junto con cada commit que toque estos
documentos — no reemplaza `git log`, lo complementa explicando el motivo
en lenguaje natural.

Formato: `AAAA-MM-DD — documento(s) — qué cambió y por qué`

---

## 2026-08-30

- **assemble.py (COMPLETO)** -- el motor de ensamblado local queda terminado:
  main.py (orquestador), image_fetcher.py (verificacion de assets, no
  descarga directa), compositores Tipo A/B/C/BASE/acentos completos y
  probados. Primera pieza real generada de punta a punta (PZA_demo, 5
  slides en produccion/output/).
- **marco_grande_cuadrado (layout nuevo)** -- portada de reel/video 9:16,
  asset fijo con vid+hoja integrados (FYR_ASSET_marco-cuadrado_9x16_v1.png,
  registrado en Airtable y Drive C12_Frames), sin escalado dinamico.
- **marco_grande_portada (layout nuevo)** -- portada de carrusel 4:5, sin
  subtitulo, ancho fijo (808px) replicando el mismo ancho absoluto que la
  portada 9:16 -- decision de consistencia de marca (4:5 vertical / 9:16
  cuadrado como default de toda portada).
- **Bug critico resuelto: centrado vertical impredecible en texto
  encadenado** -- render_text_block centraba el texto dentro de su box,
  generando offset variable cuando el tamano de fuente se reducia
  internamente. Fix: render_text_block_top (nueva funcion), y decision de
  usar posiciones Y absolutas (medidas independientes) en vez de
  encadenadas para titulo/subtitulo de portada.
- **Herramienta nueva: editor_posicion_texto.html** -- carga la portada
  real y permite ajustar posicion/tamano/interlineado de texto con
  sliders sobre la imagen real, exportando valores en pixeles reales.
- **Geometria rotada medida:** doble_marco, etiqueta_colgante,
  nota_esquina -- todos confirmados rotados en el asset real (~8-12 grados)
  con medidor_esquinas.html, corrigiendo el algoritmo simple original que
  asumia alineacion a ejes.
- **FYR_Asset_Governance_Policy.md** -- aclarada la descripcion de
  C12_Frames (dos tipos de marco distintos: rectangular alto vs cuadrado
  con decoracion integrada).
- **Feed-Your-Roots-Brand-Bible.md** -- excepcion tipografica Source Serif
  Pro corregida (nombre real, no el sucesor Source Serif 4).
- **FYR_Protocolo_De_Trabajo.md** -- fusionada estrategia de ramas desde
  CLAUDE.md (rama de Claude Code).
- **TikTok:** cuenta activa (estaba bloqueada por SIM prepago, ya resuelto).

## 2026-08-28

- **FYR_Protocolo_De_Trabajo.md** — agrega sección "Estrategia de ramas",
  fusionando el conocimiento que vivía en CLAUDE.md (rama de Claude Code):
  main es producción en vivo vía GitHub Pages, código de sitio va en rama
  separada con revisión previa, contenido/texto puede ir directo a main.

- **FYR_Motor_Ensamblado_Arquitectura_v1.md** (creado) — especifica los 6
  dominios de diseño de `assemble.py`: geometría de canvas, los 4 tipos de
  layout (A/B/C/D), tipografía, recorte de imagen, contrato del script,
  schema JSON. Es la base sobre la que se escribió todo el código de
  `production/scripts/assemble/` hasta la fecha.
- **Feed-Your-Roots-Brand-Bible.md** — agregada excepción tipográfica:
  Source Serif Pro Regular reemplaza a Playfair Display específicamente
  para el título de portada/cierre en contenido de video/carrusel
  (Instagram, TikTok). Medido por píxel contra mockup real: 93px,
  cap-height 61px, contorno 6px. Playfair Display se mantiene sin cambios
  para el sitio web y piezas impresas grandes — la Malla ya documentaba
  este criterio de uso por formato, el Brand Bible no lo reflejaba.

## 2026-08-23 a 2026-08-24 (previo a este changelog)

- **FYR_Sistema_Viral_3Skills_Fuente_de_Verdad.md** (creado) — arquitectura
  de los 3 skills (fyr-content, trend-scout, performance-lens) comunicados
  vía Airtable.
- **FYR_Asset_Governance_Policy.md** — v2.2: estructura C09-C13 (Frames,
  Layout_Elements), renombre de layout_specs a FYR_Layout_Specs_v1,
  corrección de 5 referencias rotas en SKILL.md.
- **reference_assets/FYR_Layout_Specs_v1.md** — mismo commit que arriba,
  primera versión con el nombre actual.
- **Feed-Your-Roots-PDF-Guide.md**, **seed-library-final.md** — gobernanza
  de layouts (Hook→Layout, slides por Fase, loop visual en cierre).

## 2026-08-22 (previo a este changelog)

- **FYR_Malla_60_Temas_Virales_v2.md**, **Sistema_Maestro_CRS_v2.md**,
  **hooks_verbales_20_v2.md** — creación inicial junto con la skill
  fyr-content y la base de conocimiento del sistema de contenido.

---

*Para el historial completo de cualquier documento: `git log --follow -- knowledge/NOMBRE.md`*
