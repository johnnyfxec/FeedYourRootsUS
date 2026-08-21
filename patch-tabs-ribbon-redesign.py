with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. Base CSS: pills -> segmented ribbon
# ─────────────────────────────────────────────────────────
old_base = """  .fsel-tabs{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-bottom:28px}
  .fsel-tab{position:relative;border:1.5px solid rgba(245,236,215,0.15);border-radius:40px;padding:10px 16px;cursor:pointer;background:transparent;transition:all .2s;min-width:96px;text-align:center}
  .fsel-tab:hover{border-color:rgba(212,115,42,0.5)}
  .fsel-tab.active{background:#D4732A;border-color:#D4732A}
  .fsel-tb{position:absolute;top:-11px;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap;letter-spacing:.05em;font-family:'DM Sans',sans-serif;pointer-events:none}
  .fsel-tb-pop{background:#E8B84B;color:#5C3A1E}
  .fsel-tb-sn{background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.7);border:1px solid rgba(245,236,215,0.15)}
  .fsel-tn{display:block;color:rgba(245,236,215,0.45);font-size:10px;font-weight:600;letter-spacing:.08em;margin-bottom:2px;font-family:'DM Sans',sans-serif;text-transform:uppercase}
  .fsel-tab.active .fsel-tn{color:#fff}
  .fsel-tp{display:block;color:#F5ECD7;font-size:20px;font-weight:700;font-family:'DM Sans',sans-serif;letter-spacing:-0.3px}
  .fsel-tab.active .fsel-tp{color:#fff}"""

new_base = """  .fsel-tabs{display:flex;justify-content:center;margin-bottom:28px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .fsel-tabs::-webkit-scrollbar{display:none}
  .fsel-tabs-track{display:flex;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;overflow:hidden;flex-shrink:0}
  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:12px 18px;cursor:pointer;background:transparent;transition:background .2s;min-width:84px;text-align:center;flex-shrink:0}
  .fsel-tab:last-child{border-right:none}
  .fsel-tab:hover{background:rgba(245,236,215,0.06)}
  .fsel-tab.active{background:#D4732A}
  .fsel-tb{position:absolute;top:-11px;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap;letter-spacing:.05em;font-family:'DM Sans',sans-serif;pointer-events:none}
  .fsel-tb-pop{background:#E8B84B;color:#5C3A1E}
  .fsel-tb-sn{background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.7);border:1px solid rgba(245,236,215,0.15)}
  .fsel-tn{display:block;color:rgba(245,236,215,0.45);font-size:10px;font-weight:600;letter-spacing:.08em;margin-bottom:2px;font-family:'DM Sans',sans-serif;text-transform:uppercase}
  .fsel-tab.active .fsel-tn{color:#fff}
  .fsel-tp{display:block;color:#F5ECD7;font-size:20px;font-weight:700;font-family:'DM Sans',sans-serif;letter-spacing:-0.3px}
  .fsel-tab.active .fsel-tp{color:#fff}"""

assert old_base in content, "BLOCK 1 (base tabs CSS) not found — aborting"
content = content.replace(old_base, new_base)

# ─────────────────────────────────────────────────────────
# 2. Mobile 480px overrides: smaller ribbon segments instead of forced grid
# ─────────────────────────────────────────────────────────
old_480 = """  @media(max-width:480px){
    .fsel-tabs{gap:4px;margin-bottom:16px}
    .fsel-tab{min-width:calc(20% - 4px);padding:7px 4px}
    .fsel-tn{font-size:7.5px}
    .fsel-tp{font-size:14px}
    .fsel-tb{font-size:8px;padding:2px 6px}
    .fsel-panel{padding:18px 14px;border-radius:16px}
    .fsel-tag{font-size:18px}
    .fsel-tt{max-width:220px;min-width:180px}
  }"""

new_480 = """  @media(max-width:480px){
    .fsel-tabs{justify-content:flex-start;margin-bottom:16px}
    .fsel-tab{min-width:64px;padding:8px 10px}
    .fsel-tn{font-size:7.5px}
    .fsel-tp{font-size:15px}
    .fsel-tb{font-size:8px;padding:2px 6px}
    .fsel-panel{padding:18px 14px;border-radius:16px}
    .fsel-tag{font-size:18px}
    .fsel-tt{max-width:220px;min-width:180px}
  }"""

assert old_480 in content, "BLOCK 2 (480px overrides) not found — aborting"
content = content.replace(old_480, new_480)

# ─────────────────────────────────────────────────────────
# 3. JS: wrap tabs in .fsel-tabs-track for the ribbon border/scroll container
# ─────────────────────────────────────────────────────────
old_render_tabs = """function renderFyrTabs(){document.getElementById('fyr-tabs').innerHTML=BUN.map(function(b){return '<button class="fsel-tab'+(ACT===b.id?' active':'')+'" onclick="fyrSwitch(\\''+b.id+'\\')">'+(b.popular?'<span class="fsel-tb fsel-tb-pop">MOST POPULAR</span>':'')+(b.soon?'<span class="fsel-tb fsel-tb-sn">COMING SOON</span>':'')+'<span class="fsel-tn">'+b.emoji+' '+b.name+'</span><span class="fsel-tp">$'+b.price+'</span></button>';}).join('');}"""

new_render_tabs = """function renderFyrTabs(){document.getElementById('fyr-tabs').innerHTML='<div class="fsel-tabs-track">'+BUN.map(function(b){return '<button class="fsel-tab'+(ACT===b.id?' active':'')+'" onclick="fyrSwitch(\\''+b.id+'\\')">'+(b.popular?'<span class="fsel-tb fsel-tb-pop">MOST POPULAR</span>':'')+(b.soon?'<span class="fsel-tb fsel-tb-sn">COMING SOON</span>':'')+'<span class="fsel-tn">'+b.emoji+' '+b.name+'</span><span class="fsel-tp">$'+b.price+'</span></button>';}).join('')+'</div>';}"""

assert old_render_tabs in content, "BLOCK 3 (renderFyrTabs JS) not found — aborting"
content = content.replace(old_render_tabs, new_render_tabs)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — tabs ribbon redesign applied successfully")
