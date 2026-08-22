with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. .bot-break: reduce and normalize spacing (was 4px, felt inconsistent)
# ─────────────────────────────────────────────────────────
old_botbreak = """    .bot-break { display: none; text-align: center; padding: 4px 0; margin: 0; line-height: 0; position: relative; z-index: 5; }"""
new_botbreak = """    .bot-break { display: none; text-align: center; padding: 20px 0; margin: 0; line-height: 0; position: relative; z-index: 5; }"""
assert old_botbreak in content, "BLOCK 1 (bot-break) not found — aborting"
content = content.replace(old_botbreak, new_botbreak)

# ─────────────────────────────────────────────────────────
# 2. .bundles-header: reduce margin-bottom on mobile only
# ─────────────────────────────────────────────────────────
old_mq600 = """      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .bundles-grid { grid-template-columns: 1fr; }
      .bot-break { display: block; }
    }"""
new_mq600 = """      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .bundles-grid { grid-template-columns: 1fr; }
      .bot-break { display: block; }
      .bundles-header { margin-bottom: 36px; }
    }"""
assert old_mq600 in content, "BLOCK 2 (mobile bundles-header) not found — aborting"
content = content.replace(old_mq600, new_mq600)

# ─────────────────────────────────────────────────────────
# 3. .fsel-right on mobile: stack vertically instead of cramped row
# ─────────────────────────────────────────────────────────
old_fsel_mobile = """  @media(max-width:720px){
    .fsel-inner{flex-direction:column}
    .fsel-right{width:100%;display:flex;align-items:center;gap:16px;min-width:0;text-align:left}
    .fsel-price{font-size:40px}
    .fsel-once{margin-bottom:0}
    .fsel-panel{padding:24px 20px}
    .fsel-tt{max-width:260px}
  }"""
new_fsel_mobile = """  @media(max-width:720px){
    .fsel-inner{flex-direction:column}
    .fsel-right{width:100%;display:flex;flex-direction:column;align-items:center;gap:10px;min-width:0;text-align:center}
    .fsel-price{font-size:40px;margin-bottom:0}
    .fsel-once{margin-bottom:0}
    .fsel-btn{width:100%}
    .fsel-panel{padding:24px 20px}
    .fsel-tt{max-width:260px}
  }"""
assert old_fsel_mobile in content, "BLOCK 3 (fsel-right mobile) not found — aborting"
content = content.replace(old_fsel_mobile, new_fsel_mobile)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — mobile spacing patch applied successfully")
