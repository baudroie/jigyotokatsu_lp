# SPキャリア中央揃え・LINE URL設定

## 今回の変更

- `index.html`: SPキャリアの＋画像4点、キャリア詳細CTAを撤去。LINEリンク2か所のHTML hrefを指定URLへ更新。CSS/JSのキャッシュ識別子を更新。
- `styles.css`: アイコン専用列と不要になったCTA用CSSを撤去。SPカード幅を維持し、グリッド自体を中央配置。
- `script.js`: LINE_URLを指定URLへ更新。
- `README.md`: 最新変更とリンク設定済みの状態を記録。
- 元画像、ZIP、過去の比較資料には変更なし。公開・デプロイなし。

## 結果

| 検証 | 判定 | 結果 |
|---|---|---|
| SP＋撤去 | PASS | DOM内0件 |
| キャリア内ボタン撤去 | PASS | リンク・ボタン0件 |
| SPカード中央揃え | PASS | 390pxで4枚とも画像中心195px |
| 画像サイズ維持 | PASS | 390pxで348×535.383px、変更前後同一。左端7px→21px |
| PC表示維持 | PASS | 1440pxで4列・各331.25px |
| 素材切り替え | PASS | 767pxまでSP、768px以上PC、4枚の順番維持 |
| 横はみ出し | PASS | 375/390/430/767/768/1440pxでscrollWidth=viewport幅 |
| LINE設定 | PASS | HERO・最終CTAとも指定URL。HTMLと実DOMのhrefを確認 |
| JavaScript | PASS | node --check script.js成功 |

LINEの外部ページには遷移していません。リンク先のサービス稼働や登録処理は今回の検証範囲外です。

## 記録

- `verification.json`: 6画面幅の画像寸法、中心位置、currentSrc、リンクURL。
- `before-mobile-career.png` / `after-mobile-career.png`: SPキャリアの変更前後。
- `after-desktop-career.png`: PCキャリア表示。
- `after-mobile.png`: SP全ページ表示。

## 既知の差分

今回は＋・ボタン撤去と中央揃え・LINE設定のみの追加修正です。新SP素材の縦長比率による完成デザインとの全ページ高さの不一致は引き続き残ります。今回の指定変更はPASSですが、LP全体の寸法一致が完了したという判定ではありません。
