import re, glob

html_files = ['index.html', 'about.html', 'privacy.html', 'terms.html', 'refunds.html']

print("=== Checking for any bare (unprefixed) references left ===")
bare_pattern = re.compile(r'(?<!assets/botanicals/)(?<!assets/covers/)(?<!assets/banners/)(?<!assets/brand/)(?<!assets/vision/)\b(E\d{2}|cover|backcover|P\d{2}|about-banner|legal-banner|bannerfyr|botoncta|footerfyr|FYR-logo-forest-500px|vision-[a-z]+)\.png\b')

any_issues = False
for hf in html_files:
    with open(hf, encoding='utf-8') as f:
        content = f.read()
    matches = bare_pattern.findall(content)
    if matches:
        any_issues = True
        print(f"  {hf}: POSSIBLE ISSUE — bare refs found: {set(matches)}")
    else:
        print(f"  {hf}: clean")

print("\n=== Confirming About nav link still intact ===")
with open('index.html', encoding='utf-8') as f:
    idx = f.read()
print("  about.html link present:", 'href="about.html"' in idx)
print("  broken /about link present:", 'href="/about"' in idx)

print("\n=== Sample of rewritten paths (first 3 img tags in index.html) ===")
imgs = re.findall(r'src="(assets/[^"]+)"', idx)
for i in imgs[:5]:
    print(" ", i)

print("\n", "CLEAN — no bare references found" if not any_issues else "ISSUES FOUND — review above")
