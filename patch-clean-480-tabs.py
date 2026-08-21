with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old = """    .fsel-tabs{justify-content:flex-start;margin-bottom:16px}
    .fsel-tab{min-width:64px;padding:8px 10px}"""
new = """    .fsel-tabs{margin-bottom:16px}
    .fsel-tab{padding:0.6rem 0.3rem}"""

assert old in content, "BLOCK not found — aborting"
content = content.replace(old, new)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — cleaned obsolete 480px overrides")
