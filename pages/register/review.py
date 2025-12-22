from dash import html, register_page

from features.review.components import render_review_section


def render_review_page() -> html.Div:
    return html.Div(
        [
            html.Div(
                [html.H1([html.I(className="bi bi-box-seam me-2"), "製品を登録する"])],
                className="header",
            ),
            html.Section(
                [
                    html.H2("STEP 3. API結果とタグ抽出", className="step-title"),
                    html.P(
                        "バーコードから取得した楽天APIの照合結果と、写真から抽出したタグを表示します。",
                        className="step-description",
                    ),
                    html.Div(id="rakuten-lookup-display"),
                    html.Div(id="io-intelligence-tags-display", className="mt-3"),
                ],
                className="step-section",
            ),
            html.Section(
                [
                    html.H2("STEP 4. 微調整と登録", className="step-title"),
                    html.P(
                        "タグやメモを調整し、登録内容を確認してから保存してください。",
                        className="step-description",
                    ),
                    render_review_section(),
                ],
                className="step-section",
            ),
            html.Div(id="register-alert"),
        ]
    )


register_page(
    __name__,
    path="/register/review",
    title="確認・登録 - おしごとアプリ",
)

try:
    layout = render_review_page()
except Exception as e:
    layout = html.Div(
        f"Review page error: {str(e)}", style={"color": "red", "padding": "20px"}
    )


