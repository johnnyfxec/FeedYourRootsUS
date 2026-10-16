# FYR — Plan de publicación automatizada (carrusel 4:5 / video 9:16)

**Versión 1.1 — 16-oct-2026.** Reemplaza la investigación original del 10-oct-2026 y la revisión de una segunda IA del 16-oct-2026 — ambas tenían aciertos y errores reales; este documento deja solo lo verificado contra documentación oficial/fuentes primarias, con las correcciones aplicadas. **Estado: diseño, no implementado todavía.**

---

## 1. Qué cambió respecto a la investigación original

| Punto | Investigación original (10-oct) | 2ª IA (16-oct) | Verificado aquí (16-oct) |
|---|---|---|---|
| Límite IG en 24h | "100 (o 50, la doc se contradice)" | 50 | **50** — confirmado en la doc oficial de Meta: `content_publishing_limit.quota_total` = 50 por `quota_duration` (86400s). Consultar ese endpoint antes de ráfagas, no asumir. |
| TikTok carrusel vía Buffer | Asumido como automatizable (tabla "¿Mismo endpoint? No — dos tipos separados", pero sin marcar el problema de Buffer específicamente) | "Buffer no lo soporta, cae en Notification publishing (recordatorio manual)" | **Correcto el problema, no se pudo confirmar el mecanismo exacto** (la doc de Buffer no detalla carrusel de TikTok específicamente) — pero coincide con reportes de terceros de que TikTok separa foto/video estrictamente y varias herramientas no logran automatizar carrusel de TikTok sin su API directa. Tratarlo como no confiable vía Buffer. |
| YouTube sin verificar | "100 subidas/día" (de la doc de operación) | "Fuerza los videos a `private` permanentemente hasta auditoría de 2-4 semanas" | **Ambos mal.** No hay evidencia de que los videos se fuercen a privado — el código de ejemplo de la propia fuente que citó la 2ª IA usa `privacyStatus: 'public'` sin condicionarlo. El problema real es **cuota**: proyecto nuevo = 10,000 unidades/día, `videos.insert` cuesta 1,600 → **~6 subidas/día**, no 100 ni "bloqueado". Pasado ese límite, la 7ª subida del día falla con 403 (cuota agotada), no queda privada. |
| App Review de Meta | No verificado | "No se requiere si solo publicas en tus propias cuentas (modo Development + token de Admin/Developer/Tester)" | Consistente con el comportamiento conocido de Meta — no se re-verificó a fondo porque no bloquea nada mientras FYR publique solo en sus propias cuentas (no en cuentas de terceros). |

---

## 2. Distribución por plataforma (actualizada)

| Plataforma | Vía | Qué configurar | Límite real confirmado | Etiqueta IA |
|---|---|---|---|---|
| Instagram Reels | `mikusnuz/meta-mcp` (self-hosted) | Cuenta Business/Creator + app en developers.facebook.com (modo Development, token de Admin/Developer/Tester — sin App Review mientras solo publique en cuentas propias) + token de Graph API Explorer (renovar cada ~60 días, Long-Lived User Access Token) | **50 posts/24h** (confirmado, `content_publishing_limit`) — consultar `GET /<IG_USER_ID>/content_publishing_limit` antes de ráfagas; hasta 15 min, 300MB | Sin campo en la API — manual |
| YouTube Shorts | API directa (`videos.insert`) | Proyecto de Google Cloud + credencial OAuth propia (distinta del service account de TTS) | **~6 subidas/día con cuota default** (10,000 unidades/día ÷ 1,600 por subida) — **no** 100. Pedir aumento de cuota a Google solo cuando el volumen real lo exija (decisión de Johnny, 16-oct) | `status.containsSyntheticMedia` (confirmado, existe en la API real) |
| Facebook Reels | Buffer Free (canal 1/2) | Página de Facebook conectada | 10 posts en cola por canal | No expuesta por Buffer — no verificado |
| Pinterest | Buffer Free (canal 2/2) | Cuenta Pinterest | 10 posts en cola por canal | No expuesta por Buffer — no verificado |
| TikTok | **API directa** (ya no Buffer — decisión de Johnny, 16-oct, tras confirmar que Buffer no automatiza carrusel ahí) | Cuenta TikTok tipo business + credenciales de developer de TikTok, propias (no vía Buffer) | Según cuota de la Content Posting API de TikTok — **pendiente de confirmar al implementar**, no asumir de memoria | No expuesta de forma confirmada — no verificado |

Con este cambio, Buffer Free queda en **2 canales de 3 disponibles** (Facebook + Pinterest) — el canal libre que sobra puede usarse a futuro sin costo adicional.

---

## 3. Carrusel 4:5 vs video 9:16, por plataforma (sin cambios respecto al original, ya era correcto)

