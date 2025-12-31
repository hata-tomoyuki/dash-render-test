# 開発者向けメモ（最新仕様・起動必須）

## 概要

- Dash Pages を使用し、`_pages_location.pathname` を更新してページ遷移する構成。`app.py` で `.env` を最初に読み込み、`create_app()` が `app` / `server` を生成（Gunicorn は `app:server` を起動）。
- Supabase 未設定でも UI は起動するが、保存・ギャラリー・テーマ永続化は無効。

## 起動手順（PowerShell）

- 通常:
  ```powershell
  cd C:\Users\ryone\Desktop\oshi-app
  python app.py
  ```
- ログ付き強制起動（依頼時は必ずこれ）:
  ```powershell
  cd C:\Users\ryone\Desktop\oshi-app
  powershell -ExecutionPolicy Bypass -File .\start_with_logs.ps1
  ```
  - 既存 python プロセス停止、UTF-8/アンバッファ、`.venv` 優先、`app_run.log` に保存。
  - ログ確認: `Get-Content app_run.log -Tail 50`
- ブラウザ: `http://127.0.0.1:8050`（Ctrl+Shift+R でハードリロード）
- 停止: `Ctrl+C` または `Stop-Process -Name python -ErrorAction SilentlyContinue`

## 環境変数

- ローカルは `.env`（例: `SUPABASE_URL`, `SUPABASE_KEY`, `RAKUTEN_APP_ID`, `IO_INTELLIGENCE_API_KEY` など）。
- `.dockerignore` により `.env` はイメージに入らない。Render では Environment Variables で同名を必ず設定。

## 登録 3 ステップ仕様（正しい挙動）

- URL: `/register/barcode` → `/register/photo` → `/register/review`。`/register` 直叩きは `/register/barcode` へリダイレクト。
- 自動遷移の責務: 各ステップのコールバックが成功/スキップ時に `_pages_location.pathname` を更新して次ページへ進める。
  - バーコード: `status in {captured, manual, skipped}` → `/register/photo`
  - 正面写真: `status in {captured, skipped}` → `/register/review`
- 楽天 API 結果やタグはレビュー画面で表示。
- 注意: 「ナビから登録開始したら常に新規開始」のため、`/register/barcode` に外部から入った場合は `registration-store` を初期化する。

## Supabase 接続確認（ローカル）

- コマンド:
  - `python .\scripts\check_supabase.py`
  - `python .\scripts\check_supabase.py --json`（JSON 出力）
  - `python .\scripts\check_supabase.py --write`（安全な書き込みテスト）
- 判定の目安:
  - `db.*.ok=False` かつ `permission denied` → RLS/ポリシーの可能性大
  - `db.*.ok=True` で `rows=0` → 権限は通るがデータ無し
  - `storage.photos_list.ok=False` → Storage ポリシー/バケット/キーを確認

## Render / Docker

- `Dockerfile`: python:3.11-slim, `libzbar0` 必要、`gunicorn app:server`、`PORT` デフォルト 8050、`EXPOSE 8050`、ヘルスチェック有り。
- Render (docker_web_service) では ENV に `SUPABASE_URL`, `SUPABASE_KEY`, `RAKUTEN_APP_ID`, `IO_INTELLIGENCE_API_KEY` 等を設定すること。
- `.dockerignore` で `.env`, ログ, DB, tests などを除外済み。

## よくある不具合と確認ポイント

- 画面が出ない/真っ白: ブラウザコンソールの赤エラーと `/_dash-update-component` を確認。DuplicateCallback エラー時は `allow_duplicate=True` を付ける。
- エラー共有方法：Console で Duplicate callback outputs をテキスト検索
- 自動遷移しない: `registration-store` の status 更新と `_pages_location.pathname` が更新されているかを確認。
- Supabase 取得失敗: Network タブで `supabase.co` のレスポンスを確認。`permission denied` は RLS、`0 rows` はデータ不足。
- カメラ不具合: `assets/camera.js` がロードされているか、ブラウザのカメラ許可を確認。

## ディレクトリ案内

- `app.py`: エントリ。Dash Pages、`_pages_location` 遷移、`.env` 早期読込。
- `pages/`: Dash Pages の各ページ（`register/` 配下に登録フロー、settings/home/gallery 等）。
- `features/`: 各機能のコールバックロジック（barcode/photo/review）。
- `components/`: 共通 UI・ナビ・テーマ周り。
- `services/`: Supabase や外部 API（barcode_lookup, photo_service, theme_service 等）。
- `assets/`: `styles.css`, `camera.js`（自動ロード）。
- `scripts/check_supabase.py`: 接続/権限ヘルスチェック。
