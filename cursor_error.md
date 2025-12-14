# エラー対策

## エラー 1 個目

pyzbar が依存する zbar を Render にインストールさせるため、プロジェクト直下に apt.txt を作成して以下を記載します：

```
libzbar0
libzbar-dev
```

## エラー 2 個目

Flask Dash は内部で Flask を使っていますが、Render での依存解決を安定させるために明示的に書いておくと安心です。

gunicorn Render は本番環境で python app.py ではなく WSGI サーバーを使うのが推奨です。 → gunicorn app:app のように起動することで安定稼働します。

Procfile の基本
ファイル名は必ず Procfile（拡張子なし）

アプリのルートディレクトリに置く必要があります

中身は「プロセスタイプ: 実行コマンド」という形式で書きます

例（Dash アプリの場合）：

コード
web: gunicorn app:server
✅ どういう意味？
web: → 「Web サーバーとして動かすプロセス」という意味。外部からの HTTP リクエストを受け付けるのはこのプロセスだけです。

gunicorn app:server → gunicorn という本番用 WSGI サーバーを使って、app.py 内の server という Flask インスタンスを起動する、という指示。 Dash アプリでは通常こう書きます：

python
app = dash.Dash(**name**)
server = app.server # ← これを定義しておく

## エラー 3 個目

【解決方法の可能性】⇒ 表示されず
registration-store を同じプロパティで更新するコールバックが複数あるため、最初のコールバック（バーコード処理側）の Output("registration-store", "data") に allow_duplicate=True を設定しました。Dash では同一 Output を複数コールバックで扱う際にこれを明示しないとアプリ起動時に DuplicateCallbackOutput エラーで画面が描画されません [^dash]。今回表示されなかった原因はこの設定漏れです。
【写真を登録画面のエラー解決策】
sync_tag_checklist と add_custom_tag の両方で tag-checklist（options/value）に出力していたため、Dash の「DuplicateCallbackOutput」保護機構が働き、/register ページのみ 500 エラーで空白表示になっていました。
allow_duplicate=True を追加し、双方のコールバックで同じ Output を扱えるように修正しました。
既存の registration-store に対する複数更新も同様に allow_duplicate=True を設定済み。
【今回の根本的な解決策】
修正しました。問題は、components/sections/barcode_section.py と components/sections/front_photo_section.py で dcc.Upload コンポーネントに無効なキーワード引数 \*\*{"data-camera-upload": "barcode"} を渡していたため、TypeError が発生していました。これにより render_register_page() が例外を投げ、ページが表示されていませんでした。
dcc.Upload は data- 属性を受け付けないため、これを削除しました。JavaScript は id から判断して動作します。

# コールドバック（ページ遷移エラー）の改善策

## 基本的な注意点

### 1.ID の重複・未定義

- Dash では、全てのコンポーネント ID が一意である必要がある
- 複数ページや動的生成で同じ ID を使うと、コールバックが壊れます  
  【対策】
- ID にプレフィックスを付ける
- 動的生成時は、MATCH や ALL 型のコールバックを使用する

### 2.ページ遷移時の状態保持・初期化不足

- ページを切り替えると前のページのコンポーネントが消えるため、コールバックがエラーになります  
  【対策】
- dcc.Location + dcc.Store を使って、状態を保持
- ページごとにレイアウトを分けて、コールバックを分離

### 3.コールバックの依存関係が複雑すぎる

- 多数の INPUT や state を使うと、更新順序が不明確になり、エラーが出やすくなる  
  【対策】
- コールバックを小さく分割して、機能ごとに整理
- prevent_initial_call = True を使って、初期状態読み込み時のエラーを防止

### 4.コールバックの依存関係が壊れている

- 階層追加後に Output や Input の対象が存在しないと Dash がエラーを出してページ描画を止めてしまう  
  【対策】
- 自動範囲は、dcc.Location の href を更新する

### 5.dcc.Location の更新が正しく反映されていない

- ページ遷移に使う dcc.Location の pathname を更新しても、対応するレイアウトが返さないと、空白ページになります

### 6.ページレイアウトが None になっている

- 自動遷移後に layout が空になってしまうと、ページが表示されない  
  【対策】
- ページ毎にレイアウトを関数に定義する

## API 抽出情報を項目毎に自動で反映する時の注意点

### 1.抽出結果を反映するタイミングが早すぎる

- ページがまだ描画されていない状態で、API の結果を反映しようとするとエラーになります  
  【対策】
- prevent_initial_call = True を使って、初期読み込み時のコールバックを防ぐ
- dcc.Store に一度、API 結果を保存 ⇒ ページ描画後に安全に反映

### 2.ページ描画後にタグを反映するコールバックを分離

- dcc.Location の pathname を監視して、ページが表示された後に dcc.Store の内容を反映するようにする

### 3.prevent_initial_call = True を活用

- 初期描画時にコールバックが走らないようにすることで、未描画エラーを防ぎます

### さらに安定：dcc.Interval で遅延反映

- ページ描画後に少し待ってから、タグを反映することで、描画タイミングのズレを抽出できます。
