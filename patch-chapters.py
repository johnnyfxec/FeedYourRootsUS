with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS — reemplazar .chapters-grid / .chapter-card por layout 2 columnas
# ─────────────────────────────────────────────────────────

old_css = """    #chapters { padding: 130px 24px; overflow: hidden; }
    .chapters-inner { max-width: 1200px; margin: 0 auto; position: relative; z-index: 3; }
    .chapters-header { text-align: center; margin-bottom: 32px; }
    .label-terra { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; color: #D4732A; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 14px; }
    .label-terra::before, .label-terra::after { content: ''; width: 44px; height: 1px; background: #D4732A; opacity: 0.4; display: block; }
    .chapters-h2 { font-family: 'Playfair Display', serif; font-weight: 700; font-size: clamp(30px, 4vw, 50px); color: #4A7C59; margin-bottom: 12px; }
    .chapters-sub { font-family: 'Lora', serif; font-style: italic; font-size: 17px; color: rgba(92,58,30,0.56); }
    .chapters-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 18px; }
    .chapter-card { background: rgba(253,250,242,0.88); border-radius: 14px; padding: 22px 24px; border-left: 3px solid #4A7C59; box-shadow: 0 2px 18px rgba(74,124,89,0.09); transition: all 0.35s cubic-bezier(0.22,1,0.36,1); display: flex; gap: 16px; align-items: center; }
    .chapter-card:hover { transform: translateY(-5px); box-shadow: 0 14px 40px rgba(74,124,89,0.18); background: rgba(253,250,242,1); }
    .chapter-img { width: 54px; height: 54px; object-fit: contain; flex-shrink: 0; margin-top: 2px; }
    .chapter-num { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; color: #D4732A; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; }
    .chapter-title { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: #5C3A1E; margin-bottom: 6px; line-height: 1.3; }
    .chapter-desc { font-family: 'Lora', serif; font-style: italic; font-size: 12.5px; color: rgba(92,58,30,0.6); line-height: 1.6; }"""

new_css = """    #chapters { padding: 130px 24px; overflow: hidden; }
    .chapters-inner { max-width: 1200px; margin: 0 auto; position: relative; z-index: 3; }
    .chapters-header { text-align: center; margin-bottom: 56px; }
    .label-terra { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; color: #D4732A; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 14px; }
    .label-terra::before, .label-terra::after { content: ''; width: 44px; height: 1px; background: #D4732A; opacity: 0.4; display: block; }
    .chapters-h2 { font-family: 'Playfair Display', serif; font-weight: 700; font-size: clamp(30px, 4vw, 50px); color: #4A7C59; margin-bottom: 12px; }
    .chapters-sub { font-family: 'Lora', serif; font-style: italic; font-size: 17px; color: rgba(92,58,30,0.56); }
    .chapters-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 88px; align-items: stretch; }
    .chapters-list { display: flex; flex-direction: column; justify-content: space-between; gap: 22px; }
    .chapter-row { display: flex; gap: 16px; align-items: baseline; }
    .chapter-num { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: #D4732A; flex-shrink: 0; width: 26px; }
    .chapter-outcome { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 500; color: #3A2010; line-height: 1.5; }
    .chapter-outcome-sub { font-family: 'Lora', serif; font-style: italic; font-size: 13px; color: rgba(92,58,30,0.58); line-height: 1.6; margin-top: 3px; }
    .chapters-cover { position: relative; display: flex; align-items: center; justify-content: center; }
    .chapters-cover-shadow { position: absolute; inset: 10px; background: rgba(60,30,10,0.2); border-radius: 4px 20px 20px 4px; transform: perspective(800px) rotateY(-5deg) translateX(-10px) translateY(12px); filter: blur(30px); }
    .chapters-cover img { width: 100%; max-width: 380px; border-radius: 4px 14px 14px 4px; box-shadow: -8px 6px 0 rgba(60,30,10,0.12), 0 28px 70px rgba(60,30,10,0.3); position: relative; z-index: 1; transform: perspective(1000px) rotateY(-4deg); }"""

assert old_css in content, "BLOCK 1 (chapters CSS) not found — aborting"
content = content.replace(old_css, new_css)

