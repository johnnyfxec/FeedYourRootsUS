# FYR Publisher — Documento de traspaso a chat nuevo (31-oct-2026)

**Por qué existe este documento:** el chat donde se investigó y construyó casi todo lo de publicación automatizada se saturó de contexto de otro tema (rediseño tipográfico de `doble_marco`). Para evitar perder las conclusiones reales ya verificadas y no repetir trabajo, este documento resume **todo lo relevante para construir `fyr-publisher`**, con pointers exactos a dónde está cada detalle en la gobernanza real.

**Nota de corrección (31-oct-2026):** este documento originalmente apuntaba a dos archivos separados, `FYR_Plan_Publicacion_Automatizada_v1.md` (en el repo) y `v2.md` (que en realidad nunca existió en el repo — vivía solo como doc del Project de claude.ai, invisible para Code). Esa duplicación quedó corregida: ambos se fusionaron en un único documento, **`knowledge/FYR_Plan_Publicacion_Automatizada.md`**, que es ahora la única fuente de verdad. El doc huérfano del Project debe eliminarse una vez confirmado que esta fusión es correcta.

**No leas esto como un plan desde cero.** FYR Publisher está mucho más avanzado de lo que el nombre "voy a construir el publisher" sugiere — 4 de 5 plataformas ya están conectadas y probadas con publicaciones reales. Lo que falta es, en esencia, un orquestador.

---

## 1. Dónde está la fuente de verdad (leer en este orden)

1. **`knowledge/FYR_Plan_Publicacion_Automatizada.md`** — documento único consolidado (fusiona el diseño original del 16-oct con todo lo construido y probado en producción real hasta el 29-oct). Contiene: regla crítica de qué carpetas de Drive son públicas, handles por plataforma, tabla de corrección de límites reales vs. investigación original, estado real por plataforma, tabla de endpoints carrusel/video por plataforma, qué falta construir, esquema real de Airtable, y una sección completa por cada plataforma (Instagram, Pinterest, YouTube, Facebook, TikTok) con su estado, bugs reales encontrados y resueltos, y pendientes. Es la única fuente de verdad de este tema — ya no hay v1/v2 separados.
2. **`.claude/skills/fyr-content/SKILL.md`** — fuente de verdad de los `fieldId` reales de `Content_Pieces` (los campos `Estado IG`/`Estado FB`/etc. están documentados ahí con sus IDs exactos de Airtable).
3. **`knowledge/FYR_Fase_D_Produccion_Recurrente_v1.md` §4** — cómo la Parada 4 ("Publicación y cierre") necesita evolucionar una vez que `fyr-publisher` exista.
4. **Memoria del proyecto, `/projects/.../credenciales-apis.md`** — nombres reales de las variables de entorno (.env) por plataforma. Leer esto antes de asumir nombres de token/ID — es la fuente única, no reconstruir de memoria.

---

## 2. Estado real por plataforma (al 29-oct-2026, verificar si cambió)

| Plataforma | Estado | Script | Nota clave |
|---|---|---|---|
| **Instagram** | ✅ Producción, carrusel real publicado | `production/scripts/meta/meta_publish_carousel.py` | Media ID `17996701389021317`, link real resuelto automáticamente (el shortcode NO es derivable del media_id) |
| **Pinterest** | ✅ Producción (Standard access aprobado) | `production/scripts/pinterest/pinterest_publish_pin.py` | Pin real `1151725304742928915`. **No tiene carrusel** (deprecado en 2026) — regla de 2 Pines por pieza (dolor/resultado), ver documento consolidado §7 |
| **YouTube** | ✅ Resuelto con cuenta de Google dedicada | (subida vía `videos.insert`, script de prueba ya corrido) | Bug estructural real de Brand Account "limitada a YouTube" — nunca reintentar esas rutas, están descartadas con evidencia en el documento consolidado §8. Canal `UC5ntyoURYmn-qyPfOVkMe2w` |
| **Facebook** | Pendiente (vía Buffer, siguiente en la cola) | — | Plan: Buffer Free, 2 canales (FB + Pinterest, aunque Pinterest ya se resolvió vía API directa — revisar si todavía tiene sentido usar Buffer solo para FB, o si vale la pena buscar API directa de Meta para FB también) |
| **TikTok** | 🟡 En revisión de App Review (enviado 29-oct) | `production/scripts/tiktok/tiktok_publish_video.py` | Mientras no se apruebe: todo contenido forzado a `SELF_ONLY`, cuenta debe estar en modo privado, máx. 5 usuarios/24h. Publicación de prueba ya funcionó en Sandbox |

**Regla crítica que aplica a TODAS las plataformas (documento consolidado §0):** cualquier URL de imagen/video para publicar debe resolverse SIEMPRE desde `Content_Pieces/PZA_X/<fecha>/` (la carpeta ya pública del output ensamblado), **nunca** desde `Assets`/banco de stock (no es pública, da 403). Verificar con el comando de `curl` documentado ahí antes de asumir que una URL sirve.

---

## 3. Esquema de Airtable ya construido (no inventar de nuevo)

