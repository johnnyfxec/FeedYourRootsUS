with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_desktop = "      padding: 100px 24px 40px;"
new_desktop = "      padding: 24px 24px 40px;"
assert old_desktop in content, "BLOCK 1 (desktop padding) not found — aborting"
content = content.replace(old_desktop, new_desktop)

old_tablet = "      #hero { padding-top: 64px; padding-bottom: 64px; }"
new_tablet = "      #hero { padding-top: 16px; padding-bottom: 40px; }"
assert old_tablet in content, "BLOCK 2 (tablet padding) not found — aborting"
content = content.replace(old_tablet, new_tablet)

old_mobile = "      #hero { padding: 32px 20px; }"
new_mobile = "      #hero { padding: 16px 20px 24px; }"
assert old_mobile in content, "BLOCK 3 (mobile padding) not found — aborting"
content = content.replace(old_mobile, new_mobile)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — hero top padding patch applied successfully")