| Plataforma | Carrusel 4:5 | Video 9:16 | ¿Mismo endpoint? |
|---|---|---|---|
| Instagram | `ig_publish_carousel`, 2-10 ítems (pueden incluir video) | `ig_publish_reel` (`media_type: 'REELS'` al crear el contenedor — confirmado) | Sí — mismo flujo contenedor→publicar, cambia `media_type` |
| Pinterest | `source_type: multiple_image_urls`, 2-5 imágenes | `source_type: video_id` (subida en dos pasos vía `/v5/media`) | Sí — mismo endpoint `/v5/pins`, cambia `source_type` |
| TikTok | Endpoint `photo` (hasta 35 imágenes); `is_aigc` no existe para fotos | Endpoint `video` | No — dos tipos de contenido separados en la Content Posting API; **ahora vía API directa, no Buffer** |
| Facebook | `/photos` (subida) + `/feed` con `attached_media` | Endpoint propio de Reels/video | No — rutas y permisos distintos |
| YouTube | No existe — plataforma solo-video | `videos.insert`, cuota ~6/día default | N/A — el skill descarta piezas tipo carrusel antes de intentar publicar aquí |

---

## 4. Primeros pasos para el skill (`fyr-publisher`, no construido todavía)

1. **Credenciales, las 4 vías:**
   - Meta (Instagram): app en developers.facebook.com, modo Development, token de usuario Admin/Developer/Tester con `instagram_content_publish`.
   - YouTube: proyecto de Google Cloud + OAuth "Desktop app" propia (distinta del service account de TTS de `fetch_assets.mjs` — ver `FYR_Rutas_De_Produccion.md` §1).
   - Buffer: cuenta Free con Facebook + Pinterest conectados, API key.
   - TikTok: cuenta business + app de developer de TikTok, credenciales propias para la Content Posting API (foto y video).
2. **Contrato con Airtable:** campo en `Content_Pieces` que marque una pieza lista para publicar, campo de plataformas destino (multiselect), y **un campo de estado por plataforma** (no uno solo genérico) — ver §5, porque el fallo ahora puede ser por plataforma individual, no por pieza completa.
3. **`SKILL.md`** (`fyr-publisher`): cuándo se invoca, qué lee de Airtable, y la rama de despacho por plataforma Y por tipo de pieza (carrusel vs video), según la tabla de la Sección 3.
4. **Probar cada vía suelta** con una pieza de prueba de cada tipo: un Reel y un carrusel por meta-mcp, un Short por el script de YouTube, un carrusel y un video por la API directa de TikTok, un post de cada tipo a Facebook y Pinterest vía Buffer.
5. **Escalonar la publicación:** 1 pieza/día por cuenta las primeras 1-2 semanas, para no disparar detección de automatización en cuentas nuevas.
6. **Orquestador** que dispara las vías necesarias para una pieza y actualiza Airtable con el resultado de cada una por separado.

---

## 5. Cómo esto conecta con Fase D (Parada 4)

`FYR_Fase_D_Produccion_Recurrente_v1.md` §4 describe la Parada 4 como "confirmar que todo lo aprobado en Parada 3 está subido a Drive, registrado en Airtable, y lista de qué quedó pendiente" — escrito asumiendo que "publicado" es un solo paso atómico por pieza. **No lo es, una vez que existe `fyr-publisher`:** una pieza puede publicarse bien en Instagram y fallar en TikTok, por ejemplo. Esto implica que la Parada 4, al implementarse junto con `fyr-publisher`, necesita:

- Estado de publicación **por plataforma**, no un único `Publicado`/`No publicado` por pieza.
- El mismo principio de "un fallo puntual no detiene el resto" que ya aplica a nivel de pieza en Parada 3 (§4 de Fase D) — pero aplicado ahora a nivel de plataforma dentro de una misma pieza: si TikTok falla, Instagram/YouTube/Facebook/Pinterest siguen su curso, y la plataforma fallida queda marcada para reintento o atención manual sin bloquear el cierre del lote.
- `performance-lens` (todavía no construida) necesitará poder cruzar performance por plataforma, no solo por pieza — este esquema de Airtable más granular lo deja listo para cuando se construya.

---

## 6. Pendiente de verificar antes de implementar (no asumir de ninguna de las dos investigaciones)

- [ ] Cuota real de la Content Posting API de TikTok para subidas directas (foto y video) — ninguna de las dos investigaciones la confirmó con una fuente primaria.
- [ ] Si Buffer expone campo de etiquetado IA de forma verificable (la 2ª IA lo afirma sin fuente primaria citada con el detalle exacto; no se confirmó aquí).
- [ ] Mecanismo exacto por el que Buffer rechaza/redirige un carrusel de TikTok a "Notification publishing" — confirmar con una prueba real antes de descartar del todo esa ruta para casos simples.
- [ ] Proceso y tiempo real de la solicitud de aumento de cuota de YouTube cuando llegue el momento de pedirla (no es la misma "Compliance Audit" de OAuth que a veces se confunde en foros — son dos procesos distintos de Google).
