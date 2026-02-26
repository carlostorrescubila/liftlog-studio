# frontend/components/compare.py

from dash import html, dcc
import dash_bootstrap_components as dbc


def layout_compare(df):

    exercises = sorted(df["Exercises"].unique())

    controls = dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(
                    id="compare-a",
                    options=[{"label": e, "value": e} for e in exercises],
                    value=exercises[0],
                ),
                md=4,
            ),
            dbc.Col(
                dcc.Dropdown(
                    id="compare-b",
                    options=[{"label": e, "value": e} for e in exercises],
                    value=exercises[1] if len(exercises) > 1 else exercises[0],
                ),
                md=4,
            ),
        ],
        className="mb-3",
        justify="center",
    )

    return html.Div([
        controls,
        dcc.Graph(id="compare-graph")
    ])