# ─────────────────────────────────────────────────────────
# 2. HTML — reemplazar el grid de 12 tarjetas por 2 columnas
# ─────────────────────────────────────────────────────────

old_html = """    <div class="chapters-header">
      <div class="label-terra reveal">Twelve Chapters</div>
      <h2 class="chapters-h2 reveal d1">What's Inside</h2>
      <p class="chapters-sub reveal d2">One year. One half acre. Everything you need.</p>
    </div>
    <div class="chapters-grid">
      <div class="chapter-card reveal"><img src="E01.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 1</div><div class="chapter-title">Plant First, Plan Later</div><div class="chapter-desc">Why fruit trees go in the ground on day one, and how twelve of them fit in an ordinary backyard.</div></div></div>
      <div class="chapter-card reveal d1"><img src="E03.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 2</div><div class="chapter-title">The Seed Library</div><div class="chapter-desc">Buy seeds once. Save them forever. The shoebox that funds every future garden.</div></div></div>
      <div class="chapter-card reveal d2"><img src="E05.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 3</div><div class="chapter-title">The Little Greenhouse</div><div class="chapter-desc">The shed-sized multiplier: seedlings, winter salads, and a season that never ends.</div></div></div>
      <div class="chapter-card reveal"><img src="E07.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 4</div><div class="chapter-title">Six Days to Feed Your Flock</div><div class="chapter-desc">Grow a week of fresh chicken feed on one shelf, from a cup of grain.</div></div></div>
      <div class="chapter-card reveal d1"><img src="E09.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 5</div><div class="chapter-title">Turn Everything Into Gold</div><div class="chapter-desc">Composting made civilized: every banana peel becomes next year's tomato.</div></div></div>
      <div class="chapter-card reveal d2"><img src="E11.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 6</div><div class="chapter-title">Let the Sky Pay the Water Bill</div><div class="chapter-desc">One barrel, one afternoon, six hundred free gallons per inch of rain.</div></div></div>
      <div class="chapter-card reveal"><img src="E13.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 7</div><div class="chapter-title">The Sweetest Workers</div><div class="chapter-desc">One beehive: more fruit on every tree, and the only food that never expires.</div></div></div>
      <div class="chapter-card reveal d1"><img src="E15.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 8</div><div class="chapter-title">The Calories That Keep You Full</div><div class="chapter-desc">Potatoes, beans, and squash: the crops that actually carry a family through winter.</div></div></div>
      <div class="chapter-card reveal d2"><img src="E17.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 9</div><div class="chapter-title">The Garden at Your Back Door</div><div class="chapter-desc">Proximity is the whole secret. Put food where you live and you'll actually eat it.</div></div></div>
      <div class="chapter-card reveal"><img src="E19.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 10</div><div class="chapter-title">The Art of Keeping</div><div class="chapter-desc">Freeze, can, dry: turn one abundant August into twelve fed months.</div></div></div>
      <div class="chapter-card reveal d1"><img src="E21.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 11</div><div class="chapter-title">Fences That Feed You</div><div class="chapter-desc">Property lines that grow blackberries instead of just marking territory.</div></div></div>
      <div class="chapter-card reveal d2"><img src="E24.png" class="chapter-img" alt=""><div class="chapter-content"><div class="chapter-num">Ch. 12</div><div class="chapter-title">Leave Some Wild</div><div class="chapter-desc">One untamed corner, one wild edible a month, and land that teaches you back.</div></div></div>
    </div>"""

