from dash import html
from dash import dash_table


def layout_data(df):
    """
    Data tab layout: clean, professional and fully CSS‑driven.
    """

    return html.Div(
        [
            # ------------------------------------------------------------
            # Title
            # ------------------------------------------------------------
            html.H4("Training Dataset", className="data-title mb-4"),

            # ------------------------------------------------------------
            # Data table
            # ------------------------------------------------------------
            dash_table.DataTable(
                id="data-table",
                data=df.to_dict("records"),
                columns=[{"name": col, "id": col} for col in df.columns],

                # --- Functionality ---
                sort_action="native",
                filter_action="native",
                filter_options={"case": "insensitive"},
                page_action="native",
                page_size=15,

                # --- Minimal layout style ---
                style_table={"overflowX": "auto"},

                # --- Style conditional ---
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
            ),
        ],
        className="data-container"
    )