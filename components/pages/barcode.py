from dash import html

from components.sections import render_barcode_section


def render_barcode_page() -> html.Div:
    return html.Div(
        [
            html.Div([html.H1("📦 製品を登録する")], className="header"),
            html.Section(
                [
                    html.H2("STEP 1. バーコードの取得", className="step-title"),
                    html.P(
                        "バーコードを読み取る / アップロードする / 番号を手入力するのいずれかで情報を取得します。",
                        className="step-description",
                    ),
                    render_barcode_section(),
                    html.Div(id="barcode-feedback"),
                ],
                className="step-section",
            ),
        ]
    )
