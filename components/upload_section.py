from dash import dcc, html


def render_register_section() -> html.Div:
    return html.Div(
        [
            html.Div(
                dcc.Upload(
                    id="upload-image",
                    children=html.Div(
                        [
                            html.Div(
                                "📁", style={"fontSize": "48px", "marginBottom": "10px"}
                            ),
                            html.Div(
                                "ファイルから選択",
                                style={
                                    "fontSize": "16px",
                                    "fontWeight": "600",
                                    "color": "#ff85b3",
                                },
                            ),
                            html.Div(
                                "タップして写真を選択",
                                style={
                                    "fontSize": "12px",
                                    "color": "#999",
                                    "marginTop": "5px",
                                },
                            ),
                        ]
                    ),
                    className="upload-area",
                    multiple=False,
                ),
                className="card-custom",
            ),
            html.Div(
                [
                    html.Div(
                        "またはカメラを利用",
                        style={
                            "color": "#666",
                            "fontWeight": "600",
                            "textAlign": "center",
                            "marginBottom": "12px",
                        },
                    ),
                    html.Button(
                        [
                            html.Div(
                                "📷", style={"fontSize": "48px", "marginBottom": "10px"}
                            ),
                            html.Div(
                                "カメラを起動",
                                style={
                                    "fontSize": "16px",
                                    "fontWeight": "600",
                                    "color": "#ff85b3",
                                },
                            ),
                            html.Div(
                                "タップして撮影",
                                style={
                                    "fontSize": "12px",
                                    "color": "#999",
                                    "marginTop": "5px",
                                },
                            ),
                        ],
                        id="camera-trigger-button",
                        className="camera-button",
                        style={"border": "none", "outline": "none", "width": "100%"},
                    ),
                    html.Video(
                        id="camera-video",
                        autoPlay=True,
                        muted=True,
                        style={
                            "width": "100%",
                            "maxWidth": "500px",
                            "borderRadius": "15px",
                            "display": "none",
                            "margin": "20px auto 0",
                        },
                    ),
                    html.Canvas(id="camera-canvas", style={"display": "none"}),
                    html.Div(
                        [
                            html.Button(
                                "📸 撮影",
                                id="capture-button",
                                className="btn-custom",
                                style={"display": "none", "marginTop": "10px"},
                            ),
                            html.Button(
                                "❌ キャンセル",
                                id="cancel-camera-button",
                                style={
                                    "display": "none",
                                    "marginTop": "10px",
                                    "background": "#999",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "25px",
                                    "padding": "12px 30px",
                                    "fontWeight": "600",
                                    "cursor": "pointer",
                                    "width": "100%",
                                },
                            ),
                        ],
                        style={
                            "textAlign": "center",
                            "maxWidth": "500px",
                            "margin": "0 auto",
                        },
                    ),
                    dcc.Upload(
                        id="camera-upload",
                        children=html.Div(),
                        style={"display": "none"},
                        multiple=False,
                    ),
                ],
                className="card-custom",
            ),
            html.Div(
                id="barcode-result",
                className="card-custom",
                style={"marginTop": "20px"},
            ),
            html.Div(
                [
                    html.Label(
                        "説明（オプション）",
                        style={
                            "color": "#666",
                            "fontWeight": "600",
                            "display": "block",
                            "marginBottom": "5px",
                        },
                    ),
                    dcc.Input(
                        id="photo-description",
                        type="text",
                        placeholder="写真の説明を入力...",
                        className="input-custom",
                    ),
                ],
                className="card-custom",
                style={"marginTop": "20px"},
            ),
            html.Div(
                html.Button(
                    "保存",
                    id="save-button",
                    n_clicks=0,
                    className="btn-custom",
                    disabled=True,
                ),
                className="card-custom",
                style={"marginTop": "10px"},
            ),
        ]
    )
