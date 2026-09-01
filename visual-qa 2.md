# LP visual QA — 2026-08-31

現在の判定: 修正中（以前のPASS判定を引き継がない）。

正解: デザイン案web.png (661×1804), デザイン案mobile.png (183×1793)。
比較は左がお手本。1440/390pxの撮影を横幅だけ正規化し、縦には引き伸ばさない。
境界の測定誤差は元画像の約±2px。DesktopのBenefitsはHeroに26px重なる。

## 変更前

PC/SPともコード変更前に撮影済み。
- comparison/20260831-baseline/desktop-1440.png
- comparison/20260831-baseline/mobile-390.png
- Reference/Current startY・endY・height: [境界表](comparison/20260831-baseline/metrics.md)
- 祖先まで含めた矩形クリッピング候補: PC 25件 / SP 19件（透明部分のみの候補も含む）。

### 確認した問題

- Career: PCは122%に拡大したPNGを370pxの箱で隠す。SPは300px幅のPNGを129pxの箱で隠す。年収・本文・右端が欠落。
- CTA: 固定高+overflow:hiddenでボタン下部を切断。
- Titles: 固定高と負のmarginで画像を切断。
- People: SP本文が親の右端を3px越え、overflow:hiddenで欠落。人物も過大。
- Field: scale(1.2)とsection overflow:hiddenにより外周画像が欠落。
- Benefits: 素材内のカードにCSSの白いカードを追加。素材は3枚一体のスプライトしかない。
- Final CTA: 透過余白がある背景PNGをcover表示したため、背面の単色が外周の枠に見える。

## 修正方針

- コンテンツPNGのwidth/height比率は維持。固定高、拡大、overflowによる切断を撤去。
- 画像の透明余白はレイアウト上のみ相殺できるが、クリップ・マスク・再保存はしない。
- 元画像の縦横比が正解と異なる場合、伸縮・本文の切断で隠さず残存差として記録。
- 全体境界は各sectionのpadding/normal flowで調整。下部sectionへのtranslateYは使わない。

## LOOP 1 — 見切れ解除

- PC/SP全体を再撮影し、[境界表](comparison/20260831-loop1/metrics.md)とside-by-side/overlayを保存。
- Career: 外側カードを配置だけのcareer-itemに変更。122%拡大、固定height、overflow:hiddenを削除。4枚の年収・本文・人物を復元。
- CTA/タイトル: 固定heightとoverflow:hiddenを削除。画像比率を維持。
- People: 人物と本文をnormal gridへ移行。絶対配置・固定高・右端切断を撤去。
- Field: 拡大transformとsection clipを撤去。
- 画像クリッピング候補はPC/SP各3件まで減少（既存Benefitsの3枚一体素材のみ）。
- NG: 透明なcanvasまで通常の縦余白として計上したため、Career/Peopleの高さが過大。次のloopで透明余白のレイアウト上の相殺を調整。
- 背景: PCのBenefits外側を実測した#f6f6f6へ。CSSの二重カードを撤去。

## LOOP 2 — セクション高さ

- PC/SP撮影・比較: comparison/20260831-loop2/。
- Careerの透明キャンバスを、自然比率の画像を全描画したままmargin-blockで相殺。PC/SPとも文字を切る祖先要素は0件。
- Fieldは各PNGの透明左右余白を重ねて密度を回復。全画像canvasはviewport内に収まる。
- Peopleの吹き出し・本文の透明余白を整理。人物はheight:autoを維持。
- Final CTA背景は装飾画像の表示範囲だけ調整し、外周枠を除去。ボタン画像は非切断。
- Desktopの全体末尾差は+62pxまで縮小。
- Mobile Careerは全説明文を含めると約1083px。お手本のカード素材と縦横比が異なるため、寸法はNGを維持。
- 境界再測定: 定規付き原寸比較で、SP People→Flow境界は1353px（旧概算1408pxではない）と確認。Career→Peopleは1199px、Hero→Benefitsの最初のカード上端は328px。最新の境界表では修正した実測値を使用する。

## LOOP 3 — padding / margin / gap

