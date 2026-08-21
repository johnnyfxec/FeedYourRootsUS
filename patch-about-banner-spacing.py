with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """    /* ── PAGE BANNER ── */
    .page-banner { width: 100%; aspect-ratio: 21/9; overflow: hidden; margin-top: -1px; }
    .page-banner img { width: 100%; height: 100%; object-fit: cover; display: block; }

    /* ── DOC LAYOUT ── */
    #doc { padding: 72px 24px 100px; overflow: hidden; }"""

new_css = """    /* ── PAGE BANNER ── */
    .page-banner { width: 100%; aspect-ratio: 21/9; max-height: 340px; overflow: hidden; margin-top: -1px; }
    .page-banner img { width: 100%; height: 100%; object-fit: cover; object-position: center 60%; display: block; }
    @media (max-width: 720px) {
      .page-banner { max-height: none; }
    }

    /* ── DOC LAYOUT ── */
    #doc { padding: 36px 24px 100px; overflow: hidden; }
    @media (max-width: 720px) {
      #doc { padding: 20px 24px 72px; }
    }"""

assert old_css in content, "BLOCK not found — aborting"
content = content.replace(old_css, new_css)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — banner/spacing patch applied successfully")
