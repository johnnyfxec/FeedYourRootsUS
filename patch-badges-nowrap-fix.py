with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old1 = """    .bundle-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #E8B84B; color: #5C3A1E; font-family: 'DM Sans', sans-serif; font-size: 0.8125rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; }"""
new1 = """    .bundle-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #E8B84B; color: #5C3A1E; font-family: 'DM Sans', sans-serif; font-size: 0.8125rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; max-width: 90vw; text-align: center; }"""
assert old1 in content, "BLOCK 1 not found — aborting"
content = content.replace(old1, new1)

old2 = """    .bundle-soon-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: rgba(74,124,89,0.28); color: rgba(245,236,215,0.88); font-family: 'DM Sans', sans-serif; font-size: 0.8125rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; border: 1px solid rgba(245,236,215,0.18); }"""
new2 = """    .bundle-soon-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: rgba(74,124,89,0.28); color: rgba(245,236,215,0.88); font-family: 'DM Sans', sans-serif; font-size: 0.8125rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; max-width: 90vw; text-align: center; border: 1px solid rgba(245,236,215,0.18); }"""
assert old2 in content, "BLOCK 2 not found — aborting"
content = content.replace(old2, new2)

old3 = """  .fsel-tb{position:absolute;top:-11px;left:50%;transform:translateX(-50%);font-size:0.5625rem;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap;letter-spacing:.05em;font-family:'DM Sans',sans-serif;pointer-events:none}"""
new3 = """  .fsel-tb{position:absolute;top:-11px;left:50%;transform:translateX(-50%);font-size:0.5625rem;font-weight:700;padding:2px 8px;border-radius:20px;max-width:85vw;text-align:center;letter-spacing:.05em;font-family:'DM Sans',sans-serif;pointer-events:none}"""
assert old3 in content, "BLOCK 3 not found — aborting"
content = content.replace(old3, new3)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — badge nowrap fix applied")
