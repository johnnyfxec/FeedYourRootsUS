with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS — accordion toggle button + mobile-only collapse behavior
# ─────────────────────────────────────────────────────────
old_css_anchor = """  .fsel-note{color:#9A8070;font-size:11px;margin-top:8px;font-family:'DM Sans',sans-serif}"""

new_css_anchor = """  .fsel-note{color:#9A8070;font-size:11px;margin-top:8px;font-family:'DM Sans',sans-serif}
  .fsel-toggle{display:none;width:100%;background:transparent;border:1px solid rgba(74,124,89,0.3);border-radius:50px;padding:12px 16px;font-family:'DM Sans',sans-serif;font-size:13px;color:#3A2010;align-items:center;justify-content:center;gap:8px;cursor:pointer;margin-top:16px}
  .fsel-toggle svg{width:14px;height:14px;transition:transform .2s}
  .fsel-toggle.open svg{transform:rotate(180deg)}"""

assert old_css_anchor in content, "BLOCK 1 (css anchor) not found — aborting"
content = content.replace(old_css_anchor, new_css_anchor)

# ─────────────────────────────────────────────────────────
# 2. CSS — mobile media query: hide list by default, show toggle button
# ─────────────────────────────────────────────────────────
old_mobile_mq = """  @media(max-width:720px){
    .fsel-inner{flex-direction:column}
    .fsel-right{width:100%;display:flex;flex-direction:column;align-items:center;gap:10px;min-width:0;text-align:center}
    .fsel-price{font-size:40px;margin-bottom:0}
    .fsel-once{margin-bottom:0}
    .fsel-btn{width:100%}
    .fsel-panel{padding:24px 20px}
    .fsel-tt{max-width:260px}
  }"""

new_mobile_mq = """  @media(max-width:720px){
    .fsel-inner{flex-direction:column}
    .fsel-right{width:100%;display:flex;flex-direction:column;align-items:center;gap:10px;min-width:0;text-align:center;order:1}
    .fsel-left{order:0}
    .fsel-price{font-size:40px;margin-bottom:0}
    .fsel-once{margin-bottom:0}
    .fsel-btn{width:100%}
    .fsel-panel{padding:24px 20px}
    .fsel-list{display:none}
    .fsel-list.open{display:block;margin-top:14px}
    .fsel-toggle{display:flex}
    .fsel-inh .fsel-tt{display:none}
  }"""

assert old_mobile_mq in content, "BLOCK 2 (mobile mq) not found — aborting"
content = content.replace(old_mobile_mq, new_mobile_mq)

# ─────────────────────────────────────────────────────────
# 3. JS — restructure renderFyrPanel: dsc + price + CTA + note always visible,
#    fsel-list wrapped so it can be toggled, add toggle button after CTA area
# ─────────────────────────────────────────────────────────
old_render = """function renderFyrPanel(){var b=BUN.find(function(x){return x.id===ACT;});var corner=b.popular?'<div class="fsel-corner" style="background:#E8B84B;color:#5C3A1E;">MOST POPULAR</div>':b.soon?'<div class="fsel-corner" style="background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.85);">COMING SOON</div>':'';var items=b.items.map(function(it){if(it.inh){return '<li><span class="fsel-ck-m">&middot;</span><span class="fsel-inh"><span class="fsel-it-i">'+it.t+'</span><em class="fsel-inh-ico" onclick="fyrTT(\\''+it.inh+'\\',event)">i</em>'+gTT(it.inh)+'</span></li>';}return '<li><span class="fsel-ck-g">&#10003;</span><span class="fsel-it-n">'+it.t+'</span></li>';}).join('');var url=FYR_CO[b.key];var btn=b.ok&&url?'<a href="'+url+'" class="fsel-btn" target="_blank">'+b.cta+'</a>':'<span class="fsel-btn-soon">'+b.cta+'</span>';document.getElementById('fyr-panel').innerHTML=corner+'<div class="fsel-inner"><div class="fsel-left"><div class="fsel-lbl">'+b.name+'</div><div class="fsel-tag">'+b.tag+'</div><div class="fsel-dsc">'+b.dsc+'</div><ul class="fsel-list">'+items+'</ul></div><div class="fsel-right"><div class="fsel-price"><sup>$</sup>'+b.price+'</div><div class="fsel-once">one-time &middot; instant access</div>'+btn+(b.ok?'<p class="fsel-note">All digital. Print what you need.</p>':'')+'</div></div>';document.querySelectorAll('.fsel-inh').forEach(function(w){var ico=w.querySelector('.fsel-inh-ico');var tt=w.querySelector('.fsel-tt');if(!ico||!tt)return;w.addEventListener('mouseenter',function(){tt.classList.add('show');});w.addEventListener('mouseleave',function(){tt.classList.remove('show');});});}"""

new_render = """function renderFyrPanel(){var b=BUN.find(function(x){return x.id===ACT;});var corner=b.popular?'<div class="fsel-corner" style="background:#E8B84B;color:#5C3A1E;">MOST POPULAR</div>':b.soon?'<div class="fsel-corner" style="background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.85);">COMING SOON</div>':'';var items=b.items.map(function(it){if(it.inh){return '<li><span class="fsel-ck-m">&middot;</span><span class="fsel-inh"><span class="fsel-it-i">'+it.t+'</span><em class="fsel-inh-ico" onclick="fyrTT(\\''+it.inh+'\\',event)">i</em>'+gTT(it.inh)+'</span></li>';}return '<li><span class="fsel-ck-g">&#10003;</span><span class="fsel-it-n">'+it.t+'</span></li>';}).join('');var url=FYR_CO[b.key];var btn=b.ok&&url?'<a href="'+url+'" class="fsel-btn" target="_blank">'+b.cta+'</a>':'<span class="fsel-btn-soon">'+b.cta+'</span>';var toggle='<button type="button" class="fsel-toggle" id="fsel-toggle-btn" onclick="fyrToggleList()"><span id="fsel-toggle-txt">See what\\'s included</span><svg viewBox="0 0 24 24" fill="none"><path d="M6 9l6 6 6-6" stroke="#3A2010" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>';document.getElementById('fyr-panel').innerHTML=corner+'<div class="fsel-inner"><div class="fsel-left"><div class="fsel-lbl">'+b.name+'</div><div class="fsel-tag">'+b.tag+'</div><div class="fsel-dsc">'+b.dsc+'</div><ul class="fsel-list" id="fsel-list">'+items+'</ul></div><div class="fsel-right"><div class="fsel-price"><sup>$</sup>'+b.price+'</div><div class="fsel-once">one-time &middot; instant access</div>'+btn+(b.ok?'<p class="fsel-note">All digital. Print what you need.</p>':'')+toggle+'</div></div>';document.querySelectorAll('.fsel-inh').forEach(function(w){var ico=w.querySelector('.fsel-inh-ico');var tt=w.querySelector('.fsel-tt');if(!ico||!tt)return;w.addEventListener('mouseenter',function(){tt.classList.add('show');});w.addEventListener('mouseleave',function(){tt.classList.remove('show');});});}
  function fyrToggleList(){var l=document.getElementById('fsel-list');var btn=document.getElementById('fsel-toggle-btn');var txt=document.getElementById('fsel-toggle-txt');if(!l||!btn)return;var open=l.classList.toggle('open');btn.classList.toggle('open',open);txt.textContent=open?'Hide details':'See what\\'s included';}"""

assert old_render in content, "BLOCK 3 (renderFyrPanel) not found — aborting"
content = content.replace(old_render, new_render)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — bundle mobile accordion patch applied successfully")
