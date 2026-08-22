with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ─────────────────────────────────────────────────────────
# 1. Fixed rem-based width for ribbon so it never overflows/clips oddly
# ─────────────────────────────────────────────────────────
old_track = """  .fsel-tabs-track{display:flex;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;flex-shrink:0}"""
new_track = """  .fsel-tabs-track{display:flex;width:max-content;max-width:100%;border:1.5px solid rgba(245,236,215,0.18);border-radius:16px;flex-shrink:0}"""
assert old_track in content, "BLOCK 1 (track) not found — aborting"
content = content.replace(old_track, new_track)

old_tab = """  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:12px 18px;cursor:pointer;background:transparent;transition:background .2s;min-width:84px;text-align:center;flex-shrink:0}"""
new_tab = """  .fsel-tab{position:relative;border:none;border-right:1px solid rgba(245,236,215,0.12);padding:0.75rem 1rem;cursor:pointer;background:transparent;transition:background .2s;width:5.25rem;flex-shrink:0}"""
assert old_tab in content, "BLOCK 2 (tab) not found — aborting"
content = content.replace(old_tab, new_tab)

# ─────────────────────────────────────────────────────────
# 2. Remove duplicate .fsel-note inside the card (keep only the outer one)
# ─────────────────────────────────────────────────────────
old_note = """(b.ok?'<p class="fsel-note">All digital. Print what you need.</p>':'')+toggle"""
new_note = """toggle"""
assert old_note in content, "BLOCK 3 (duplicate note) not found — aborting"
content = content.replace(old_note, new_note)

# ─────────────────────────────────────────────────────────
# 3. Boost contrast of the outer "All digital..." note
# ─────────────────────────────────────────────────────────
old_outer_note = """color:rgba(245,236,215,0.28);margin-top:24px;letter-spacing:0.4px;">All digital. Instant delivery. Print what you need, keep it forever.</p>"""
new_outer_note = """color:rgba(245,236,215,0.55);margin-top:16px;letter-spacing:0.4px;">All digital. Instant delivery. Print what you need, keep it forever.</p>"""
assert old_outer_note in content, "BLOCK 4 (outer note contrast) not found — aborting"
content = content.replace(old_outer_note, new_outer_note)

# ─────────────────────────────────────────────────────────
# 4. Compact overall section spacing on mobile
# ─────────────────────────────────────────────────────────
old_bh = """      .bundles-header { margin-bottom: 24px; }"""
new_bh = """      .bundles-header { margin-bottom: 16px; }
      #bundles { padding: 24px 16px !important; }"""
assert old_bh in content, "BLOCK 5 (bundles-header/padding) not found — aborting"
content = content.replace(old_bh, new_bh)

old_tabs_pad = """  .fsel-tabs{padding-top:16px}"""
new_tabs_pad = """  .fsel-tabs{padding-top:16px;margin-bottom:20px}"""
assert old_tabs_pad in content, "BLOCK 6 (fsel-tabs spacing) not found — aborting"
content = content.replace(old_tabs_pad, new_tabs_pad)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — full bundle compaction applied")
