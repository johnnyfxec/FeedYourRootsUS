with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_mobile = """    .fsel-inner{flex-direction:column}"""
new_mobile = """    .fsel-inner{flex-direction:column;gap:12px}
    .fsel-dsc{margin-bottom:0}"""

assert old_mobile in content, "BLOCK not found — aborting"
content = content.replace(old_mobile, new_mobile)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — mobile gap reduction applied")
