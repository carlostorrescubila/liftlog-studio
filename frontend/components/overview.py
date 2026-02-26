from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

from frontend.components.kpi_card import kpi_card
from frontend.components.graphs import sessions_bar_months, volume_area_months
from backend.calculations import pr_by_exercise, month_comparison_3m


def layout_overview(df):
    """
    Overview tab layout with robust validation.
    Ensures missing columns or wrong dtypes do not break the dashboard.
    """

    # Current calendar month and year (system date)
    today = datetime.today()
    current_year = today.year
    current_month = today.month

    # Filter dataframe to current calendar month
    df_current = df[
        (df["Date"].dt.year == current_year) &
        (df["Date"].dt.month == current_month)
    ]

    # ------------------------------------------------------------
    # Row 1: Global KPIs
    # ------------------------------------------------------------

    # - Total sessions
    try:
        total_sessions = df_current["Date"].nunique()
    except Exception:
        total_sessions = 0

    # - Total volume
    try:
        total_volume = df_current["Volume"].sum()
    except Exception:
        total_volume = 0

    # - Avg sessions per week (last 12 weeks)
    try:
        start_12w = today - timedelta(weeks=12)
        df_12w = df[df["Date"].between(start_12w, today)]
        sessions_12w = df_12w["Date"].nunique()
        avg_sessions_week = sessions_12w / 12
    except Exception:
        avg_sessions_week = 0

    # - Volume trend (current vs avg last 3 months)
    try:
        vol_trend = month_comparison_3m(df, "Volume")[2]
    except Exception:
        vol_trend = 0

    row1 = dbc.Row(
        [
            dbc.Col(
                kpi_card(
                    "Total Sessions",
                    f"{total_sessions}",
                    icon="📅",
                    subtitle="Current month"
                ),
                xs=12, sm=6, md=3
            ),
            dbc.Col(
                kpi_card(
                    "Total Volume",
                    f"{int(total_volume):,} kg",
                    icon="📦",
                    subtitle="Current month"
                ),
                xs=12, sm=6, md=3
            ),
            dbc.Col(
                kpi_card(
                    "Average Sessions",
                    f"{avg_sessions_week:.1f}",
                    icon="📊",
                    subtitle="Last 12 weeks"
                ),
                xs=12, sm=6, md=3
            ),
            dbc.Col(
                kpi_card(
                    "Volume Trend",
                    f"{vol_trend:+.1f}%",
                    icon="📈",
                    subtitle="Current vs 3 months avg"
                ),
                xs=12, sm=6, md=3
            ),
        ],
        className="mb-4 g-4 overview-row1"
    )

    # ------------------------------------------------------------
    # Row 2: PRs by Exercise + Most Intense Exercises
    # ------------------------------------------------------------

    # PRs
    try:
        prs = pr_by_exercise(df)
        pr_list = [html.P(f"🏋️ {ex}: {int(w)} kg") for ex, w in prs.items()]
    except Exception:
        pr_list = [html.P("No PR data available")]

    # Intensity
    try:
        intensity_df = (
            df.groupby("Exercises")["Volume"]
            .mean()
            .sort_values(ascending=False)
            .head(5)
        )
        intensity_list = [html.P(f"🔥 {ex}: {int(v)} kg/session") for ex, v in intensity_df.items()]
    except Exception:
        intensity_list = [html.P("No intensity data available")]

    row2 = dbc.Row(
        [
            dbc.Col(
                kpi_card("PRs by Exercise", pr_list, icon="🏆"),
                xs=12, md=6
            ),
            dbc.Col(
                kpi_card("Most Intense Exercises", intensity_list, icon="🔥"),
                xs=12, md=6
            ),
        ],
        className="mb-4 g-4 overview-row2"
    )

    # ------------------------------------------------------------
    # Row 3 and 4: Charts
    # ------------------------------------------------------------

    row3 = dbc.Row(
        [dcc.Graph(figure=sessions_bar_months(df), className="overview-chart")],
        className="mb-4"
    )

    row4 = dbc.Row(
        [dcc.Graph(figure=volume_area_months(df), className="overview-chart")],
        className="mb-4"
    )

    return html.Div(
        [row1, row2, row3, row4],
        style={"padding": "10px"}
    )