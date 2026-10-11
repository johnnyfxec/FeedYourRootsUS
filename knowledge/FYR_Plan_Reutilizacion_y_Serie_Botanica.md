# FYR — Plan de reutilización de assets y serie botánica
**Versión 1.0 — 11 de octubre de 2026**
**Propósito:** que el banco de assets ya producido (241 registros en `Assets`) sea parte permanente de cómo se decide y se produce cada pieza, y fijar la serie recurrente basada en las ilustraciones botánicas. Se edita en su sitio: cuando algo cambia se reescribe la sección afectada.

---

## 1. Principio (decisión de Johnny, 11-oct-2026)

No se genera "a lo loco". Antes de pedir una imagen nueva se revisa el banco; lo que se genera de nuevo debe volver al banco y poder reutilizarse. La calidad de las ilustraciones existentes es un activo de marca, no material de un solo uso.

## 2. Qué hay en el banco (conteo en Airtable, 11-oct-2026)

| Clase | Cantidad | Cómo se usa |
|---|---|---|
| **Escenas narrativas** (`06_Narrative_Stock`) | 21 | Imagen de slide directa. 5 usadas en PZA_4.2, **16 libres**: 10 en 9:16, 5 en 4:5, 1 en 1:1 |
| **Ilustraciones botánicas de fondo transparente** (`03_Seed_Library/WObg` L01–L101 + `02_Decorative_Elements` E01–E36) | 136 (101 + 35) | Piezas de construcción: necesitan un layout propio (ver §5). Base de la serie |
| Portadas de producto, social, marca, marcos, anuncios, web | ~84 | CTA visual del recurso, portadas de video, marcos de layout |

Solo 6 assets tienen una pieza enlazada (los de PZA_4.2). El enlace `Assets Usados` de `Content_Pieces` es la memoria de uso: cada pieza nueva lo llena y de ahí salen "veces usado" y "último uso".

Escenas libres hoy:
- **4:5 (5):** `STOCK-vecino-terreno-subutilizado`, `STOCK-patio-abandonado-pov`, `STOCK-patio-prospero-pov`, `STOCK-comparacion-vecino-libreta`, `STOCK-plano-ideal-homestead_4x5`.
- **1:1 (1):** `STOCK-plano-ideal-homestead_1x1`.
- **9:16 (10):** `patio-abandonado-notas`, `patio-prospero-notas`, `jar-harvest-2023`, `hand-holding-jar-blank-tag`, `child-greenhouse-seedtray`, `industrial-warehouse-distribution`, `bare-feet-soil`, `kitchen-table-harvest`, `open-hand-single-seed`, `woman-harvesting-tomatoes`.
- Varias escenas traen texto horneado ("Spring Sowing 24", "Garden Bed III"): se reutilizan menos. Las nuevas se piden sin texto.

## 3. Mecanismos (cómo se vuelve costumbre)

1. **Primero el banco.** Paso 4 de `fyr-content`: buscar en `Assets` antes de proponer `[GENERAR EN GEMINI]`. El brief declara "X de N slides salen del banco".
2. **De assets a temas.** Paso 0 de `fyr-content`: además de elegir tema y buscar assets, se puede partir de assets libres o poco usados y proponer temas que los aprovechen. En la elección de tema pesa la cobertura del banco (§4).
3. **Memoria de uso.** Campos en `Assets`: veces usado, último uso, en descanso. Una escena no se repite en dos piezas seguidas. Los escribe Claude.
4. **Generar para el banco.** Gemini se pide en kits de 8–10 escenas por pilar, sin texto horneado, con el bloque de composición de `FYR_Layout_Specs_v1.md`. Cada imagen nueva se registra en `Assets` con tags pensados para reuso.
5. **Medirlo.** El resumen semanal incluye porcentaje de reutilización y assets sin usar.

Límite honesto: con 4 publicaciones al día, las 16 escenas libres alcanzan para 2–3 semanas. El banco es un arranque; el punto 4 es lo que lo sostiene.

## 4. Informe de cobertura: Malla (61 temas) contra el banco

Estimado por nombres, descripciones y tags de los assets, **sin revisión visual imagen por imagen**. Se rehace cuando entran assets nuevos.

