import base64
from typing import Any, Dict, List

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback_context, html
from dash.exceptions import PreventUpdate

from components.layout import create_app_layout
from components.pages import (
    render_gallery,
    render_home,
    render_register_page,
    render_settings,
)
from services.barcode_service import decode_from_base64
from services.photo_service import (
    delete_all_photos,
    insert_photo_record,
    upload_to_storage,
)
from services.supabase_client import get_supabase_client

supabase = get_supabase_client()


def _fetch_home_metrics() -> Dict[str, int]:
    if supabase is None:
        return {"total": 0, "unique": 0}
    try:
        response = supabase.table("photos").select("barcode").execute()
        data = response.data or []
        total = len(data)
        unique = len({item.get("barcode") for item in data if item.get("barcode")})
        return {"total": total, "unique": unique}
    except Exception:
        return {"total": 0, "unique": 0}


def _fetch_photos() -> List[Dict[str, Any]]:
    if supabase is None:
        return []
    try:
        response = (
            supabase.table("photos")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return response.data or []
    except Exception:
        return []


def _fetch_total_photos() -> int:
    return len(_fetch_photos()) if supabase is not None else 0


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no",
        }
    ],
)

app.title = "写真管理アプリ"
app.layout = create_app_layout()


@app.callback(
    [
        Output("page-content", "children"),
        Output("nav-home", "className"),
        Output("nav-register", "className"),
        Output("nav-gallery", "className"),
        Output("nav-settings", "className"),
    ],
    Input("url", "pathname"),
)
def display_page(pathname: str):
    classes = ["nav-button", "nav-button", "nav-button", "nav-button"]

    if pathname == "/register":
        classes[1] = "nav-button active"
        page = render_register_page()
    elif pathname == "/gallery":
        classes[2] = "nav-button active"
        page = render_gallery(_fetch_photos())
    elif pathname == "/settings":
        classes[3] = "nav-button active"
        page = render_settings(_fetch_total_photos())
    else:
        classes[0] = "nav-button active"
        metrics = _fetch_home_metrics()
        page = render_home(metrics["total"], metrics["unique"])

    return [page, *classes]


@app.callback(
    [
        Output("barcode-result", "children"),
        Output("save-button", "disabled"),
        Output("current-photo-data", "data"),
    ],
    [Input("upload-image", "contents"), Input("camera-upload", "contents")],
    [State("upload-image", "filename"), State("camera-upload", "filename")],
)
def process_upload(file_contents, camera_contents, file_filename, camera_filename):
    triggered = callback_context.triggered
    if not triggered:
        return None, True, None

    triggered_id = triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "camera-upload" and camera_contents:
        contents = camera_contents
        filename = camera_filename or "camera_photo.jpg"
    elif triggered_id == "upload-image" and file_contents:
        contents = file_contents
        filename = file_filename
    else:
        raise PreventUpdate

    try:
        decode_result = decode_from_base64(contents)
    except ValueError as exc:
        message = html.Div(
            [
                html.Div(
                    "❌ アップロードエラー",
                    style={"fontWeight": "600", "marginBottom": "10px"},
                ),
                html.Div(str(exc), style={"fontSize": "12px"}),
            ],
            className="alert-custom",
            style={
                "background": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
            },
        )
        return message, True, None

    if not decode_result:
        message = html.Div(
            [
                html.Div(
                    "⚠️ バーコードが検出されませんでした",
                    style={
                        "color": "#ff6b6b",
                        "fontWeight": "600",
                        "marginBottom": "10px",
                    },
                ),
                html.P(
                    "別の写真を試してください。バーコードがはっきり写っている写真を選んでください。",
                    style={"color": "#999", "fontSize": "14px"},
                ),
            ]
        )
        return message, True, None

    preview = html.Div(
        [
            html.Div(
                "✅ バーコード検出成功！",
                style={
                    "color": "#4caf50",
                    "fontWeight": "600",
                    "marginBottom": "15px",
                    "fontSize": "16px",
                },
            ),
            html.Img(
                src=contents,
                style={
                    "width": "100%",
                    "maxHeight": "300px",
                    "objectFit": "contain",
                    "borderRadius": "15px",
                    "marginBottom": "15px",
                },
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Strong("バーコード: ", style={"color": "#ff85b3"}),
                            html.Span(
                                decode_result["barcode"], style={"color": "#333"}
                            ),
                        ],
                        style={"marginBottom": "8px"},
                    ),
                    html.Div(
                        [
                            html.Strong("タイプ: ", style={"color": "#ff85b3"}),
                            html.Span(
                                decode_result["barcode_type"], style={"color": "#333"}
                            ),
                        ]
                    ),
                ],
                style={
                    "background": "#fff9fc",
                    "padding": "15px",
                    "borderRadius": "10px",
                },
            ),
        ]
    )

    store_data = {
        "image_content": contents,
        "filename": filename,
        "barcode": decode_result["barcode"],
        "barcode_type": decode_result["barcode_type"],
        "content_type": decode_result.get("content_type", "image/jpeg"),
    }

    return preview, False, store_data


