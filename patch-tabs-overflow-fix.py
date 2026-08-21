with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """  .fsel-tabs-track{display:flex;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;overflow:hidden;flex-shrink:0}
  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:12px 18px;cursor:pointer;background:transparent;transition:background .2s;min-width:84px;text-align:center;flex-shrink:0}"""

new_css = """  .fsel-tabs{padding-top:16px}
  .fsel-tabs-track{display:flex;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;flex-shrink:0}
  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:12px 18px;cursor:pointer;background:transparent;transition:background .2s;min-width:84px;text-align:center;flex-shrink:0}
  .fsel-tab:first-child{border-radius:14px 0 0 14px}
  .fsel-tab:last-child{border-radius:0 14px 14px 0}"""

assert old_css in content, "BLOCK 1 (tabs CSS) not found — aborting"
content = content.replace(old_css, new_css)

if content == orig:
    print("NO CHANGES APPLIED — check block")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — tabs overflow fix applied")