| Cobertura | Temas | Qué cubre el banco | Qué falta |
|---|---|---|---|
| **Alta** | 1.2 (carrusel) | Set completo en 4:5: vecino, patio abandonado, patio próspero, comparación con libreta, plano | Nada de imágenes; solo texto y layout |
| **Alta** | 1.5 (carrusel) | Mismo set patio antes/después | Compite con 1.2 por las mismas escenas: se produce uno primero |
| **Parcial-alta** | 1.1 (video) | 5 escenas 9:16 (patio abandonado, semilla en mano, pies en tierra, patio próspero, mesa de cocina) + portada de video | Una imagen del lápiz/papel (la única nueva) |
| **Parcial-alta** | 8.6 (carrusel) | Patio abandonado + plano ideal en 4:5 | Cierre y 1–2 slides |
| **Parcial** | 7.1, 7.4 (video) | `jar-harvest-2023`, `hand-holding-jar-blank-tag`, `kitchen-table-harvest` | 2–3 escenas de proceso |
| **Parcial** | 5.3 (video) | Mesa de cocina, cosecha de mujer | Receta/niño cocinando |
| **Parcial** | 4.1, 4.5 (video) | `child-greenhouse-seedtray` + escenas de 4.2 tras su descanso | Escenas de otras edades |
| **Parcial** | 3.4 (video), 8.1/8.2, 1.3 | 1 escena cada uno (semilla en mano, plano) | El resto |
| **Material listo, falta layout** | 3.1, 3.2, 3.5 y la serie botánica (§5) | 101 ilustraciones de plantas de alta calidad | Layout `ficha_planta` |
| **Sin cobertura** | Pilares 2, 6, 9, 10, 11 y el resto | — | Se genera en kits por pilar (§3.4) |

Escena sin tema en la Malla: `industrial-warehouse-distribution` (dependencia de la cadena de distribución), con `bare-feet-soil` y `open-hand-single-seed` forma el arco "por qué Feed Your Roots". Candidato a tema nuevo.

## 5. Serie "Conoce la planta" (nombre de trabajo)

**Idea (Johnny, 11-oct-2026):** hay 101 ilustraciones botánicas en la Seed Library y 52 semanas: **2 plantas por semana, cada una en carrusel 4:5 y en video 9:16** (4 piezas por semana de la serie). 101 plantas ÷ 2 por semana = unas 51 semanas, es decir, un año completo. Las 35 ilustraciones decorativas y las plantas extra sirven de reserva.

- **Contenido:** característica, curiosidad, cuándo sembrar, con qué se lleva bien. Sale de los PDF (Seed Library, Planting Calendar, Troubleshooting): es el ejemplo de tema extraído de un PDF.
- **Imágenes:** la ilustración de la planta es la protagonista; las demás imágenes de la pieza se generan en relación con ella.
- **CTA:** al Seed Library Kit (Starter Bundle) cuando corresponda; no en todas las piezas.
- **Calendario:** ordenar las plantas por temporada de siembra en EE. UU. para que la planta de la semana sea la que toca sembrar.
- **Recordación:** es una serie con nombre, formato fijo y ritmo semanal; eso es lo que la audiencia aprende a esperar.
- **Requisito técnico:** layout nuevo `ficha_planta` (ilustración transparente centrada sobre pergamino, con título y texto). Verificar antes el tamaño y proporción reales de las ilustraciones.
- **Registro:** tabla nueva en Airtable con las 101 plantas (semana, estado, piezas), llevada por Claude.
- **Se mide como cualquier variable:** primero un piloto de una planta en los dos formatos, antes de comprometer las 52 semanas.

## 6. Primera corrida (decidida el 11-oct-2026)

Dos temas con escenas ya generadas y distintas de las de PZA_4.2, pensados como primeros posts de los fundadores:

| Formato | Tema | Por qué |
|---|---|---|
| Carrusel 4:5 | **1.2** "5 ACRES VS HALF AN ACRE" | Set completo en 4:5 ya generado; historia de fundadores; entrada al Core Bundle |
| Video 9:16 | **1.1** "I STARTED WITH HALF AN ACRE AND A PENCIL" | Origen de la marca; 5 escenas 9:16 libres; una sola imagen nueva |

Ambos comparten el mundo del patio antes/después con assets distintos por formato. Si Johnny prefiere imágenes sin repetir, el video alterno es 7.1 (tarros).

PZA_4.2: producida por completo en 9:16, solo pendiente de publicar. En Airtable quedó `Estado Producción = Ensamblado` y `Hook Usado = 17` (el asignado en `Themes`).

## 7. Orden de ejecución acordado

1. **Registro y cobertura:** este documento, CHANGELOG, Proyecto. *(hecho)*
2. **Memoria de uso:** campos de uso en `Assets` y llenado a partir de `Assets Usados`.
3. **`fyr-content`:** reglas de §3.1 y §3.2 en el Paso 0 y el Paso 4; enlace a este documento. Tarjeta de skill única al final de la fase.
4. **Corrida 1.2 + 1.1:** briefs, config/JSON, ensamblado (carrusel en la PC, video en Actions) y registro en Airtable por paso. Mide el tiempo real del carrusel.
5. **Publicación:** `fyr-publisher` con YouTube primero; salen 4.2, 1.1 y 1.2. Orden sugerido de salida: 1.1 (quiénes somos), 4.2, 1.2; una publicación diaria las primeras dos semanas.
6. **Serie botánica:** layout `ficha_planta` (en paralelo mientras Johnny genera y revisa imágenes del punto 4), piloto de una planta en dos formatos, tabla de plantas y calendario por temporada.
7. **Kits de generación por pilar** para mantener el banco por delante de la publicación.
