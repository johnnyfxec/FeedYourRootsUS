with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_hero = """    #hero {
      min-height: 100vh;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 24px 24px 40px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

new_hero = """    #hero {
      display: flex; flex-direction: column; align-items: center;
      padding: 28px 24px 48px;
      overflow: hidden;
      background: radial-gradient(ellipse at 20% 15%, rgba(255,248,235,0.85) 0%, transparent 48%),
                  radial-gradient(ellipse at 80% 85%, rgba(220,195,145,0.4) 0%, transparent 48%);
    }"""

assert old_hero in content, "BLOCK 1 (hero base) not found — aborting"
content = content.replace(old_hero, new_hero)

old_tablet = "      #hero { padding-top: 16px; padding-bottom: 40px; }"
new_tablet = "      #hero { padding-top: 20px; padding-bottom: 40px; }"
assert old_tablet in content, "BLOCK 2 (tablet) not found — aborting"
content = content.replace(old_tablet, new_tablet)

old_mobile = "      #hero { padding: 16px 20px 24px; }"
new_mobile = "      #hero { padding: 16px 20px 28px; }"
assert old_mobile in content, "BLOCK 3 (mobile) not found — aborting"
content = content.replace(old_mobile, new_mobile)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — hero flow layout patch applied successfully")
