import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_960_block = """    @media (max-width: 960px) {
      .hero-inner { grid-template-columns: 1fr; gap: 52px; text-align: center; }
      .hero-book { order: -1; }
      .hero-book img { max-width: 280px; }
      .hero-bot { display: none; }
      .bot-break { display: block; }
      .label-green { justify-content: center; }
      .label-green::before { content: ''; width: 44px; height: 1px; background: #4A7C59; opacity: 0.4; display: block; }
      .solution-inner { grid-template-columns: 1fr; gap: 52px; }
      .solution-pages { height: 320px; }
      .page-1 { width: 178px; height: 226px; }
      .page-2 { width: 178px; height: 226px; }
      .page-3 { width: 162px; height: 205px; }
      .vision-grid { grid-template-columns: 1fr 1fr; }
      .chapters-grid { grid-template-columns: 1fr 1fr; }
      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
    }
    @media (max-width: 600px) {
      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .chapters-grid, .bundles-grid { grid-template-columns: 1fr; }
      .chapter-card { flex-direction: column; }
      .float-el { display: none; }
      .bot-break { display: block; }
    }"""

new_960_block = """    @media (max-width: 960px) {
      .hero-inner { grid-template-columns: 1fr; gap: 52px; text-align: center; }
      .hero-book { order: -1; }
      .hero-book img { max-width: 280px; }
      .hero-bot { display: none; }
      .bot-break { display: block; }
      .label-green { justify-content: center; }
      .label-green::before { content: ''; width: 44px; height: 1px; background: #4A7C59; opacity: 0.4; display: block; }
      .solution-inner { grid-template-columns: 1fr; gap: 52px; }
      .solution-pages { height: 320px; }
      .page-1 { width: 178px; height: 226px; }
      .page-2 { width: 178px; height: 226px; }
      .page-3 { width: 162px; height: 205px; }
      .vision-grid { grid-template-columns: 1fr 1fr; }
      .chapters-grid { grid-template-columns: 1fr 1fr; }
      .bundles-grid { grid-template-columns: 1fr 1fr; }
      .bundle-card.popular { transform: none; }
      .float-el { display: none; }
    }
    @media (max-width: 600px) {
      #hero { padding: 50px 20px 30px; }
      #solution,#chapters,#close { padding: 40px 20px; }
      #problem,#vision,#bundles { padding: 44px 20px; }
      .vision-grid, .chapters-grid, .bundles-grid { grid-template-columns: 1fr; }
      .chapter-card { flex-direction: column; }
      .bot-break { display: block; }
    }"""

assert old_960_block in content, "BLOCK 1 (media queries) not found — aborting"
content = content.replace(old_960_block, new_960_block)

old_js = """  document.querySelectorAll('.bot-break img').forEach(img => {
    img.src = pickRandom() + '.png';
  });"""

new_js = """  document.querySelectorAll('.bot-break img').forEach(img => {
    img.src = pickRandom() + '.png';
  });
  // ALEATORIZAR FLOAT DECORATIONS DESKTOP (excluye cover/backcover, que no son .float-el)
  document.querySelectorAll('.float-el').forEach(img => {
    img.src = pickRandom() + '.png';
  });"""

assert old_js in content, "BLOCK 2 (pickRandom JS) not found — aborting"
content = content.replace(old_js, new_js)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — patch applied successfully")
