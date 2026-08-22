with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_vision = """    #vision {
      background: #385F42;
      padding: 100px 40px;
      border-radius: 32px;
      margin: 0 16px;
      box-shadow: 0 32px 80px rgba(30,60,35,0.28);
      overflow: hidden;
    }"""

new_vision = """    #vision {
      background: #385F42;
      padding: 100px 40px;
      border-radius: 32px;
      margin: 0 16px 64px;
      box-shadow: 0 32px 80px rgba(30,60,35,0.28);
      overflow: hidden;
    }"""

assert old_vision in content, "BLOCK not found — aborting"
content = content.replace(old_vision, new_vision)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — vision-bundles gap patch applied successfully")
