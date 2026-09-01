# Design QA — 2026-09-01 キャリア年収なし素材・モーション

final result: passed

## Source and implementation

- Source visual truth: `新素材/キャリア/PC/*.png`（4枚、各1600×1040）と `新素材/キャリア/SP/*.png`（4枚、各1040×1600）。年収記載なし。
- Implementation: `assets/career/no-income-20260901/` の同名8枚を `index.html` のpicture/sourceで参照。
- Browser captures: `comparison/20260901-career-no-income/after-raw-1440-final.png`（1440×3760）/ `after-raw-390-final.png`（390×6482）。CSS実表示幅1440/390、全reveal完了後。
- Focused evidence: `desktop-source-implementation.png`（PC4枚）/ `mobile-source-implementation.png`（SP1枚）/ `source-contact-sheet.jpg`（全8枚）。元比率を維持し、ページ全体を別の高さへ引き伸ばしていない。
- 変更前のQAは `comparison/20260901-career-no-income/previous-design-qa.md` に保持。

## Findings

P0/P1/P2なし。8枚すべてが正しいPC/SPの表示幅で読み込まれ、年収を含まない画像内容・代替テキストになっている。旧参照はHTML/asset-mapから除去し、旧ファイル自体は保持した。

## Required fidelity surfaces

- Fonts/typography: カード内文字は新しい完成PNGそのもの。HTMLのfont-size・family・line-heightは未変更。altから旧年収だけを除去。
- Spacing/layout rhythm: PCカード331.25×215.3125px、SP390で348×535.3828px。ページ高は変更前と同じPC3760px/SP6482px。section width/height、padding、margin、gapは未変更。
- Colors/tokens: CSS色・背景・影・radiusは未変更。新PNGの色を加工していない。
- Image quality/asset fidelity: sourceと配置先のSHA-256が全8枚で一致。自然寸法、RGBA、24px透過境界、object-fit:contain、overflow:visibleを確認。crop・再圧縮・変形なし。
- Copy/content: 年次・役割・説明文は新PNGどおり。カード外の既存PC年収注記は別素材かつ変更対象外なので維持。
- Responsive/accessibility: 767px以下はSP、768px以上はPC。currentSrcを1440/390/375相当で確認。＋とキャリア詳細ボタンは前回指示どおり0件。
- Interaction/motion: IntersectionObserverの一度だけ表示、reduced motion、SP先輩2名カルーセル、2ドット、スワイプ、キーボードを維持。静止時opacity1/translate none。

## Comparison history

1. 初回比較: 新旧ファイル名は同じだがSHA-256が全8枚で異なり、HTMLは旧 `assets/career/new-20260831/` を参照していた。
2. 修正: 新素材を別ディレクトリへ原寸コピーし、pictureのPC/SP参照とalt、asset-mapを更新。
3. 修正後比較: focused source/implementationで人物・年次・役割・説明文・年収なしを確認。表示寸法・ページ高さ差0。追加P0/P1/P2なし。

## Verification

- `node --check script.js`: PASS。
- `comparison/20260831-221634-motion/check-motion.cjs`: 7/7 PASS。
- Chrome 1440/390の上から下までのスクロール: 表示レイアウトを持つ未発火reveal 0、opacity不正0、横overflowなし。
- 390px carousel: Slide1→左スワイプ→Slide2→active dot変更→dotでSlide1へ復帰。panel高さ212px不変。
- 375pxは前回の同一CSS/JSの実測QAを維持し、今回のカード参照はSP4枚・自然寸法1040×1600・表示幅333pxを確認。
- 新規ブラウザタブ console error/warning: 0。

final result: passed
