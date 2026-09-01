# スクロール演出とSP先輩カルーセル

## 対象・制約

- 変更ファイル: `index.html`, `styles.css`, `script.js`, `README.md`。
- 元PNG、ZIP、以前の成果物は変更なし。外部ライブラリ・ビルドツール・デプロイなし。
- 今回の正解は変更直前の静止レイアウト。元の完成画像は `デザイン案web.png`（661×1804）, `デザイン案mobile.png`（183×1793）。各画像の縦横比を保ち、reference / before / afterの3列比較も保存した。
- 前回までの新素材比率に由来する完成画像との寸法差は変更していない。今回のPASSは既存デザインの維持とモーション・操作機能の判定であり、その既知の差が解消したという意味ではない。

## 実装

- HERO: load後、ロゴ→メインコピー→サブ→説明→LINE→キャリア。表示対象ごと120msずつ（SPで非表示の説明文は順番を消費しない）。背景は動かさない。
- IntersectionObserver: threshold 0.15、rootMargin `0px 0px -4% 0px`。表示後unobserveし、再非表示にはしない。未対応時もコンテンツを表示。
- 訴求・キャリア: PCは100ms順次、SPはカードごとに入画した時に遅延なしで表示。
- 黒背景図解: タイトル→M&A→矢印→PMI→矢印→若手人材→説明文。図解の同時交差を起点に順序を固定。
- フィールド90ms、フロー100msずつ。先輩はPC左右20px、SPはfadeのみ。最終CTAは0/120/240ms。Footerは子要素のfadeのみで背景不変。
- transformの個別成分であるCSS `translate` を使い、既存HEROの `skewX(-3deg)` を上書きしない。
- SP先輩: 既存2名、2ドット、Pointer Eventsで50px閾値・縦方向優位/小移動/cancelは無効。loopあり、自動再生なし。
- 2枚の自然高さを共有するGridにより高さを揃え、PCではtrackをdisplay:contentsとして元の2列を保持。本文画像の透過canvasが既存の負marginで下へ出ているため、最初のoverflow:hidden案は却下し、横clip/縦visibleに修正した。
- paginationは旧230×76.664pxの占有領域、既存marginを維持。見えるdotは12px・間隔8px、active橙/inactive灰。旧3つの装飾dot→指定された2つの操作dotのみが静止画の意図した差分。
- aria-label / aria-current / aria-hidden / inert / polite live statusを実装。左右/Home/Endキーも利用可能。
- PC fine pointerのみCTA画像のhover -2px/200ms。revealは外側、hoverは内側、carousel transformは別track。

## ブラウザQA

| 幅 | ページ高さ 前→後 | セクション位置/高さ差 | 既存画像のx/y/width/height差 | 横はみ出し | 判定 |
|---|---|---|---|---|---|
| 1440 | 3760→3760 | 全9セクション0px | 全画像0px | なし | PASS |
| 390 | 6482→6482 | 全9セクション0px | 既存表示画像0px | なし | PASS |
| 375 | 6301→6301 | 全9セクション0px | 既存表示画像0px | なし | PASS |

HERO / Benefits / Frontline / Field（SP非表示維持）/ Career / People / Flow / CTA / Footer: すべて静止配置維持PASS。padding・margin・gap・背景・フォント・画像サイズの既存値は変更していない。

- ページ上から下までスクロール。1440pxで43対象、390/375pxで35対象が表示済み。表示レイアウトを持つ未発火要素0、表示済みopacity不正0。スクロール途中の横幅もviewportと一致。
- 390/375px: Slide1→左ドラッグスワイプ→Slide2→activeドット更新→dotでSlide1へ復帰: PASS。マウスのPointer操作をブラウザで実行。実機タッチは未実施だが同じPointer Eventsを使用し、touch-actionで縦パンとピンチを許可。
- 切替前後: panel212px / slide210pxを維持。人物・吹き出し・本文・署名を目視確認。本文PNGの縦方向canvasをクリップしない。
- 20px横移動、縦方向優位ドラッグで誤切替なし。ドットクリック、キーボードArrowLeft、メニューから先輩へスクロール、768↔390px切替、PC2列復帰を確認: PASS。
- ENTRY hoverの実computed transform: `matrix(1,0,0,1,0,-2)`。SPにはhoverルール非適用。
- 新規QAタブのconsole error 0 / warning 0。旧タブに実装前の拡張機能メッセージチャネルエラーが残っていたため、新規タブで今回のコードを確認した。
- 画像読み込み・フォント完了後に最終スクリーンショットを取得。読み込み失敗なし。

## 自動テスト・reduced motion

`node --check script.js`: PASS。

`node comparison/20260831-221634-motion/check-motion.cjs`: 7テストPASS。

1. reduced motion初期設定: Observerを作らずreveal非表示も付かない。カルーセル操作は可能。
2. IntersectionObserver未対応時: コンテンツ表示とカルーセル操作維持。
3. 一度表示後unobserve。スクロールアウトしても非表示へ戻らない。
4. 動作中にreduced motionへ変更すると全表示しObserver切断。
5. スワイプ、小移動、縦移動、cancel、loop。
6. ドット、キーボード、PC/SPブレークポイント変更時のアクセシビリティ状態。
7. 自動再生timer・外部アニメーション依存なし。

CSSのreduced-motion media ruleは実ブラウザCSSOMでも確認。JSの分岐はNode VMで設定値をモックして検証し、OSのユーザー設定は変更していない。従って実機のOS設定切替は未実施。

## 比較と記録

- `before-1440.png`, `before-390.png`, `before-375.png`
- `after-1440.png`, `after-390.png`, `after-375.png`
- `desktop/mobile/small-mobile-before-after.png`: 同幅の変更前後。
- `desktop/mobile/small-mobile-overlay.png`: 50% overlay。
- `desktop/mobile/small-mobile-reference-before-after.png`: お手本/変更前/変更後。全体高さを引き伸ばしていない。
- `*-people-comparison.png`, `slide2-390.png`, `slide2-375.png`: 先輩の比較と操作結果。
- `before-metrics.json`, `after-metrics.json`, `layout-deltas.json`: ページ座標での数値比較。
- `reveal-runs.json`, `functional-tests.json`, `swipe-tests.json`, `console.json`: 発火・操作記録。
- `pixel-comparison.json`: ピクセル差分の範囲。PCでは32/255を超えるピクセル差0。微小差は画像描画・合成の差、SPの明確な差はドット2個化。見た目と数値の両方を確認した。