- PC/SP撮影・比較: comparison/20260831-loop3/。
- PC各sectionのstart/endは正解換算値と±1px以内。ただし境界一致だけでは視覚PASSにしない。
- People: 見出しをpanel上部と同じgrid領域に配置。本文と吹き出しはflexで透明marginの相殺を安定化。人の上下を切らずnormal gridで整列。
- SP Peopleは331px、Flowは412pxまで調整。実測Referenceはそれぞれ328px / 409px。
- SP Heroは固定高を使わず、内容+paddingで699px（Reference 699px）に整合。
- NG: SP Careerは1083px / Reference727px。提供PNG内の説明文まで全表示すると現在の幅では357px長くなる。全体の累積差の主因として記録。
- Benefitsの単一合成PNGは、個別のカード素材とは区別してNGを維持。次loopでは少なくともカード本体の下端・角丸を切らない表示範囲にする。

## LOOP 4 — 微調整

- PC/SP撮影・比較: comparison/20260831-loop4/。
- Hero PCサブコピー41px・説明24pxに拡大。CTAは全画像表示のままy位置を維持。SPサブコピーの改行をお手本に合わせた（文言変更なし）。
- Frontlineのタイトル・アイコン群を上げ、下部paddingを再配分。sectionの高さは変えない。
- Flow PCの見出しとカード上端を上へ。Footerのロゴ・住所を拡大。
- Benefitsは元PNG内のカード全体（y=300〜720）を含む既存の部分表示に修正。文字・イラスト・下枠は切らない。ただしPNG全体表示ではなく、見切れ検査には依然3件残るためNG。
- SP Benefitsは画像比率からwidthを調整して617.9px。これは元画像を切ってsection高を合わせる処理ではないが、カード幅は正解より狭いため残存差。
- SP People328.1px / Flow409.1px / CTA275.4px。キャリア以外のsection高さは正解と約1px以内。
- 1280/768/375pxで横スクロールなしを確認。768pxではPC用の最低高が余白過多を生んでいるため追加loopへ。

## LOOP 5 — 追加レスポンシブ検証

- PC/SP撮影・比較: comparison/20260831-loop5/。
- 768pxのHero/Benefits/Career/People/CTAでPC専用min-heightを解除または縮小。
- 768〜1023pxはCareerを2列として、読めない4列縮小を回避。
- タブレットの本文サイズを調整し、不自然な1文字だけの折り返しを解消。
- Heroのh1は1つに統一し、改行だけを切り替える。モバイルで見出し全体がaria-hiddenになっていた点も修正。
- 768px再撮影: comparison/20260831-tablet-final/。scrollWidth=clientWidth=768。

## LOOP 6 — 背景位置とCTA左右バランス

- PC/SP撮影・比較: comparison/20260831-loop6/。
- SP Heroの背景だけを拡大して上へ配置。人物頭部のy位置を参考画像へ合わせ、下端まで背景を満たす。本文・ボタン画像は切らない。
- Final CTA PCは列比率・column-gap・左右paddingで位置を合わせた。translateXなし。
- CTAの実クリックで追加問題を発見: 全表示に戻したキャリア画像の透明部分が「キャリアの詳細を見る」の上へ重なり、クリックを奪う場合がある。外観だけで完了にせず、次loopで操作判定を修正。

## LOOP 7 — 非表示領域の操作干渉を修正

- PC/SP撮影・比較: comparison/20260831-loop7/。
- Careerの非操作画像にpointer-events:noneを設定。画像描画や見える内容は変更せず、透明部分のクリック妨害だけを解消。
- 「キャリアの詳細を見る」を再クリックし、#peopleへスクロール（top=0.008px）を確認。
- メニュー開閉・選考フローへの移動・ENTRY・キャリア移動も確認。LINE_URLは未設定の#を維持。
- 全体表示の比率が変形した画像: PC/SPとも0。合成カード以外のクリッピング候補: PC/SPとも0。
- 全imgを対象にしたクリッピング候補はPC25→3、SP19→3。解消はPC22表示箇所/SP16表示箇所。透明canvasのみの旧候補も含むため、「切れた文字38件」とは数えない。

## 判定 — 未完了

