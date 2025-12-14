from dash import html, register_page

from features.photo.components import render_front_photo_section


def render_photo_page() -> html.Div:
    return html.Div(
        [
            html.Div(
                [html.H1([html.I(className="bi bi-box-seam me-2"), "製品を登録する"])],
                className="header",
            ),
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


register_page(
    __name__,
    path="/register/photo",
    title="写真登録 - おしごとアプリ",
)

try:
    layout = render_photo_page()
except Exception as e:
    layout = html.Div(
        f"Photo page error: {str(e)}", style={"color": "red", "padding": "20px"}
    )
