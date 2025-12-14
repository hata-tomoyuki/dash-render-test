# Available Bootswatch themes
BOOTSWATCH_THEMES = [
    "cerulean",
    "cosmo",
    "cyborg",
    "darkly",
    "flatly",
    "journal",
    "litera",
    "lumen",
    "lux",
    "materia",
    "minty",
    "morph",
    "pulse",
    "quartz",
    "sandstone",
    "simplex",
    "sketchy",
    "slate",
    "solar",
    "spacelab",
    "superhero",
    "united",
    "vapor",
    "yeti",
    "zephyr",
]

# Load/save theme
THEME_FILE = "theme.txt"


def load_theme() -> str:
    try:
        with open(THEME_FILE, "r") as f:
            theme = f.read().strip()
            if theme in BOOTSWATCH_THEMES:
                return theme
    except FileNotFoundError:
        pass
    return "minty"


def save_theme_to_file(theme: str):
    with open(THEME_FILE, "w") as f:
        f.write(theme)


# Current theme
CURRENT_THEME = load_theme()


def get_bootswatch_css(theme: str) -> str:
    """Get Bootswatch CSS URL for the given theme."""
    return (
        f"https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/{theme}/bootstrap.min.css"
    )


# Theme management callbacks
def register_theme_callbacks(app):
    from dash import Input, Output, State, html

    @app.callback(
        Output("register-alert", "children", allow_duplicate=True),
        Input("save-theme-button", "n_clicks"),
        State("theme-selector", "value"),
        prevent_initial_call="initial_duplicate",
    )
    def save_theme(n_clicks, selected_theme):
        if not n_clicks or not selected_theme:
            return ""

        try:
            save_theme_to_file(selected_theme)
            return html.Div(
                f"テーマ '{selected_theme}' を保存しました。",
                className="alert alert-success",
            )
        except Exception as e:
            return html.Div(
                f"テーマの保存に失敗しました: {str(e)}",
                className="alert alert-danger",
            )

    @app.callback(
        Output("bootswatch-theme", "href"),
        Input("theme-selector", "value"),
        prevent_initial_call=True,
    )
    def update_theme_css(selected_theme):
        return get_bootswatch_css(selected_theme)
