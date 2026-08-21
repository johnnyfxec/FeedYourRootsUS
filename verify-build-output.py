import re

files = ['about.html', 'privacy.html', 'terms.html', 'refunds.html']
bare_pattern = re.compile(r'(?<!assets/botanicals/)(?<!assets/covers/)(?<!assets/banners/)(?<!assets/brand/)(?<!assets/vision/)\b(E\d{2}|cover|backcover|P\d{2}|about-banner|legal-banner|FYR-logo-forest-500px)\.png\b')

print("=== Checking built pages for bare/broken image refs ===")
for f in files:
    with open(f, encoding='utf-8') as fh:
        content = fh.read()
    matches = bare_pattern.findall(content)
    print(f"  {f}: {'CLEAN' if not matches else 'ISSUE: ' + str(set(matches))}")

print("\n=== Checking shared.css link resolves (file exists at root) ===")
import os
print("  shared.css exists at root:", os.path.exists('shared.css'))

print("\n=== Checking nav-active marking ===")
with open('about.html', encoding='utf-8') as f:
    print("  about.html has nav-active on About link:", 'class="nav-active"' in f.read())
