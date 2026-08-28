# FYR — Protocolo de trabajo (edición de archivos en repositorio)

Este documento existe para que cualquier sesión de Claude (chat o Claude Code) siga el mismo proceso, sin que Johnny tenga que re-explicarlo cada vez.

**Este archivo vive en dos lugares que deben mantenerse sincronizados:** como archivo de Proyecto en Claude.ai (para esta sesión de chat) y como `knowledge/FYR_Protocolo_De_Trabajo.md` en el repo real de Termux (para que Claude Code también lo siga). Cualquier cambio a este documento se hace en AMBOS lugares en la misma sesión — nunca en uno solo.

---

## Regla de oro

**Todo archivo que ya vive en el repositorio de Termux (`~/FeedYourRootsUS`) se edita EN Termux, vía comando — nunca regenerando el archivo completo desde el chat.** Regenerar completo cuesta tokens innecesarios y arriesga perder contexto/contenido que no debía cambiar.

Esto aplica sin excepción a: `FYR_Asset_Governance_Policy.md`, `SKILL.md`, cualquier archivo en `knowledge/`, cualquier archivo en `production/`.

**Único caso donde SÍ se genera un archivo nuevo desde el chat:** cuando el archivo no existe todavía en el repo (primera creación). Ahí se entrega completo una vez, se descarga, y de ahí en adelante se edita solo por comando.

---

## Los dos entornos — no confundirlos

| Entorno | Qué es | Cómo se accede |
|---|---|---|
| **Termux (tablet Android)** | El clon real del repo, donde Johnny teclea comandos a mano | App Termux directa |
| **Claude Code (dentro de la app)** | Otra sesión de Claude, con su propio clon del mismo repo, corre la skill `fyr-content` | Tab/sesión de Claude Code en la app |

Son dos clones independientes del mismo repo de GitHub. Un cambio en uno **no aparece automáticamente** en el otro — hay que `git push` desde donde se editó y `git pull` desde donde se quiere ver el cambio.

Claude (esta sesión de chat) **no tiene acceso directo a ninguno de los dos** — no puede ejecutar comandos en el Termux de Johnny ni en su Claude Code. Solo puede: (a) darle a Johnny el comando exacto para que él lo corra, o (b) generar contenido nuevo para que Johnny lo baje y lo suba manualmente.

**Cuidado con alias de shell que redefinen comandos estándar de Unix.** Si un comando básico (`touch`, `ls`, etc.) empieza a comportarse de forma inesperada (por ejemplo, abre Claude Code solo, o cambia de directorio solo), verificar primero con `type nombre_comando` antes de asumir que es un bug del script — puede ser un alias personal en `.bashrc`/`.bash_profile` pisando el comando real.

---

## El patrón de edición: grep → Python heredoc → grep

Para cualquier edición a un archivo ya existente en el repo:

### 1. Verificar el texto exacto (grep)
Nunca se asume el contenido de memoria. Se pide siempre:
```bash
grep -n "texto a buscar" ruta/al/archivo.md
```
o, si la línea es larga o tiene caracteres especiales, se usa `sed -n` con rango de líneas:
```bash
sed -n '135,140p' ruta/al/archivo.md
```

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

## Reglas de comportamiento (aprendidas de correcciones reales de Johnny)

- **Nunca encadenar varios comandos especulativos sin confirmar el anterior.** Si el primer comando de una cadena falla, toda la cadena se pierde y hay que repetir. Un paso, una confirmación, siguiente paso.
- **Nunca mandar grep + comando de reemplazo en el mismo mensaje si Claude no está seguro del texto exacto.** El grep existe para *obtener* información antes de actuar — pedirlo y no esperar la respuesta es teatro inútil.
- **Si Claude ya tiene certeza del texto exacto** (porque lo escribió él mismo momentos antes y fue confirmado), puede dar grep+reemplazo+grep en un solo bloque de una vez — no hace falta partir en dos mensajes cuando no hay incertidumbre real.
- **Nunca trabajar en `/tmp`.** Todo vive dentro del repositorio real. Para descargas temporales de fuentes/assets externos que no son del proyecto, usar una carpeta fuera del repo pero dentro del HOME de Termux (ej. `~/tmp_downloads`), y limpiarla al terminar — nunca dejar resultados de trabajo real ahí, esos van directo al repo.
- **Nunca sugerir abrir Claude Code dentro de Termux ni mezclar los dos entornos.** Cuando Johnny está en Termux, los comandos son bash/Python puro — nunca `claude` como comando.
- **Los archivos que Johnny descarga del chat llegan a `/storage/emulated/0/Download/`.** El patrón para moverlos al repo siempre verifica que haya exactamente 1 coincidencia antes de mover, para no arrastrar duplicados de descargas repetidas:
```bash
  cd ~/FeedYourRootsUS && D=/storage/emulated/0/Download && \
  n=$(ls $D/nombre_archivo.md 2>/dev/null | wc -l); \
  if [ "$n" -ne 1 ]; then echo "❌ FALLO: $n coincidencias en Download (esperaba 1)."; ls $D/nombre_archivo*.md 2>/dev/null; else \
  mv $D/nombre_archivo.md ruta/destino/nombre_archivo.md && echo "✓ movido al repo"; fi
```
- **`git add` siempre con rutas explícitas, nunca `git add .` ni `git add -A` sin revisar antes.** El repo de Termux vive dentro de un repo git más grande que incluye el home completo (`.npm`, `.cache`, otros proyectos) — un `add` sin acotar puede arrastrar archivos ajenos a FYR. Siempre confirmar con `git status` antes de `git commit`.
- **Commits con mensaje descriptivo real** (qué cambió y por qué), no genérico tipo "update".
- **Después de cada `git push`**, si el cambio afecta algo que Claude Code también usa (Skill, Policy, knowledge/), recordar que Claude Code necesita su propio `git pull` para verlo — no ocurre automático.
- **Archivos de test/verificación visual (`_tests_output/` u otras carpetas de prueba) se borran una vez que cumplieron su propósito** — no se acumulan como referencia "por si acaso". El dato real que vale la pena conservar de una medición o prueba va al código o a `knowledge/`, no la imagen que lo generó.

