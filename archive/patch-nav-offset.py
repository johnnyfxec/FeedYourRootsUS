with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_body = "body { font-family: 'Lora', Georgia, serif; background: #F5ECD7; color: #5C3A1E; overflow-x: hidden; }"
new_body = "body { font-family: 'Lora', Georgia, serif; background: #F5ECD7; color: #5C3A1E; overflow-x: hidden; padding-top: 70px; }"

assert old_body in content, "BLOCK 1 (body) not found — aborting"
content = content.replace(old_body, new_body)

old_mq = "      #site-nav { padding: 16px 20px; }"
new_mq = "      #site-nav { padding: 16px 20px; }\n      body { padding-top: 66px; }"

assert old_mq in content, "BLOCK 2 (mobile media query) not found — aborting"
content = content.replace(old_mq, new_mq)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — nav offset patch applied successfully")
