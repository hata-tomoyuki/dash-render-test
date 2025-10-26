from dash import html


def render_home(total_photos: int, unique_barcodes: int) -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.H1("📷 写真管理"),
                    html.P(
                        "バーコードで写真を管理",
                        className="text-muted mb-0",
                    ),
                ],
                className="header",
            ),
            html.Div(
                [
                    html.H3(
                        "ようこそ",
                        className="card-title",
                    ),
                    html.P(
                        "バーコードをスキャンして写真を簡単に管理できます。",
                        className="card-text",
                    ),
                ],
                className="card bg-primary text-white mb-3",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        str(total_photos), className="stat-number"
                                    ),
                                    html.Div("登録済み写真", className="stat-label"),
                                ],
                                className="stat-box",
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        str(unique_barcodes), className="stat-number"
                                    ),
                                    html.Div(
                                        "ユニークなバーコード", className="stat-label"
                                    ),
                                ],
                                className="stat-box",
                            ),
                        ],
                        className="d-flex justify-content-around gap-3 mb-4",
                    ),
                ],
                className="card bg-light p-3",
            ),
            html.Div(
                [
                    html.H4(
                        "使い方",
                        className="card-title",
                    ),
                    html.Ol(
                        [
                            html.Li(
                                "「写真を登録」から写真をアップロード",
                                className="mb-2",
                            ),
                            html.Li(
                                "写真からバーコードを自動検出",
                                className="mb-2",
                            ),
                            html.Li(
                                "説明を追加して保存",
                                className="mb-2",
                            ),
                            html.Li(
                                "「写真一覧」で確認",
                                className="mb-2",
                            ),
                        ],
                        className="card-text ps-3",
                    ),
                ],
                className="card bg-primary text-white mb-3 mt-3",
            ),
        ]
    )
