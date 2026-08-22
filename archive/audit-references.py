import re, glob

files_to_move = {
    'botanicals': [f'E{i:02d}.png' for i in range(1, 31)],
    'covers': ['cover.png', 'backcover.png'] + [f'P{i:02d}.png' for i in range(1, 12)],
    'banners': ['about-banner.png', 'legal-banner.png', 'bannerfyr.png', 'botoncta.png', 'footerfyr.png'],
    'brand': ['FYR-logo-forest-500px.png'],
    'vision': ['vision-abundance.png', 'vision-flock.png', 'vision-greenhouse.png', 'vision-january.png', 'vision-legacy.png', 'vision-roots.png'],
}

html_files = glob.glob('*.html')
print(f"Scanning: {html_files}\n")

for category, filenames in files_to_move.items():
    print(f"=== {category}/ ===")
    for fname in filenames:
        total = 0
        locations = []
        for hf in html_files:
            with open(hf, encoding='utf-8') as f:
                content = f.read()
            count = content.count(fname)
            if count > 0:
                total += count
                locations.append(f"{hf}:{count}")
        if total > 0:
            print(f"  {fname}: {total} refs -> {', '.join(locations)}")
        else:
            print(f"  {fname}: NOT FOUND (ok if unused)")
    print()
