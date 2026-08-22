with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_track = """  .fsel-tabs-track{display:flex;width:max-content;max-width:100%;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;flex-shrink:0}"""
new_track = """  .fsel-tabs-track{display:flex;width:100%;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px}"""
assert old_track in content, "BLOCK 1 (track) not found — aborting"
content = content.replace(old_track, new_track)

old_tab = """  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:0.75rem 1rem;cursor:pointer;background:transparent;transition:background .2s;width:5.25rem;flex-shrink:0}"""
new_tab = """  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:0.75rem 0.5rem;cursor:pointer;background:transparent;transition:background .2s;flex:1;min-width:0}"""
assert old_tab in content, "BLOCK 2 (tab) not found — aborting"
content = content.replace(old_tab, new_tab)

# tabs container no longer needs to scroll since all 5 fit by design
old_tabs_container = """  .fsel-tabs{display:flex;justify-content:center;margin-bottom:28px;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
  .fsel-tabs::-webkit-scrollbar{display:none}
  .fsel-tabs{padding-top:16px;margin-bottom:20px}"""
new_tabs_container = """  .fsel-tabs{display:flex;justify-content:center;padding-top:16px;margin-bottom:20px}"""
if old_tabs_container in content:
    content = content.replace(old_tabs_container, new_tabs_container)
    print("merged tabs container rule")
else:
    print("tabs container merge pattern not found — leaving as-is, checking separately")

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — tabs fit-all patch applied")
