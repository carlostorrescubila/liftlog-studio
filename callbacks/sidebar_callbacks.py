from dash import Input, Output, State, callback


@callback(
    Output("sidebar", "className"),
    Output("topbar", "className"),
    Output("page-content", "className"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "className"),
)
def toggle_sidebar(n, current_class):
    if n is None:
        return current_class, "topbar", "content-area"

    if "expanded" in current_class:
        return (
            "sidebar-collapsed",
            "topbar topbar-collapsed",
            "content-area content-collapsed"
        )
    else:
        return (
            "sidebar-expanded",
            "topbar",
            "content-area"
        )