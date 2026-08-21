import os, re

BUILD_DIR = 'build'
SRC_DIR = os.path.join(BUILD_DIR, 'src')

# ─────────────────────────────────────────────────────────
# 1. Fix asset paths inside the 4 source HTML files
# ─────────────────────────────────────────────────────────
moves = {}
moves['about-banner.png'] = 'assets/banners/about-banner.png'
moves['legal-banner.png'] = 'assets/banners/legal-banner.png'
moves['FYR-logo-forest-500px.png'] = 'assets/brand/FYR-logo-forest-500px.png'
for i in range(1, 31):
    fn = f'E{i:02d}.png'
    moves[fn] = f'assets/botanicals/{fn}'

print("=== FIXING ASSET PATHS IN build/src/*.html ===")
for fname in ['about.html', 'privacy.html', 'terms.html', 'refunds.html']:
    path = os.path.join(SRC_DIR, fname)
    if not os.path.exists(path):
        print(f"  {fname}: NOT FOUND, skipping")
        continue
    with open(path, encoding='utf-8') as f:
        content = f.read()
    orig = content
    n_total = 0
    for old_name, new_path in moves.items():
        pattern = re.compile(r'(?<!assets/botanicals/)(?<!assets/banners/)(?<!assets/brand/)\b' + re.escape(old_name) + r'\b')
        content, n = pattern.subn(new_path, content)
        n_total += n
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {fname}: {n_total} references fixed")
    else:
        print(f"  {fname}: no changes needed")

# ─────────────────────────────────────────────────────────
# 2. Fix build.py so it knows it now lives in build/,
#    but must write final HTML to the repo root (one level up)
# ─────────────────────────────────────────────────────────
print("\n=== FIXING build/build.py OUTPUT PATH ===")
build_py_path = os.path.join(BUILD_DIR, 'build.py')
with open(build_py_path, encoding='utf-8') as f:
    content = f.read()

old_paths = '''BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BUILD_DIR, "src")
OUT_DIR = BUILD_DIR  # final files go straight into the repo root'''

new_paths = '''BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BUILD_DIR, "src")
OUT_DIR = os.path.dirname(BUILD_DIR)  # repo root — one level up from build/'''

if old_paths in content:
    content = content.replace(old_paths, new_paths)
    with open(build_py_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  OK — OUT_DIR now points to repo root (one level up from build/)")
else:
    print("  Pattern not found — build.py may already be correct, check manually")

# Also fix shared.css and FYR-logo reference inside _nav.html
# (shared.css link and logo src need to be relative to repo root,
#  since the FINAL about.html/privacy.html/etc. live in the root,
#  not in build/)
print("\n=== VERIFYING _nav.html and src files reference shared.css correctly ===")
nav_path = os.path.join(BUILD_DIR, '_nav.html')
with open(nav_path, encoding='utf-8') as f:
    nav_content = f.read()
if 'assets/brand/FYR-logo-forest-500px.png' in nav_content:
    print("  _nav.html: logo path OK")
else:
    old_logo = 'src="FYR-logo-forest-500px.png"'
    new_logo = 'src="assets/brand/FYR-logo-forest-500px.png"'
    if old_logo in nav_content:
        nav_content = nav_content.replace(old_logo, new_logo)
        with open(nav_path, 'w', encoding='utf-8') as f:
            f.write(nav_content)
        print("  _nav.html: logo path fixed")
    else:
        print("  _nav.html: logo reference not found in expected format, check manually")

for fname in ['about.html', 'privacy.html', 'terms.html', 'refunds.html']:
    path = os.path.join(SRC_DIR, fname)
    if not os.path.exists(path):
        continue
    with open(path, encoding='utf-8') as f:
        c = f.read()
    has_shared_css = 'href="shared.css"' in c
    print(f"  {fname}: shared.css link present = {has_shared_css} (this is correct — final file will be in repo root alongside shared.css)")

print("\nDone. Now run: cd build && python3 build.py && cd ..")
