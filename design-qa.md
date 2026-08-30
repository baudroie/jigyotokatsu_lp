# Design QA

## Comparison target

- Source visual truth: `デザイン案web.png`, `デザイン案mobile.png`
- Final implementation screenshots: `comparison/desktop-1440.png`, `comparison/mobile-390.png`
- Desktop source pixels: 661×1804
- Desktop implementation pixels: 1440×3932; normalized to 661×1805
- Desktop CSS viewport: 1440×900; device scale factor 1
- Mobile source pixels: 183×1793
- Mobile implementation pixels: 390×3821; normalized to 183×1793
- Mobile CSS viewport: 390×844; device scale factor 1
- State: initial page state, menu closed

## Evidence

- Full-view desktop: `comparison/desktop-side-by-side.png`, `comparison/desktop-overlay.png`, `comparison/desktop-diff.png`
- Full-view mobile: `comparison/mobile-side-by-side.png`, `comparison/mobile-overlay.png`, `comparison/mobile-diff.png`
- Focused desktop: `comparison/focused-desktop-hero.png`, `comparison/focused-desktop-career.png`, `comparison/focused-desktop-final.png`
- Focused mobile: `comparison/focused-mobile-hero.png`, `comparison/focused-mobile-career.png`, `comparison/focused-mobile-final.png`
- Additional responsive captures: `comparison/final/desktop-1280.png`, `comparison/final/mobile-375.png`

## Required fidelity surfaces

- Fonts and typography: PASS. Japanese Gothic fallback, weight, three-line SP HERO wrap, heading hierarchy, line height, and CTA image text were checked. Remaining stroke-shape differences are confined to raster/source-font differences.
- Spacing and layout rhythm: PASS. Section boundaries, card gaps, HERO/CTA rhythm, people/flow density, final CTA, and footer height align with the reference. Mobile normalized total height matches exactly.
- Colors and visual tokens: PASS. The 3cards background now uses the reference-like light gray; dark and orange sections match the intended balance.
- Image quality and asset fidelity: PASS. Original supplied assets are used without rewriting, cropping files, or destructive edits. CSS wrappers only control visible transparent margins and overflow.
- Copy and content: PASS. Copy and section order are unchanged. Image alt text retains important rasterized copy.
- Responsiveness: PASS. 1440, 1280, 390, and 375px checked; no horizontal overflow.
- Accessibility: PASS for the tested scope. Semantic headings, alt text, aria labels, menu expanded state, keyboard-capable links/buttons, and reduced-motion CSS remain present.

## Comparison history

- Loop 1: P1 mobile HERO blank space, P1 career double-card treatment, P1 mobile vertical drift, P2 3cards background, people/flow/final CTA density.
- Loop 2: Removed career wrapper surfaces, changed 3cards background, rebalanced HERO and major mobile section heights.
- Loop 3: Matched mobile section boundaries; enlarged desktop career imagery; refined people and final CTA.
- Loop 4: Increased CTA image presentation without changing aspect ratio; compacted mobile flow; matched footer and total page height.
- Loop 5: Rejected a HERO typography experiment that created a fourth line.
- Loop 6: Restored a three-line HERO and passed same-viewport comparison.
- Loop 7: Rejected an HTML salary overlay because it competed with raster copy.
- Loop 8: Reverted to clean source-image presentation and repeated full comparison; no actionable P0/P1/P2 findings remained.

## Interaction and browser verification

- Mobile menu: opens with `aria-expanded=true`, closes with `aria-expanded=false`.
- Career CTA: navigates to `#career`; target top reached.
- ENTRY CTA: navigates to `#flow`; target reached.
- Console errors: 0.
- 1280px: `scrollWidth = clientWidth = 1280`.
- 375px: `scrollWidth = clientWidth = 375`.

## Findings

- No actionable P0/P1/P2 findings remain.
- P3 accepted: minor image-internal illustration/type differences remain because the supplied raster assets differ from the raster content embedded in the reference. This was explicitly outside the main correction scope and the originals were not altered.

## Final result

final result: passed
