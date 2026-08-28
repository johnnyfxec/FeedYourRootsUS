# FYR — Changelog de gobernanza

Registro legible de cambios a los documentos de `knowledge/` (fuente de
verdad del proyecto). Se actualiza junto con cada commit que toque estos
documentos — no reemplaza `git log`, lo complementa explicando el motivo
en lenguaje natural.

Formato: `AAAA-MM-DD — documento(s) — qué cambió y por qué`

---

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
