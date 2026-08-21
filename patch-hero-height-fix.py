with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# Remove min-height:100vh (was causing oversized section + botanicals
# positioned via bottom-% to float in wrong place). Use a fixed generous
# padding-bottom instead — enough to push Problem below the fold on
# typical screens, without creating leftover empty space when content
# is short.
old_hero = """    #hero {
      min-height: 100vh;
      box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center;
      padding: 28px 24px 48px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

new_hero = """    #hero {
      box-sizing: border-box;
      display: flex; flex-direction: column; align-items: center;
      padding: 28px 24px 96px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

assert old_hero in content, "BLOCK 1 (hero) not found — aborting"
content = content.replace(old_hero, new_hero)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — hero height fix applied successfully")
