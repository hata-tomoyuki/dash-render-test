from dash import html


def render_home(total_photos: int, unique_barcodes: int) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.H1("📷 写真管理"),
                    html.P(
                        "バーコードで写真を管理",
                        style={"color": "#999", "margin": "0"},
                    ),
                ],
                className="header",
            ),
            html.Div(
                [
                    html.H3(
                        "ようこそ",
                        style={"color": "#ff85b3", "marginBottom": "15px"},
                    ),
                    html.P(
                        "バーコードをスキャンして写真を簡単に管理できます。",
                        style={"color": "#666", "lineHeight": "1.6"},
                    ),
                ],
                className="card-custom",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(str(total_photos), className="stat-number"),
                            html.Div("登録済み写真", className="stat-label"),
                        ],
                        className="stat-box",
                    ),
                    html.Div(
                        [
                            html.Div(str(unique_barcodes), className="stat-number"),
                            html.Div("ユニークなバーコード", className="stat-label"),
                        ],
                        className="stat-box",
                    ),
                ],
                className="stats-container",
            ),
            html.Div(
                [
                    html.H4(
                        "使い方",
                        style={"color": "#ff85b3", "marginBottom": "15px"},
                    ),
                    html.Ol(
                        [
                            html.Li(
                                "「写真を登録」から写真をアップロード",
                                style={"marginBottom": "10px"},
                            ),
                            html.Li(
                                "写真からバーコードを自動検出",
                                style={"marginBottom": "10px"},
                            ),
                            html.Li(
                                "説明を追加して保存",
                                style={"marginBottom": "10px"},
                            ),
                            html.Li(
                                "「写真一覧」で確認",
                                style={"marginBottom": "10px"},
                            ),
                        ],
                        style={"color": "#666", "paddingLeft": "20px"},
                    ),
                ],
                className="card-custom",
                style={"marginTop": "20px"},
            ),
        ]
    )
