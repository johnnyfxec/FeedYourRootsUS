with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. Add min-height:100vh back WITHOUT justify-content:center —
#    content stays pinned to top, section still fills the screen
# ─────────────────────────────────────────────────────────
old_hero = """    #hero {
      display: flex; flex-direction: column; align-items: center;
      padding: 28px 24px 48px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

new_hero = """    #hero {
      min-height: 100vh;
      box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center;
      padding: 28px 24px 48px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

assert old_hero in content, "BLOCK 1 (hero min-height) not found — aborting"
content = content.replace(old_hero, new_hero)

# ─────────────────────────────────────────────────────────
# 2. Reflow H1: "You Don't Need a Farm." on one line,
#    "You Need / Half an Acre / and a Plan." on the next 3
# ─────────────────────────────────────────────────────────
old_h1 = """<h1 class="hero-h1 reveal d1">You Don't Need<br>a Farm. You Need<br>Half an Acre<br>and a Plan.</h1>"""
new_h1 = """<h1 class="hero-h1 reveal d1">You Don't Need a Farm.<br>You Need<br>Half an Acre<br>and a Plan.</h1>"""
assert old_h1 in content, "BLOCK 2 (H1 reflow) not found — aborting"
content = content.replace(old_h1, new_h1)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — hero min-height + H1 reflow patch applied successfully")

# verification
print("--- VERIFICATION ---")
import re
m = re.search(r'#hero \{[^}]+\}', content)
print(m.group(0) if m else "hero block not found")
m2 = re.search(r'<h1 class="hero-h1[^>]*>.*?</h1>', content)
print(m2.group(0) if m2 else "h1 not found")
