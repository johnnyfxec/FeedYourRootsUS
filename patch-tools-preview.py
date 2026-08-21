with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS — insertar antes de </style>
# ─────────────────────────────────────────────────────────

old_style_end = """    @media (max-width: 960px) {
      #site-nav { padding: 16px 20px; }
      body { padding-top: 66px; }
      .nav-links { display: none; }
      .nav-burger { display: flex; }
      .nav-brand-text { font-size: 16px; }
    }
  </style>"""

new_style_end = """    @media (max-width: 960px) {
      #site-nav { padding: 16px 20px; }
      body { padding-top: 66px; }
      .nav-links { display: none; }
      .nav-burger { display: flex; }
      .nav-brand-text { font-size: 16px; }
    }

    /* ══════════════════════════
       TOOLS PREVIEW CAROUSEL
    ══════════════════════════ */
    #tools-preview { padding: 100px 24px; overflow: hidden; }
    .tp-inner { max-width: 1300px; margin: 0 auto; position: relative; z-index: 3; }
    .tp-header { text-align: center; margin-bottom: 8px; }
    .tp-stage { position: relative; height: clamp(460px, 62vh, 640px); display: flex; align-items: center; justify-content: center; margin: 40px 0; }
    .tp-card { position: absolute; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.35); transition: all 0.5s cubic-bezier(0.22,1,0.36,1); background: #FDFAF2; }
    .tp-card img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .tp-card.tp-current { width: min(70vw, 420px); height: clamp(400px, 56vh, 560px); z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-prev { width: min(50vw, 340px); height: clamp(360px, 50vh, 500px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next { width: min(50vw, 340px); height: clamp(360px, 50vh, 500px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-arrow { position: absolute; top: 50%; transform: translateY(-50%); z-index: 4; width: 52px; height: 52px; border-radius: 50%; background: rgba(253,250,242,0.85); backdrop-filter: blur(6px); border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 8px 24px rgba(60,30,10,0.2); transition: all 0.25s ease; }
    .tp-arrow:hover { background: #FDFAF2; transform: translateY(-50%) scale(1.08); }
    .tp-arrow svg { width: 20px; height: 20px; }
    .tp-arrow-prev { left: calc(50% - min(70vw, 420px)/2 - 66px); }
    .tp-arrow-next { right: calc(50% - min(70vw, 420px)/2 - 66px); }
    .tp-meta { text-align: center; max-width: 520px; margin: 0 auto; }
    .tp-tier { display: inline-block; font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; color: #4A7C59; background: rgba(74,124,89,0.1); border: 1px solid rgba(74,124,89,0.25); padding: 5px 14px; border-radius: 20px; margin-bottom: 14px; }
    .tp-title { font-family: 'Playfair Display', serif; font-weight: 700; font-size: clamp(22px, 3vw, 30px); color: #4A7C59; margin-bottom: 10px; line-height: 1.25; }
    .tp-desc { font-family: 'Lora', serif; font-style: italic; font-size: 15px; color: rgba(92,58,30,0.68); line-height: 1.7; }
    .tp-dots { display: flex; justify-content: center; gap: 8px; margin-top: 36px; }
    .tp-dot { width: 7px; height: 7px; border-radius: 50%; background: rgba(74,124,89,0.25); border: none; cursor: pointer; padding: 0; transition: all 0.25s ease; }
    .tp-dot.active { background: #D4732A; width: 22px; border-radius: 4px; }

    @media (max-width: 720px) {
      #tools-preview { padding: 60px 0; min-height: 100dvh; display: flex; align-items: center; }
      .tp-inner { width: 100%; }
      .tp-stage { height: 46vh; margin: 28px 0; }
      .tp-card.tp-current { width: 72vw; height: 46vh; }
      .tp-card.tp-prev { width: 40vw; height: 38vh; transform: scale(0.85) translateX(-46vw); }
      .tp-card.tp-next { width: 40vw; height: 38vh; transform: scale(0.85) translateX(46vw); }
      .tp-arrow { width: 42px; height: 42px; }
      .tp-arrow-prev { left: 4vw; }
      .tp-arrow-next { right: 4vw; }
      .tp-header, .tp-meta { padding: 0 24px; }
    }
  </style>"""

assert old_style_end in content, "BLOCK 1 (style end) not found — aborting"
content = content.replace(old_style_end, new_style_end)

# ─────────────────────────────────────────────────────────
# 2. HTML — insertar entre </section> de Solution y <!-- VISION -->
# ─────────────────────────────────────────────────────────

old_html_anchor = """<!-- ════════════ VINE ════════════ -->

<!-- ════════════ VISION ════════════ -->"""

