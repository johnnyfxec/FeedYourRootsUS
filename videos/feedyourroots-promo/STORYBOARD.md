---
format: 1080x1920
duration: 38s
message: "Half an acre is enough — Feed Your Roots gives suburban families a complete homesteading system to grow food on the space they already have."
arc: Hook → Product Intro → Feature Showcase → Benefit/Price → CTA
audience: Suburban families in USDA Zones 5–9 curious about homesteading
mode: autonomous
music: none
---

## Video direction

**Palette system** (from frame.md): ink (#0A0A0A) is the sole ground throughout — pure dark on every frame. Primary copy: cream (#F5ECD7). Accent marks and KPI figures: pink (#E8B84B, gold). Sub-accent rule lines: pink-deep (#D4732A, terracotta). Chrome (topbar, labels): JetBrains Mono 500 uppercase, cream. Every frame carries a mono topbar (JetBrains Mono 500 uppercase, cream, top edge flush to slide-pad).

**Motion grammar**: Long-tail decel (`power3`) on every entrance. No bouncy / no `back.out` / no `elastic.out`. Smooth long-tail settle is the default. `spring-pop-entrance` only for tile entries where the "landing" feel is right.

**Reveal model**: This is a silent video. "VO-paced" translate to **story-paced**: each element reveals at the natural reading beat it occupies — a line that is its own thought enters alone; a sub-line waits for the first to settle. Never dump the whole canvas at t=0. Reveals stay sequenced across the **back ~60%** of each frame.

**Rhythm / held-frame allocation**: Frame 1 (Hook) holds after the second clause lands — deliberate cinematic stillness before the world opens. Frame 5 (CTA) holds to the final frame. Frames 2, 3, 4 reveal across their full duration; none front-loads.

**Negative list**: No box-shadow / no gradient / no glow (flat paper per frame.md). No italic in display type. No lazy breathing / no circular scale loop. No slow back-half camera drift. No elements floating independently. No bouncy entrances. No wall-clock / no `Math.random`. No CSS `transition` / `@keyframes` for motion.

**Grain / documentary warmth** (per-frame CSS, every composition): A `::after` pseudo on the root composites a subtle 3% opacity SVG noise over the entire canvas — `mix-blend-mode: overlay`. Deterministic (no randomness). This is the film-grain register that makes ink #0A0A0A read warm rather than digital.

**Caption band**: No captions on this video. Bottom ~17% kept clear anyway per convention.

**BGM note (for later)**:
<!-- Suggested BGM: Ambient acoustic fingerpicked guitar, fingerstyle, key of G, slow tempo (~60 BPM), warm and intimate. Mood: "a morning in the garden before the day starts." No percussion, no swell. Options: Artlist "acoustic morning", Epidemic Sound "quiet homestead", or Musicbed "pastoral fingerstyle". Trim from 0:12 (past cold intro), fade out at ~0:36. -->

---

## Frame 1 — Hook

- scene: "HALF AN ACRE." then "A WHOLE LIFE." — two clauses, each alone, display-hero scale, cream on ink
- voiceover: ""
- duration: 8s
- transition_in: cut
- status: outline
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Future pacing — the viewer imagines the outcome before the product is named
- beat: aspiration + quiet longing
- blueprint: kinetic-type-beats (Adapt — centered-beat-triptych variant: three beats on a constant ink field, each element alone, third beat holds)
- asset_candidates: (typography only)
- poster: 5s

**Shot sequence (8s)**

Scene 1 (0.0–1.5s): Ink ground settles. A single 2px cream horizontal hairline draws from left to right across the vertical center — SVG self-draw (`svg-path-draw`), slow and deliberate, full width in 1.5s. Nothing else. Centered. Topbar (JetBrains Mono, "FEED YOUR ROOTS", cream, upper-left) appears on a smooth fade at 0.8s — `fromTo` opacity 0→1 on `power3`.

Scene 2 (1.5–4.2s): "HALF AN ACRE." enters above the hairline — Playfair Display 500, display-hero scale (~11.5cqw), cream, centered, tight line-height 0.92, tracking −0.02em. Two cues: "HALF AN ACRE" per-word staggered reveal (`dynamic-content-sequencing`), words landing left→right each on a smooth `power3` settle with a 0.15s stagger. Then the period "." arrives as a separate beat 0.3s after "ACRE", same weight. The entry runs 1.5s; the line settles and holds.

Scene 3 (4.2–6.5s): In-place token cycle (`discrete-text-sequence`) — hard cut on the same center position: "HALF AN ACRE." exits (instant opacity 0) and "A WHOLE LIFE." arrives (instant opacity 1). Same display-hero scale, cream, centered. No cross-fade — the hard cut is the beat, the swap is the signature move. "A WHOLE LIFE." lands fully formed, no additional stagger. Dwell 0.8s.

Scene 4 (6.5–8.0s): Hold. Both hairline rules now bracket the text (the lower one — 2px pink-deep — draws in under "A WHOLE LIFE." via `svg-path-draw` at 6.5s, 0.6s draw). Subtle jitter (`sine-wave-loop`, low amplitude: ±1.5px positional, 0.02 scale) on the headline block keeps it alive without drifting. No camera drift, no breathing.

narrativeRole: Open cold on the payoff promise. Two clauses in silence, each allowed to breathe. The hard swap is the heartbeat of the hook. The hairline rules frame it — the only decoration, and the editorial system's spine.
keyMessage: A small piece of land is enough for a full life.

---

## Frame 2 — Product Intro

- scene: "THE COMPLETE HOMESTEADING SYSTEM / for suburban families" — serif lockup, cream on ink, two tones
- voiceover: ""
- duration: 7s
- transition_in: crossfade
- status: outline
- src: compositions/frames/02-product-intro.html
- type: product_intro
- persuasion: Category announcement — names the product's genre before naming the product
- beat: clarity + recognition
- blueprint: titlecard-reveal (Reproduce — calm two-line value title card, slide-up crossfade, then held still)
- asset_candidates: (typography only)
- poster: 4s

**Shot sequence (7s)**

Scene 1 (0.0–1.2s): Ink ground. Topbar (JetBrains Mono, "FEED YOUR ROOTS", cream) appears at 0.0s — `fromTo` opacity, `power3`. A 2px pink-deep hairline draws left-to-right at upper-third position (`svg-path-draw`, 0.6s draw starting at 0.4s). Frame is intentionally spare — the hairline is the only mark.

Scene 2 (1.2–3.2s): "THE COMPLETE" reveals as JetBrains Mono 500 uppercase label (cream, tracking 0.18em) — `fromTo` translateY +24px → 0, opacity 0→1, `power3`, 0.5s. Positioned above the hairline, left-aligned within slide-pad. The label is the editorial chrome announcing what follows.

Scene 3 (3.2–5.5s): "HOMESTEADING SYSTEM" slides up from below — Playfair Display 500, headline-xl (~5cqw), cream, tight tracking −0.02em — `fromTo` translateY +40px → 0, opacity 0→1, `power3`, 0.7s. This is the dominant visual weight. Then "for suburban families" reveals 0.4s later — Playfair Display 400, body-card scale (~1.56cqw), cream, opacity 0→1 only (no translateY — it floats up subtly). A 2px cream hairline appears beneath as a closing rule, drawn left-to-right, 0.5s.

Scene 4 (5.5–7.0s): Hold. All three text lines stable. No motion. The stillness is the confident landing — `titlecard-reveal`'s signature is the low-motion hold. At most subtle jitter (`sine-wave-loop`, ±1px) on the headline line only.

narrativeRole: Name the product category. The viewer just felt the aspiration; now we name what creates it. One clean serif lockup in the editorial-forest register — authority without noise.
keyMessage: There is a complete system designed for exactly you.

---

## Frame 3 — Feature Showcase

- scene: Three credential tiles cascade onto ink — "13 DOCUMENTS · 160+ PAGES · USDA ZONES 5–9"
- voiceover: ""
- duration: 9s
- transition_in: blur-crossfade
- status: outline
- src: compositions/frames/03-feature-showcase.html
- type: feature_showcase
- persuasion: Value stacking — proof of depth arrives as a visual accumulation, not a list
- beat: confidence + credibility
- blueprint: grid-card-assemble (Adapt — three topic-tiles stacked vertically for 9:16, each with stat-figure + caption-mono, assembling with spring-pop-entrance; no camera zoom-out)
- asset_candidates: (typography only)
- poster: 6s

**Shot sequence (9s)**

Adapt: keep the staggered self-assemble signature; content is three KPI credentials not a logo wall; surface is ink-ground topic-tiles in rotating fills (green / pink / pink-deep per tile); no zoom-out needed on 9:16 (tiles fill the vertical).

Scene 1 (0.0–1.8s): Ink ground. Topbar (JetBrains Mono, "WHAT'S INSIDE", cream) appears at 0.0s. A 2px cream hairline draws below topbar label, full-width, 0.8s draw (`svg-path-draw`). Below the hairline, the three tile slots are invisible — no placeholder chrome, just the ground.

Scene 2 (1.8–4.2s): Tile 1 springs in — `spring-pop-entrance`, smooth long-tail settle, no overshoot. Tile surface: green fill (#674B0D from frame.md's green token), 6px radius, no shadow. Content: "13" in stat-figure scale (Playfair Display 500, ~11.5cqw, pink/#E8B84B), then "DOCUMENTS" in caption-mono (JetBrains Mono 500, uppercase, cream, 0.14em tracking) below. The tile occupies roughly the top third of the stacked layout, left-padded to slide-pad. 2px pink hairline rule above the stat figure inside the tile.

Scene 3 (4.2–6.6s): Tile 2 springs in 0.8s after Tile 1's peak — `spring-pop-entrance`, stagger 0.0s (sequential, not simultaneous). Tile surface: pink fill (#E8B84B), 6px radius. Content: "160+" stat-figure (Playfair Display 500, ~11.5cqw, green-deep/#513B0A), "PAGES" caption-mono (green-deep, 0.14em tracking). 2px green-deep rule inside tile.

Scene 4 (6.6–8.5s): Tile 3 springs in. Tile surface: pink-deep fill (#D4732A), 6px radius. Content: "USDA ZONES" caption-mono (Playfair Display 500 weight for the stat below; caption in cream, 0.14em tracking), "5–9" stat-figure (Playfair Display 500, ~11.5cqw, cream). 2px cream rule inside tile.

Scene 5 (8.5–9.0s): All three tiles stable. Hold. Subtle jitter (`sine-wave-loop`, ±1.5px) on each tile in a 0.15s phase offset so they feel independent and alive without breathing. No camera drift.

narrativeRole: Prove the scope. Three credential facts land one by one as accumulating tiles — the assembly creates the feeling of something comprehensive being handed to the viewer.
keyMessage: This is substantial, thorough, and built for your climate zone.

---

## Frame 4 — Pricing

- scene: "5 BUNDLES / starting at / $37" — gold figure on ink, slow slide-up reveal, held
- voiceover: ""
- duration: 7s
- transition_in: crossfade
- status: outline
- src: compositions/frames/04-pricing.html
- type: benefit_highlight
- persuasion: Risk reversal — price presented after value is established; $37 feels light
- beat: relief + low-friction desire
- blueprint: titlecard-reveal (Reproduce — calm two-line value title; one slide-up crossfade per element then held still)
- asset_candidates: (typography only)
- poster: 4s

**Shot sequence (7s)**

Scene 1 (0.0–1.0s): Ink ground. Topbar (JetBrains Mono, "CHOOSE YOUR BUNDLE", cream). A 2px pink-deep hairline draws in, upper-third, full width, `svg-path-draw`, 0.6s.

Scene 2 (1.0–2.8s): "5 BUNDLES" enters — JetBrains Mono 500, label scale, cream, tracking 0.18em — `fromTo` translateY +20px → 0, opacity 0→1, `power3`, 0.5s. Positioned just below the hairline rule, centered.

Scene 3 (2.8–4.5s): "starting at" enters — Playfair Display 400, body-card scale (~1.56cqw), cream — `fromTo` translateY +16px → 0, opacity 0→1, `power3`, 0.4s. Below "5 BUNDLES", slight spacing gap (editorial breathing room). The `titlecard-reveal` signature: this is the slide-up into a still.

Scene 4 (4.5–6.5s): "$37" enters — Playfair Display 500, display scale (~7.3cqw), pink (#E8B84B, gold), tracking −0.02em — `fromTo` translateY +28px → 0, opacity 0→1, `power3`, 0.7s. A 2px pink hairline appears above "$37" simultaneously, drawn right-to-left `svg-path-draw`, 0.4s — drawing inward as the number arrives, drawing attention to the figure. This is the frame's weight center.

Scene 5 (6.5–7.0s): Hold. "$37" in gold at display scale dominates. The hairline holds. No drift, no breathing. Subtle jitter (`sine-wave-loop`, ±1px) on "$37" only — it's the payoff, keep it alive.

narrativeRole: Remove the friction. After category, scope, and depth, the price is the permission slip — specific, affordable, and given weight by gold treatment.
keyMessage: There's a bundle for your stage. Entry is $37.

---

## Frame 5 — CTA

- scene: "feedyourroots.us" assembles on ink — wordmark lockup, cream on dark, pink-deep period, held to black
- voiceover: ""
- duration: 7s
- transition_in: zoom-through
- status: outline
- src: compositions/frames/05-cta.html
- type: cta
- persuasion: Inevitability — after aspiration, category, proof, and price, the URL is the only remaining step
- beat: urgency-to-act + peace of mind
- blueprint: logo-assemble-lockup (Adapt — wordmark assembles char-by-char/segment cascade into centered lockup; signature move: spring-bloom whole from zero on cleared stage; no push-through needed since no logo mark; extends to URL end-card hold)
- asset_candidates: (typography only)
- poster: 4s

**Shot sequence (7s)**

Adapt: the "logo" is the URL itself. Keep the cascade-assemble signature move and the centered lockup. Surface is pure ink — no other UI. The ".us" TLD is the spring-bloom payoff in pink-deep.

Scene 1 (0.0–1.2s): Ink ground. Topbar (JetBrains Mono, "START HERE", cream, appears at 0.0s `fromTo` opacity). A 2px cream hairline draws left-to-right, centered vertically at upper-third, `svg-path-draw`, 0.7s. The stage is cleared — this is the arrival frame.

Scene 2 (1.2–4.5s): "feedyourroots" assembles — Playfair Display 500, headline-xl scale (~5cqw), cream, tracking −0.02em — per-word staggered reveal (`dynamic-content-sequencing`) split into three cue segments: "feed" → "your" → "roots", each landing on a smooth `power3` long-tail settle with 0.18s stagger between segments. The assembly runs left-to-right, like words being placed. Total run: ~1.8s; settles at ~3.0s.

Scene 3 (3.0–4.5s): ".us" spring-blooms in — `spring-pop-entrance` (smooth long-tail settle, zero overshoot), in pink-deep (#D4732A, terracotta), same headline-xl scale, landing immediately after "roots". The color difference is the signature accent — the TLD is different from the brand name, it's the domain suffix that makes the URL complete. A 2px cream hairline draws in below the full wordmark, `svg-path-draw`, 0.5s.

Scene 4 (4.5–6.0s): Below the lower hairline, a body-card line appears — "The Half-Acre Blueprint" — Playfair Display 400, ~1.56cqw, cream, opacity 0→1, 0.4s — a subtitle that names the product. This gives the end card a second level of information without adding visual noise.

Scene 5 (6.0–7.0s): Hold. The full lockup — wordmark + subtitle + hairlines — is stable. Topbar holds. Subtle jitter (`sine-wave-loop`, ±1px) on "feedyourroots.us" only. No motion elsewhere. The stillness is the confidence of the final frame.

narrativeRole: The single action. Everything before this earned the right to ask. The URL arrives assembled, not slapped on — the assembly is the respect shown to the viewer's attention.
keyMessage: feedyourroots.us
