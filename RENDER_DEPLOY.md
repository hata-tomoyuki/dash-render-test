# Render デプロイガイド

このアプリをRenderにデプロイする手順です。

## 方法1: Webサービスとしてデプロイ（推奨）

### 手順1: Renderアカウントの準備

1. [Render](https://render.com/)にアクセスしてアカウントを作成
2. GitHubアカウントと連携

### 手順2: 新しいWebサービスを作成

1. Renderダッシュボードで「New +」→「Web Service」を選択
2. GitHubリポジトリを選択（`hata-tomoyuki/dash-render-test`）
3. 以下の設定を入力：

   **基本設定:**
   - **Name**: `oshi-app`（任意）
   - **Region**: `Oregon (US West)` または最寄りのリージョン
   - **Branch**: `main` または `master`
   - **Root Directory**: （空白のまま）
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn server:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --worker-class gthread`

   **環境変数:**
   以下を「Environment Variables」セクションで追加：

   ```
   PORT=8050
   PYTHON_VERSION=3.11.0

   # Supabase設定（必須: データ保存機能を使用する場合）
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key

   # 認証機能を使用する場合
   APP_BASE_URL=https://your-app-name.onrender.com
   COOKIE_SECURE=true
   COOKIE_SAMESITE=Lax

   # IO Intelligence API（オプション）
   IO_INTELLIGENCE_API_KEY=your-api-key

   # 楽天API（オプション）
   RAKUTEN_APPLICATION_ID=your-application-id
   RAKUTEN_AFFILIATE_ID=your-affiliate-id
   ```

### 手順3: システム依存関係の設定

Renderは`zbar`ライブラリを自動インストールできないため、以下のいずれかの方法を使用：

#### オプションA: Buildpackを使用（推奨）

1. 「Advanced」セクションで「Build Command」を以下に変更：
   ```bash
   apt-get update && apt-get install -y libzbar0 && pip install -r requirements.txt
   ```

   ただし、Renderの無料プランでは`apt-get`が使えない場合があります。

#### オプションB: Dockerを使用（推奨）

1. 「Environment」で「Docker」を選択
2. Dockerfileが自動的に使用されます
3. この方法が最も確実です

### 手順4: デプロイ

1. 「Create Web Service」をクリック
2. 初回ビルドが開始されます（5-10分かかる場合があります）
3. デプロイが完了すると、`https://your-app-name.onrender.com` でアクセス可能

## 方法2: Dockerを使用したデプロイ

### 手順

1. Renderダッシュボードで「New +」→「Web Service」を選択
2. GitHubリポジトリを選択
3. 「Environment」で「Docker」を選択
4. 環境変数を設定（方法1と同じ）
5. 「Create Web Service」をクリック

Dockerfileが自動的に使用され、`zbar`ライブラリも含めてビルドされます。

## 環境変数の設定

### 必須（Supabaseを使用する場合）

- `SUPABASE_URL`: SupabaseプロジェクトのURL
- `SUPABASE_KEY`: Supabaseのanon key

### 推奨

- `APP_BASE_URL`: デプロイ後のアプリURL（認証機能を使用する場合）
- `COOKIE_SECURE`: `true`（HTTPS使用時）
- `PORT`: `8050`（Renderが自動設定するため通常は不要）

### オプション

- `IO_INTELLIGENCE_API_KEY`: 画像解析機能用
- `RAKUTEN_APPLICATION_ID`: バーコード検索機能用
- `RAKUTEN_AFFILIATE_ID`: アフィリエイト用

## トラブルシューティング

### ビルドエラー: zbarが見つからない

**解決方法**: Dockerを使用するか、以下のBuild Commandを使用：

```bash
apt-get update && apt-get install -y libzbar0 && pip install -r requirements.txt
```

### アプリが起動しない

1. ログを確認（Renderダッシュボードの「Logs」タブ）
2. 環境変数が正しく設定されているか確認
3. `PORT`環境変数が設定されているか確認（Renderが自動設定するため通常は不要）

### データベースエラー

1. Supabaseのテーブルが作成されているか確認
2. `supabase/sql/create_all_tables.sql`をSupabaseで実行
3. RLSポリシーが正しく設定されているか確認

### 認証エラー

1. `APP_BASE_URL`が正しく設定されているか確認（`https://your-app-name.onrender.com`）
2. `COOKIE_SECURE=true`に設定
3. Supabaseの認証設定を確認

## 無料プランの制限

- 15分間の非アクティブ後にスリープ（次回アクセス時に自動起動、30秒程度かかる）
- 月間750時間の使用制限
- 512MB RAM

本番環境では有料プラン（Starter以上）の使用を推奨します。

## カスタムドメインの設定

1. Renderダッシュボードで「Settings」→「Custom Domains」
2. ドメインを追加
3. DNS設定を更新

## 参考リンク

- [Render公式ドキュメント](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Docker on Render](https://render.com/docs/docker)

