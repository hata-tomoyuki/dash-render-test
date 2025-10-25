from dash import html


def render_settings(total_photos: int) -> html.Div:
    return html.Div(
        [
            html.Div([html.H1("⚙️ 設定")], className="header"),
            html.Div(
                [
                    html.H4(
                        "アプリ情報",
                        style={"color": "#ff85b3", "marginBottom": "15px"},
                    ),
                    html.Div(
                        [html.Strong("バージョン: "), "1.0.0"],
                        style={"marginBottom": "10px", "color": "#666"},
                    ),
                    html.Div(
                        [html.Strong("登録写真数: "), f"{total_photos} 枚"],
                        style={"marginBottom": "10px", "color": "#666"},
                    ),
                ],
                className="card-custom",
            ),
            html.Div(
                [
                    html.H4(
                        "データ管理",
                        style={"color": "#ff85b3", "marginBottom": "15px"},
                    ),
                    html.Button(
                        "全てのデータを削除",
                        id="delete-all-button",
                        n_clicks=0,
                        className="btn-danger",
                    ),
                    html.Div(id="delete-result", style={"marginTop": "15px"}),
                ],
                className="card-custom",
            ),
            html.Div(
                [
                    html.H4(
                        "使い方",
                        style={"color": "#ff85b3", "marginBottom": "15px"},
                    ),
                    html.P(
                        "このアプリは、商品のバーコードをスキャンして写真を管理するためのアプリです。",
                        style={
                            "color": "#666",
                            "lineHeight": "1.6",
                            "marginBottom": "10px",
                        },
                    ),
                    html.P(
                        "写真をアップロードすると、自動的にバーコードを検出して登録します。",
                        style={"color": "#666", "lineHeight": "1.6"},
                    ),
                ],
                className="card-custom",
            ),
        ]
    )
