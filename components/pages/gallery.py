from dash import html
from typing import Iterable, Mapping

Photo = Mapping[str, str]


def render_gallery(photos: Iterable[Photo]) -> html.Div:
    photos = list(photos)
    header = html.Div([html.H1("🖼️ 写真一覧")], className="header")

    if not photos:
        summary = html.Div(
            [
                html.P(
                    "まだ写真が登録されていません",
                    style={
                        "color": "#999",
                        "textAlign": "center",
                        "marginBottom": "20px",
                    },
                )
            ]
        )
        grid = None
    else:
        summary = html.Div(
            [
                html.P(
                    f"全 {len(photos)} 枚の写真",
                    style={
                        "color": "#999",
                        "textAlign": "center",
                        "marginBottom": "20px",
                    },
                )
            ]
        )
        grid = html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src=photo.get("image_url"),
                                    style={
                                        "width": "100%",
                                        "height": "150px",
                                        "objectFit": "cover",
                                    },
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            f"バーコード: {photo.get('barcode', '')[:15]}...",
                                            style={
                                                "fontWeight": "600",
                                                "color": "#333",
                                                "marginBottom": "5px",
                                            },
                                        ),
                                        html.Div(
                                            photo.get("description") or "説明なし",
                                            style={
                                                "color": "#999",
                                                "fontSize": "11px",
                                            },
                                        ),
                                    ],
                                    className="photo-info",
                                ),
                            ],
                            className="photo-card",
                        )
                    ]
                )
                for photo in photos
            ],
            className="photo-grid",
        )

    return html.Div([header, summary, grid] if grid else [header, summary])
