#!/usr/bin/env python3
"""
patch-bundle-selector.py
Reemplaza <section id="bundles"> en index.html con el
selector animado de 5 tabs + affiliate link loader.
"""

import sys

FILE = '/data/data/com.termux/files/home/FeedYourRootsUS/index.html'

NEW_SECTION = r"""<section id="bundles">
  <div class="float-layer">
    <img class="float-el" src="E29.png" style="width:210px;top:4%;left:-8px;opacity:0.75;" data-speed="0.28">
    <img class="float-el" src="E25.png" style="width:170px;bottom:5%;right:-8px;opacity:0.75;" data-speed="0.38">
  </div>
  <style>
  #fyr-sel{max-width:760px;margin:0 auto}
  .fsel-tabs{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin-bottom:28px}
  .fsel-tab{position:relative;border:1.5px solid rgba(245,236,215,0.15);border-radius:40px;padding:10px 16px;cursor:pointer;background:transparent;transition:all .2s;min-width:96px;text-align:center}
  .fsel-tab:hover{border-color:rgba(212,115,42,0.5)}
  .fsel-tab.active{background:#D4732A;border-color:#D4732A}
  .fsel-tb{position:absolute;top:-11px;left:50%;transform:translateX(-50%);font-size:9px;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap;letter-spacing:.05em;font-family:'DM Sans',sans-serif;pointer-events:none}
  .fsel-tb-pop{background:#E8B84B;color:#5C3A1E}
  .fsel-tb-sn{background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.7);border:1px solid rgba(245,236,215,0.15)}
  .fsel-tn{display:block;color:rgba(245,236,215,0.45);font-size:10px;font-weight:600;letter-spacing:.08em;margin-bottom:2px;font-family:'DM Sans',sans-serif;text-transform:uppercase}
  .fsel-tab.active .fsel-tn{color:#fff}
  .fsel-tp{display:block;color:#F5ECD7;font-size:20px;font-weight:700;font-family:'Playfair Display',serif}
  .fsel-tab.active .fsel-tp{color:#fff}
  .fsel-panel{background:radial-gradient(ellipse at 40% 10%,#FBF3E2 0%,#F5ECD7 100%);border-radius:22px;padding:32px 36px;position:relative;transition:opacity .18s,transform .18s;box-shadow:0 10px 52px rgba(0,0,0,0.32)}
  .fsel-panel.fading{opacity:0;transform:translateY(6px)}
  .fsel-corner{position:absolute;top:0;right:0;font-size:10px;font-weight:700;padding:5px 18px;border-bottom-left-radius:12px;border-top-right-radius:22px;letter-spacing:.06em;font-family:'DM Sans',sans-serif}
  .fsel-inner{display:flex;gap:28px;align-items:flex-start}
  .fsel-left{flex:1;min-width:0}
  .fsel-lbl{color:#D4732A;font-size:10px;font-weight:700;letter-spacing:.12em;margin-bottom:4px;font-family:'DM Sans',sans-serif;text-transform:uppercase}
  .fsel-tag{font-family:'Playfair Display',serif;font-size:22px;color:#5C3A1E;margin:0 0 8px;font-style:italic;font-weight:700}
  .fsel-dsc{color:#6B4226;font-family:'Lora',serif;font-size:13px;line-height:1.7;margin:0 0 18px}
  .fsel-list{list-style:none;padding:0;margin:0}
  .fsel-list li{display:flex;align-items:flex-start;gap:8px;margin-bottom:9px;font-size:13px;position:relative}
  .fsel-ck-g{color:#4A7C59;font-weight:700;flex-shrink:0;margin-top:1px;font-family:'DM Sans',sans-serif}
  .fsel-ck-m{color:#B0A898;font-weight:700;flex-shrink:0;margin-top:1px;font-family:'DM Sans',sans-serif}
  .fsel-it-n{color:#3A2010;font-weight:500;font-family:'DM Sans',sans-serif;line-height:1.5}
  .fsel-it-i{color:#9A8878;font-family:'DM Sans',sans-serif;line-height:1.5}
  .fsel-inh{position:relative;display:inline-flex;align-items:center;gap:4px}
  .fsel-inh-ico{width:14px;height:14px;border-radius:50%;background:#C0B8A8;color:#F5ECD7;font-size:9px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;font-style:normal;flex-shrink:0;line-height:1;font-family:'DM Sans',sans-serif}
  .fsel-inh-ico:hover{background:#7A6A5A}
  .fsel-tt{position:absolute;left:0;bottom:calc(100% + 8px);background:#3A1A08;border:1px solid rgba(212,115,42,0.3);border-radius:12px;padding:14px 16px;min-width:250px;max-width:320px;z-index:50;opacity:0;pointer-events:none;transition:opacity .15s;box-shadow:0 4px 20px rgba(0,0,0,0.45)}
  .fsel-tt.show{opacity:1;pointer-events:auto}
  .fsel-tt-tier{margin-bottom:10px}
  .fsel-tt-tier:last-child{margin-bottom:0}
  .fsel-tt-name{color:#D4732A;font-size:9px;font-weight:700;letter-spacing:.1em;margin-bottom:5px;font-family:'DM Sans',sans-serif;text-transform:uppercase}
  .fsel-tt-item{display:flex;gap:6px;margin-bottom:4px;font-size:11px;color:#D4C8A0;line-height:1.4;font-family:'DM Sans',sans-serif}
  .fsel-tt-ck{color:#4A7C59;font-weight:700;flex-shrink:0}
  .fsel-right{text-align:center;min-width:140px;flex-shrink:0}
  .fsel-price{font-family:'Playfair Display',serif;font-size:52px;font-weight:700;color:#5C3A1E;line-height:1;margin-bottom:4px}
  .fsel-price sup{font-size:22px;vertical-align:super}
  .fsel-once{color:#9A8070;font-size:11px;margin-bottom:18px;font-family:'DM Sans',sans-serif}
  .fsel-btn{display:block;background:#D4732A;color:#fff;font-family:'DM Sans',sans-serif;font-weight:500;font-size:14px;padding:14px 20px;border-radius:50px;text-align:center;letter-spacing:.3px;transition:all .3s ease;border:none;cursor:pointer;width:100%}
  .fsel-btn:hover{background:#B85E1E;transform:translateY(-2px)}
  .fsel-btn-soon{display:block;background:rgba(74,124,89,0.1);color:rgba(92,58,30,0.38);font-family:'DM Sans',sans-serif;font-size:13px;padding:14px 20px;border-radius:50px;border:1px solid rgba(74,124,89,0.18);cursor:default;text-align:center}
  .fsel-note{color:#9A8070;font-size:11px;margin-top:8px;font-family:'DM Sans',sans-serif}
  @media(max-width:720px){
    .fsel-inner{flex-direction:column}
    .fsel-right{width:100%;display:flex;align-items:center;gap:16px;min-width:0;text-align:left}
    .fsel-price{font-size:40px}
    .fsel-once{margin-bottom:0}
    .fsel-panel{padding:24px 20px}
    .fsel-tt{max-width:260px}
  }
  @media(max-width:480px){
    .fsel-tabs{gap:5px}
    .fsel-tab{min-width:calc(33.3% - 7px);padding:9px 8px}
    .fsel-tn{font-size:9px}
    .fsel-tp{font-size:17px}
    .fsel-tb{font-size:8px;padding:2px 6px}
    .fsel-panel{padding:18px 14px;border-radius:16px}
    .fsel-tag{font-size:18px}
    .fsel-tt{max-width:220px;min-width:180px}
  }
  </style>
  <div class="bundles-inner">
    <div class="bundles-header">
      <h2 class="bundles-title reveal">Choose Your Blueprint</h2>
      <p class="bundles-sub reveal d1">Every bundle includes the complete 48-page illustrated guide.</p>
    </div>
    <div id="fyr-sel">
      <div class="fsel-tabs" id="fyr-tabs"></div>
      <div class="fsel-panel" id="fyr-panel"></div>
    </div>
    <p style="text-align:center;font-family:'DM Sans',sans-serif;font-size:12px;color:rgba(245,236,215,0.28);margin-top:24px;letter-spacing:0.4px;">All digital. Instant delivery. Print what you need, keep it forever.</p>
  </div>
  <script>
  var FYR_CO={core:'https://pay.hotmart.com/S107078295H',starter:'https://pay.hotmart.com/K107078722B',family:'https://pay.hotmart.com/C107078806J',homestead:'https://pay.hotmart.com/V107078877Y',complete:null};
  (function(){var aff=new URLSearchParams(window.location.search).get('aff');if(!aff)return;fetch('/affiliates.json').then(function(r){return r.json();}).then(function(d){var a=(d.affiliates||[]).find(function(x){return x.code===aff;});if(a&&a.links){Object.assign(FYR_CO,a.links);}if(typeof renderFyrPanel==='function')renderFyrPanel();}).catch(function(){});})();
  var TI={core:['The Half-Acre Blueprint (48 illustrated pages)','12 chapters: fruit trees, seed saving, composting, rainwater, chickens, bees','USDA Zones 5–9 · All seasons','Instant PDF download · Print forever'],starter:['Half-Acre Quick Calendar — 36 plants, Zones 5–9','Seed Library Kit — 101 botanical illustrations + envelopes','Seed Library Tracker — Google Sheets'],family:['Family Homestead Skill Map — 24 tasks × 5 age groups',"Kids' Roots Activity Pack — 5 printable activities, ages 5–12"],homestead:['Half-Acre Planting Calendar — 101 plants, 19 pages','Homestead Preservation Log — canning, fermentation, dehydrating, freezing']};
  var TO=['core','starter','family','homestead'];
  var BUN=[
    {id:'core',name:'CORE',emoji:'🌱',price:37,cta:'Get the Core',tag:'The Blueprint.',dsc:'The complete 48-page illustrated guide. Every system, every step, every season. Everything you need to begin this weekend.',items:[{t:'The Half-Acre Blueprint (48 illustrated pages)',n:true},{t:'12 chapters: fruit trees, seed saving, composting, rainwater, chickens, bees',n:true},{t:'USDA Zones 5–9 · All seasons',n:true},{t:'Instant PDF download · Print forever',n:true}],key:'core',ok:true},
    {id:'starter',name:'STARTER',emoji:'🌿',price:47,cta:'Get the Starter',tag:'Blueprint + First Year Tools.',dsc:'The guide plus the tools that map day one and keep your seeds organized for every season that follows.',items:[{t:'Everything in Core',n:false,inh:'core'},{t:'Half-Acre Quick Calendar — 36 plants, Zones 5–9',n:true},{t:'Seed Library Kit — 101 botanical illustrations + envelopes',n:true},{t:'Seed Library Tracker — Google Sheets',n:true}],key:'starter',ok:true},
    {id:'family',name:'FAMILY',emoji:'🏡',price:67,cta:'Get the Family Bundle',tag:'Everything, for every pair of hands.',dsc:'A half acre runs best as a crew. Adds the tools to involve every family member — from toddler to teen.',items:[{t:'Everything in Starter',n:false,inh:'starter'},{t:'Family Homestead Skill Map — 24 tasks × 5 age groups',n:true},{t:"Kids' Roots Activity Pack — 5 printable activities, ages 5–12",n:true}],key:'family',ok:true},
    {id:'homestead',name:'HOMESTEAD',emoji:'🌾',price:97,cta:'Get the Homestead Bundle',tag:'The full system, deeper.',dsc:'Everything above plus the tools that turn a seasonal garden into a year-round food operation.',items:[{t:'Everything in Family',n:false,inh:'family'},{t:'Half-Acre Planting Calendar — 101 plants, per-zone timing, 19 pages',n:true},{t:'Homestead Preservation Log — canning, fermentation, dehydrating, freezing',n:true}],popular:true,key:'homestead',ok:true},
    {id:'complete',name:'COMPLETE',emoji:'🏆',price:150,cta:'Join the Waitlist',tag:'The full library.',dsc:'The complete Feed Your Roots system — every document, every plan, every reference guide. Nothing left to add.',items:[{t:'Everything in Homestead',n:false,inh:'homestead'},{t:'Half-Acre Master Layout — 6 detailed site plans',n:true},{t:'First Year 52-Week Action Plan',n:true},{t:'Shopping & Sourcing Guide',n:true},{t:'Troubleshooting Field Guide',n:true},{t:'USDA Canning Guide',n:true}],soon:true,key:'complete',ok:false}
  ];
  var ACT='homestead',FADING=false;
  function gTT(id){var idx=TO.indexOf(id);if(idx<0)return '';var tiers=TO.slice(0,idx+1);return '<div class="fsel-tt" id="tt-'+id+'">'+tiers.map(function(t){return '<div class="fsel-tt-tier"><div class="fsel-tt-name">'+t.toUpperCase()+'</div>'+TI[t].map(function(i){return '<div class="fsel-tt-item"><span class="fsel-tt-ck">&#10003;</span><span>'+i+'</span></div>';}).join('')+'</div>';}).join('')+'</div>';}
  function renderFyrTabs(){document.getElementById('fyr-tabs').innerHTML=BUN.map(function(b){return '<button class="fsel-tab'+(ACT===b.id?' active':'')+'" onclick="fyrSwitch(\''+b.id+'\')">'+(b.popular?'<span class="fsel-tb fsel-tb-pop">MOST POPULAR</span>':'')+(b.soon?'<span class="fsel-tb fsel-tb-sn">COMING SOON</span>':'')+'<span class="fsel-tn">'+b.emoji+' '+b.name+'</span><span class="fsel-tp">$'+b.price+'</span></button>';}).join('');}
  function renderFyrPanel(){var b=BUN.find(function(x){return x.id===ACT;});var corner=b.popular?'<div class="fsel-corner" style="background:#E8B84B;color:#5C3A1E;">MOST POPULAR</div>':b.soon?'<div class="fsel-corner" style="background:rgba(74,124,89,0.25);color:rgba(245,236,215,0.85);">COMING SOON</div>':'';var items=b.items.map(function(it){if(it.inh){return '<li><span class="fsel-ck-m">&middot;</span><span class="fsel-inh"><span class="fsel-it-i">'+it.t+'</span><em class="fsel-inh-ico" onclick="fyrTT(\''+it.inh+'\',event)">i</em>'+gTT(it.inh)+'</span></li>';}return '<li><span class="fsel-ck-g">&#10003;</span><span class="fsel-it-n">'+it.t+'</span></li>';}).join('');var url=FYR_CO[b.key];var btn=b.ok&&url?'<a href="'+url+'" class="fsel-btn" target="_blank">'+b.cta+'</a>':'<span class="fsel-btn-soon">'+b.cta+'</span>';document.getElementById('fyr-panel').innerHTML=corner+'<div class="fsel-inner"><div class="fsel-left"><div class="fsel-lbl">'+b.name+'</div><div class="fsel-tag">'+b.tag+'</div><div class="fsel-dsc">'+b.dsc+'</div><ul class="fsel-list">'+items+'</ul></div><div class="fsel-right"><div class="fsel-price"><sup>$</sup>'+b.price+'</div><div class="fsel-once">one-time &middot; instant access</div>'+btn+(b.ok?'<p class="fsel-note">All digital. Print what you need.</p>':'')+'</div></div>';document.querySelectorAll('.fsel-inh').forEach(function(w){var ico=w.querySelector('.fsel-inh-ico');var tt=w.querySelector('.fsel-tt');if(!ico||!tt)return;w.addEventListener('mouseenter',function(){tt.classList.add('show');});w.addEventListener('mouseleave',function(){tt.classList.remove('show');});});}
  function fyrTT(id,e){e.stopPropagation();var tt=document.getElementById('tt-'+id);if(!tt)return;var s=tt.classList.contains('show');document.querySelectorAll('.fsel-tt.show').forEach(function(t){t.classList.remove('show');});if(!s)tt.classList.add('show');}
  function fyrSwitch(id){if(id===ACT||FADING)return;FADING=true;var p=document.getElementById('fyr-panel');p.classList.add('fading');setTimeout(function(){ACT=id;renderFyrTabs();renderFyrPanel();p.classList.remove('fading');FADING=false;},180);}
  document.addEventListener('click',function(){document.querySelectorAll('.fsel-tt.show').forEach(function(t){t.classList.remove('show');});});
  renderFyrTabs();renderFyrPanel();
  </script>
</section>"""

# ── Read ─────────────────────────────────────────────────
with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# ── Find section boundaries ──────────────────────────────
START_TAG = '<section id="bundles">'
END_TAG   = '</section>'

start = html.find(START_TAG)
if start == -1:
    print('ERROR: <section id="bundles"> not found')
    sys.exit(1)

end = html.find(END_TAG, start)
if end == -1:
    print('ERROR: closing </section> not found')
    sys.exit(1)

end += len(END_TAG)

# ── Replace ──────────────────────────────────────────────
new_html = html[:start] + NEW_SECTION + html[end:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)

print('✓ Bundle selector updated — lines replaced successfully')
print('  Next: git add -A && git commit -m "feat: animated bundle selector + affiliate loader" && git push')
