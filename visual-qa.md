# Visual QA

正解画像は `デザイン案web.png` と `デザイン案mobile.png`。各ループで、同じ幅に正規化した side-by-side / overlay / diff を確認した。

## LOOP 1

### Desktop
- HERO: NG — 見出しとCTAが正解より小さく、背景人物の見え方も弱い。
- 3cards: NG — 背景が白く見え、正解の淡いグレーとのつながりが不足。
- career: NG — カードが小さく、セクション下側の情報密度が低い。
- people / flow / final CTA: NG — 人物・カード・コピーのサイズと縦位置が不足。

### Mobile
- HERO: NG — 見出しが上詰め、CTAが小さく、その下に黒い空白が残る。
- 3cards: NG — 背景差とカード周辺余白が目立つ。
- frontline: NG — セクション末尾の黒い空白が長い。
- career: NG — 外側カードと画像内カードが重なり、二重カードに見える。
- flow / footer: NG — フローが長く、footerが短い。

### 修正内容
- 3cards背景を淡いグレーへ変更。
- careerの外枠・影・背景を削除し、画像主体の構造へ変更。
- HERO、frontline、career、flow、footerのモバイル縦寸法を再設計。

## LOOP 2

### Desktop
- career: 改善 — カード表示を拡大したが、上下の見切れと密度に差が残った。
- people / final CTA: 改善 — 人物とタイトル位置を正解へ寄せた。

### Mobile
- HERO: 改善 — 見出し位置は合ったが、CTAの高さと黒余白が残った。
- career: 改善 — 二重カードは解消。カード内情報の見切れを再調整する必要あり。
- flow: NG — セクション末尾で最終カードがCTAへ近すぎる。

### 修正内容
- SPのセクション境界を正解画像から再計測。
- frontline 509px、career 710px、people 466px、flow 288pxへ調整。
- career画像の表示位置とプラス位置を再設定。

## LOOP 3

### Desktop
- career: PASS — カード群の開始位置・高さ・注釈位置が正解に近接。
- flow: 改善 — タイトルとカード群を上へ寄せた。
- final CTA: 改善 — タイトルのみを下へ寄せ、サブコピーとの間隔を合わせた。

### Mobile
- HERO: 改善 — 黒余白は縮小。CTA自体がまだわずかに低密度。
- frontline / career / people: PASS — セクション境界が正解とほぼ一致。
- flow / final CTA / footer: PASS — 全体の縦位置が正解へ揃った。

### 修正内容
- HERO CTA画像を比率維持で拡大し、wrapper内で左右のみ見切らせた。
- フローのカード高・gap・アイコンサイズをコンパクト化。
- footerを256px相当へ拡張。

## LOOP 4

### Desktop
- 全セクション: PASS — ページ全高は正解比+1px（正規化後）。

### Mobile
- HERO / 3cards / frontline / career / people / flow / final CTA / footer: PASS。
- ページ全高は正解と一致（183×1793pxへ正規化）。

### 修正内容
- 375pxと1280pxでも横スクロールがないことを確認。
- CTAサイズ、CTA間隔、最終CTAのボタン高を最終調整。

## LOOP 5

### Mobile
- HERO: NG — 見出し幅を広げる試行で句点が4行目へ折り返した。

### 修正内容
- 試行を採用せず、3行を維持する58px / line-height 1.02へ戻した。

## LOOP 6

### Desktop / Mobile
- 全対象: PASS。
- Desktop正規化: 661×1805px（正解 661×1804px）。
- Mobile正規化: 183×1793px（正解 183×1793px）。

## LOOP 7

### Mobile
- career: NG — 年収テキスト補完のHTML重ね合わせが素材内文字と競合した。

### 修正内容
- 重ね合わせを不採用とし、元画像を加工せず表示する構成へ復帰。

## LOOP 8（最終）

### Desktop
- HERO: PASS
- 3cards: PASS
- frontline: PASS
- field: PASS
- career: PASS
- people: PASS
- flow: PASS
- final CTA: PASS
- footer: PASS

### Mobile
- HERO: PASS
- 3cards: PASS
- frontline: PASS
- career: PASS
- people: PASS
- flow: PASS
- final CTA: PASS
- footer: PASS

### 最終確認
- 1440px: 横スクロールなし。
- 1280px: `scrollWidth = clientWidth = 1280`。
- 390px: 横スクロールなし。
- 375px: `scrollWidth = clientWidth = 375`。
- モバイルメニュー開閉、career CTA、ENTRY CTAを確認。
- ブラウザconsole error: 0件。

## 自己採点

| 項目 | 点数 | 判定 |
|---|---:|---|
| Desktop visual accuracy | 96 | PASS |
| Mobile visual accuracy | 96 | PASS |
| Layout accuracy | 97 | PASS |
| Spacing accuracy | 97 | PASS |
| CTA accuracy | 98 | PASS |

残存差分は、提供済みHERO・3cards・career等の画像内描画と正解画像内描画の差、および画像内文字の微細な太さのみ。今回の主対象だった余白、背景、二重カード、見切れ、セクション密度、SP崩れにはP0/P1/P2差分なし。
