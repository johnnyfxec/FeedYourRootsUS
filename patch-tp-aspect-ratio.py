with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# Reemplazar dimensiones width/height fijas por aspect-ratio real.
# Vertical = 0.707 (1587x2245), Horizontal = 1.414 (2000x1414)
# El contenedor fija solo la ALTURA (que es lo que determina el
# tamaño visual en un carrusel horizontal), y el ancho lo calcula
# aspect-ratio automáticamente — cero espacio sobrante.
# ─────────────────────────────────────────────────────────

old_css = """    .tp-card.tp-current { width: min(70vw, 420px); height: clamp(340px, 46vh, 460px); z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-current.tp-land { width: min(85vw, 620px); height: clamp(280px, 36vh, 360px); }
    .tp-card.tp-prev { width: min(50vw, 340px); height: clamp(300px, 40vh, 400px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-prev.tp-land { width: min(60vw, 460px); height: clamp(240px, 30vh, 300px); transform: scale(0.88) translateX(calc(-1 * min(42vw, 280px))); }
    .tp-card.tp-next { width: min(50vw, 340px); height: clamp(300px, 40vh, 400px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next.tp-land { width: min(60vw, 460px); height: clamp(240px, 30vh, 300px); transform: scale(0.88) translateX(calc(min(42vw, 280px))); }"""

new_css = """    .tp-card.tp-current { height: clamp(340px, 46vh, 460px); width: auto; aspect-ratio: 0.707; z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-current.tp-land { height: clamp(240px, 32vh, 320px); width: auto; aspect-ratio: 1.414; }
    .tp-card.tp-prev { height: clamp(300px, 40vh, 400px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-prev.tp-land { height: clamp(220px, 29vh, 290px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(-1 * min(42vw, 280px))); }
    .tp-card.tp-next { height: clamp(300px, 40vh, 400px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next.tp-land { height: clamp(220px, 29vh, 290px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(min(42vw, 280px))); }"""

assert old_css in content, "BLOCK 1 (tp CSS desktop) not found — aborting"
content = content.replace(old_css, new_css)

old_mq = """      .tp-card.tp-current { width: 72vw; height: 40vh; }
      .tp-card.tp-current.tp-land { width: 88vw; height: 30vh; }
      .tp-card.tp-prev { width: 40vw; height: 32vh; transform: scale(0.85) translateX(-46vw); }
      .tp-card.tp-prev.tp-land { width: 50vw; height: 24vh; transform: scale(0.85) translateX(-50vw); }
      .tp-card.tp-next { width: 40vw; height: 32vh; transform: scale(0.85) translateX(46vw); }
      .tp-card.tp-next.tp-land { width: 50vw; height: 24vh; transform: scale(0.85) translateX(50vw); }"""

new_mq = """      .tp-card.tp-current { height: 40vh; width: auto; aspect-ratio: 0.707; }
      .tp-card.tp-current.tp-land { height: 26vh; width: auto; aspect-ratio: 1.414; }
      .tp-card.tp-prev { height: 32vh; width: auto; aspect-ratio: 0.707; transform: scale(0.85) translateX(-46vw); }
      .tp-card.tp-prev.tp-land { height: 21vh; width: auto; aspect-ratio: 1.414; transform: scale(0.85) translateX(-50vw); }
      .tp-card.tp-next { height: 32vh; width: auto; aspect-ratio: 0.707; transform: scale(0.85) translateX(46vw); }
      .tp-card.tp-next.tp-land { height: 21vh; width: auto; aspect-ratio: 1.414; transform: scale(0.85) translateX(50vw); }"""

assert old_mq in content, "BLOCK 2 (tp CSS mobile) not found — aborting"
content = content.replace(old_mq, new_mq)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — exact aspect-ratio patch applied successfully")
