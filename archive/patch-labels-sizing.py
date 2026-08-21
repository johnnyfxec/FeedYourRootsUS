with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

replacements = [
    (
        ".label-gold { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; color: #E8B84B; margin-bottom: 36px; display: flex; align-items: center; justify-content: center; gap: 14px; }",
        ".label-gold { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 2.5px; color: #E8B84B; margin-bottom: 36px; display: flex; align-items: center; justify-content: center; gap: 14px; }"
    ),
    (
        ".label-green { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; color: #4A7C59; margin-bottom: 22px; display: flex; align-items: center; gap: 14px; }",
        ".label-green { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 2.5px; color: #4A7C59; margin-bottom: 22px; display: flex; align-items: center; gap: 14px; }"
    ),
    (
        ".label-terra { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 3px; color: #D4732A; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 14px; }",
        ".label-terra { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 2.5px; color: #D4732A; margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 14px; }"
    ),
]

for old, new in replacements:
    assert old in content, f"BLOCK not found: {old[:60]}... — aborting"
    content = content.replace(old, new)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — labels sizing patch applied successfully")