| Section | Desktop | Mobile | 見切れ |
|---|---|---|---|
| Hero | PASS | PASS | PASS |
| Benefits | NG（カード寸法・合成素材の部分表示） | NG（カード幅・合成素材の部分表示） | NG（PNG全体表示の条件） |
| Frontline | PASS | PASS | PASS |
| Field | PASS | 非表示維持 | PASS |
| Career | NG（画像内カードの縦横比） | NG（全表示時のsection高+357px） | PASS（4枚の全内容） |
| People | PASS | NG（累積startY、単体の高さはPASS） | PASS |
| Flow | PASS | NG（累積startY、単体の高さはPASS） | PASS |
| Final CTA | PASS | NG（累積startY、単体レイアウトはPASS） | PASS |
| Footer | PASS | NG（累積startY、単体レイアウトはPASS） | PASS |

PASSは今回の対象であるレイアウト・切断に対する判定。支給画像の絵柄・画像内書体・文言配置自体の違いは含めない。Benefits/Careerの寸法差は今回の対象なのでNG。

### 残存差と必要な判断

1. Benefits: 唯一の該当素材は見出し+横3カードの合成画像。3つを縦に並べるための既存の部分表示は、各カードの文字・イラスト・下枠を完全に含めたが、PNGそのものの全体表示ではない。個別カード素材、または合成素材からカードを抽出する許可が必要。
2. Career: 元カードの主な不透明領域の高さ/幅は約0.72 / 0.53 / 0.56 / 0.68。SP正解は約0.35。widthを保ちheight:autoで全内容を見せると同じ高さにはならない。現在の文字可読幅を保つと+357px。小さくしすぎればカード幅と可読性が正解から離れるため、compact版素材の追加か高さ差を許容する判断が必要。
3. LINE/プライバシー/利用規約のURLは未設定。勝手にURLを作らない。

### 検査環境

- 1440×900 / 390×844、DPR=1のChrome全ページ撮影。スクリーンショット実寸1440×3929 / 390×4178。
- 1280/768/375pxも検査。bodyでoverflow-xを隠すことなくscrollWidth=clientWidth。
- 原画像は再保存・削除・加工なし。画像生成なし。
- 既存JSは変更なし。ブラウザ拡張の通信形式と一致するmessage-channel警告5件を記録（LP JSに該当する非同期リスナー処理はない）。LP由来とは断定せず、functional-tests.jsonへ原文を保存。

### overflow全件確認

- .visually-hidden: 読み上げ用テキストの視覚非表示。画像なし。
- .benefit-desktop-card / .benefit-card: 既存の合成PNG部分表示。唯一残るNG。
- それ以外のcontent wrapper、全section、bodyから画像を切断するoverflowを撤去。
- imgのobject-fit:coverは0件。HeroとFinal CTAの装飾背景のみbackground-sizeによる表示範囲調整あり。

## 境界の記録（確定したReference座標で再計算）

## 20260831-baseline

Reference is LEFT; coordinates are CSS px after width-only scaling.
Reference section boundaries were measured manually (±2 source pixels). No vertical stretching.

### desktop

| Section | Ref start | Ref end | Ref height | Current start | Current end | Current height | Δstart | Δend |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hero | 0.0 | 845.3 | 845.3 | 0.0 | 845.0 | 845.0 | 0.0 | -0.3 |
| benefits | 788.6 | 1165.5 | 376.9 | 789.0 | 1165.0 | 376.0 | 0.4 | -0.5 |
| frontline | 1165.5 | 1760.2 | 594.7 | 1165.0 | 1761.0 | 596.0 | -0.5 | 0.8 |
| field | 1760.2 | 2195.9 | 435.7 | 1761.0 | 2168.0 | 407.0 | 0.8 | -27.9 |
| career | 2195.9 | 2694.8 | 498.9 | 2168.0 | 2699.0 | 531.0 | -27.9 | 4.2 |
| people | 2694.8 | 3165.4 | 470.6 | 2699.0 | 3163.0 | 464.0 | 4.2 | -2.4 |
| flow | 3165.4 | 3492.2 | 326.8 | 3163.0 | 3494.0 | 331.0 | -2.4 | 1.8 |
| final-cta | 3492.2 | 3781.9 | 289.7 | 3494.0 | 3784.0 | 290.0 | 1.8 | 2.1 |
| site-footer | 3781.9 | 3930.0 | 148.1 | 3784.0 | 3932.0 | 148.0 | 2.1 | 2.0 |

Bounding-box clipping candidates: 25. This is a geometric test; transparent gutters are not equivalent to clipped text.

### mobile

