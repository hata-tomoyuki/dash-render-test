# -*- coding: utf-8 -*-
from dash import html, register_page


register_page(
    __name__,
    path="/login",
    title="ログイン - 推し活グッズ管理",
)


layout = html.Div(
    [
        html.H1("ログインが必要です"),
        html.P("Googleでサインインしてご利用ください。"),
        html.A("Googleでログイン", href="/auth/login", className="btn btn-primary"),
    ],
    style={"padding": "40px"},
)

