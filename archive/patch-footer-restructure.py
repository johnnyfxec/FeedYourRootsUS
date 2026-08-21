with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

old_css = """    footer { background: #160A02; padding: 60px 24px 44px; }
    .footer-inner { max-width: 760px; margin: 0 auto; text-align: center; }
    .footer-logo { font-family: 'Satisfy', cursive; font-size: 28px; color: #D4732A; margin-bottom: 8px; }
    .footer-tagline { font-family: 'Lora', serif; font-style: italic; font-size: 20px; color: rgba(245,236,215,0.48); margin-bottom: 34px; }
    .footer-links { display: flex; justify-content: center; gap: 34px; flex-wrap: wrap; margin-bottom: 28px; }
    .footer-links a { font-family: 'DM Sans', sans-serif; font-size: 16px; color: rgba(245,236,215,0.44); letter-spacing: 0.3px; transition: color 0.2s; }
    .footer-links a:hover { color: #F5ECD7; }
    .footer-divider { height: 1px; background: rgba(245,236,215,0.07); margin-bottom: 20px; }
    .footer-domain { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #4A7C59; letter-spacing: 0.5px; margin-bottom: 6px; }
    .footer-copy { font-family: 'DM Sans', sans-serif; font-size: 13px; color: rgba(245,236,215,0.2); }"""

new_css = """    footer { background: #160A02; padding: 60px 24px 44px; }
    .footer-inner { max-width: 760px; margin: 0 auto; text-align: center; }
    .footer-logo { font-family: 'Satisfy', cursive; font-size: 28px; color: #D4732A; margin-bottom: 8px; }
    .footer-tagline { font-family: 'Lora', serif; font-style: italic; font-size: 20px; color: rgba(245,236,215,0.48); margin-bottom: 34px; }
    .footer-links { display: flex; justify-content: center; gap: 34px; flex-wrap: wrap; margin-bottom: 28px; }
    .footer-links a { font-family: 'DM Sans', sans-serif; font-size: 16px; color: rgba(245,236,215,0.44); letter-spacing: 0.3px; transition: color 0.2s; }
    .footer-links a:hover { color: #F5ECD7; }
    .footer-divider { height: 1px; background: rgba(245,236,215,0.07); margin-bottom: 22px; }
    .footer-nav-row { display: flex; justify-content: center; gap: 28px; flex-wrap: wrap; margin-bottom: 14px; }
    .footer-nav-row a { font-family: 'DM Sans', sans-serif; font-size: 14px; color: rgba(245,236,215,0.5); letter-spacing: 0.3px; transition: color 0.2s; }
    .footer-nav-row a:hover { color: #F5ECD7; }
    .footer-legal-row { display: flex; justify-content: center; gap: 28px; flex-wrap: wrap; margin-bottom: 22px; }
    .footer-legal-row a { font-family: 'DM Sans', sans-serif; font-size: 12.5px; color: rgba(245,236,215,0.32); letter-spacing: 0.3px; transition: color 0.2s; }
    .footer-legal-row a:hover { color: rgba(245,236,215,0.7); }
    .footer-domain { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #4A7C59; letter-spacing: 0.5px; margin-bottom: 6px; }
    .footer-copy { font-family: 'DM Sans', sans-serif; font-size: 13px; color: rgba(245,236,215,0.2); }"""

assert old_css in content, "BLOCK 1 (footer CSS) not found — aborting"
content = content.replace(old_css, new_css)

old_html = """<footer>
  <div class="footer-inner">
    <div class="footer-logo">Feed Your Roots</div>
    <div class="footer-tagline">Half an acre. A whole life.</div>
    <div class="footer-links">
      <a href="https://www.instagram.com/feedyourrootsus" target="_blank">Instagram</a>
      <a href="https://www.tiktok.com/@feedyourrootsus" target="_blank">TikTok</a>
      <a href="https://www.pinterest.com/feedyourrootsus" target="_blank">Pinterest</a>
      <a href="https://www.youtube.com/@feedyourrootsus" target="_blank">YouTube</a>
    </div>
    <div class="footer-divider"></div>
    <div class="footer-domain">feedyourroots.us</div>
    <div class="footer-copy">© 2025 Feed Your Roots. All rights reserved.</div>
  </div>
</footer>"""

new_html = """<footer>
  <div class="footer-inner">
    <div class="footer-logo">Feed Your Roots</div>
    <div class="footer-tagline">Half an acre. A whole life.</div>
    <div class="footer-links">
      <a href="https://www.instagram.com/feedyourrootsus" target="_blank">Instagram</a>
      <a href="https://www.tiktok.com/@feedyourrootsus" target="_blank">TikTok</a>
      <a href="https://www.pinterest.com/feedyourrootsus" target="_blank">Pinterest</a>
      <a href="https://www.youtube.com/@feedyourrootsus" target="_blank">YouTube</a>
    </div>
    <div class="footer-divider"></div>
    <div class="footer-nav-row">
      <a href="about.html">About</a>
      <a href="/journal" onclick="return false;">The Journal</a>
      <a href="#bundles">Bundles</a>
    </div>
    <div class="footer-legal-row">
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Service</a>
      <a href="refunds.html">Refund Policy</a>
    </div>
    <div class="footer-domain">feedyourroots.us</div>
    <div class="footer-copy">© 2026 Feed Your Roots US. All rights reserved.</div>
  </div>
</footer>"""

assert old_html in content, "BLOCK 2 (footer HTML) not found — aborting"
content = content.replace(old_html, new_html)

if content == orig:
    print("NO CHANGES APPLIED — check blocks")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK — footer restructure patch applied successfully")
