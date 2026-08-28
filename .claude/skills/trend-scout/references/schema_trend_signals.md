# Schema — tabla `Trend_Signals` (Airtable)

Se importa desde `Trend_Signals_Airtable_Import.csv` una sola vez (o se crea manual con estos campos). A partir de ahí, Airtable es la fuente de verdad — igual que `Themes` y `Content_Pieces` en el sistema `fyr-content`.

| Campo | Tipo Airtable | Notas |
|---|---|---|
| Signal_ID | Texto (primary) | Formato `TR-####`, consecutivo. Nunca reusar un ID. |
| Fecha_Deteccion | Fecha | Cuándo se registró la señal. |
| Tipo_Señal | singleSelect | Sonido / Hashtag / Formato / Ángulo narrativo |
| Nombre_Señal | Texto | Nombre del sonido, hashtag (con #) o descripción corta del formato/ángulo. |
| Plataforma | singleSelect | TikTok / Instagram Reels / YouTube Shorts |
| Pais | Texto | Código de país usado en la búsqueda (ej. US) |
| Industria_CC | Texto | Categoría de Creative Center usada como filtro (ej. Home & Garden) |
| Curva_Momentum | singleSelect | Ascendente / Meseta / Descendente |
| Volumen_Uso | Número | Views o posts asociados, si la fuente lo da. Puede quedar vacío. |
| Ventana_Vida_Estimada | Texto | Estimación libre, ej. "7-14 dias". No es un dato duro, es una lectura de la skill. |
| Score_Afinidad_Avatar | Número (1-5) | Qué tanto le habla esta señal al avatar de la marca. Ver criterio en SKILL.md. |
| Pilar_Relacionado | singleSelect | Debe coincidir exacto con los nombres de Pilar usados en `Themes` (Airtable `appMy5aOwifSbBLPR`). Vacío si no aplica a ningún pilar. |
| Hook_CRS_Equivalente | singleSelect | Uno de los 20 hooks verbales, mismo formato que `Hook Asignado` en `Themes` (ej. "11. Mito"). Este es el campo puente hacia `fyr-content`. |
| Fase_Embudo_Sugerida | singleSelect | F1/F2/F3/F4 |
| Formato_Sugerido | singleSelect | POV / Antes-Después / Countdown / Storytime — mismo vocabulario que `Themes.Formato` |
| Brief_Adaptacion | Texto largo | 2-4 frases: qué hace viral a esta señal y cómo se traduce a la voz/avatar de la marca. Este es el output central de la skill. |
| Sonido_URL_Referencia | URL | Link al sonido original en la plataforma, si aplica. |
| Video_Referencia_URL | URL | Link al video líder deconstruido (si se hizo deconstrucción). |
| Estado | singleSelect | Detectada / Aprobada / Usada / Expirada / Descartada |
| Tema_Vinculado | Texto o Link | Número de tema en `Themes` (ej. "3.1") si la señal calza con un tema existente. Vacío si no. |
| Content_Piece_Generada | Texto o Link | ID `PZA-###` de la pieza que terminó usando esta señal. Se llena cuando `fyr-content` produce algo montado sobre esta tendencia. |
| Fecha_Aprobacion | Fecha | Cuándo el usuario aprobó pasar la señal de Detectada a Aprobada. |
| Fecha_Expiracion | Fecha | Fecha_Deteccion + Ventana_Vida_Estimada, calculada al aprobar. Pasada esta fecha sin usarse, la skill sugiere marcar como Expirada. |
| Resultado_Post_Uso | singleSelect | Alto / Medio / Bajo / Sin datos — mismo vocabulario que `Content_Pieces.Performance`, para que `performance-lens` (futura skill 3) pueda cruzar ambas tablas sin traducción. |
| Notas | Texto largo | Libre. |

## Reglas de escritura (igual que fyr-content)

- Para singleSelect/multipleSelects: escribir el nombre exacto de la opción como string, usar `typecast: true` si la opción puede no existir aún.
- `Pilar_Relacionado` y `Hook_CRS_Equivalente` deben calzar carácter por carácter con las opciones ya usadas en `Themes` — si no calzan, Airtable crea una opción duplicada con variación mínima y el cruce entre tablas se rompe silenciosamente. Verificar contra `Themes` antes de escribir, nunca asumir el nombre exacto de memoria.
- `Signal_ID`: antes de asignar uno nuevo, consultar el último `TR-####` existente — igual que la regla ya usada para `PZA-###` en `fyr-content`.
