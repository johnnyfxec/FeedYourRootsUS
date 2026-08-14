#!/usr/bin/env python3
"""
patch-keywords.py
Integrates 5 high-intent SEO keywords into feedyourroots.us
Two surgical changes — natural language, no forced copy.
"""

import sys

FILE = '/data/data/com.termux/files/home/FeedYourRootsUS/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

original = html
changes = []

# ── CHANGE 1 ─────────────────────────────────────────────────────
# "working food system" → "seed to pantry system"
# Location: Solution section — "how a half acre (or less) becomes a working food system"
# Keywords added: "seed to pantry system"

OLD1 = 'becomes a working food system'
NEW1 = 'becomes a complete seed to pantry system'

if NEW1 in html:
    print('\u26a0\ufe0f  Change 1 already applied \u2014 skipping')
elif OLD1 in html:
    html = html.replace(OLD1, NEW1, 1)
    changes.append('\u2713 Change 1: seed to pantry system')
else:
    print('\u274c  Change 1 not found \u2014 check string manually')
    sys.exit(1)

# ── CHANGE 2 ─────────────────────────────────────────────────────
# Bundle section subtitle — add all remaining 4 keywords naturally
# Location: "Choose Your Blueprint" intro line
# Keywords added: urban homestead bundle, suburban homestead planting calendar,
#                 half acre homestead layout, backyard food production plan

OLD2 = 'Every bundle includes the complete 48-page illustrated guide.'
NEW2 = ('Every urban homestead bundle includes the complete 48-page illustrated guide '
        '\u2014 your suburban homestead planting calendar, half acre homestead layout, '
        'and backyard food production plan, all in one place.')

if NEW2 in html:
    print('\u26a0\ufe0f  Change 2 already applied \u2014 skipping')
elif OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    changes.append('\u2713 Change 2: 4 keywords added to bundle intro')
else:
    print('\u274c  Change 2 not found \u2014 check string manually')
    sys.exit(1)

# ── WRITE ─────────────────────────────────────────────────────────
if html != original:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n'.join(changes))
    print('\nAll 5 keywords integrated. Ready to push.')
else:
    print('No changes made.')
