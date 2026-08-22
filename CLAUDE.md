# Feed Your Roots — Notas de flujo de trabajo (Claude)

## Contexto fundacional
Antes de trabajar en producción de contenido, leer completos:
- `docs/project_rescue/FYR_Asset_Governance_Policy.md`
- `docs/project_rescue/Feed-Your-Roots-Brand-Bible.md`
- `knowledge/` (Malla de temas, Sistema CRS v2, hooks verbales) — usados por el skill `fyr-content`

## Entornos de trabajo (importante — no confundir)
Johnny trabaja este mismo repo desde varios lugares en paralelo:
- **Claude Code web (esta sesión / sesiones tipo "claude/xxx")**: corre en contenedor remoto aislado, sin acceso al filesystem de Johnny. Cada sesión clona el repo desde cero.
- **Claude Chat vía Termux (Android, local)**: Johnny edita código directamente ahí, con acceso a su propio filesystem.
- Ninguno de los dos "ve" al otro en vivo — la única sincronización real es a través de GitHub (push/pull). Cuidado con rutas tipo `~` o `/storage/emulated/0/...` — solo existen en Termux, no en las sesiones remotas.

## Estrategia de ramas
- **`main`** = producción real. Este repo es GitHub Pages (tiene `CNAME`, `index.html` en raíz) — lo que está en `main` se sirve en vivo en feedyourroots.us. No hay paso de build/deploy intermedio.
- **Código del sitio (HTML/CSS/JS que afecta funcionamiento o apariencia)**: trabajar en rama separada + PR antes de mergear a `main`. Da un punto de revisión antes de que algo llegue a producción.
- **Contenido/texto (trabajo de `fyr-content`: briefs, copy, knowledge base)**: se puede ir directo a `main`, riesgo bajo — no es código que rompa el sitio.
- Fusionar ramas entre sesiones/entornos es seguro siempre que no se haya tocado el mismo archivo en ambos lados — git resuelve solo (fast-forward o merge limpio) en ese caso. Conflicto real solo si ambos editan las mismas líneas del mismo archivo.
- Antes de empezar a trabajar en cualquier sesión: `git pull` (o `fetch` + `merge`) desde el remoto para traer lo que se haya hecho en otro entorno. Antes de cerrar/cambiar de entorno: `git push`.

## Alcance de esta sesión (Claude Code web)
Este agente/sesión debe limitarse a trabajar en **`fyr-content`** (el skill de producción de contenido: briefs de carrusel/video, Malla de 61 temas, Sistema CRS, voz de marca) — no tocar código del sitio (HTML/CSS/JS) salvo pedido explícito de Johnny. La edición de código del sitio la hace Johnny directamente vía Termux/Claude Chat.