| Section | Ref start | Ref end | Ref height | Current start | Current end | Current height | Δstart | Δend |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hero | 0.0 | 699.0 | 699.0 | 0.0 | 682.0 | 682.0 | 0.0 | -17.0 |
| benefits | 699.0 | 1317.0 | 618.0 | 682.0 | 1318.0 | 636.0 | -17.0 | 1.0 |
| frontline | 1317.0 | 1828.5 | 511.5 | 1318.0 | 1827.0 | 509.0 | 1.0 | -1.5 |
| career | 1828.5 | 2555.2 | 726.7 | 1827.0 | 2537.0 | 710.0 | -1.5 | -18.2 |
| people | 2555.2 | 2883.4 | 328.2 | 2537.0 | 3003.0 | 466.0 | -18.2 | 119.6 |
| flow | 2883.4 | 3292.6 | 409.2 | 3003.0 | 3291.0 | 288.0 | 119.6 | -1.6 |
| final-cta | 3292.6 | 3567.5 | 274.9 | 3291.0 | 3565.0 | 274.0 | -1.6 | -2.5 |
| site-footer | 3567.5 | 3821.1 | 253.6 | 3565.0 | 3821.0 | 256.0 | -2.5 | -0.1 |

Bounding-box clipping candidates: 19. This is a geometric test; transparent gutters are not equivalent to clipped text.


## 20260831-loop7

Reference is LEFT; coordinates are CSS px after width-only scaling.
Reference section boundaries were measured manually (±2 source pixels). No vertical stretching.

### desktop

| Section | Ref start | Ref end | Ref height | Current start | Current end | Current height | Δstart | Δend |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hero | 0.0 | 845.3 | 845.3 | 0.0 | 845.0 | 845.0 | 0.0 | -0.3 |
| benefits | 788.6 | 1165.5 | 376.9 | 789.0 | 1165.0 | 376.0 | 0.4 | -0.5 |
| frontline | 1165.5 | 1760.2 | 594.7 | 1165.0 | 1760.2 | 595.2 | -0.5 | -0.0 |
| field | 1760.2 | 2195.9 | 435.7 | 1760.2 | 2195.5 | 435.3 | -0.0 | -0.4 |
| career | 2195.9 | 2694.8 | 498.9 | 2195.5 | 2694.5 | 499.0 | -0.4 | -0.3 |
| people | 2694.8 | 3165.4 | 470.6 | 2694.5 | 3164.5 | 470.0 | -0.3 | -0.9 |
| flow | 3165.4 | 3492.2 | 326.8 | 3164.5 | 3491.4 | 326.9 | -0.9 | -0.8 |
| final-cta | 3492.2 | 3781.9 | 289.7 | 3491.4 | 3781.4 | 290.0 | -0.8 | -0.5 |
| site-footer | 3781.9 | 3930.0 | 148.1 | 3781.4 | 3929.4 | 148.0 | -0.5 | -0.6 |

Bounding-box clipping candidates: 3. This is a geometric test; transparent gutters are not equivalent to clipped text.

### mobile

| Section | Ref start | Ref end | Ref height | Current start | Current end | Current height | Δstart | Δend |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hero | 0.0 | 699.0 | 699.0 | 0.0 | 699.0 | 699.0 | 0.0 | -0.0 |
| benefits | 699.0 | 1317.0 | 618.0 | 699.0 | 1316.8 | 617.9 | -0.0 | -0.2 |
| frontline | 1317.0 | 1828.5 | 511.5 | 1316.8 | 1828.1 | 511.3 | -0.2 | -0.4 |
| career | 1828.5 | 2555.2 | 726.7 | 1828.1 | 2911.5 | 1083.4 | -0.4 | 356.3 |
| people | 2555.2 | 2883.4 | 328.2 | 2911.5 | 3239.6 | 328.1 | 356.3 | 356.1 |
| flow | 2883.4 | 3292.6 | 409.2 | 3239.6 | 3648.7 | 409.1 | 356.1 | 356.1 |
| final-cta | 3292.6 | 3567.5 | 274.9 | 3648.7 | 3924.1 | 275.4 | 356.1 | 356.5 |
| site-footer | 3567.5 | 3821.1 | 253.6 | 3924.1 | 4178.1 | 254.0 | 356.5 | 356.9 |

Bounding-box clipping candidates: 3. This is a geometric test; transparent gutters are not equivalent to clipped text.
