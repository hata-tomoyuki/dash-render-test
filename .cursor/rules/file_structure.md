# 基本品質基準（常時適用）

Apply Mode: Always Apply

# このファイルは Cursor への指示用です。【このファイルの内容を修正禁止】

# 最低限のファイル構成

- app.py # Dash アプリのメインファイル
- server.py # Flask(Supabase JWT 保護の入口)
- pages/ # ルーティング対象（登録+レイアウト+ページ固有 callback）
  - home.py
- features/ # 機能別モジュール（UI 断片・コールバックサービスの結合部）
  - barcode/
    - componets.py # UI 断片（ページ固有の UI）
    - controller.py # コールバック(UI⇔services の橋渡し)
- components/ # 再利用可能なコンポーネント・UI 部分（ページ横断のナビ、ヘッダー、フッター、モーダル等）
  - layout.py # 全体レイアウト構成
  - upload_section.py # 画像・バーコードアップロード UI
- services/ # ロジック(API 呼び出し・照合処理など）※UI 非依存
  - barcode_service.py # バーコード解析
  - photo_service.py # 画像ストレージ・DB への CRUD
  - barcode_lookup.py # 楽天 API などでバーコード照合
  - image_description.py # IO Intelligence API で画像説明生成
  - tag_extraction.py # タグ抽出処理
  - db_handler.py # DB 登録・取得処理
- assets/ # CSS や画像などの静的ファイル
  - styles.css # デザイン調整用 CSS
  - camera.js
- tests/ # テストコードの全てをまとめる
- .cursor/
  - rules/ # cursor への指示
    - file_structure.md # フォルダ構成指示
    - spec.md # Cursor に伝えるようの仕様書
    - database_configuration.md # データベース構成指示
- apt.txt # 使用ライブラリ一覧（OS レベル）
- requirements.txt # 使用ライブラリ一覧（Python レベル）
- .env # API キーなどの環境変数
- .env.example # API キーなどの環境変数テンプレート
- README.md # プロジェクト説明・使い方・構成
- Cursor.md # Cursor が修正した内容説明
- cursor_error.md # Cursor と開発者の共同エラー解決記録
- .gitignore
- Dockerfile # Render の起動に必要。Python だけでは、写真が無理だった。
- supabase #使用する可能性があるので、残す。簡易 DB

# 注意事項

他に必要なファイルがあれば、残してください
不要なファイルやフォルダは、開発者に確認後に消去してください
