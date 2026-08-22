with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS — replace grid layout with banner-on-top layout
# ─────────────────────────────────────────────────────────
old_css = """    #hero {
      min-height: 100vh;
      display: flex; align-items: center; justify-content: center;
      padding: 120px 24px 110px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }
    .hero-inner { position: relative; z-index: 3; max-width: 1180px; width: 100%; display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center; }
    .hero-eyebrow { font-family: 'Satisfy', cursive; font-size: 22px; color: #4A7C59; margin-bottom: 24px; }
    .hero-h1 { font-family: 'Playfair Display', serif; font-weight: 900; font-size: clamp(38px, 5.5vw, 66px); color: #5C3A1E; line-height: 1.05; margin-bottom: 24px; }
    .hero-sub { font-family: 'Lora', serif; font-size: clamp(15px, 1.8vw, 18px); color: rgba(92,58,30,0.76); line-height: 1.85; margin-bottom: 40px; }

    .hero-book { position: relative; display: flex; justify-content: center; }
    .hero-book-shadow { position: absolute; inset: 10px; background: rgba(60,30,10,0.22); border-radius: 4px 20px 20px 4px; transform: perspective(800px) rotateY(-5deg) translateX(-12px) translateY(14px); filter: blur(34px); }
    .hero-book img { width: 100%; max-width: 360px; border-radius: 4px 14px 14px 4px; box-shadow: -10px 8px 0 rgba(60,30,10,0.12), 0 30px 76px rgba(60,30,10,0.32); transform: perspective(1000px) rotateY(-4deg); position: relative; z-index: 1; transition: transform 0.5s cubic-bezier(0.22,1,0.36,1); }
    .hero-book img:hover { transform: perspective(1000px) rotateY(-2deg) translateY(-7px); }"""

new_css = """    #hero {
      min-height: 100vh;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 100px 24px 40px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }
    .hero-inner { position: relative; z-index: 3; max-width: 1180px; width: 100%; display: flex; flex-direction: column; align-items: center; gap: 32px; }
    .hero-banner { width: 100%; aspect-ratio: 21/9; max-height: 34vh; border-radius: 20px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.3); }
    .hero-banner img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .hero-text { text-align: center; max-width: 720px; }
    .hero-eyebrow { font-family: 'Satisfy', cursive; font-size: 22px; color: #4A7C59; margin-bottom: 18px; }
    .hero-h1 { font-family: 'Playfair Display', serif; font-weight: 900; font-size: clamp(32px, 4.6vw, 56px); color: #5C3A1E; line-height: 1.08; margin-bottom: 18px; }
    .hero-sub { font-family: 'Lora', serif; font-size: clamp(14px, 1.6vw, 17px); color: rgba(92,58,30,0.76); line-height: 1.75; margin-bottom: 28px; }"""

assert old_css in content, "BLOCK 1 (hero CSS) not found — aborting"
content = content.replace(old_css, new_css)

# ─────────────────────────────────────────────────────────
# 2. HTML — replace grid (text + floating book) with banner-on-top + centered text
# ─────────────────────────────────────────────────────────
old_html = """  <div class="hero-inner">
    <div class="hero-text">
      <p class="hero-eyebrow reveal">Half an acre. A whole life.</p>
      <h1 class="hero-h1 reveal d1">You Don't Need<br>a Farm. You Need<br>Half an Acre<br>and a Plan.</h1>
      <p class="hero-sub reveal d2">The illustrated guide that turns the yard you already have into an orchard, a pantry, and a quiet kind of freedom — no experience, no tractor, no six figures required.</p>
      <div class="reveal d3">
        <a href="#bundles" class="btn-primary">Get the Blueprint — $37</a>
        <span class="btn-micro">Instant download · 48 illustrated pages · Yours forever</span>
      </div>
    </div>
    <div class="hero-book reveal d2">
      <div class="hero-book-shadow"></div>
      <img src="assets/covers/cover.png" alt="Feed Your Roots book cover">
    </div>
  </div>"""

new_html = """  <div class="hero-inner">
    <div class="hero-banner reveal">
      <img src="assets/banners/hero-banner.png" alt="A suburban backyard transforming from empty lawn into a thriving vegetable garden with fruit trees and chickens">
    </div>
    <div class="hero-text">
      <p class="hero-eyebrow reveal">Half an acre. A whole life.</p>
      <h1 class="hero-h1 reveal d1">You Don't Need<br>a Farm. You Need<br>Half an Acre<br>and a Plan.</h1>
      <p class="hero-sub reveal d2">The illustrated guide that turns the yard you already have into an orchard, a pantry, and a quiet kind of freedom — no experience, no tractor, no six figures required.</p>
      <div class="reveal d3">
        <a href="#bundles" class="btn-primary">Get the Blueprint — $37</a>
        <span class="btn-micro">Instant download · 48 illustrated pages · Yours forever</span>
      </div>
    </div>
  </div>"""

assert old_html in content, "BLOCK 2 (hero HTML) not found — aborting"
content = content.replace(old_html, new_html)

# ─────────────────────────────────────────────────────────
# 3. Remove now-obsolete mobile override for .hero-book / .hero-inner grid
#    (960px breakpoint had hero-inner grid + hero-book order rules)
# ─────────────────────────────────────────────────────────
old_mq960 = """      .hero-inner { grid-template-columns: 1fr; gap: 52px; text-align: center; }
      .hero-book { order: -1; }
      .hero-book img { max-width: 280px; }
      .hero-bot { display: none; }"""

new_mq960 = """      .hero-banner { max-height: 26vh; }
      .hero-bot { display: none; }"""

assert old_mq960 in content, "BLOCK 3 (960px hero overrides) not found — aborting"
content = content.replace(old_mq960, new_mq960)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — hero banner patch applied successfully")
