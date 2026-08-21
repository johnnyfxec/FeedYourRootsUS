import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

def px_to_rem(match):
    px_value = float(match.group(1))
    rem_value = px_value / 16
    rem_str = f"{rem_value:.4f}".rstrip('0').rstrip('.')
    return f"{rem_str}rem"

# This time: zero or more spaces after the colon (covers the compact
# inline <style> block used for the bundle selector, e.g. font-size:9px)
pattern = re.compile(r'(?<=font-size:)\s*(\d+(?:\.\d+)?)px')
content, count = pattern.subn(lambda m: (' ' if m.group(0).startswith(' ') else '') + px_to_rem(m), content)

print(f"Converted {count} additional font-size:Npx rules (compact syntax)")

if content == orig:
    print("NO CHANGES APPLIED")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — pass 2 applied")
