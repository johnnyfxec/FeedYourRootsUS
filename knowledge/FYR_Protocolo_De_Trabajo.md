# FYR — Protocolo de trabajo (repositorio, skills y conocimiento)

Este documento existe para que cualquier sesión de Claude (chat o Claude Code) siga el mismo proceso, sin que Johnny tenga que re-explicarlo cada vez.

**Fuente de verdad: el repositorio de GitHub (`knowledge/`, `.claude/skills/`, `production/`).** El Proyecto de Claude.ai es un espejo de lectura para las sesiones de chat. Se actualizó el 10-oct-2026: desde que una sesión de Claude Code puede clonar el repo, editarlo y escribir en el Proyecto, Johnny ya no copia archivos a mano entre Termux, Descargas y el Proyecto.

---

## Regla de oro

**Cuando Claude tiene el repo clonado en su sesión, Claude edita el archivo directamente (edición quirúrgica del fragmento, nunca regenerando el archivo completo), hace commit con mensaje descriptivo y sube.** Johnny no ejecuta comandos para esto. Regenerar un archivo completo cuesta tokens y arriesga perder contenido que no debía cambiar.

**Actualizar un documento significa revisarlo y reescribir lo que quedó viejo en su lugar** — no anexar un parche al final. Un documento de política debe leerse como la realidad actual, sin capas históricas contradictorias.

**Qué sigue haciendo Johnny (lo que Claude no puede):** generar las imágenes en Gemini y exportarlas a Drive, aprobar briefs y piezas terminadas, publicar, y crear/aprobar cosas en cuentas de terceros (credenciales, secretos de GitHub). No hay PC: el render de video corre en GitHub Actions y todo lo demás en la sesión de Claude. El detalle por formato está en `knowledge/FYR_Rutas_De_Produccion.md`.

### Dónde escribe Claude

| Qué | Dónde | Cómo |
|---|---|---|
| Documentos de `knowledge/`, skills, `CHANGELOG.md` | **`main` directo**, cuando Johnny lo pide en la sesión | commit + push |
| Código de `production/scripts/` y workflows | **`main` directo** (ya no hay PC que sincronizar); se prueba antes con datos sintéticos o con el servidor de Drive simulado | commit + push |
| Espejo en el Proyecto de Claude.ai | `project_write` desde la misma sesión, en el mismo turno que el commit | Claude lo hace; Johnny no sube nada |
| Skills de la cuenta de Claude.ai | Tarjeta `propose_skills` (Johnny pulsa Guardar) | el archivo del repo es la versión de referencia |

Nunca `git push --force`, nunca reescribir historia, nunca commitear credenciales ni salidas de trabajo (`node_modules/`, `build/`, `salida/`, `img/`).

---

## Los entornos — no confundirlos

| Entorno | Qué es | Qué se hace ahí |
|---|---|---|
| **Sesión de Claude Code (nube)** | Clon propio del repo, con acceso al Proyecto de Claude.ai y a los conectores (Airtable, Drive…) | Editar documentos, skills y código; commits y push; sincronizar el Proyecto; consultar y ajustar Airtable. Es el entorno principal. |
| **GitHub Actions** | Runner de Ubuntu que dispara el push de un archivo de `production/queue/` | Render de video (Node, Google Cloud TTS, Clipkit) y subida del MP4 a Drive. Es el único lugar donde se renderiza video. |
| **Termux (tablet Android)** | Otro clon, para teclear comandos a mano | Respaldo cuando no hay sesión de Claude Code; ver «Respaldo: edición por comando». |
| **Chat de Claude.ai (Proyecto)** | Conversación con el conocimiento del Proyecto | Planear y decidir. No toca el repo; lo que decida se aplica en una sesión de Claude Code. |

Los clones son independientes: un cambio en uno no aparece en los otros hasta hacer `git push` donde se editó y `git pull` donde se quiere ver. Los scripts y JSON viajan por repo; las imágenes, el audio y el video viajan por Drive.

Con Google en la lista de dominios permitidos (Configuración → Capacidades en un chat; **Network access** del entorno en una sesión de Claude Code), la sesión sube archivos pesados con `production/scripts/drive/drive_client.py` (permiso mínimo `drive.file`); todo lo demás de Drive va por el conector. Las credenciales nunca se commitean (el repo es público).

**Cuidado con alias de shell que redefinen comandos estándar de Unix.** Si un comando básico (`touch`, `ls`, etc.) empieza a comportarse de forma inesperada (por ejemplo, abre Claude Code solo, o cambia de directorio solo), verificar primero con `type nombre_comando` antes de asumir que es un bug del script — puede ser un alias personal en `.bashrc`/`.bash_profile` pisando el comando real.

