import subprocess, re, glob, os

def git_mv(src, dst):
    if not os.path.exists(src):
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    result = subprocess.run(['git', 'mv', src, dst], capture_output=True, text=True)
    if result.returncode != 0:
        os.rename(src, dst)
    return True

print("=== MOVING BUILD FILES ===")
for src in ['shared.css', '_nav.html', '_footer.html', 'build.py']:
    if os.path.exists(src):
        git_mv(src, f'build/{src}')
        print(f"  {src} -> build/{src}")
    else:
        print(f"  already moved or missing: {src}")

os.makedirs('build/src', exist_ok=True)
for src in ['src/about.html', 'src/privacy.html', 'src/terms.html', 'src/refunds.html']:
    if os.path.exists(src):
        git_mv(src, f'build/{src}')
        print(f"  {src} -> build/{src}")
    else:
        print(f"  already moved or missing: {src}")

print("\n=== MOVING PATCH SCRIPTS TO archive/ ===")
os.makedirs('archive', exist_ok=True)
patch_scripts = glob.glob('patch-*.py')
for p in patch_scripts:
    git_mv(p, f'archive/{p}')
print(f"  Moved {len(patch_scripts)} patch scripts -> archive/")

print("\n=== REWRITING HTML REFERENCES ===")
moves = {}
for i in range(1, 31):
    fn = f'E{i:02d}.png'
    moves[fn] = f'assets/botanicals/{fn}'
for fn in ['cover.png', 'backcover.png'] + [f'P{i:02d}.png' for i in range(1, 12)]:
    moves[fn] = f'assets/covers/{fn}'
for fn in ['about-banner.png', 'legal-banner.png', 'bannerfyr.png', 'botoncta.png', 'footerfyr.png']:
    moves[fn] = f'assets/banners/{fn}'
moves['FYR-logo-forest-500px.png'] = 'assets/brand/FYR-logo-forest-500px.png'
for fn in ['vision-abundance.png', 'vision-flock.png', 'vision-greenhouse.png',
           'vision-january.png', 'vision-legacy.png', 'vision-roots.png']:
    moves[fn] = f'assets/vision/{fn}'

html_files = ['index.html', 'about.html', 'privacy.html', 'terms.html', 'refunds.html']

for hf in html_files:
    if not os.path.exists(hf):
        print(f"  {hf}: NOT FOUND, skipping")
        continue
    with open(hf, encoding='utf-8') as f:
        content = f.read()
    orig = content
    replacements = 0
    for old_name, new_path in moves.items():
        pattern = re.compile(r'(?<!assets/botanicals/)(?<!assets/covers/)(?<!assets/banners/)(?<!assets/brand/)(?<!assets/vision/)\b' + re.escape(old_name) + r'\b')
        new_content, n = pattern.subn(new_path, content)
        if n > 0:
            content = new_content
            replacements += n
    if content != orig:
        with open(hf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  {hf}: {replacements} references updated")
    else:
        print(f"  {hf}: no changes needed (already updated or nothing found)")

print("\n=== FIXING JS DYNAMIC PATHS (index.html) ===")
if os.path.exists('index.html'):
    with open('index.html', encoding='utf-8') as f:
        content = f.read()
    old_js = "img.src = pickRandom() + '.png';"
    new_js = "img.src = 'assets/botanicals/' + pickRandom() + '.png';"
    count = content.count(old_js)
    if count > 0:
        content = content.replace(old_js, new_js)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed {count} occurrence(s)")
    else:
        print("  Already fixed or pattern not found")

print("\nDone.")
