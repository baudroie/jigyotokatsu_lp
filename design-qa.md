# Design QA — 2026-08-31

final result: blocked

This supersedes the previous PASS report. Matching page height is not evidence that text images are uncut.

## Source and capture

- Visual truth: デザイン案web.png (661×1804) / デザイン案mobile.png (183×1793).
- Rendered implementation: comparison/20260831-loop7/desktop-1440.png (1440×3929) / mobile-390.png (390×4178).
- Viewports: 1440×900 and 390×844; DPR=1; initial state, menu closed.
- Normalization: width only, preserving aspect ratio; desktop becomes661×1804, mobile183×1960. Blank canvas pads the shorter side, never stretches it.
- Full-view evidence: comparison/20260831-loop7/{desktop,mobile}-side-by-side.png, -overlay.png (50%), -diff.png.
- Focused evidence: same folder, {desktop,mobile}-{hero,benefits,career,people,final-cta}-focused.png. These align section starts only and preserve original scale.
- Additional final responsive evidence: comparison/20260831-responsive-final/ at1280,768,375px.
- In-app full-width capture was blocked by its viewport/capture limitation in prior work; Chrome browser-rendered captures are used.

## Findings

### [P1] Composite Benefits image cannot satisfy whole-PNG display and vertical cards simultaneously

The provided cards-strip.png is a heading plus three cards in a single2048×768 PNG.
Existing desktop/mobile viewports still select individual cards from it. Each complete card's text, illustration, and lower border now fits, and CSS duplicate white backgrounds/borders/shadows are removed. The whole source PNG is nevertheless NOT displayed.
Evidence: Benefits focused comparisons and the3 clipping candidates in each viewport's image-layout-audit.json.
Need individual source PNGs or explicit permission for asset extraction. Do not mark the strict no-partial-PNG condition PASS.

### [P1] Career source artwork has a different aspect ratio from the compact reference cards

All four complete PNGs, including titles, descriptions, salary figures and people, are displayed with natural aspect ratio. No clipping ancestor, fixed image height, cover, or outer CSS card remains.
The SP reference's card content is compact and omits the body text present in the supplied source. Keeping all source content at readable width makes Career1083.4px tall vs726.7px reference, a356.7px section-height difference.
This causes the downstream Mobile sections' start/end positions to remain about356px lower. Their own heights are matched; translating them upwards would overlap content.
Desktop section boundaries match within1px, but the source's shorter, wider internal cards do not match the reference card height. No distortion is used to conceal this.
Need compact source assets or acceptance of this aspect-ratio-driven difference.

## Required fidelity surfaces

- Fonts/typography: HTML Hero copy size and mobile line breaks refined, field/flow hierarchy preserved. Raster-internal fonts are supplied artwork, outside this turn's artwork-redesign scope.
- Spacing/layout: Desktop section boundaries within1px of width-normalized reference. SP Hero/Benefits/Frontline and the individual heights of People/Flow/CTA/Footer match within about1px. Career and cumulative Mobile positions remain NG as above.
- Colors: Benefits surrounding canvas sampled from reference bottom-left offwhite pixels (#f6f6f6); final CTA decorative background expanded to remove the external frame. Existing image colors untouched. Mobile orange bottom boundary retained; exact composite-background treatment remains part of Benefits NG.
- Image quality: all76 visible image instances across PC/SP retain natural ratio (41PC,35SP). Non-composite clipping candidates0/0. Composite clipping candidates3/3. Never claim that means all-img clipping0.
- Copy/content: no visible wording or section-order changes; only responsive line breaks. Hero heading unified so it is available to assistive technology on mobile.
- Responsive: no document horizontal overflow at1440,1280,768,390,375px without body overflow-x hiding. Tablet Career uses2 columns; SP Field stays hidden.
- Accessibility: image alternatives, focus styles, menu aria-expanded preserved; decorative plus has no false “open details” label. Comprehensive assistive-technology certification not performed.

## Iteration history

1. Baseline captured before edits: clipping candidates25PC/19SP.
2. LOOP1: remove fixed image clipping and duplicate card surfaces; image candidates reduce to3/3, but natural transparent canvases make sections too tall.
3. LOOP2: layout-only compensation for transparent gutters; section-height correction; sources are never masked or re-saved.
4. LOOP3: recompute precise SP People/Flow boundaries; reposition People heading/panel; balance section padding.
5. LOOP4: Hero text scale, Frontline/Flow rhythm, Footer; include complete Benefits card bodies in existing composite windows.
6. LOOP5: tablet minimum-height excess and card readability; single accessible h1.
7. LOOP6: SP background focal point and final CTA column alignment.
8. LOOP7: fix transparent Career image intercepting Career-details clicks with pointer-events:none on noninteractive images.

Every correction loop has1440/390 full-page screenshots and width-normalized side-by-side/overlay evidence. Full history and boundary tables are in visual-qa.md.

## Browser interaction checks

- Hero career CTA -> #career, top0.109px: PASS.
- Career details -> #people, top0.008px after click-interception fix: PASS.
- Menu open and selection -> #flow, menu closes: PASS.
- Desktop ENTRY -> #flow, scroll clamped at the page's maximum because less than one viewport remains: PASS.
- LINE URL stays #, as provided; external destination not tested/configured.
- Browser log includes5 message-channel listener warnings with an extension-style signature. LP JS contains no corresponding async listener; warnings are retained verbatim in functional-tests.json, not misreported as0 errors.

## Implementation checklist

- [x] Existing assets preserved; no generation, re-save, destructive edits.
- [x] Career/people/title/CTA text is no longer container-cropped.
- [x] Full PC/SP screenshots, overlays, image audit and boundary metrics saved.
- [x]7 correction loops and alternate-width checks.
- [ ] Individual Benefits assets / extraction decision.
- [ ] Compact Career assets / aspect-ratio difference decision.
- [ ] Re-run comparison and achieve all-section PASS after these constraints are resolved.

final result: blocked
