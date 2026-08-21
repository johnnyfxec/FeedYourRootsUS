#!/usr/bin/env python3
"""
patch-seo-complete.py
1. Adds SEO meta tags to <head>
2. Activates Homestead Complete bundle ($150)
3. Updates CTA from 'Join the Waitlist' to 'Get the Complete Bundle'
"""

import sys

FILE = '/data/data/com.termux/files/home/FeedYourRootsUS/index.html'

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

original = html
changes = []

# ── 1. META TAGS ─────────────────────────────────────────────────
META = (
    '\n  <meta name="description" content="The complete half-acre homesteading '
    'system for suburban families. Planting calendars, seed libraries, '
    'preservation logs and site plans for USDA Zones 5\u20139.">'
    '\n  <meta property="og:title" content="Feed Your Roots \u2014 '
    'Half-Acre Blueprint for Suburban Homesteaders">'
    '\n  <meta property="og:description" content="From seed to pantry on '
    '0.25\u20130.5 acres. 13 documents, 160+ pages, 5 bundles from $37.">'
    '\n  <meta property="og:url" content="https://feedyourroots.us">'
    '\n  <meta property="og:type" content="website">'
)

if 'og:title' in html:
    print('\u26a0\ufe0f  Meta tags already present \u2014 skipping')
else:
    html = html.replace('<head>', '<head>' + META, 1)
    changes.append('\u2713 SEO meta tags added to <head>')

# ── 2. ACTIVATE COMPLETE URL ─────────────────────────────────────
OLD_URL = "complete:null"
NEW_URL = "complete:'https://pay.hotmart.com/G107154913B'"

if NEW_URL in html:
    print('\u26a0\ufe0f  Complete URL already active \u2014 skipping')
elif OLD_URL in html:
    html = html.replace(OLD_URL, NEW_URL, 1)
    changes.append('\u2713 Homestead Complete URL activated')
else:
    print('\u274c  Could not find complete:null \u2014 check manually')
    sys.exit(1)

# ── 3. UPDATE CTA TEXT ───────────────────────────────────────────
OLD_CTA = "cta:'Join the Waitlist'"
NEW_CTA = "cta:'Get the Complete Bundle'"

if NEW_CTA in html:
    print('\u26a0\ufe0f  CTA already updated \u2014 skipping')
elif OLD_CTA in html:
    html = html.replace(OLD_CTA, NEW_CTA, 1)
    changes.append('\u2713 CTA updated to Get the Complete Bundle')
else:
    print('\u274c  Could not find Join the Waitlist CTA \u2014 check manually')

# ── 4. REMOVE COMING SOON / ENABLE BUTTON ───────────────────────
OLD_FLAGS = "soon:true,key:'complete',ok:false"
NEW_FLAGS = "soon:false,key:'complete',ok:true"

if NEW_FLAGS in html:
    print('\u26a0\ufe0f  Bundle flags already updated \u2014 skipping')
elif OLD_FLAGS in html:
    html = html.replace(OLD_FLAGS, NEW_FLAGS, 1)
    changes.append('\u2713 Coming Soon removed, Complete bundle enabled')
else:
    print('\u274c  Could not find bundle flags \u2014 check manually')

# ── WRITE ────────────────────────────────────────────────────────
if html != original:
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print('\n' + '\n'.join(changes))
    print('\nReady to push.')
else:
    print('\nNo changes made.')
