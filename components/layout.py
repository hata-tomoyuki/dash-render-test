from dash import dcc, html

NAV_ITEMS = [
    {"href": "/", "label": "ホーム", "icon": "🏠", "id": "nav-home"},
    {"href": "/register", "label": "写真を登録", "icon": "📸", "id": "nav-register"},
    {"href": "/gallery", "label": "写真一覧", "icon": "🖼️", "id": "nav-gallery"},
    {"href": "/settings", "label": "設定", "icon": "⚙️", "id": "nav-settings"},
]


def _build_navigation():
    return html.Div(
        [
            html.A(
                [
                    html.Div(item["icon"], className="nav-icon"),
                    html.Div(item["label"], className="nav-label"),
                ],
                href=item["href"],
                className="nav-button",
                id=item["id"],
            )
            for item in NAV_ITEMS
        ],
        className="bottom-nav",
    )


def create_app_layout():
    """Return the root Dash layout."""
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content", className="page-container"),
            _build_navigation(),
            dcc.Store(id="current-photo-data"),
        ]
    )
