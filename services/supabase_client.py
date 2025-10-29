import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"DEBUG Supabase URL: {SUPABASE_URL}")
print(f"DEBUG Supabase key configured: {bool(SUPABASE_KEY)}")


@lru_cache(maxsize=1)
def get_supabase_client() -> Optional[Client]:
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabaseの環境変数が設定されていません。ダミー接続で起動します。")
        return None

    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("DEBUG Supabase client initialized successfully")
        return client
    except Exception as exc:  # pragma: no cover - ログ用
        print(f"Supabase接続エラー: {exc}")
        print("    データベース機能は利用できませんが、UIは表示されます。")
        return None
