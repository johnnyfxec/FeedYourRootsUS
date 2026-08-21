with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """    .chapters-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 88px; align-items: stretch; }
    .chapters-list { display: flex; flex-direction: column; justify-content: space-between; gap: 22px; }
    .chapter-row { display: flex; gap: 16px; align-items: baseline; }
    .chapter-num { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: #D4732A; flex-shrink: 0; width: 26px; }
    .chapter-outcome { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 500; color: #3A2010; line-height: 1.5; }
    .chapter-outcome-sub { font-family: 'Lora', serif; font-style: italic; font-size: 13px; color: rgba(92,58,30,0.58); line-height: 1.6; margin-top: 3px; }
    .chapters-cover { position: relative; display: flex; align-items: center; justify-content: center; }
    .chapters-cover-shadow { position: absolute; inset: 10px; background: rgba(60,30,10,0.2); border-radius: 4px 20px 20px 4px; transform: perspective(800px) rotateY(-5deg) translateX(-10px) translateY(12px); filter: blur(30px); }
    .chapters-cover img { width: 100%; max-width: 380px; border-radius: 4px 14px 14px 4px; box-shadow: -8px 6px 0 rgba(60,30,10,0.12), 0 28px 70px rgba(60,30,10,0.3); position: relative; z-index: 1; transform: perspective(1000px) rotateY(-4deg); }"""

new_css = """    .chapters-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 88px; align-items: center; }
    .chapters-list { display: flex; flex-direction: column; gap: 16px; }
    .chapter-row { display: flex; gap: 16px; align-items: baseline; }
    .chapter-num { font-family: 'Playfair Display', serif; font-size: 16px; font-weight: 700; color: #D4732A; flex-shrink: 0; width: 28px; }
    .chapter-outcome { font-family: 'DM Sans', sans-serif; font-size: 17px; font-weight: 500; color: #3A2010; line-height: 1.5; }
    .chapter-outcome-sub { font-family: 'Lora', serif; font-style: italic; font-size: 14.5px; color: rgba(92,58,30,0.58); line-height: 1.6; margin-top: 3px; }
    .chapters-cover { position: relative; display: flex; align-items: center; justify-content: center; }
    .chapters-cover-shadow { position: absolute; inset: 10px; background: rgba(60,30,10,0.2); border-radius: 4px 20px 20px 4px; transform: perspective(800px) rotateY(-5deg) translateX(-10px) translateY(12px); filter: blur(30px); }
    .chapters-cover img { width: 100%; max-width: 520px; border-radius: 4px 14px 14px 4px; box-shadow: -8px 6px 0 rgba(60,30,10,0.12), 0 28px 70px rgba(60,30,10,0.3); position: relative; z-index: 1; transform: perspective(1000px) rotateY(-4deg); }"""

assert old_css in content, "BLOCK not found — aborting"
content = content.replace(old_css, new_css)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — sizing patch applied successfully")