@app.callback(
    Output("register-alert", "children"),
    Input("save-button", "n_clicks"),
    State("current-photo-data", "data"),
    State("photo-description", "value"),
    prevent_initial_call=True,
)
def save_photo(n_clicks, photo_data, description):
    if not n_clicks:
        raise PreventUpdate

    if not photo_data:
        return html.Div(
            [
                html.Div(
                    "❌ 保存できません",
                    style={"fontWeight": "600", "marginBottom": "5px"},
                ),
                html.Div(
                    "写真を選択または撮影してください。", style={"fontSize": "12px"}
                ),
            ],
            className="alert-custom",
            style={
                "background": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
            },
        )

    if supabase is None:
        return html.Div(
            [
                html.Div(
                    "❌ データベース接続エラー",
                    style={"fontWeight": "600", "marginBottom": "5px"},
                ),
                html.Div(
                    ".envファイルでSupabase設定を確認してください",
                    style={"fontSize": "12px"},
                ),
            ],
            className="alert-custom",
            style={
                "background": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
            },
        )

    try:
        content_string = photo_data["image_content"].split(",", 1)[1]
        file_bytes = base64.b64decode(content_string)
        content_type = photo_data.get("content_type", "image/jpeg")

        image_url = upload_to_storage(
            supabase,
            file_bytes,
            photo_data.get("filename", "photo.jpg"),
            content_type,
        )
        insert_photo_record(
            supabase,
            photo_data["barcode"],
            photo_data["barcode_type"],
            image_url,
            description or "",
        )
    except Exception as exc:
        return html.Div(
            [
                html.Div(
                    "❌ 保存中にエラーが発生しました",
                    style={"fontWeight": "600", "marginBottom": "5px"},
                ),
                html.Div(str(exc), style={"fontSize": "12px"}),
            ],
            className="alert-custom",
            style={
                "background": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
            },
        )

    return html.Div(
        [
            html.Div(
                "✅ 写真が正常に保存されました！",
                style={"fontWeight": "600", "marginBottom": "5px"},
            ),
            html.A(
                "写真一覧を見る",
                href="/gallery",
                style={"color": "#ff85b3", "textDecoration": "underline"},
            ),
        ],
        className="alert-custom",
        style={
            "background": "#d4edda",
            "color": "#155724",
            "border": "1px solid #c3e6cb",
        },
    )


@app.callback(
    Output("delete-result", "children"), Input("delete-all-button", "n_clicks")
)
def handle_delete(n_clicks):
    if not n_clicks:
        raise PreventUpdate

    if supabase is None:
        return html.Div(
            "❌ データベース接続エラー",
            style={
                "color": "#ff6b6b",
                "fontWeight": "600",
                "textAlign": "center",
                "marginTop": "10px",
            },
        )

    try:
        delete_all_photos(supabase)
    except Exception as exc:
        return html.Div(
            f"❌ エラー: {exc}",
            style={
                "color": "#ff6b6b",
                "fontWeight": "600",
                "textAlign": "center",
                "marginTop": "10px",
            },
        )

    return html.Div(
        "✅ 全てのデータを削除しました",
        style={
            "color": "#4caf50",
            "fontWeight": "600",
            "textAlign": "center",
            "marginTop": "10px",
        },
    )


if __name__ == "__main__":
    print("")
    print("=" * 60)
    print("📷 写真管理アプリを起動しています...")
    print("=" * 60)
    print("")
    if supabase is None:
        print("⚠️  警告: Supabaseに接続されていません")
        print("    データベース機能を使用するには、.envファイルを設定してください")
        print("")
    print("🌐 ブラウザで以下のURLにアクセスしてください:")
    print("   http://localhost:8050")
    print("")
    print("📱 スマホからアクセスする場合:")
    print("   http://[あなたのPCのIPアドレス]:8050")
    print("")
    print("=" * 60)
    print("")
    app.run(debug=False, host="0.0.0.0", port=8050)
