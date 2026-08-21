with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. Reduce .bot-break padding on mobile (sections already have their own)
# ─────────────────────────────────────────────────────────
old_botbreak = """    .bot-break { display: none; text-align: center; padding: 20px 0; margin: 0; line-height: 0; position: relative; z-index: 5; }"""
new_botbreak = """    .bot-break { display: none; text-align: center; padding: 8px 0; margin: 0; line-height: 0; position: relative; z-index: 5; }"""
assert old_botbreak in content, "BLOCK 1 (bot-break) not found — aborting"
content = content.replace(old_botbreak, new_botbreak)

# ─────────────────────────────────────────────────────────
# 2. Reduce desktop padding for Chapters and Tools Preview
# ─────────────────────────────────────────────────────────
old_chapters_pad = """    #chapters { padding: 130px 24px; overflow: hidden; }"""
new_chapters_pad = """    #chapters { padding: 90px 24px; overflow: hidden; }"""
assert old_chapters_pad in content, "BLOCK 2 (chapters padding) not found — aborting"
content = content.replace(old_chapters_pad, new_chapters_pad)

old_tp_pad = """    #tools-preview { padding: 100px 24px; overflow: hidden; }"""
new_tp_pad = """    #tools-preview { padding: 80px 24px; overflow: hidden; }"""
assert old_tp_pad in content, "BLOCK 3 (tools-preview padding) not found — aborting"
content = content.replace(old_tp_pad, new_tp_pad)

# ─────────────────────────────────────────────────────────
# 3. Scale up desktop carousel by 20% (stage + all card sizes)
# ─────────────────────────────────────────────────────────
old_stage = """    .tp-stage { position: relative; height: clamp(380px, 52vh, 520px); display: flex; align-items: center; justify-content: center; margin: 20px 0; }"""
new_stage = """    .tp-stage { position: relative; height: clamp(456px, 62vh, 624px); display: flex; align-items: center; justify-content: center; margin: 20px 0; }"""
assert old_stage in content, "BLOCK 4 (tp-stage) not found — aborting"
content = content.replace(old_stage, new_stage)

old_cards = """    .tp-card.tp-current { height: clamp(340px, 46vh, 460px); width: auto; aspect-ratio: 0.707; z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-current.tp-land { height: clamp(240px, 32vh, 320px); width: auto; aspect-ratio: 1.414; }
    .tp-card.tp-prev { height: clamp(300px, 40vh, 400px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-prev.tp-land { height: clamp(220px, 29vh, 290px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(-1 * min(42vw, 280px))); }
    .tp-card.tp-next { height: clamp(300px, 40vh, 400px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next.tp-land { height: clamp(220px, 29vh, 290px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(min(42vw, 280px))); }"""

new_cards = """    .tp-card.tp-current { height: clamp(408px, 55vh, 552px); width: auto; aspect-ratio: 0.707; z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-current.tp-land { height: clamp(288px, 38vh, 384px); width: auto; aspect-ratio: 1.414; }
    .tp-card.tp-prev { height: clamp(360px, 48vh, 480px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-prev.tp-land { height: clamp(264px, 35vh, 348px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(-1 * min(42vw, 280px))); }
    .tp-card.tp-next { height: clamp(360px, 48vh, 480px); width: auto; aspect-ratio: 0.707; z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next.tp-land { height: clamp(264px, 35vh, 348px); width: auto; aspect-ratio: 1.414; transform: scale(0.88) translateX(calc(min(42vw, 280px))); }"""

assert old_cards in content, "BLOCK 5 (tp-card sizes) not found — aborting"
content = content.replace(old_cards, new_cards)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — final spacing + carousel scale patch applied successfully")
