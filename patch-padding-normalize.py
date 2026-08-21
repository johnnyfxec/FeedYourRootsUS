with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. Add tablet-range (960px) padding for all sections — currently missing,
#    they inherit full desktop padding which is too much for that width.
# ─────────────────────────────────────────────────────────
old_960_end = """      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
      .float-el { display: none; }
    }"""

new_960_end = """      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
      .float-el { display: none; }
      #hero { padding-top: 64px; padding-bottom: 64px; }
      #problem, #solution, #vision, #chapters, #tools-preview, #bundles, #close { padding-top: 64px; padding-bottom: 64px; }
    }"""

assert old_960_end in content, "BLOCK 1 (960px tablet padding) not found — aborting"
content = content.replace(old_960_end, new_960_end)

# ─────────────────────────────────────────────────────────
# 2. Normalize mobile (600px) padding to uniform 32px, add tools-preview here
# ─────────────────────────────────────────────────────────
old_mobile = """      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .bundles-grid { grid-template-columns: 1fr; }
      .bot-break { display: block; }
      .bundles-header { margin-bottom: 36px; }
    }"""

new_mobile = """      #hero { padding: 32px 20px; }
      #solution,#chapters,#close { padding: 32px 20px; }
      #problem,#vision,#bundles { padding: 32px 20px; }
      #tools-preview { padding: 32px 0; min-height: 100dvh; display: flex; align-items: center; }
      .vision-grid, .bundles-grid { grid-template-columns: 1fr; }
      .bot-break { display: block; }
      .bundles-header { margin-bottom: 36px; }
    }"""

assert old_mobile in content, "BLOCK 2 (mobile padding) not found — aborting"
content = content.replace(old_mobile, new_mobile)

# ─────────────────────────────────────────────────────────
# 3. Change tools-preview's own breakpoint from 720px to 600px,
#    and remove its now-redundant padding declaration (handled above)
# ─────────────────────────────────────────────────────────
old_tp_mq = """    @media (max-width: 720px) {
      #tools-preview { padding: 60px 0; min-height: 100dvh; display: flex; align-items: center; }
      .tp-inner { width: 100%; }"""

new_tp_mq = """    @media (max-width: 600px) {
      .tp-inner { width: 100%; }"""

assert old_tp_mq in content, "BLOCK 3 (tools-preview breakpoint) not found — aborting"
content = content.replace(old_tp_mq, new_tp_mq)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — padding normalization patch applied successfully")
