# frontend/components/data.py

from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table


def layout_data(df):

    return html.Div(
        [
            html.H4(
                "Training Log",
                className="mb-4",
                style={
                    "fontWeight": "600",
                    "letterSpacing": "0.5px",
                    "color": "#333",
                },
            ),

            dash_table.DataTable(
                data=df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in df.columns],

                # --- Styling ---
                style_table={
                    "overflowX": "auto",
                    "borderRadius": "12px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
                },
                style_header={
                    "backgroundColor": "#f7f7f7",
                    "fontWeight": "600",
                    "border": "none",
                    "fontSize": "14px",
                    "color": "#333",
                },
                style_cell={
                    "padding": "10px",
                    "fontSize": "14px",
                    "textAlign": "center",
                    "border": "none",
                },
                style_data={
                    "backgroundColor": "white",
                    "borderBottom": "1px solid #eee",
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "odd"},
                        "backgroundColor": "#fafafa",
                    },
                    {
                        "if": {"state": "active"},
                        "backgroundColor": "#ffe9b3",
                        "border": "1px solid #ffcc66",
                    },
                ],

                # --- Functionality ---
                sort_action="native",
                filter_action="native",
                page_size=10,
            ),
        ],
        style={
            "padding": "20px",
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
        },
    )