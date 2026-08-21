with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content
changes = []

replacements = [
    (".btn-micro { display: block; margin-top: 14px; font-family: 'DM Sans', sans-serif; font-size: 12px; color: #4A7C59; letter-spacing: 0.5px; }",
     ".btn-micro { display: block; margin-top: 14px; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #4A7C59; letter-spacing: 0.5px; }"),

    (".vision-card-hint { font-family: 'DM Sans', sans-serif; font-size: 9px; color: rgba(245,236,215,0.4); letter-spacing: 1px; }",
     ".vision-card-hint { font-family: 'DM Sans', sans-serif; font-size: 12px; color: rgba(245,236,215,0.4); letter-spacing: 1px; }"),

    (".lightbox-caption-label { font-family: 'DM Sans', sans-serif; font-size: 10px; color: #E8B84B; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px; }",
     ".lightbox-caption-label { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #E8B84B; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 6px; }"),

    (".bundle-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #E8B84B; color: #5C3A1E; font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; }",
     ".bundle-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #E8B84B; color: #5C3A1E; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; }"),

    (".bundle-soon-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: rgba(74,124,89,0.28); color: rgba(245,236,215,0.88); font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; border: 1px solid rgba(245,236,215,0.18); }",
     ".bundle-soon-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: rgba(74,124,89,0.28); color: rgba(245,236,215,0.88); font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; padding: 7px 18px; border-radius: 50px; white-space: nowrap; border: 1px solid rgba(245,236,215,0.18); }"),

    (".bundle-tier { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; color: #4A7C59; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }",
     ".bundle-tier { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #4A7C59; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }"),

    (".bundle-desc { font-family: 'Lora', serif; font-size: 13.5px; color: #6B4226; line-height: 1.8; margin-bottom: 26px; min-height: 95px; }",
     ".bundle-desc { font-family: 'Lora', serif; font-size: 16px; color: #6B4226; line-height: 1.8; margin-bottom: 26px; min-height: 95px; }"),

    (".btn-bundle-soon { display: block; text-align: center; background: rgba(74,124,89,0.1); color: rgba(92,58,30,0.38); font-family: 'DM Sans', sans-serif; font-size: 13px; padding: 15px 20px; border-radius: 50px; border: 1px solid rgba(74,124,89,0.18); cursor: default; }",
     ".btn-bundle-soon { display: block; text-align: center; background: rgba(74,124,89,0.1); color: rgba(92,58,30,0.38); font-family: 'DM Sans', sans-serif; font-size: 16px; padding: 15px 20px; border-radius: 50px; border: 1px solid rgba(74,124,89,0.18); cursor: default; }"),

    (".close-attr { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #D4732A; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 64px; }",
     ".close-attr { font-family: 'DM Sans', sans-serif; font-size: 15px; color: #D4732A; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 64px; display: flex; align-items: center; justify-content: center; gap: 14px; }\n    .close-attr::after { content: ''; width: 44px; height: 1px; background: #D4732A; opacity: 0.4; display: block; }"),

    (".footer-tagline { font-family: 'Lora', serif; font-style: italic; font-size: 14px; color: rgba(245,236,215,0.48); margin-bottom: 34px; }",
     ".footer-tagline { font-family: 'Lora', serif; font-style: italic; font-size: 20px; color: rgba(245,236,215,0.48); margin-bottom: 34px; }"),

    (".footer-links a { font-family: 'DM Sans', sans-serif; font-size: 13px; color: rgba(245,236,215,0.44); letter-spacing: 0.3px; transition: color 0.2s; }",
     ".footer-links a { font-family: 'DM Sans', sans-serif; font-size: 16px; color: rgba(245,236,215,0.44); letter-spacing: 0.3px; transition: color 0.2s; }"),

    (".footer-domain { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #4A7C59; letter-spacing: 0.5px; margin-bottom: 6px; }",
     ".footer-domain { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #4A7C59; letter-spacing: 0.5px; margin-bottom: 6px; }"),

    (".footer-copy { font-family: 'DM Sans', sans-serif; font-size: 11px; color: rgba(245,236,215,0.2); }",
     ".footer-copy { font-family: 'DM Sans', sans-serif; font-size: 13px; color: rgba(245,236,215,0.2); }"),

    (".nav-links a { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #5C3A1E; letter-spacing: 0.3px; transition: color 0.2s; }",
     ".nav-links a { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 500; color: #5C3A1E; letter-spacing: 0.3px; transition: color 0.2s; }"),

    (".nav-cta { display: inline-block; background: #D4732A; color: #fff !important; font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 13px; padding: 11px 24px; border-radius: 50px; letter-spacing: 0.3px; transition: all 0.3s ease; }",
     ".nav-cta { display: inline-block; background: #D4732A; color: #fff !important; font-family: 'DM Sans', sans-serif; font-weight: 500; font-size: 15px; padding: 11px 24px; border-radius: 50px; letter-spacing: 0.3px; transition: all 0.3s ease; }"),

    (".nav-overlay-soon { font-family: 'DM Sans', sans-serif; font-size: 11px; color: rgba(245,236,215,0.4); letter-spacing: 1px; text-transform: uppercase; display: block; margin-top: 6px; }",
     ".nav-overlay-soon { font-family: 'DM Sans', sans-serif; font-size: 13px; color: rgba(245,236,215,0.4); letter-spacing: 1px; text-transform: uppercase; display: block; margin-top: 6px; }"),

    (".tp-tier { display: inline-block; font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; color: #4A7C59; background: rgba(74,124,89,0.1); border: 1px solid rgba(74,124,89,0.25); padding: 5px 14px; border-radius: 20px; margin-bottom: 14px; }",
     ".tp-tier { display: inline-block; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 1.5px; color: #4A7C59; background: rgba(74,124,89,0.1); border: 1px solid rgba(74,124,89,0.25); padding: 5px 14px; border-radius: 20px; margin-bottom: 14px; }"),

    (".vision-card-num { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 500; color: #E8B84B; text-transform: uppercase; letter-spacing: 2.5px; background: rgba(0,0,0,0.55); padding: 4px 10px; border-radius: 20px; display: inline-block; backdrop-filter: blur(4px); transition: opacity 0.3s; align-self: flex-start; width: fit-content; }",
     ".vision-card-num { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #E8B84B; text-transform: uppercase; letter-spacing: 2.5px; background: rgba(0,0,0,0.55); padding: 4px 10px; border-radius: 20px; display: inline-block; backdrop-filter: blur(4px); transition: opacity 0.3s; align-self: flex-start; width: fit-content; }"),
]

for old, new in replacements:
    assert old in content, f"NOT FOUND: {old[:70]}..."
    content = content.replace(old, new)
    changes.append(old[:50])

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK — {len(changes)} font-size rules updated successfully")
