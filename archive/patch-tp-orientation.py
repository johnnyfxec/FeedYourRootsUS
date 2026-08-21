with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. CSS — object-fit:contain + dimensiones por orientación + menos margin
# ─────────────────────────────────────────────────────────

old_css = """    .tp-stage { position: relative; height: clamp(460px, 62vh, 640px); display: flex; align-items: center; justify-content: center; margin: 40px 0; }
    .tp-card { position: absolute; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.35); transition: all 0.5s cubic-bezier(0.22,1,0.36,1); background: #FDFAF2; }
    .tp-card img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .tp-card.tp-current { width: min(70vw, 420px); height: clamp(400px, 56vh, 560px); z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-prev { width: min(50vw, 340px); height: clamp(360px, 50vh, 500px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next { width: min(50vw, 340px); height: clamp(360px, 50vh, 500px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }"""

new_css = """    .tp-stage { position: relative; height: clamp(380px, 52vh, 520px); display: flex; align-items: center; justify-content: center; margin: 20px 0; }
    .tp-card { position: absolute; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.35); transition: all 0.5s cubic-bezier(0.22,1,0.36,1); background: #FDFAF2; display: flex; align-items: center; justify-content: center; }
    .tp-card img { width: 100%; height: 100%; object-fit: contain; display: block; }
    .tp-card.tp-current { width: min(70vw, 420px); height: clamp(340px, 46vh, 460px); z-index: 3; opacity: 1; transform: scale(1) translateX(0); cursor: pointer; }
    .tp-card.tp-current.tp-land { width: min(85vw, 620px); height: clamp(280px, 36vh, 360px); }
    .tp-card.tp-prev { width: min(50vw, 340px); height: clamp(300px, 40vh, 400px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(-1 * min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-prev.tp-land { width: min(60vw, 460px); height: clamp(240px, 30vh, 300px); transform: scale(0.88) translateX(calc(-1 * min(42vw, 280px))); }
    .tp-card.tp-next { width: min(50vw, 340px); height: clamp(300px, 40vh, 400px); z-index: 2; opacity: 0.32; transform: scale(0.88) translateX(calc(min(38vw, 240px))); pointer-events: none; }
    .tp-card.tp-next.tp-land { width: min(60vw, 460px); height: clamp(240px, 30vh, 300px); transform: scale(0.88) translateX(calc(min(42vw, 280px))); }"""

assert old_css in content, "BLOCK 1 (tp CSS) not found — aborting"
content = content.replace(old_css, new_css)

# ─────────────────────────────────────────────────────────
# 2. CSS mobile — mismo criterio en el breakpoint 720px
# ─────────────────────────────────────────────────────────

old_mq = """      .tp-stage { height: 46vh; margin: 28px 0; }
      .tp-card.tp-current { width: 72vw; height: 46vh; }
      .tp-card.tp-prev { width: 40vw; height: 38vh; transform: scale(0.85) translateX(-46vw); }
      .tp-card.tp-next { width: 40vw; height: 38vh; transform: scale(0.85) translateX(46vw); }"""

new_mq = """      .tp-stage { height: 40vh; margin: 16px 0; }
      .tp-card.tp-current { width: 72vw; height: 40vh; }
      .tp-card.tp-current.tp-land { width: 88vw; height: 30vh; }
      .tp-card.tp-prev { width: 40vw; height: 32vh; transform: scale(0.85) translateX(-46vw); }
      .tp-card.tp-prev.tp-land { width: 50vw; height: 24vh; transform: scale(0.85) translateX(-50vw); }
      .tp-card.tp-next { width: 40vw; height: 32vh; transform: scale(0.85) translateX(46vw); }
      .tp-card.tp-next.tp-land { width: 50vw; height: 24vh; transform: scale(0.85) translateX(50vw); }"""

assert old_mq in content, "BLOCK 2 (mobile mq) not found — aborting"
content = content.replace(old_mq, new_mq)

# ─────────────────────────────────────────────────────────
# 3. JS — agregar flag land:true a P01, P04, P08
# ─────────────────────────────────────────────────────────

old_tp_array_start = """  const TP = [
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
  ];"""

new_tp_array_start = """  const TP = [
    { img:'P01.png', tier:'Starter', title:'Half-Acre Quick Calendar', desc:'The 36 plants that matter most, mapped to your zone — what to plant this month, not a 12-month manual to read first.', land:true },
    { img:'P02.png', tier:'Starter', title:'Seed Library Kit', desc:'101 heirloom varieties, illustrated and ready to print. Buy seeds once. Save them forever.' },
    { img:'P03.png', tier:'Starter', title:'Seed Library Tracker', desc:'The spreadsheet that remembers what you planted, what sprouted, and what to swap next season.' },
    { img:'P04.png', tier:'Family', title:"Family Homestead Skill Map", desc:'24 tasks sorted by age, from toddler to teen. Everyone gets a job that actually fits them.', land:true },
    { img:'P05.png', tier:'Family', title:"Kids' Roots Activity Pack", desc:'5 printable activities that turn "go play outside" into "go learn how food grows."' },
    { img:'P06.png', tier:'Homestead', title:'Half-Acre Planting Calendar', desc:'101 plants, timed to your exact zone. The full-season version of the Quick Calendar.' },
    { img:'P07.png', tier:'Homestead', title:'Homestead Preservation Log', desc:'Canning, fermenting, dehydrating, freezing — one log to track what\\'s in every jar.' },
    { img:'P08.png', tier:'Complete', title:'Master Layout', desc:'6 site plans for different lot shapes. Find the one that matches your yard and copy it.', land:true },
    { img:'P09.png', tier:'Complete', title:'First & Second Year Action Plan', desc:"52 weeks, mapped out. Never wonder what you're supposed to be doing this week." },
    { img:'P10.png', tier:'Complete', title:'Troubleshooting Field Guide', desc:'150+ evidence-based fixes for garden, soil, pests, chickens, and preservation problems.' },
    { img:'P11.png', tier:'Complete', title:'Shopping & Sourcing Guide', desc:'Real market prices, curated suppliers, and a monthly calendar so you buy at the right time.' },
  ];"""

assert old_tp_array_start in content, "BLOCK 3 (TP array) not found — aborting"
content = content.replace(old_tp_array_start, new_tp_array_start)

# ─────────────────────────────────────────────────────────
# 4. JS — tpRender aplica/quita clase tp-land según orientación
# ─────────────────────────────────────────────────────────

old_tprender = """  function tpRender() {
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
  }"""

new_tprender = """  function tpRender() {
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
    document.getElementById('tp-card-current').classList.toggle('tp-land', !!cur.land);
    document.getElementById('tp-card-prev').classList.toggle('tp-land', !!TP[prevIdx].land);
    document.getElementById('tp-card-next').classList.toggle('tp-land', !!TP[nextIdx].land);
    tpRenderDots();
  }"""

assert old_tprender in content, "BLOCK 4 (tpRender) not found — aborting"
content = content.replace(old_tprender, new_tprender)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — orientation-aware patch applied successfully")
