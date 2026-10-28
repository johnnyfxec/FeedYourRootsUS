# FYR — Banco de Cierres / CTA — v1

**Origen (27-oct-2026):** Johnny identificó que toda pieza de FYR termina en el mismo patrón — nombrar el recurso/bundle del tema (campo `CTA Sugerido` en `Content_Pieces`, texto libre) y decir "link in bio" — sin importar la fase del embudo. Esto se siente como venta dura incluso en piezas F1/F2 donde Morgan todavía ni sabe que tiene el problema. La corrección no es "vender menos" en abstracto: es tener más de un tipo de cierre disponible, y elegir el correcto según qué tan lista está la persona para comprar algo.

**Corrección 27-oct-2026 (más tarde el mismo día):** la versión original de este documento decía que "Bundle Relacionado" era el nombre histórico de `CTA Sugerido`, migrado/renombrado en Route B. Eso era falso — verificado contra `get_table_schema` en vivo: `Themes.Bundle Relacionado` (singleSelect: Starter/Family/Core/Homestead/Homestead Complete) sigue existiendo hoy, nunca lo tocó Route B, y es un campo DISTINTO de `Content_Pieces.CTA Sugerido`. El error no cambia nada de la lógica de este documento (las 3 familias de cierre y el mapeo por fase son correctos), pero sí importa para quien escriba el cierre: el recurso que se nombra en un cierre A puede venir del `Bundle Relacionado` del tema (la opción "canónica" por pilar) o del `CTA Sugerido` de la pieza (más específico, puede variar de la canónica si el brief lo justifica) — ver `fyr-content/SKILL.md` §1 para ambos campos.

**Principio rector:** el cierre no es el "parche de monetización" al final de la pieza — es la continuación lógica de lo que la pieza ya hizo. Si la pieza dio valor real, el cierre correcto casi nunca es "compra esto". Casi siempre es "sigue la conversación que ya empezamos" o, en las fases donde sí corresponde vender, nombrar la solución como consecuencia natural de la objeción que la pieza acaba de resolver.

---

## Las 3 familias de cierre

### A. CIERRE DE VENTA
**Qué hace:** nombra el recurso/bundle específico de la pieza (campo `CTA Sugerido` en `Content_Pieces`), con "link in bio".

**Principio psicológico:** funciona solo cuando la persona ya cruzó el umbral de "sé que tengo este problema y estoy evaluando qué hacer". Antes de ese punto, nombrar un producto no vende — interrumpe.

**Regla de uso:** reservado casi en exclusiva a F3 (destruir objeción) y F4 (autoridad/resultado). En F1/F2 solo se usa si el tema específico lo pide explícitamente (p. ej. una pieza diseñada deliberadamente como anuncio directo) — nunca por defecto.

**Estructura:**
> [resolución del último loop abierto] + [nombre del recurso] + "link in bio"

**Ejemplos (ya en uso, sin cambios):**
- "Preservation log and troubleshooting guide, link in bio." (F1 — *mal usado*, ver nota abajo)
- "Your zone, your calendar, your plan. Climate Zone Garden Planner → link in bio." (F4 — uso correcto)
- "Same coop, same hens — just not the overpriced version." + "Shopping & Sourcing Guide, real price ranges included — link in bio." (F2 — uso correcto, nombra el recurso como la forma de evitar el error que la pieza mostró)

**Nota de la auditoría 27-oct:** PZA_7.1 y PZA_11.2 (ambas F1) usan este cierre cuando según el Paso 3 del SKILL debería ser implícito/sin bundle. Son los casos que motivaron este documento.

---

### B. CIERRE DE ENGAGEMENT
**Qué hace:** invita a comentar, contar su propia experiencia, etiquetar a alguien que vive lo mismo, o elegir entre dos opciones. Cero mención de producto.

**Principio psicológico:** en F1 la persona recién está reconociendo el problema — pedirle que compre es prematuro, pero pedirle que *hable* es natural, porque la pieza ya la hizo sentirse identificada. Además genera prueba social real (comentarios genuinos) que alimenta futuras piezas, en vez de depender solo de autoridad declarada.

**Regla de uso — relatable, no competitivo:** la invitación busca compañía en la experiencia, no el caso más dramático. "Cuéntame cuál fue el peor" pide que entretengan con su fracaso. "Seguro no soy el único" pide identificarse. Siempre la segunda lógica, nunca la primera.

**Estructura:**
> [pregunta o invitación específica atada al error/dato exacto que la pieza mostró] + [frase que normaliza, no que premia el extremo]

