import base64
import datetime
import gc
import os
import re
import tempfile
from typing import Any, Dict, List, Optional

import dash
from dash import (
    Input,
    Output,
    State,
    callback_context,
    html,
    dcc,
    no_update,
    page_container,
)
from dash.exceptions import PreventUpdate

from components.layout import create_app_layout
from components.theme_utils import load_theme, get_bootswatch_css
from components.state_utils import empty_registration_state
from components.layout import _build_navigation
from copy import deepcopy

# Load environment variables EARLY so services read correct .env (models, flags)
try:
    from dotenv import load_dotenv

    load_dotenv()
    print("DEBUG: Early .env loaded before services imports")
except Exception as _early_env_err:
    print(f"DEBUG: Early .env load skipped: {_early_env_err}")

# In-memory storage for demo purposes when Supabase is not available
PHOTOS_STORAGE: List[Dict[str, Any]] = []

# テーマ関連関数は components/theme_utils.py に移動


# pages機能によりページ関数は直接インポート不要
from services.barcode_lookup import (
    lookup_product_by_barcode,
    lookup_product_by_keyword,
)
from services.io_intelligence import describe_image
from services.tag_extraction import extract_tags
from services.barcode_service import decode_from_base64
from services.photo_service import (
    delete_all_products,
    get_all_products,
    get_product_stats,
    insert_product_record,
    insert_photo_record,
    list_storage_buckets,
    upload_to_storage,
)
from services.supabase_client import get_supabase_client
from components.state_utils import (
    empty_registration_state,
    ensure_state,
    serialise_state,
)

supabase = get_supabase_client()


# データ取得関数は services/data_service.py に移動


PLACEHOLDER_IMAGE_URL = "https://placehold.co/600x600?text=No+Photo"


# UIレンダリング関数は components/ui_components.py に移動


# _update_tags関数は services/tag_service.py に移動


# テーマ関連処理は components/theme_utils.py に移動

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    use_pages=True,
    # allow_duplicate を使うコールバックがあるため initial_duplicate を指定
    prevent_initial_callbacks="initial_duplicate",
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no",
        }
    ],
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
    ],
)
server = app.server
app.title = "推し活グッズ管理"


# serve_layout関数は削除（pages機能では不要）


# ページ切り替えコールバックはDash pages機能により不要


# Xシェアコールバックは features/photo/controller.py に移動
def toggle_x_share(n_clicks, text_value):
    # Show config after first click; keep visible afterwards
    visible = {"display": "block"} if (n_clicks or 0) > 0 else {"display": "none"}
    length = len(text_value) if text_value else 0
    return visible, f"文字数: {length}/280"


# バーコード関連コールバックは features/barcode/controller.py に移動


# 古いprocess_tags関数は削除（インターバルベースに変更）


# render_tag_feedbackコールバックは features/review/controller.py に移動


# 写真関連コールバックは features/photo/controller.py に移動


# 写真アップロード後のページ遷移
# auto_navigate_on_photo_uploadコールバックは features/photo/controller.py に移動


# toggle_save_buttonコールバックは features/review/controller.py に移動


# sync_tag_checklistコールバックは features/review/controller.py に移動


# add_custom_tagコールバックは features/review/controller.py に移動


# レビュー関連コールバックは features/review/controller.py に移動


# update_photo_thumbnailは features/review/controller.py に移動


# process_tagsは features/review/controller.py に移動


# trigger_auto_fill_on_page_changeコールバックは features/review/controller.py に移動


# auto_fill_form_from_tagsコールバックは features/review/controller.py に移動


# display_api_resultsコールバックは features/review/controller.py に移動


# save_registration関数は services/registration_service.py に移動


# テーマ関連コールバックは components/theme_utils.py に移動


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8050))

    # .envファイルから環境変数を読み込む
    try:
        from dotenv import load_dotenv

        load_dotenv()
        print("DEBUG: Loaded environment variables from .env file")
    except ImportError:
        print("DEBUG: python-dotenv not available, using system environment variables")

    # テスト: IO Intelligence APIキーの確認
    import os

    # 環境変数が設定されていない場合のみテスト用キーを設定
    current_key = os.getenv("IO_INTELLIGENCE_API_KEY")
    if not current_key:
        os.environ["IO_INTELLIGENCE_API_KEY"] = "test_key_for_debugging"
        print("DEBUG: Set test IO_INTELLIGENCE_API_KEY for debugging")
    else:
        print(
            f"DEBUG: Using existing IO_INTELLIGENCE_API_KEY (length: {len(current_key)})"
        )

    from services.io_intelligence import IO_API_KEY, describe_image

    print(f"DEBUG: IO_API_KEY is set: {bool(IO_API_KEY)}")
    if IO_API_KEY:
        print(f"DEBUG: IO_API_KEY length: {len(IO_API_KEY)}")
        print(
            f"DEBUG: IO_API_KEY starts with: {IO_API_KEY[:10] if IO_API_KEY else 'None'}..."
        )

        # 本番では起動時のdescribe_imageテスト呼び出しは行わない
    else:
        print("DEBUG: IO_API_KEY is still not set - this should not happen")

    # 機能別controllerの登録
    from features.barcode.controller import register_barcode_callbacks
    from features.photo.controller import register_photo_callbacks
    from features.review.controller import register_review_callbacks
    from components.theme_utils import register_theme_callbacks

    register_barcode_callbacks(app)
    register_photo_callbacks(app)
    register_review_callbacks(app)
    register_theme_callbacks(app)

    # Dash Pages推奨: page_container に任せ、Location はPages側を使用
    app.layout = html.Div(
        [
            html.Link(
                rel="stylesheet",
                href=get_bootswatch_css(load_theme()),
                id="bootswatch-theme",
            ),
            dcc.Location(id="nav-redirect", refresh=False),  # 独自遷移用
            dash.page_container,  # ページ内容は Pages 側が挿入
            _build_navigation(),  # 共通ナビ
            dcc.Store(
                id="registration-store", data=deepcopy(empty_registration_state())
            ),
            html.Div(id="auto-fill-trigger", style={"display": "none"}),
        ]
    )

    app.run(host="0.0.0.0", port=port)
