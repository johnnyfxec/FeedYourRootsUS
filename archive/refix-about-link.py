with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_nav = '<a href="/about" onclick="return false;">About</a>'
new_nav = '<a href="about.html">About</a>'
assert old_nav in content, "BLOCK 1 (nav link) not found — aborting"
content = content.replace(old_nav, new_nav)

old_overlay = '<a href="/about" onclick="closeNavOverlay(); return false;">About<span class="nav-overlay-soon">Coming Soon</span></a>'
new_overlay = '<a href="about.html" onclick="closeNavOverlay()">About</a>'
assert old_overlay in content, "BLOCK 2 (overlay link) not found — aborting"
content = content.replace(old_overlay, new_overlay)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — about link re-fixed")