**5 ejemplos:**
- "¿Cuántos frascos tuviste que perder antes de encontrar esto? Cuéntame — seguro no soy el único."
- "Si tu suelo también huele raro cuando lo volteas, cuéntame qué hiciste — quiero saber si a todos nos pasó lo mismo."
- "¿A ti también te tocó perder una temporada completa por seguir la fecha del paquete? Dímelo abajo."
- "Etiqueta a quien necesita ver esto antes de que pase lo mismo con su próximo pedido de enero."
- "¿Empiezas con media acre o con algo más chico? Cuéntame tu punto de partida — tengo curiosidad real."

**Compatible con:** F1 (uso principal, casi siempre), F2 (mitad engagement / mitad venta suave, ver tabla abajo)

---

### C. CIERRE DE LOOP / RETENCIÓN
**Qué hace:** cierra el loop visual/narrativo abierto en la portada (regla ya existente del SKILL, Paso 3) sin pedir ninguna acción explícita — o, en video, el cierre A/B ya documentado (pregunta cuya respuesta son las primeras palabras / frase cortada que el inicio completa). El valor y el perfil hablan solos.

**Principio psicológico:** cuando la pieza ya demostró autoridad (F4) o cuando forzar cualquier CTA rompería el tono (piezas de pura demostración/resultado), no pedir nada es más persuasivo que pedir algo — la ausencia de venta confirma que el valor entregado era el punto, no el anzuelo.

**Regla de uso:** no sustituye a A o B — se usa cuando ninguno de los dos encaja sin forzar el tono. Es el cierre por defecto del formato video ya implementado (cierre A/B); en carrusel es la opción menos usada, reservada a piezas F4 de pura demostración.

**Estructura:**
> [resolución visual del loop de portada, transformado] — sin texto de acción, o con la pregunta/frase-gancho ya documentada para video

**Ejemplos:** el mecanismo de cierre A/B de video ya está documentado en `FYR_Protocolo_Edicion_Video.md` — no se repite aquí. En carrusel: PZA_1.1 ("Cierre B: pregunta cuya respuesta son las primeras palabras del video") aplicado a slides, usando el mismo principio.

---

## Mapeo por defecto: Fase Embudo → tipo de cierre

| Fase | Cierre por defecto | Por qué | Excepción |
|---|---|---|---|
| F1 - Baja conciencia | **B (Engagement)** | Apenas descubre el problema; pedir compra es prematuro, pedir que hable es natural | Si el tema fue diseñado deliberadamente como anuncio directo (raro, confirmar con Johnny) |
| F2 - Media conciencia | **Mitad B, mitad A suave** (nombra el recurso sin presión de urgencia, ej. "Shopping & Sourcing Guide, real price ranges included") | Está evaluando alternativas — algo de autoridad ayuda sin presionar | — |
| F3 - Alta conciencia | **A (Venta directa)** | Ya está convencida del problema, decide la solución — ofrecer es natural aquí | Puede combinarse con B si el tema se presta ("y cuéntame si a ti también...") |
| F4 - Autoridad | **A (venta de resultado) o C (loop/retención)** | Ya confía — el cierre invita a actuar o a replicar, con o sin venta | — |

**Mezcla mensual de referencia:** con la distribución de fases ya establecida (40/27/20/13 para F1/F2/F3/F4), este mapeo implica que la mayoría de piezas del mes (≈67%, F1+F2) llevan cierre de engagement o mixto — no venta directa. Esto es intencional: es la corrección al patrón "siempre hay CTA de venta" que motivó este documento.

---

## Efecto sobre `CTA Sugerido` y `Bundle Relacionado`

Ambos campos (`Content_Pieces.CTA Sugerido`, texto libre por pieza; `Themes.Bundle Relacionado`, singleSelect canónico por tema) dejan de ser una instrucción obligatoria ("esta pieza/tema SIEMPRE cierra nombrando este recurso") y pasan a ser **la opción de venta disponible**, que el Paso 3 de `fyr-content/SKILL.md` usa solo cuando la Fase Embudo de la pieza dice que corresponde cierre A. En F1 ninguno de los dos se consulta para el cierre. No requiere cambio de esquema en Airtable — solo cambia cómo el SKILL decide usarlos.

---

*Documento v1 — 27-oct-2026. Complementa `hooks_verbales_20_v2.md` (que rige la apertura) y el Paso 3 de `fyr-content/SKILL.md` (que rige el cierre). Próxima revisión: cuando haya suficientes piezas publicadas con este sistema para medir si el engagement real (comentarios) sube en F1/F2.*
