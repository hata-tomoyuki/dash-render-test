#!/bin/bash

echo "📷 写真管理アプリのセットアップを開始します..."
echo ""

echo "1️⃣ Pythonのバージョンを確認しています..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3がインストールされていません。"
    echo "   Python 3.8以上をインストールしてください。"
    exit 1
fi

echo ""
echo "2️⃣ 必要なパッケージをインストールしています..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ パッケージのインストールに失敗しました。"
    exit 1
fi

echo ""
echo "3️⃣ zbarライブラリの確認..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   macOSを検出しました。"
    if ! command -v brew &> /dev/null; then
        echo "   ⚠️  Homebrewがインストールされていません。"
        echo "   zbarを手動でインストールしてください: brew install zbar"
    else
        echo "   zbarをインストールしています..."
        brew install zbar
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   Linuxを検出しました。"
    echo "   zbarをインストールしています..."
    sudo apt-get update
    sudo apt-get install -y libzbar0
fi

echo ""
echo "4️⃣ .envファイルの確認..."
if [ ! -f .env ]; then
    echo "❌ .envファイルが見つかりません。"
    echo "   Supabaseの設定を含む.envファイルを作成してください。"
    exit 1
fi

echo "✅ .envファイルが見つかりました。"

echo ""
echo "✅ セットアップが完了しました！"
echo ""
echo "アプリケーションを起動するには以下のコマンドを実行してください："
echo "  python3 app.py"
echo ""
echo "ブラウザで http://localhost:8050 にアクセスしてください。"
