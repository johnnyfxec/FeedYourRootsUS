with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """    .tp-card { position: absolute; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.35); transition: all 0.5s cubic-bezier(0.22,1,0.36,1); background: #FDFAF2; display: flex; align-items: center; justify-content: center; }"""

new_css = """    .tp-card { position: absolute; border-radius: 18px; overflow: hidden; box-shadow: 0 30px 80px rgba(60,30,10,0.35); transition: transform 0.5s cubic-bezier(0.22,1,0.36,1), opacity 0.5s cubic-bezier(0.22,1,0.36,1); background: #FDFAF2; display: flex; align-items: center; justify-content: center; }"""

assert old_css in content, "BLOCK not found — aborting"
content = content.replace(old_css, new_css)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — transition fix applied successfully")
