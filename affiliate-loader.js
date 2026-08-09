/**
 * Feed Your Roots — Affiliate Link Loader
 * Reads ?aff=CODE from the URL, fetches affiliates.json,
 * and returns the correct checkout URLs for the bundle selector.
 *
 * Usage: include before the bundle selector script.
 * Access resolved URLs via window.FYR_CHECKOUT
 */

window.FYR_CHECKOUT = {
  core:      'https://pay.hotmart.com/S107078295H',
  starter:   'https://pay.hotmart.com/K107078722B',
  family:    'https://pay.hotmart.com/C107078806J',
  homestead: 'https://pay.hotmart.com/V107078877Y',
  complete:  null
};

(async function () {
  const affCode = new URLSearchParams(window.location.search).get('aff');
  if (!affCode) return;

  try {
    const res  = await fetch('/affiliates.json');
    const data = await res.json();
    const aff  = data.affiliates.find(a => a.code === affCode);

    if (aff && aff.links) {
      Object.assign(window.FYR_CHECKOUT, aff.links);
      console.log('[FYR] Affiliate loaded:', aff.name);
    } else {
      console.warn('[FYR] Affiliate code not found:', affCode);
    }
  } catch (e) {
    console.error('[FYR] Could not load affiliates.json:', e);
  }

  if (typeof window.FYR_RENDER_SELECTOR === 'function') {
    window.FYR_RENDER_SELECTOR();
  }
})();
