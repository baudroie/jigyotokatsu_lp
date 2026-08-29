# Design QA

**Final result: passed**

## Comparison target

- Desktop source visual truth: `/Users/baudroie/Downloads/LP事業統括/デザイン案web.png`
- Desktop implementation screenshot: `/Users/baudroie/Downloads/LP事業統括/screenshot-desktop-1440-final.png`
- Mobile source visual truth: `/Users/baudroie/Downloads/LP事業統括/デザイン案mobile.png`
- Mobile implementation screenshot: `/Users/baudroie/Downloads/LP事業統括/screenshot-mobile-390-final.png`
- State: initial page state, menus closed, no hover/focus state.

## Viewports and normalization

- Desktop source: 661 × 1804 px, normalized to 1440 × 3930 px.
- Desktop implementation: 1440 × 3933 px. The in-app browser’s 1440 CSS px layout was captured as overlapping browser-rendered segments and normalized to 1440 px at device scale 1 equivalent.
- Mobile source: 183 × 1793 px, normalized to 390 × 3821 px.
- Mobile implementation: 390 × 3843 px at a 390 × 844 CSS viewport, device scale factor 1. Browser-rendered segments were stitched at their measured scroll positions without width resampling.
- Full-view evidence: `comparison-desktop-side-by-side.png`, `comparison-desktop-overlay.png`, `comparison-mobile-side-by-side.png`, `comparison-mobile-overlay.png`.
- Focused evidence: Hero, black diagram, career, people, flow, final CTA, and footer were also inspected in the browser as individual viewport captures. Focused captures are retained as the `final-*part-*.jpg` and `deliver-*part-*.jpg` files.

## Required fidelity surfaces

- Fonts and typography: Japanese system Gothic fallbacks use heavy weights, line heights and explicit desktop/mobile wrapping. Hero uses separate PC/SP line breaks. Remaining optical differences from the raster reference are minor antialiasing/font-engine differences.
- Spacing and layout rhythm: Desktop and mobile full-page heights differ from normalized references by 3 px and 22 px respectively. Section boundaries, card direction, CTA stacking, and the SP-only FIELD omission align with the sources.
- Colors and visual tokens: orange, LINE green, dark section, off-white canvas, card shadows, and footer black match sampled/inferred source colors. Provided raster gradients are used unchanged.
- Image quality and asset fidelity: all custom imagery/icons are supplied assets copied without modification. PC/SP Hero backgrounds are separate. No screenshot-as-page, generated replacement art, inline SVG, or CSS illustration is used.
- Copy and content: source copy, fixed line breaks, career amounts, two existing employee stories, four flow steps, address, and footer text are preserved.
- Responsive behavior: no horizontal overflow at 1440, 1280, 768, 390, or 375 px. FIELD is visible from 768 px and hidden at 767 px and below.
- Accessibility: semantic headings/sections, image alt text, CTA labels, keyboard-capable menu, reduced-motion handling, and hidden text for the image-led benefit heading are present.

## Comparison history

### Pass 1 — blocked before fixes

- P1: Hero desktop/mobile copy duplicated because both heading variants rendered. Fixed by mutually exclusive PC/SP copy display rules.
- P1: PC benefit cards exposed the strip headline/transparent area and appeared too short. Fixed with three independent crop windows and full-height card surfaces while preserving the source image ratio.
- P1: Mobile black section and total page height were about 267 px too tall. Fixed by matching section heights and compacting icon/text scale; final page-height delta is 22 px.
- P2: Mobile final CTA subtitle transparency created a large gap and clipped the LINE button. Fixed with the source copy as HTML on SP and corrected vertical spacing.
- P2: LINE and offer flow icons were mapped to the wrong source files. Corrected the asset map/copies.
- P2: PC section boundaries drifted by 56 px after the benefit cards. Fixed the benefit section height; normalized desktop page-height delta is 3 px.

### Pass 2 — post-fix evidence

- Hero uses a single correct heading at each breakpoint, with correct CTA order and separate PC/SP backgrounds.
- Mobile section starts and total height align; career, people, flow, CTA, and footer remain in the correct order.
- Desktop section boundaries align from Hero through footer; FIELD is six-up and excluded on SP.
- Browser console: no warnings or errors during final interaction testing.
- Interactions tested: mobile menu open/close, menu link to `#career`, career/entry anchor behavior, LINE URL assignment, and smooth in-page navigation.

## Remaining P3 polish

- Raster-reference font antialiasing and the exact Hero display-face shape differ slightly from available local Japanese Gothic fonts.
- The benefit-card source strip has a wider native card aspect than the completed design; the implementation preserves the supplied image ratio and uses white card surfaces to match the completed layout’s height without distorting the asset.

## Self-assessment

- Desktop reproduction: 93/100
- Mobile reproduction: 93/100
- Asset usage accuracy: 96/100
- Responsive: 96/100
- Typography: 91/100
- Spacing: 93/100
- Functional: 97/100
