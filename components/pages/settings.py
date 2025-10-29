from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


def render_settings(total_photos: int, current_theme: str = "minty") -> html.Div:
    return html.Div(
        [
            html.Div(
                [html.H1([html.I(className="bi bi-gear me-2"), "設定"])],
                className="header",
            ),
            html.Div(
                [
                    html.H4(
                        "アプリ情報",
                        className="card-title",
                    ),
                    html.P(
                        [html.Strong("バージョン: "), "1.0.0"],
                        className="card-text mb-2",
                    ),
                    html.P(
                        [html.Strong("登録写真数: "), f"{total_photos} 枚"],
                        className="card-text mb-0",
                    ),
                ],
                className="card text-white bg-primary mb-3",
            ),
            html.Div(
                [
                    html.H4(
                        "テーマ設定",
                        className="card-title",
                    ),
                    html.P(
                        "アプリの見た目を変更できます。変更後はページをリロードしてください。",
                        className="card-text mb-3",
                    ),
                    dbc.Select(
                        id="theme-selector",
                        options=[
                            {"label": theme.title(), "value": theme}
                            for theme in [
                                "cerulean",
                                "cosmo",
                                "cyborg",
                                "darkly",
                                "flatly",
                                "journal",
                                "litera",
                                "lumen",
                                "lux",
                                "materia",
                                "minty",
                                "morph",
                                "pulse",
                                "quartz",
                                "sandstone",
                                "simplex",
                                "sketchy",
                                "slate",
                                "solar",
                                "spacelab",
                                "superhero",
                                "united",
                                "vapor",
                                "yeti",
                                "zephyr",
                            ]
                        ],
                        value=current_theme,
                        className="mb-3",
                    ),
                    html.Button(
                        "テーマを保存",
                        id="save-theme-button",
                        n_clicks=0,
                        className="btn btn-light",
                    ),
                    html.Div(id="theme-save-result", className="mt-3"),
                ],
                className="card text-white bg-primary mb-3",
            ),
            html.Div(
                [
                    html.H4(
                        "タグ管理",
                        className="card-title",
                    ),
                    html.P(
                        "カラータグ、カテゴリータグ、収納場所タグの設定ができます。",
                        className="card-text mb-3",
                    ),
                    # Color Tags Section - Temporarily disabled
                    dbc.Button(
                        [html.I(className="bi bi-palette me-2"), "カラータグ（準備中）"],
                        color="secondary",
                        outline=True,
                        disabled=True,
                        className="w-100 text-start mb-3",
                    ),
                    html.Div(
                        id="color-tags-container",
                        className="row g-3 mb-4",
                    ),
                    # Color Tag Editor Modal
                    dbc.Modal(
                        [
                            dbc.ModalHeader("カラータグ編集"),
                            dbc.ModalBody(
                                [
                                    html.Div(id="color-tag-editor-content"),
                                ]
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button(
                                        "キャンセル",
                                        id="color-tag-cancel",
                                        className="me-2",
                                    ),
                                    dbc.Button(
                                        "保存", id="color-tag-save", color="primary"
                                    ),
                                ]
                            ),
                        ],
                        id="color-tag-modal",
                        size="lg",
                    ),
                    # Category Tags Section
                    dbc.Button(
                        [html.I(className="bi bi-tags me-2"), "カテゴリータグ"],
                        color="secondary",
                        outline=True,
                        className="w-100 text-start mb-3",
                        style={"cursor": "pointer", "transition": "all 0.2s ease"},
                        id="category-tags-button",
                        n_clicks=0,
                    ),
                    html.Div(
                        id="category-tags-container",
                        className="row g-3 mb-4",
                    ),
                    # Category Tag Editor Modal
                    dbc.Modal(
                        [
                            dbc.ModalHeader("カテゴリータグ編集"),
                            dbc.ModalBody(
                                [
                                    html.Div(id="category-tag-editor-content"),
                                ]
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button(
                                        "キャンセル",
                                        id="category-tag-cancel",
                                        className="me-2",
                                    ),
                                    dbc.Button(
                                        "保存", id="category-tag-save", color="primary"
                                    ),
                                ]
                            ),
                        ],
                        id="category-tag-modal",
                        size="lg",
                    ),
                    # Receipt Location Tags Section
                    dbc.Button(
                        [html.I(className="bi bi-box-seam me-2"), "収納場所タグ"],
                        color="secondary",
                        outline=True,
                        className="w-100 text-start mb-3",
                        style={"cursor": "pointer", "transition": "all 0.2s ease"},
                        id="receipt-location-tags-button",
                        n_clicks=0,
                    ),
                    html.Div(
                        id="receipt-location-tags-container",
                        className="row g-3 mb-4",
                    ),
                    # Receipt Location Tag Editor Modal
                    dbc.Modal(
                        [
                            dbc.ModalHeader("収納場所タグ編集"),
                            dbc.ModalBody(
                                [
                                    html.Div(id="receipt-location-tag-editor-content"),
                                ]
                            ),
                            dbc.ModalFooter(
                                [
                                    dbc.Button(
                                        "キャンセル",
                                        id="receipt-location-tag-cancel",
                                        className="me-2",
                                    ),
                                    dbc.Button(
                                        "保存",
                                        id="receipt-location-tag-save",
                                        color="primary",
                                    ),
                                ]
                            ),
                        ],
                        id="receipt-location-tag-modal",
                        size="lg",
                    ),
                    html.Button(
                        "タグ設定を保存",
                        id="save-tags-button",
                        n_clicks=0,
                        className="btn btn-success",
                    ),
                    html.Div(id="tags-save-result", className="mt-3"),
                ],
                className="card text-white bg-success mb-3",
            ),
            html.Div(
                [
                    html.H4(
                        "データ管理",
                        className="card-title",
                    ),
                    html.Button(
                        "全てのデータを削除",
                        id="delete-all-button",
                        n_clicks=0,
                        className="btn btn-danger w-100",
                        style={"cursor": "pointer", "transition": "all 0.2s ease"},
                    ),
                    html.Div(id="delete-result", className="mt-3"),
                ],
                className="card text-white bg-secondary mb-3",
            ),
            html.Div(
                [
                    html.H4(
                        "使い方",
                        className="card-title",
                    ),
                    html.P(
                        "このアプリは、商品のバーコードをスキャンして写真を管理するためのアプリです。",
                        className="card-text mb-3",
                    ),
                    html.P(
                        "写真をアップロードすると、自動的にバーコードを検出して登録します。",
                        className="card-text mb-0",
                    ),
                ],
                className="card text-white bg-primary mb-3",
            ),
        ]
    )
