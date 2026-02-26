# frontend/components/exercises.py

from dash import html, dcc
import dash_bootstrap_components as dbc


def layout_exercises(df):

    exercises = sorted(df["Exercises"].unique())

    selector = dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id="exercise-selector",
                    options=[{"label": e, "value": e} for e in exercises],
                    value=exercises[0],
                    clearable=False,
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "padding": "4px",
                    },
                ),
                md=4,
            ),
            dbc.Col(
                dcc.DatePickerRange(
                    id="exercise-date-range",
                    start_date=None,
                    end_date=None,
                    display_format="DD/MM/YYYY",
                    style={
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                        "padding": "6px",
                    },
                ),
                md=4,
            ),
        ],
        className="mb-4 justify-content-center",
    )

    kpi_row = html.Div(
        id="exercise-kpis",
        className="d-flex flex-wrap justify-content-center gap-4 mb-4"
    )

    charts = html.Div(
        [
            html.Div(
                dcc.Graph(id="exercise-weekly-volume"),
                style={"marginBottom": "30px"},
            ),
            html.Div(
                dcc.Graph(id="exercise-average-sets-reps"),
                style={"marginBottom": "30px"},
            ),
            html.Div(
                dcc.Graph(id="exercise-weight-distribution"),
                style={"marginBottom": "30px"},
            ),
        ],
        style={
            "padding": "10px 20px",
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        },
    )

    return html.Div(
        [
            selector,
            kpi_row,
            charts,
        ],
        style={
            "padding": "20px",
        },
    )