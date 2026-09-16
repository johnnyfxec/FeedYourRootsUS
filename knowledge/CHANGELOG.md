# FYR — Changelog de gobernanza

Registro legible de cambios a los documentos de `knowledge/` (fuente de
verdad del proyecto). Se actualiza junto con cada commit que toque estos
documentos — no reemplaza `git log`, lo complementa explicando el motivo
en lenguaje natural.

Formato: `AAAA-MM-DD — documento(s) — qué cambió y por qué`

---

## 2026-09-16

- **favicon.ico** -- publicado en la raiz del repo (era el ultimo pendiente
  de la Rama web del handoff del simbolo C14). Fuente: Drive
- **Wordmark solo (cuarta variante de marca)** -- 'Feed Your Roots' sin simbolo, Playfair Display Bold, 4 colores. Aprobado solo para cuando el simbolo ya aparece en otra parte de la misma pieza -- nunca como primera aparicion de marca. Documentado en FYR_Brand_Mark_Spec_v1.md Seccion 05 y en el PDF del manual. Registrado en Airtable y Drive (01_Brand_Assets/C14_Brand_Mark/).
  `01_Brand_Assets/C14_Brand_Mark/favicon.ico`.
- **FYR_Protocolo_De_Trabajo.md** -- se prohibe `sed -n` como comando de
  lectura por indice de linea; se reemplaza por `cat -n` / `awk` con `NR`
  en los tres puntos del documento que lo mencionaban. Se agrega regla
  nueva: cuando el texto de un reemplazo (`old`) tiene mas de una linea
  y contiene tildes o ene, usar reemplazo por indice de linea
  (`readlines()` + `assert` de la linea esperada) en vez de heredoc de
  texto largo como primer intento -- evita fallos de assert por
  diferencias de codificacion/normalizacion Unicode.

## 2026-09-15

- **Simbolo oficial de marca (C14)** -- alta del logo/isotipo aprobado
  (frasco con arbol), trazado en vector desde el original de Johnny.
  4 variantes de color + lockup horizontal + lockup vertical, registrados
  en Airtable (4 filas, un registro por pieza maestra agrupando sus
  variantes). Nuevo `knowledge/FYR_Brand_Mark_Spec_v1.md` con reglas
  medibles (espacio de proteccion X = 15.6% altura, minimo 32px con
  excepcion favicon 16px, proporcion fija 1:1.405).
- **FYR_Asset_Governance_Policy.md** -- v2.3: separacion de C14_Brand_Mark
  de C01-C03_Logo_Concepts (que pasa a ser exploracion historica), y
  excepcion de estilo documentada para el simbolo de marca (tinta plana,
  sin acuarela -- unica excepcion al bloque de estilo base).
- **Badge FYR retirado** de uso activo (no llego a existir en repo/Airtable,
  solo en Drive). **Tree of Life (C01)** reclasificado: ya no es "logo
  oficial", pasa a ilustracion insignia de marca -- descripcion en Airtable
  corregida.
- **Pendiente v1.1** (no bloqueante): gap del lockup vertical mide 142px,
  deberia ser X=99.5px -- ver seccion "Pendientes" en FYR_Brand_Mark_Spec_v1.md.

## 2026-09-13 a 2026-09-14

- **Bug critico resuelto: centrado impredecible en marco_grande_portada** --
  mismo patron que el bug de 30-ago mencionado abajo, ahora en el titulo de
  portada de carrusel: render_text_block centraba el texto dentro de su box,
  generando offset cuando fit_text reducia la fuente. Fix: render_text_block_top
  con margen fijo de 20px bajo el marco.
- **Salto de linea manual en titulos (\n en texto_titulo)** -- _wrap_text
  hacia text.split(), que colapsaba \n como espacio -- no habia forma de
  forzar jerarquia retorica en un titulo de 2 lineas. Fix: _wrap_text respeta
  \n como salto forzado, wrap automatico dentro de cada segmento.
- **full_bleed corregido de raiz + ventana_texto (layout nuevo)** -- full_bleed
  recortaba la imagen al canvas completo y pegaba un overlay semi-transparente
  encima, dejando SIEMPRE imagen real visible detras del texto sin importar el
  contenido. Confirmado con evidencia visual real en PZA_1.2 Slide 2.
  full_bleed se corrige a SOLO imagen (modo contain, nunca crop), nunca texto.
  ventana_texto (nuevo) reemplaza el uso-con-texto: imagen contenida arriba +
  franja de texto SOLIDA (sin transparencia) abajo. Refaccion completa de
  punta a punta: codigo (base.py, config_loader.py, layout_specs.py),
  gobernanza (FYR_Layout_Specs_v1.md, FYR_Motor_Ensamblado_Arquitectura_v1.md,
  FYR_Principios_De_Composicion.md), SKILL.md (3 referencias corregidas), y
  migracion de los 4 briefs existentes que usaban full_bleed con texto.
- **Proporcion derivada en ventana_texto** -- la zona de imagen ya no es 2/3
  fijo, se calcula a partir del ratio real de la imagen (ancho canvas / ratio),
  con tope maximo 80% imagen / piso minimo 20% texto. Validado con caso real
  (portada del Half-Acre Blueprint, ratio 0.773 -> 78% imagen calculado antes
  del tope, coincide con el 80% pedido).
- **render_text_block_top aplicado a texto de cuerpo** -- solo_texto,
  ventana_texto, texto_lateral usaban render_text_block (centrado, con el
  mismo bug de offset). Los 3 migrados a render_text_block_top.
- **Politica de salto de linea manual en texto de cuerpo (gobernanza nueva)**
  -- 3 formas retoricas identificadas (producto/activo nombrado -> linea
  propia; serie de clausulas cortas -> setup agrupado + remate aislado; caso
  general -> pausa gramatical mas cercana al punto medio), con verificacion
  de ancho real via draw.textlength() antes de fijar el corte. Documentado en
  FYR_Motor_Ensamblado_Arquitectura_v1.md Seccion 3.
- **Puentes narrativos entre slides de imagen pura (gobernanza nueva,
  FYR_Principios_De_Composicion.md Seccion 8)** -- Test de Silueta (principio
  de animacion clasica) + apertura/cierre de loop narrativo (ya documentado
  en Sistema_Maestro_CRS_v2.md) combinados en una regla: cuando una secuencia
  de full_bleed cambia de sujeto o abre un loop sin nombrarlo, insertar un
  slide solo_texto puente -- nunca agregarle texto a la imagen. Fase 4 del
  roadmap (extension a video/reels) identificada y anotada, no iniciada.
- **Limpieza de repositorio:** .gitignore actualizado (produccion nunca va a
  Git -- production/briefs/, assets_local/, output/, pdfs_normalized/);
  archivos ya trackeados desde antes sacados del tracking con git rm --cached
  (contenido intacto en disco). Confirmado que las 3 piezas demo
  (PZA_demo/_seeds/_reel) usaban placeholders sinteticos que ocultaban el bug
  de full_bleed -- no son referencia confiable hasta regenerarse.
- **FYR_Protocolo_De_Trabajo.md** -- 6 reglas de comportamiento nuevas:
  codigo siempre con indice de linea, grep/sed de confirmacion en el mismo
  bloque que el cambio, comando de Termux automatico ante pedidos de
  actualizar/verificar, prohibicion de /tmp, evitar `!` en heredocs de bash
  interactivo (history expansion), y registro obligatorio en este CHANGELOG
  tras hitos importantes.

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
