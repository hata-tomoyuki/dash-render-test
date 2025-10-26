from dash import dcc, html


def render_review_section() -> html.Div:
    return html.Div(
        [
            html.Div(
                [
                    html.H3("タグを微調整", className="card-title"),
                    html.P(
                        "自動生成されたタグにチェックを付け直せます。不要なタグは外し、必要なタグは追加してください。",
                        className="card-text",
                    ),
                    dcc.Checklist(id="tag-checklist", className="form-check"),
                    html.Div(
                        [
                            dcc.Input(
                                id="custom-tag-input",
                                type="text",
                                placeholder="タグを追加 (例: イベント名)",
                                className="form-control",
                            ),
                            html.Button(
                                "タグを追加",
                                id="add-tag-button",
                                className="btn btn-secondary ms-2",
                            ),
                        ],
                        className="input-group mb-3",
                    ),
                ],
                className="card bg-primary text-white mb-3",
            ),
            html.Div(
                [
                    html.H3("メモ / 特記事項", className="card-title"),
                    dcc.Textarea(
                        id="note-editor",
                        className="form-control",
                        placeholder="タグに補足したい情報や保管場所などを入力できます。",
                        style={"minHeight": "120px"},
                    ),
                ],
                className="card bg-primary text-white mb-3",
            ),
            html.Div(id="review-summary", className="card bg-info text-white mb-3"),
            html.Div(
                html.Button(
                    "保存して登録を完了",
                    id="save-button",
                    className="btn btn-primary",
                    disabled=True,
                ),
                className="card bg-primary text-white mb-3 p-3",
            ),
        ]
    )
