import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

def px_to_rem(match):
    px_value = float(match.group(1))
    rem_value = px_value / 16
    # format cleanly: strip trailing zeros but keep precision
    rem_str = f"{rem_value:.4f}".rstrip('0').rstrip('.')
    return f"{rem_str}rem"

# Convert font-size: Npx -> Nrem (handles decimals like 14.5px too)
pattern = re.compile(r'(?<=font-size:\s)(\d+(?:\.\d+)?)px')
content, count_fs = pattern.subn(px_to_rem, content)

# Convert px values inside clamp() calls used for font-size specifically.
# We target the two known clamp(...) forms used for font-size in this file:
# e.g. clamp(38px, 5.5vw, 66px) when preceded by "font-size:"
def clamp_px_to_rem(match):
    prefix = match.group(1)
    a = float(match.group(2)) / 16
    mid = match.group(3)
    b = float(match.group(4)) / 16
    a_str = f"{a:.4f}".rstrip('0').rstrip('.')
    b_str = f"{b:.4f}".rstrip('0').rstrip('.')
    return f"{prefix}clamp({a_str}rem, {mid}, {b_str}rem)"

clamp_pattern = re.compile(r'(font-size:\s*)clamp\((\d+(?:\.\d+)?)px,\s*([^,]+),\s*(\d+(?:\.\d+)?)px\)')
content, count_clamp = clamp_pattern.subn(clamp_px_to_rem, content)

print(f"Converted {count_fs} plain font-size:Npx rules")
print(f"Converted {count_clamp} font-size:clamp(...) rules")

if content == orig:
    print("NO CHANGES APPLIED")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — index.html font-size px-to-rem conversion applied")