new_html = """    <div class="chapters-header">
      <div class="label-terra reveal">The Half-Acre Blueprint</div>
      <h2 class="chapters-h2 reveal d1">What's Inside</h2>
      <p class="chapters-sub reveal d2">One year. One half acre. Everything you need.</p>
    </div>
    <div class="chapters-cols">
      <div class="chapters-list">
        <div class="chapter-row reveal"><span class="chapter-num">01</span><div><div class="chapter-outcome">12 fruit trees, one backyard.</div><div class="chapter-outcome-sub">Exact spacing and placement for a standard suburban lot.</div></div></div>
        <div class="chapter-row reveal d1"><span class="chapter-num">02</span><div><div class="chapter-outcome">Stop buying seeds every spring.</div><div class="chapter-outcome-sub">The one-shelf system that saves and organizes them forever.</div></div></div>
        <div class="chapter-row reveal d2"><span class="chapter-num">03</span><div><div class="chapter-outcome">A growing season that starts before spring does.</div><div class="chapter-outcome-sub">Seedlings in February, harvests by July–August.</div></div></div>
        <div class="chapter-row reveal"><span class="chapter-num">04</span><div><div class="chapter-outcome">A week of chicken feed from one cup of grain.</div><div class="chapter-outcome-sub">The 6-tray fodder system, step by step.</div></div></div>
        <div class="chapter-row reveal d1"><span class="chapter-num">05</span><div><div class="chapter-outcome">Every food scrap becomes next year's soil.</div><div class="chapter-outcome-sub">The 3-bin compost method, no smell, no mess.</div></div></div>
        <div class="chapter-row reveal d2"><span class="chapter-num">06</span><div><div class="chapter-outcome">600 free gallons per inch of rain.</div><div class="chapter-outcome-sub">One barrel, one afternoon, zero plumbing.</div></div></div>
        <div class="chapter-row reveal"><span class="chapter-num">07</span><div><div class="chapter-outcome">More fruit on every tree.</div><div class="chapter-outcome-sub">What one beehive does for pollination — and the honey.</div></div></div>
        <div class="chapter-row reveal d1"><span class="chapter-num">08</span><div><div class="chapter-outcome">The 3 crops that actually feed a family through winter.</div><div class="chapter-outcome-sub">Potatoes, beans, squash — yields and storage.</div></div></div>
        <div class="chapter-row reveal d2"><span class="chapter-num">09</span><div><div class="chapter-outcome">Food you'll actually eat.</div><div class="chapter-outcome-sub">Why proximity beats acreage, and where to put it.</div></div></div>
        <div class="chapter-row reveal"><span class="chapter-num">10</span><div><div class="chapter-outcome">One August turns into 12 fed months.</div><div class="chapter-outcome-sub">Freezing, canning, and drying — the decision tree.</div></div></div>
        <div class="chapter-row reveal d1"><span class="chapter-num">11</span><div><div class="chapter-outcome">Property lines that grow blackberries.</div><div class="chapter-outcome-sub">Living fences that replace fencing costs.</div></div></div>
        <div class="chapter-row reveal d2"><span class="chapter-num">12</span><div><div class="chapter-outcome">One wild corner, one edible a month.</div><div class="chapter-outcome-sub">What to leave untouched — and why it matters.</div></div></div>
      </div>
      <div class="chapters-cover reveal d2">
        <div class="chapters-cover-shadow"></div>
        <img src="cover.png" alt="Feed Your Roots — The Half-Acre Blueprint book cover">
      </div>
    </div>"""

assert old_html in content, "BLOCK 2 (chapters HTML) not found — aborting"
content = content.replace(old_html, new_html)

# ─────────────────────────────────────────────────────────
# 3. Media queries — actualizar referencias a .chapters-grid (ya no existe)
# ─────────────────────────────────────────────────────────

old_mq_960 = """      .vision-grid { grid-template-columns: 1fr 1fr; }
      .chapters-grid { grid-template-columns: 1fr 1fr; }
      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
      .float-el { display: none; }
    }"""

new_mq_960 = """      .vision-grid { grid-template-columns: 1fr 1fr; }
      .chapters-cols { grid-template-columns: 1fr; gap: 48px; }
      .chapters-cover { order: -1; }
      .chapters-cover img { max-width: 280px; }
      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
      .float-el { display: none; }
    }"""

assert old_mq_960 in content, "BLOCK 3 (media query 960) not found — aborting"
content = content.replace(old_mq_960, new_mq_960)

old_mq_600 = """      .vision-grid, .chapters-grid, .bundles-grid { grid-template-columns: 1fr; }
      .chapter-card { flex-direction: column; }
      .bot-break { display: block; }
    }"""

new_mq_600 = """      .vision-grid, .bundles-grid { grid-template-columns: 1fr; }
      .bot-break { display: block; }
    }"""

assert old_mq_600 in content, "BLOCK 4 (media query 600) not found — aborting"
content = content.replace(old_mq_600, new_mq_600)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — chapters patch applied successfully")
