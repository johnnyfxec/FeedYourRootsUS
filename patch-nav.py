with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS del nav + overlay — insertar justo antes de </style>
# ─────────────────────────────────────────────────────────

old_style_end = """    @media (max-width: 600px) {
      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .chapters-grid, .bundles-grid { grid-template-columns: 1fr; }
      .chapter-card { flex-direction: column; }
      .bot-break { display: block; }
    }
  </style>"""

new_style_end = """    @media (max-width: 600px) {
      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .chapters-grid, .bundles-grid { grid-template-columns: 1fr; }
      .chapter-card { flex-direction: column; }
      .bot-break { display: block; }
    }

    /* ══════════════════════════
       NAV
    ══════════════════════════ */
    #site-nav { position: fixed; top: 0; left: 0; right: 0; z-index: 500; display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; background: rgba(245,236,215,0.82); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1px solid rgba(92,58,30,0.08); }
    .nav-brand { display: flex; align-items: center; gap: 10px; }
    .nav-brand img { height: 34px; width: auto; display: block; }
    .nav-brand-text { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 18px; color: #5C3A1E; letter-spacing: -0.2px; }
    .nav-links { display: flex; align-items: center; gap: 36px; }
    .nav-links a { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #5C3A1E; letter-spacing: 0.3px; transition: color 0.2s; }
    .nav-links a:hover { color: #D4732A; }
    .nav-cta { display: inline-block; background: #D4732A; color: #fff !important; font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 13px; padding: 11px 24px; border-radius: 50px; letter-spacing: 0.3px; transition: all 0.3s ease; }
    .nav-cta:hover { background: #B85E1E; }
    .nav-burger { display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer; padding: 8px; }
    .nav-burger span { width: 24px; height: 2px; background: #5C3A1E; display: block; transition: all 0.3s ease; }

    /* NAV OVERLAY (mobile menu) */
    .nav-overlay { display: none; position: fixed; inset: 0; background: #180A02; z-index: 999; align-items: center; justify-content: center; opacity: 0; transition: opacity 0.35s ease; }
    .nav-overlay.active { display: flex; opacity: 1; }
    .nav-overlay-close { position: absolute; top: 24px; right: 28px; color: #F5ECD7; font-size: 28px; cursor: pointer; opacity: 0.7; transition: opacity 0.2s; line-height: 1; background: none; border: none; }
    .nav-overlay-close:hover { opacity: 1; }
    .nav-overlay-links { display: flex; flex-direction: column; align-items: center; gap: 34px; }
    .nav-overlay-links a { font-family: 'Playfair Display', serif; font-weight: 700; font-size: clamp(28px, 6vw, 42px); color: #F5ECD7; transition: color 0.25s; }
    .nav-overlay-links a:hover { color: #E8B84B; }
    .nav-overlay-links .nav-cta { margin-top: 14px; font-family: 'DM Sans', sans-serif; font-size: 15px; padding: 16px 36px; }
    .nav-overlay-soon { font-family: 'DM Sans', sans-serif; font-size: 11px; color: rgba(245,236,215,0.4); letter-spacing: 1px; text-transform: uppercase; display: block; margin-top: 6px; }

    @media (max-width: 960px) {
      #site-nav { padding: 16px 20px; }
      .nav-links { display: none; }
      .nav-burger { display: flex; }
      .nav-brand-text { font-size: 16px; }
    }
  </style>"""

assert old_style_end in content, "BLOCK 1 (style end) not found — aborting"
content = content.replace(old_style_end, new_style_end)

# ─────────────────────────────────────────────────────────
# 2. HTML del nav + overlay — insertar justo después de <body>
# ─────────────────────────────────────────────────────────

old_body_open = """<body>

<!-- ════════════ HERO ════════════ -->"""

new_body_open = """<body>

<!-- ════════════ NAV ════════════ -->
<nav id="site-nav">
  <a href="#hero" class="nav-brand">
    <img src="FYR-logo-forest-500px.png" alt="Feed Your Roots logo">
    <span class="nav-brand-text">Feed Your Roots</span>
  </a>
  <div class="nav-links">
    <a href="#tools-preview">Bundles</a>
    <a href="/journal" onclick="return false;">The Journal</a>
    <a href="/about" onclick="return false;">About</a>
    <a href="#bundles" class="nav-cta">Get the Blueprint</a>
  </div>
  <button class="nav-burger" onclick="openNavOverlay()" aria-label="Open menu">
    <span></span><span></span><span></span>
  </button>
</nav>

<div class="nav-overlay" id="nav-overlay">
  <button class="nav-overlay-close" onclick="closeNavOverlay()">✕</button>
  <div class="nav-overlay-links">
    <a href="#tools-preview" onclick="closeNavOverlay()">Bundles</a>
    <a href="/journal" onclick="closeNavOverlay(); return false;">The Journal<span class="nav-overlay-soon">Coming Soon</span></a>
    <a href="/about" onclick="closeNavOverlay(); return false;">About<span class="nav-overlay-soon">Coming Soon</span></a>
    <a href="#bundles" class="nav-cta" onclick="closeNavOverlay()">Get the Blueprint</a>
  </div>
</div>

<!-- ════════════ HERO ════════════ -->"""

assert old_body_open in content, "BLOCK 2 (body open) not found — aborting"
content = content.replace(old_body_open, new_body_open)

# ─────────────────────────────────────────────────────────
# 3. JS del toggle — insertar antes del cierre del segundo <script>,
#    junto a openLightbox/closeLightbox para mantener el mismo patrón
# ─────────────────────────────────────────────────────────

old_lightbox_js = """  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
  }
  document.addEventListener('keydown', e => { if(e.key === 'Escape') closeLightbox(); });"""

new_lightbox_js = """  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
    document.body.style.overflow = '';
  }

  // NAV OVERLAY
  function openNavOverlay() {
    document.getElementById('nav-overlay').classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  function closeNavOverlay() {
    document.getElementById('nav-overlay').classList.remove('active');
    document.body.style.overflow = '';
  }

  document.addEventListener('keydown', e => { if(e.key === 'Escape') { closeLightbox(); closeNavOverlay(); } });"""

assert old_lightbox_js in content, "BLOCK 3 (lightbox JS) not found — aborting"
content = content.replace(old_lightbox_js, new_lightbox_js)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — nav patch applied successfully")
