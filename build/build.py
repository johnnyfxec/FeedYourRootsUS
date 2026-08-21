#!/usr/bin/env python3
"""
Feed Your Roots — static site builder.

Reads shared nav/footer templates + per-page source content,
and writes final static HTML files ready to commit and push.

Run this after editing:
  - _nav.html or _footer.html (header/footer changes)
  - shared.css (shared style changes)
  - any src/*.html source file (page content changes)

Usage:
  python3 build.py

Output: about.html, privacy.html, terms.html, refunds.html
        (index.html is NOT built by this script — it stays hand-edited,
         see note at bottom of this file)
"""

import re
import os

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BUILD_DIR, "src")
OUT_DIR = os.path.dirname(BUILD_DIR)  # repo root — one level up from build/

with open(os.path.join(BUILD_DIR, "_nav.html"), encoding="utf-8") as f:
    NAV_TEMPLATE = f.read()

with open(os.path.join(BUILD_DIR, "_footer.html"), encoding="utf-8") as f:
    FOOTER_TEMPLATE = f.read()

# Each page declares which nav link (if any) should be marked active,
# and what its relative URLs to other pages look like.
# Since only about.html/privacy.html/terms.html/refunds.html are built
# here (all siblings in the repo root), URLs are simple relative paths.
PAGES = {
    "about.html": {
        "active": "ABOUT",
    },
    "privacy.html": {
        "active": None,
    },
    "terms.html": {
        "active": None,
    },
    "refunds.html": {
        "active": None,
    },
}

COMMON_VARS = {
    "HOME_URL": "index.html",
    "BUNDLES_URL": "index.html#tools-preview",
    "ABOUT_URL": "about.html",
    "CTA_URL": "index.html#bundles",
    "PRIVACY_URL": "privacy.html",
    "TERMS_URL": "terms.html",
    "REFUNDS_URL": "refunds.html",
}


def render_nav(active_key):
    html = NAV_TEMPLATE
    for key, val in COMMON_VARS.items():
        html = html.replace("{{" + key + "}}", val)
    for marker in ["ACTIVE_BUNDLES", "ACTIVE_JOURNAL", "ACTIVE_ABOUT"]:
        target = marker.replace("ACTIVE_", "")
        css = ' class="nav-active"' if active_key == target else ""
        html = html.replace("{{" + marker + "}}", css)
    return html


def render_footer():
    html = FOOTER_TEMPLATE
    for key, val in COMMON_VARS.items():
        html = html.replace("{{" + key + "}}", val)
    return html


def build_page(filename, config):
    src_path = os.path.join(SRC_DIR, filename)
    if not os.path.exists(src_path):
        print(f"SKIP {filename}: no source file at src/{filename}")
        return False

    with open(src_path, encoding="utf-8") as f:
        src = f.read()

    nav_html = render_nav(config["active"])
    footer_html = render_footer()

    out = src.replace("{{NAV}}", nav_html).replace("{{FOOTER}}", footer_html)

    out_path = os.path.join(OUT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"OK   built {filename} ({len(out)} bytes)")
    return True


def copy_shared_css():
    src_css = os.path.join(BUILD_DIR, "shared.css")
    dst_css = os.path.join(OUT_DIR, "shared.css")
    if not os.path.exists(src_css):
        print(f"WARN: {src_css} not found, skipping copy")
        return
    with open(src_css, encoding="utf-8") as f:
        css_content = f.read()
    with open(dst_css, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"OK   copied shared.css -> repo root ({len(css_content)} bytes)")


def main():
    if not os.path.isdir(SRC_DIR):
        print(f"ERROR: source directory not found: {SRC_DIR}")
        print("Create src/about.html, src/privacy.html, src/terms.html, src/refunds.html")
        return
    copy_shared_css()
    built = 0
    for filename, config in PAGES.items():
        if build_page(filename, config):
            built += 1
    print(f"\n{built}/{len(PAGES)} pages built successfully.")


if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────────────────
# NOTE on index.html:
# index.html is intentionally NOT part of this build system.
# It has extensive page-specific CSS/JS (Tools Preview carousel,
# bundle selector, parallax config) that doesn't fit the simple
# nav/footer template pattern used here. It continues to be
# hand-edited directly, same as before.
#
# If index.html's nav or footer HTML changes, update it manually
# there AND in _nav.html / _footer.html so the two stay in sync.
# ─────────────────────────────────────────────────────────
