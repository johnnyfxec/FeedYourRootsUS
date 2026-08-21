with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """    /* ── PAGE BANNER ── */
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

new_css = """    /* ── PAGE BANNER ── */
    .page-banner { width: 100%; display: flex; justify-content: center; padding: 32px 24px 0; }
    .page-banner-inner { width: 100%; max-width: 1020px; aspect-ratio: 21/9; overflow: hidden; border-radius: 18px; box-shadow: 0 20px 60px rgba(60,30,10,0.22); }
    .page-banner-inner img { width: 100%; height: 100%; object-fit: cover; display: block; }
    @media (max-width: 720px) {
      .page-banner { padding: 20px 16px 0; }
      .page-banner-inner { border-radius: 12px; }
    }

    /* ── DOC LAYOUT ── */
    #doc { padding: 36px 24px 100px; overflow: hidden; }
    @media (max-width: 720px) {
      #doc { padding: 20px 24px 72px; }
    }"""

assert old_css in content, "BLOCK 1 (banner CSS) not found — aborting"
content = content.replace(old_css, new_css)

old_html = """<div class="page-banner">
  <img src="about-banner.png" alt="An aerial illustration of a suburban street where one backyard has been transformed into a small homestead">
</div>"""

new_html = """<div class="page-banner">
  <div class="page-banner-inner">
    <img src="about-banner.png" alt="An aerial illustration of a suburban street where one backyard has been transformed into a small homestead">
  </div>
</div>"""

assert old_html in content, "BLOCK 2 (banner HTML) not found — aborting"
content = content.replace(old_html, new_html)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — banner width patch applied successfully")
