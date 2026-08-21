with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_480 = """    .fsel-tabs{gap:5px}
    .fsel-tab{min-width:calc(33.3% - 7px);padding:9px 8px}
    .fsel-tn{font-size:9px}
    .fsel-tp{font-size:17px}"""

new_480 = """    .fsel-tabs{gap:4px;margin-bottom:16px}
    .fsel-tab{min-width:calc(20% - 4px);padding:7px 4px}
    .fsel-tn{font-size:7.5px}
    .fsel-tp{font-size:14px}"""

assert old_480 in content, "BLOCK 1 (480px tabs) not found — aborting"
content = content.replace(old_480, new_480)

old_bh = """      .bundles-header { margin-bottom: 36px; }"""
new_bh = """      .bundles-header { margin-bottom: 24px; }"""
assert old_bh in content, "BLOCK 2 (bundles-header) not found — aborting"
content = content.replace(old_bh, new_bh)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — tab compaction patch applied successfully")
