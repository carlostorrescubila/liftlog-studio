from dash import html, dcc
import dash_bootstrap_components as dbc


def make_layout(app, exercises):

    sidebar = html.Div(
        [
            html.Div(
                [
                    html.Span("LiftLog Studio.idea/", className="sidebar-title"),
                    html.I(className="bi bi-lightning-charge-fill sidebar-logo-icon"),
                ],
                className="sidebar-title-container"
            ),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-speedometer2 sidebar-icon"),
                            html.Span("Overview", className="sidebar-text"),
                        ],
                        href="/",
                        active="exact",
                        className="sidebar-link",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-bar-chart-line sidebar-icon"),
                            html.Span("Exercises", className="sidebar-text"),
                        ],
                        href="/exercises",
                        active="exact",
                        className="sidebar-link",
                        id="Exercises"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-graph-up-arrow sidebar-icon"),
                            html.Span("Comparisons", className="sidebar-text"),
                        ],
                        href="/compare",
                        active="exact",
                        className="sidebar-link",
                        id="Comparisons"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-table sidebar-icon"),
                            html.Span("Data", className="sidebar-text"),
                        ],
                        href="/data",
                        active="exact",
                        className="sidebar-link",
                        id="Data"
                    ),
                ],
                vertical=True,
                pills=True,
                className="mt-4"
            ),
        ],
        id="sidebar",
        className="sidebar-expanded"
    )

    topbar = html.Div(
        [
            html.Button(
                html.I(className="bi bi-list"),
                id="sidebar-toggle",
                className="sidebar-toggle-btn"
            ),
            html.H4("Dashboard", className="m-0 ms-3"),
        ],
        id="topbar",
        className="topbar"
    )

    content = html.Div(
        id="page-content",
        className="content-area"
    )

    return html.Div(
        [
            dcc.Location(id="url"),
            sidebar,
            topbar,
            content,
        ]
    )