---

## Auditoría antes de dar por cerrado un cambio grande

Cuando se hace una actualización de gobernanza (Policy, SKILL.md, estructura de carpetas), antes de commitear conviene revisar:
1. ¿El número de versión del documento se incrementó?
2. ¿Alguna otra parte del MISMO documento hace referencia cruzada a lo que se cambió (número de sección, nombre de archivo, versión citada) y quedó desactualizada?
3. ¿Otro documento del repo (Policy ↔ SKILL.md) menciona lo mismo y también quedó desactualizado?

Este tipo de auditoría cruzada ha encontrado errores reales más de una vez — vale la pena el paso extra antes del commit final.

---

## Registro de cambios (CHANGELOG)

`knowledge/CHANGELOG.md` es el registro legible de cambios a los documentos de `knowledge/` — complementa a `git log`, no lo reemplaza. Cada vez que se cierra un cambio de documentación (no código), se agrega una entrada nueva ahí mismo, en el mismo bloque de comandos que hace el commit correspondiente. Formato: fecha, documento(s) afectados, qué cambió y por qué en lenguaje natural — no solo el mensaje técnico del commit.

Esto existe porque el historial de git responde "qué cambió y cuándo" pero no siempre "por qué" de forma legible sin abrir cada commit uno por uno.

---

## Evitar reconstruir herramientas ya creadas

Antes de resolver un problema de medición, verificación o utilidad técnica desde cero, revisar si ya existe algo reutilizable en `production/scripts/tools/`. Por ejemplo, `medidor_esquinas.html` (medición de 4 esquinas de cualquier región en una imagen, con zoom/pan, coordenadas reales) se construyó una vez para medir los marcos rotados de `doble_marco`, pero sirve para cualquier layout con geometría no rectangular futura — no se reconstruye, se reutiliza.

Si en algún punto parece que el proyecto está acumulando demasiado código/herramientas de soporte sin necesidad, la pregunta útil no es "¿estamos escribiendo mucho código?" sino "¿estamos repitiendo trabajo que una herramienta ya resuelta debería cubrir?". El costo real de una herramienta como el medidor se paga una sola vez; el costo de no tenerla se paga cada vez que hace falta medir algo a mano de nuevo.

---

## Estrategia de ramas

Este repo es GitHub Pages (tiene `CNAME`, `index.html` en raíz) — lo que está en `main` se sirve EN VIVO en feedyourroots.us, sin paso de build/deploy intermedio. Esto hace que `main` sea más sensible de lo que parece.

- **Código del sitio (HTML/CSS/JS que afecta funcionamiento o apariencia):** trabajar en rama separada + revisión de Johnny antes de mergear a `main`. Da un punto de control antes de que algo llegue a producción.
- **Contenido/texto (briefs, copy, knowledge base, trabajo del skill `fyr-content`):** puede ir directo a `main`, riesgo bajo — no es código que pueda romper el sitio.
- **Sesiones de Claude Code (contenedor remoto, sin acceso al filesystem de Johnny):** por defecto trabajan en su propia rama (`claude/nombre-de-sesion`), nunca directo en `main`, salvo que la tarea sea puramente de contenido de bajo riesgo.
- Fusionar ramas entre sesiones/entornos es seguro siempre que no se haya tocado el mismo archivo en ambos lados — git resuelve solo (fast-forward o merge limpio). Conflicto real solo si ambos editaron las mismas líneas del mismo archivo.
- Antes de empezar a trabajar en cualquier sesión: `git pull` (o `fetch` + `merge`) desde el remoto para traer lo que se haya hecho en otro entorno. Antes de cerrar/cambiar de entorno: `git push`.
- Para ver el contenido de una rama remota sin fusionarla ni cambiarte a ella: `git show origin/nombre-rama:ruta/archivo.md`.

---

## Registro en Airtable de archivos nuevos

Cualquier asset de imagen nuevo (marco, layout, escena) que se sube a Drive **también se registra en la tabla `Assets` de Airtable** en la misma sesión — nunca se deja para después. Si un campo de Airtable (ej. `Reutilizable en`) no tiene la opción de ubicación necesaria todavía, usar `typecast: true` al crear el record para que Airtable la cree automáticamente — no requiere edición manual del schema salvo que typecast no lo soporte para ese tipo de campo.