new_html_anchor = """<!-- ════════════ VINE ════════════ -->

<!-- ════════════ TOOLS PREVIEW ════════════ -->
<section id="tools-preview">
  <div class="tp-inner">
    <div class="tp-header">
      <div class="label-terra reveal" style="justify-content:center;">Tools Preview</div>
      <h2 class="chapters-h2 reveal d1">Everything Inside the Bundles</h2>
      <p class="chapters-sub reveal d2">11 resources. Real pages. See exactly what you're getting.</p>
    </div>

    <div class="tp-stage" id="tp-stage">
      <button class="tp-arrow tp-arrow-prev" onclick="tpNav(-1)" aria-label="Previous">
        <svg viewBox="0 0 24 24" fill="none"><path d="M15 18l-6-6 6-6" stroke="#5C3A1E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
      <div class="tp-card tp-prev" id="tp-card-prev"><img id="tp-img-prev" src="" alt=""></div>
      <div class="tp-card tp-current" id="tp-card-current" onclick="openLightbox(TP[TPI].img, TP[TPI].title, TP[TPI].desc)"><img id="tp-img-current" src="" alt=""></div>
      <div class="tp-card tp-next" id="tp-card-next"><img id="tp-img-next" src="" alt=""></div>
      <button class="tp-arrow tp-arrow-next" onclick="tpNav(1)" aria-label="Next">
        <svg viewBox="0 0 24 24" fill="none"><path d="M9 6l6 6-6 6" stroke="#5C3A1E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>

    <div class="tp-meta">
      <span class="tp-tier" id="tp-tier"></span>
      <h3 class="tp-title" id="tp-title"></h3>
      <p class="tp-desc" id="tp-desc"></p>
    </div>

    <div class="tp-dots" id="tp-dots"></div>
  </div>
</section>

<!-- ════════════ VINE ════════════ -->

<!-- ════════════ VISION ════════════ -->"""

assert old_html_anchor in content, "BLOCK 2 (html anchor) not found — aborting"
content = content.replace(old_html_anchor, new_html_anchor)

# ─────────────────────────────────────────────────────────
# 3. JS — insertar antes del cierre del <script> principal,
#    junto al resto de la lógica de interacción
# ─────────────────────────────────────────────────────────

old_js_anchor = """  // NAV OVERLAY
  function openNavOverlay() {"""

new_js_anchor = """  // TOOLS PREVIEW CAROUSEL
  const TP = [
    { img:'P01.png', tier:'Starter', title:'Half-Acre Quick Calendar', desc:'The 36 plants that matter most, mapped to your zone — what to plant this month, not a 12-month manual to read first.' },
    { img:'P02.png', tier:'Starter', title:'Seed Library Kit', desc:'101 heirloom varieties, illustrated and ready to print. Buy seeds once. Save them forever.' },
    { img:'P03.png', tier:'Starter', title:'Seed Library Tracker', desc:'The spreadsheet that remembers what you planted, what sprouted, and what to swap next season.' },
    { img:'P04.png', tier:'Family', title:"Family Homestead Skill Map", desc:'24 tasks sorted by age, from toddler to teen. Everyone gets a job that actually fits them.' },
    { img:'P05.png', tier:'Family', title:"Kids' Roots Activity Pack", desc:'5 printable activities that turn "go play outside" into "go learn how food grows."' },
    { img:'P06.png', tier:'Homestead', title:'Half-Acre Planting Calendar', desc:'101 plants, timed to your exact zone. The full-season version of the Quick Calendar.' },
    { img:'P07.png', tier:'Homestead', title:'Homestead Preservation Log', desc:'Canning, fermenting, dehydrating, freezing — one log to track what\\'s in every jar.' },
    { img:'P08.png', tier:'Complete', title:'Master Layout', desc:'6 site plans for different lot shapes. Find the one that matches your yard and copy it.' },
    { img:'P09.png', tier:'Complete', title:'First & Second Year Action Plan', desc:"52 weeks, mapped out. Never wonder what you're supposed to be doing this week." },
    { img:'P10.png', tier:'Complete', title:'Troubleshooting Field Guide', desc:'150+ evidence-based fixes for garden, soil, pests, chickens, and preservation problems.' },
    { img:'P11.png', tier:'Complete', title:'Shopping & Sourcing Guide', desc:'Real market prices, curated suppliers, and a monthly calendar so you buy at the right time.' },
  ];
  let TPI = 0;

  function tpRenderDots() {
    document.getElementById('tp-dots').innerHTML = TP.map((_, i) =>
      '<button class="tp-dot' + (i === TPI ? ' active' : '') + '" onclick="tpGoTo(' + i + ')" aria-label="Go to slide ' + (i+1) + '"></button>'
    ).join('');
  }

  function tpRender() {
    const cur = TP[TPI];
    const prevIdx = (TPI - 1 + TP.length) % TP.length;
    const nextIdx = (TPI + 1) % TP.length;
    document.getElementById('tp-img-current').src = cur.img;
    document.getElementById('tp-img-current').alt = cur.title;
    document.getElementById('tp-img-prev').src = TP[prevIdx].img;
    document.getElementById('tp-img-next').src = TP[nextIdx].img;
    document.getElementById('tp-tier').textContent = cur.tier;
    document.getElementById('tp-title').textContent = cur.title;
    document.getElementById('tp-desc').textContent = cur.desc;
    tpRenderDots();
  }

  function tpNav(dir) {
    TPI = (TPI + dir + TP.length) % TP.length;
    tpRender();
  }

  function tpGoTo(i) {
    TPI = i;
    tpRender();
  }

  tpRender();

  // Swipe support (mobile)
  (function() {
    const stage = document.getElementById('tp-stage');
    if (!stage) return;
    let startX = 0, startY = 0, tracking = false;
    stage.addEventListener('touchstart', e => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
      tracking = true;
    }, { passive: true });
    stage.addEventListener('touchend', e => {
      if (!tracking) return;
      tracking = false;
      const dx = e.changedTouches[0].clientX - startX;
      const dy = e.changedTouches[0].clientY - startY;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
        tpNav(dx < 0 ? 1 : -1);
      }
    }, { passive: true });
  })();

  // NAV OVERLAY
  function openNavOverlay() {"""

assert old_js_anchor in content, "BLOCK 3 (js anchor) not found — aborting"
content = content.replace(old_js_anchor, new_js_anchor)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — tools-preview carousel patch applied successfully")