### Entornos retirados

La PC con Windows (VSCodium + Git Bash) dejó de usarse el 14-oct-2026: no hay más PC. Sus particularidades (rutas `E:\`, `python` en vez de `python3`, CRLF, parches pegados en Git Bash) ya no aplican. Termux queda solo como respaldo manual.

---

## Respaldo: edición por comando (Termux, PC o cuando Claude no tiene el repo clonado)

Todo lo que sigue hasta «Reglas de comportamiento» aplica solo cuando Johnny debe pegar comandos él mismo. Si Claude tiene el repo clonado, edita directo y nada de esto es necesario.


Para cualquier edición a un archivo ya existente en el repo:

### 1. Verificar el texto exacto (grep)
Nunca se asume el contenido de memoria. Se pide siempre:
```bash
grep -n "texto a buscar" ruta/al/archivo.md
```
o, si la línea es larga o tiene caracteres especiales o hace falta ver contexto alrededor, se usa `cat -n` con rango de líneas vía `head`/`tail`, o `awk` con `NR`:
```bash
cat -n ruta/al/archivo.md | head -n 15
```
o, para un rango específico:
```bash
awk 'NR==135,NR==140{print NR": "$0}' ruta/al/archivo.md
```
**`sed -n` queda prohibido para este propósito** — usar siempre `cat`/`awk` con número de línea explícito.

Johnny pega el resultado real. Solo con ese texto confirmado se construye el reemplazo — nunca antes.

**Si el `assert` de un reemplazo falla con "esperaba 1, encontré 0"**, no reintentar con el mismo texto — pedir `cat -A` del rango de líneas relevante para revisar caracteres invisibles (líneas en blanco, espacios finales) antes de reintentar. Reemplazar por posición de línea (`readlines()` + insertar por índice) es más robusto que buscar un bloque de texto largo cuando el espaciado exacto no está 100% confirmado.

### 2. Reemplazo quirúrgico (Python heredoc, con `assert`)
```bash
python3 << 'PYEOF'
path = "ruta/al/archivo.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = "texto exacto tal como salió del grep"
new = "texto nuevo"

assert content.count(old) == 1, f"old: esperaba 1, encontre {content.count(old)}"
content = content.replace(old, new)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK: descripcion breve del cambio")
PYEOF
```

El `assert` es obligatorio — si el texto no aparece exactamente una vez (0 veces = no coincide, 2+ veces = ambiguo), el script falla ANTES de escribir nada, así nunca se corrompe el archivo con un reemplazo a ciegas.

**Nunca usar comillas triples de Python (`"""`) dentro de un heredoc de bash si el contenido tiene bloques de código con \`\`\`** — genera conflicto de parsing. Si hace falta, construir el string con concatenación de líneas (`"linea1\n" "linea2\n"`) en vez de un bloque triple-quoted.

### 3. Confirmar el cambio (grep de nuevo)
```bash
grep -n "fragmento del texto nuevo" ruta/al/archivo.md
```
Un solo bloque de comandos, en este orden: grep de confirmación siempre al final del mismo bloque que hizo el cambio — nunca un mensaje aparte pidiendo "corre esto y dime" sin haber hecho el cambio todavía.

---

## Reglas de comportamiento

### Generales (toda sesión)

- **`git add` siempre con rutas explícitas, nunca `git add .` ni `git add -A` sin revisar antes.** En Termux el repo vive dentro de un repo git más grande que incluye el home completo (`.npm`, `.cache`, otros proyectos) — un `add` sin acotar puede arrastrar archivos ajenos a FYR. Siempre confirmar con `git status` antes de `git commit`.
- **Commits con mensaje descriptivo real** (qué cambió y por qué), no genérico tipo "update".
- **Después de cada `git push`** que afecte lo que se ejecuta en la PC o en Termux (scripts, JSON, skills), esos clones necesitan su propio `git pull` — no ocurre automático. Claude lo recuerda con el comando exacto.
- **Archivos de test/verificación visual (`_tests_output/` u otras carpetas de prueba) se borran una vez que cumplieron su propósito** — no se acumulan como referencia "por si acaso". El dato real que vale la pena conservar de una medición o prueba va al código o a `knowledge/`, no la imagen que lo generó.
- **Nunca dejar resultados de trabajo real fuera del repo.** Los temporales van en una carpeta cubierta por `.gitignore` (o en el directorio temporal de la sesión) y se borran al terminar; el dato que vale conservar va al código o a `knowledge/`.
- **Después de una cantidad importante de cambios o hitos en una sesión (bugs resueltos, layouts nuevos, políticas de gobernanza nuevas), se registra una entrada en `knowledge/CHANGELOG.md` antes de cerrar esa sesión de trabajo, en el mismo commit que el cambio** — mismo formato que las entradas existentes (`## FECHA` + bullets `**Documento/Feature** -- qué cambió y por qué`). Un cambio aislado y chico (un typo, un ajuste de 1 línea) no necesita entrada propia; una sesión con varios hitos reales sí, para no depender de la memoria de la conversación para reconstruir qué se decidió y por qué.

### Modo comando (solo cuando Johnny pega los comandos él mismo)

- **Nunca encadenar varios comandos especulativos sin confirmar el anterior.** Si el primer comando de una cadena falla, toda la cadena se pierde y hay que repetir. Un paso, una confirmación, siguiente paso.
- **Nunca mandar grep + comando de reemplazo en el mismo mensaje si Claude no está seguro del texto exacto.** El grep existe para *obtener* información antes de actuar — pedirlo y no esperar la respuesta es teatro inútil.
- **Si Claude ya tiene certeza del texto exacto** (porque lo escribió él mismo momentos antes y fue confirmado), puede dar grep+reemplazo+grep en un solo bloque de una vez — no hace falta partir en dos mensajes cuando no hay incertidumbre real.
- **Nunca sugerir abrir Claude Code dentro de Termux ni mezclar los dos entornos.** Cuando Johnny está en Termux, los comandos son bash/Python puro — nunca `claude` como comando.
- **Los archivos que Johnny descarga del chat llegan a `/storage/emulated/0/Download/`.** El patrón para moverlos al repo siempre verifica que haya exactamente 1 coincidencia antes de mover, para no arrastrar duplicados de descargas repetidas:
```bash
  cd ~/FeedYourRootsUS && D=/storage/emulated/0/Download && \
  n=$(ls $D/nombre_archivo.md 2>/dev/null | wc -l); \
  if [ "$n" -ne 1 ]; then echo "❌ FALLO: $n coincidencias en Download (esperaba 1)."; ls $D/nombre_archivo*.md 2>/dev/null; else \
  mv $D/nombre_archivo.md ruta/destino/nombre_archivo.md && echo "✓ movido al repo"; fi
```
- **Todo pedido de "actualiza", "verifica" o "revisa" código del repositorio se responde automáticamente con el comando de Termux correspondiente** — nunca con una descripción en prosa de lo que habría que hacer. Claude nunca pide a Johnny que pegue código sin haber dado primero el comando exacto que lo extrae (grep/cat/awk con índice de línea).
- **Todo fragmento de código que Claude solicita o recibe debe incluir número de línea** (via `grep -n`, `cat -n` o `awk` con `NR`). Código sin índice de línea no es suficiente para construir un `old =` confiable en el heredoc.
- **El grep/cat/awk de confirmación después de un cambio va siempre en el mismo bloque de comando que hizo el cambio, sin excepción** — nunca en un mensaje aparte pidiendo "corré esto y decime". Esto aplica incluso cuando Claude ya tenía certeza del texto exacto: la certeza autoriza saltar el grep *previo* de verificación (Sección "El patrón de edición", punto 3 de esta lista), no el grep *posterior* de confirmación, que siempre es obligatorio y siempre va en el mismo bloque.
- **`/tmp` está prohibido sin excepción, incluso para scripts de una sola corrida que se borran de inmediato.** No hay caso especial de "descartable" que lo habilite -- en el Termux de Johnny además está bloqueado por permisos, así que cualquier comando que lo use falla. Para un script Python temporal de verificación, usar un heredoc de `python3 << 'PYEOF' ... PYEOF` directo (sin escribir archivo intermedio), o si hace falta archivo, crearlo dentro del repo en una ruta ya cubierta por `.gitignore` y borrarlo al final del mismo bloque.
- **Nunca usar `!` dentro de comandos Python pasados con `-c` a bash interactivo** (ej. `!r` en f-strings) -- bash lo interpreta como history expansion y corrompe el comando completo, arrastrando errores de sintaxis a las líneas siguientes. Preferir heredoc (`python3 << 'PYEOF'`) para cualquier script con f-strings, comillas anidadas, o caracteres especiales -- nunca `-c` con lógica no trivial.
- **Si el `old` de un reemplazo incluye texto largo (más de una línea) con tildes o ñ, no usar el heredoc de texto como primer intento** — ir directo a reemplazo por índice de línea (`readlines()`, verificar la línea esperada con `assert lines[N].startswith(...)`, reemplazar `lines[N:M]`). Esto evita fallos de `assert` por diferencias de codificación/normalización Unicode entre lo tipeado en el heredoc y lo real del archivo. El heredoc de texto largo queda reservado para bloques sin tildes/ñ o de una sola línea corta.

---

## Auditoría antes de dar por cerrado un cambio grande

Cuando se hace una actualización de gobernanza (Policy, SKILL.md, estructura de carpetas), antes de commitear conviene revisar:
1. ¿El número de versión del documento se incrementó?
2. ¿Alguna otra parte del MISMO documento hace referencia cruzada a lo que se cambió (número de sección, nombre de archivo, versión citada) y quedó desactualizada?
3. ¿Otro documento del repo (Policy ↔ SKILL.md) menciona lo mismo y también quedó desactualizado?

Este tipo de auditoría cruzada ha encontrado errores reales más de una vez — vale la pena el paso extra antes del commit final.

---

## Registro de cambios (CHANGELOG)

`knowledge/CHANGELOG.md` es el registro legible de cambios a los documentos de `knowledge/` — complementa a `git log`, no lo reemplaza. Cada vez que se cierra un cambio de documentación (no código), se agrega una entrada nueva ahí mismo, en el mismo commit. Formato: fecha, documento(s) afectados, qué cambió y por qué en lenguaje natural — no solo el mensaje técnico del commit.

Esto existe porque el historial de git responde "qué cambió y cuándo" pero no siempre "por qué" de forma legible sin abrir cada commit uno por uno.

---

## Evitar reconstruir herramientas ya creadas

Antes de resolver un problema de medición, verificación o utilidad técnica desde cero, revisar si ya existe algo reutilizable en `production/scripts/tools/`. Por ejemplo, `medidor_esquinas.html` (medición de 4 esquinas de cualquier región en una imagen, con zoom/pan, coordenadas reales) se construyó una vez para medir los marcos rotados de `doble_marco`, pero sirve para cualquier layout con geometría no rectangular futura — no se reconstruye, se reutiliza.

Si en algún punto parece que el proyecto está acumulando demasiado código/herramientas de soporte sin necesidad, la pregunta útil no es "¿estamos escribiendo mucho código?" sino "¿estamos repitiendo trabajo que una herramienta ya resuelta debería cubrir?". El costo real de una herramienta como el medidor se paga una sola vez; el costo de no tenerla se paga cada vez que hace falta medir algo a mano de nuevo.

---

## Estrategia de ramas

Este repo es GitHub Pages (tiene `CNAME`, `index.html` en raíz) — lo que está en `main` se sirve EN VIVO en feedyourroots.us, sin paso de build/deploy intermedio. Esto hace que `main` sea más sensible de lo que parece.

- **Código del sitio (HTML/CSS/JS en la raíz que afecta funcionamiento o apariencia) y código que corre en la PC (`production/scripts/`, `assemble.py`):** rama separada (`claude/<nombre>`) + confirmación de Johnny antes de mergear a `main`. Da un punto de control antes de que algo llegue a producción o rompa una corrida.
- **Contenido/texto (briefs, copy, `knowledge/`, skills en `.claude/skills/`, `CHANGELOG.md`):** Claude lo sube directo a `main` cuando Johnny lo pide en la sesión; riesgo bajo, no es código que pueda romper el sitio.
- **Sesiones de Claude Code (contenedor remoto):** push a `main` está permitido (la rama no tiene protección; verificado 10-oct-2026), pero se usa solo para contenido de bajo riesgo como arriba. Todo lo demás, en rama. Nunca `--force`.
- Fusionar ramas entre sesiones/entornos es seguro siempre que no se haya tocado el mismo archivo en ambos lados — git resuelve solo (fast-forward o merge limpio). Conflicto real solo si ambos editaron las mismas líneas del mismo archivo.
- Antes de empezar a trabajar en cualquier sesión: `git pull` (o `fetch` + `merge`) desde el remoto para traer lo que se haya hecho en otro entorno. Antes de cerrar/cambiar de entorno: `git push`.
- Para ver el contenido de una rama remota sin fusionarla ni cambiarte a ella: `git show origin/nombre-rama:ruta/archivo.md`.

---

## Registro en Airtable de archivos nuevos

Cualquier asset de imagen nuevo (marco, layout, escena) que se sube a Drive **también se registra en la tabla `Assets` de Airtable** en la misma sesión — nunca se deja para después. Si un campo de Airtable (ej. `Reutilizable en`) no tiene la opción de ubicación necesaria todavía, usar `typecast: true` al crear el record para que Airtable la cree automáticamente — no requiere edición manual del schema salvo que typecast no lo soporte para ese tipo de campo.
