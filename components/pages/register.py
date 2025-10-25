from dash import html

from components.upload_section import render_register_section


def render_register_page() -> html.Div:
    return html.Div(
        [
            html.Div([html.H1("📸 写真を登録")], className="header"),
            render_register_section(),
        ]
    )
