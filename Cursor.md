# Cursor メモ

## 目的

- 写真管理アプリ (Dash) をフレームワーク非依存な構造に整理。
- UI とロジックを `components/` / `services/` に分離して、将来 React / Flask 等へ移植しやすくした。
- Supabase を簡易 DB として扱うが、利用しない場合でも UI が動くように防衛コードを追加。

## 主な変更

- `components/` にレイアウト・ページ・登録セクションを分割。
- `services/` に Supabase 接続とバーコード解析・写真保存処理を関数化して配置。
- CSS / JavaScript を `assets/` へ移動 (`styles.css`, `camera.js`)。Dash の自動ロード機能を利用。
- `app.py` はルーティングとコールバックのハブのみ担当。UI は Components、データ処理は Services を呼び出す構造。
- `data/products.json` など spec.md が示すフォルダを準備。
- README をユーザー向けに刷新。旧 README/QUICKSTART は統合済み。

## Supabase まわり

- `.env` が未設定でも動作し、警告表示のみ。
- 将来別 DB へ差し替える場合は `services/photo_service.py` と `supabase_client.py` の実装を置き換えれば良い。

## TODO 候補

- services 層に楽天 API / タグ抽出など spec で求められている機能を追加。
- Supabase を使わないローカル JSON / SQLite ストレージ実装の検証。
- Dash から別フレームワーク (FastAPI + React 等) へ移行する際は Components をテンプレート化して再利用。

## 注意点

- `spec.md` は仕様書なので編集禁止。
- 外部サービス (GitHub/Render) へのデプロイはこの環境からは実行できない。利用時はローカルで実施すること。