En `Content_Pieces` (`tblevmNSbGTzdjuDF`), ya existen (ver `fyr-content/SKILL.md` para los `fieldId` exactos):
- `Estado IG` / `Estado FB` / `Estado Pinterest` / `Estado YouTube` / `Estado TikTok` — singleSelect independientes, no un solo campo genérico (para que un fallo en una plataforma no oculte el éxito en otra).
- `Post ID IG` / `Post ID FB` / `Post ID Pinterest` / `Post ID YouTube` / `Post ID TikTok` — texto, el ID crudo de cada API (para auditar/borrar después). Pinterest puede necesitar 2 IDs en ese mismo campo (separador `;`) por la regla de 2 Pines.
- `Fecha Publicación Programada` — separado de `Fecha de Generación`.
- `Plataformas Destino` **fue eliminado** (28-oct) — se deriva en el momento de `Tipo de Pieza` (Carrusel → IG/FB/Pinterest/TikTok; Video → esas 4 + YouTube). No recrear ese campo.
- `Estado Producción` sigue siendo el estado del proceso de armado (Brief Generado → Assets en Drive → Ensamblado → Publicado) — el orquestador debe moverlo a `Publicado` solo cuando TODAS las plataformas destino de esa pieza queden en `Publicado`.

---

## 4. Lo que falta construir (en orden, según el documento consolidado §4)

1. ~~Esquema Airtable~~ — ✅ hecho.
2. Borrar posts/pines/videos de prueba que quedaron en las plataformas (varios pendientes — ver checklist de v2, cada sección tiene su propio "Pendiente inmediato").
3. **`SKILL.md` de `fyr-publisher`** — el verdadero trabajo pendiente. Debe:
   - Leer `Content_Pieces` filtrando por `Estado Producción = Ensamblado` y el `Estado <plataforma>` correspondiente = `Pendiente`.
   - Respetar la ventana de cautela (1 publicación/día por plataforma durante las primeras 1-2 semanas de cada cuenta — cada plataforma cuenta su propia ventana desde que arrancó, no comparten reloj).
   - Despachar la llamada correcta por tipo de pieza (Carrusel/Video) y plataforma — tabla completa en el documento consolidado §3. Pinterest es la excepción: despacha 2 llamadas (2 Pines), no 1.
   - Actualizar `Estado <plataforma>` y `Post ID <plataforma>` al terminar cada una, independientemente de las demás — un fallo en TikTok no debe bloquear ni ocultar el éxito en Instagram.
   - Resolver URLs siempre desde `Content_Pieces`, nunca desde `Assets` (regla crítica, Sección 2 arriba).
4. Completar Facebook (vía Buffer o API directa — decisión abierta) y TikTok (esperando App Review).
5. Decisiones todavía abiertas, sin resolver (documento consolidado §13 completa la lista): ventana de cautela de Instagram (¿1 o 2 semanas?), si usar `location_id`, si agregar comentario automático con link, dónde se genera el alt text, stack de analytics/retargeting, y si el Pin de "dolor" debe apuntar a blog/journal una vez que exista.

---

## 5. Mi lectura sobre "headless" (respuesta a tu pregunta directa)

**Sí, es la jugada correcta — y de hecho ya está medio construida así sin que se haya nombrado explícitamente.** Cada script de publicación (`meta_publish_carousel.py`, `pinterest_publish_pin.py`, `tiktok_publish_video.py`) ya es un script Python autónomo, sin UI, que toma argumentos y llama APIs directas — eso ya es headless por diseño. Lo único que falta para que **todo el flujo** sea headless, no solo cada pieza suelta, es el orquestador.

Ahí hay una decisión real que tomar en el chat nuevo, no asumida todavía en ningún documento: **¿el orquestador corre bajo demanda (alguien le dice a Code "publica el lote de hoy") o corre solo por cron, sin que nadie lo invoque?**

Mi argumento a favor de **cron en GitHub Actions** (mismo patrón que `render-video.yml`, que ya corre sin supervisión):
- Ya existe el precedente técnico funcionando (`render-video.yml`).
- La ventana de cautela (1 post/día) es exactamente el tipo de regla que un cron diario respeta naturalmente — un disparo manual corre el riesgo de que alguien publique 3 piezas el mismo día por descuido.
- Ningún paso de publicación toca la Mesa de Producción (eso quedó confirmado en la sesión del rediseño tipográfico, no en esta) — publicar es terreno 100% de Code/scripts, no necesita a Chat en ningún punto del camino. Eso hace que "headless total" sea coherente con la arquitectura de 3 capas que ya está documentada en `fase-d-planner/SKILL.md` §5-bis y en memoria del proyecto (`content-pipeline.md`).
- El modelo ya acepta fallos parciales por plataforma sin bloquear el resto (Sección 3 arriba) — eso es exactamente lo que un cron sin supervisión necesita para no quedar atascado esperando una decisión humana a mitad de ejecución.

El riesgo real a sopesar: con cron, un bug en el orquestador puede publicar algo incorrecto (caption roto, pieza equivocada) sin que nadie lo vea antes de que salga. `knowledge/FYR_Fase_D_Produccion_Recurrente_v1.md` §5 ya anotó esto como fuera de alcance deliberado ("Alertas/notificaciones de fallos sin supervisión... se retoma cuando el patrón cambie a disparar trabajo en paralelo/background sin nadie mirando activamente") — si el orquestador de publicación corre por cron, ese punto deja de estar fuera de alcance, hay que resolverlo junto con él (al menos una notificación de fallo, aunque sea simple).

---

## 6. Qué llevar al chat nuevo

Basta con decirle al chat nuevo: *"Lee `knowledge/FYR_Traspaso_fyr_publisher_31oct2026.md`, y después `knowledge/FYR_Plan_Publicacion_Automatizada.md` completo, antes de proponer nada."* Ambos documentos ya están en el repo — no hace falta copiar/pegar texto a mano, cualquier sesión con acceso al repo los puede leer directamente (Code incluido, a diferencia de antes).
