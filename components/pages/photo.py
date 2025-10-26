from dash import html

from components.sections import render_front_photo_section


def render_photo_page() -> html.Div:
    return html.Div(
        [
            html.Div([html.H1("📦 製品を登録する")], className="header"),
            html.Section(
                [
                    html.H2("STEP 2. 正面写真の登録", className="step-title"),
                    html.P(
                        "グッズの正面がしっかり写る写真を撮影またはアップロードしてください。スキップも選択できます。",
                        className="step-description",
                    ),
                    render_front_photo_section(),
                    html.Div(id="front-feedback"),
                ],
                className="step-section",
            ),
        ]
    )
