from dash import html, register_page

from features.barcode.components import render_barcode_section


def render_barcode_page() -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.Div(id="register-success-banner", className="mb-2"),
                    html.H1([html.I(className="bi bi-box-seam me-2"), "製品を登録する"]),
                ],
                className="header",
            ),
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


register_page(
    __name__,
    path="/register/barcode",
    title="バーコード登録 - おしごとアプリ",
)

try:
    layout = render_barcode_page()
except Exception as e:
    layout = html.Div(
        f"Barcode page error: {str(e)}", style={"color": "red", "padding": "20px"}
    )


