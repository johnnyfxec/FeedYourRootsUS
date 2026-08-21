with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_keyframes = """    @keyframes tpFlipNext {
      0% { transform: scale(1) translateX(0) rotateY(0deg); }
      50% { transform: scale(0.94) translateX(-6%) rotateY(-14deg); opacity: 0.7; }
      100% { transform: scale(1) translateX(0) rotateY(0deg); }
    }
    @keyframes tpFlipPrev {
      0% { transform: scale(1) translateX(0) rotateY(0deg); }
      50% { transform: scale(0.94) translateX(6%) rotateY(14deg); opacity: 0.7; }
      100% { transform: scale(1) translateX(0) rotateY(0deg); }
    }"""

new_keyframes = """    @keyframes tpFlipNext {
      0% { transform: scale(0.94) translateX(10%) rotateY(-18deg); opacity: 0.4; }
      100% { transform: scale(1) translateX(0) rotateY(0deg); opacity: 1; }
    }
    @keyframes tpFlipPrev {
      0% { transform: scale(0.94) translateX(-10%) rotateY(18deg); opacity: 0.4; }
      100% { transform: scale(1) translateX(0) rotateY(0deg); opacity: 1; }
    }"""

assert old_keyframes in content, "BLOCK not found — aborting"
content = content.replace(old_keyframes, new_keyframes)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — flip direction patch applied successfully")
