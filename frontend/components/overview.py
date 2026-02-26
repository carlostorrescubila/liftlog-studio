# frontend/components/overview.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

from frontend.components.kpi_card import kpi_card
from frontend.components.graphs import sessions_bar_months, volume_area_months
from backend.calculations import pr_by_exercise, month_comparison


def layout_overview(df):
    """
    Overview tab layout with robust validation.
    Ensures missing columns or wrong dtypes do not break the dashboard.
    """

    # ------------------------------------------------------------
    # Ensure Date column exists and is datetime
    # ------------------------------------------------------------
    if "Date" not in df:
        return html.Div("Error: 'Date' column missing in dataframe")

    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ------------------------------------------------------------
    # Global KPIs (Row 1)
    # ------------------------------------------------------------

    # Total sessions
    total_sessions = df["SessionID"].nunique() if "SessionID" in df else 0

    # Total volume
    total_volume = df["Volume"].sum() if "Volume" in df else 0

    # Avg sessions per week
    if df["Date"].notna().sum() > 1:
        days = (df["Date"].max() - df["Date"].min()).days
        weeks = days / 7 if days > 0 else 1
    else:
        weeks = 1

    avg_sessions_week = total_sessions / weeks

    # Volume trend
    try:
        _, _, vol_pct = month_comparison(df, "Volume")
    except Exception:
        vol_pct = 0

    row1 = dbc.Row(
        [
            dbc.Col(kpi_card("Total Sessions", f"{total_sessions}", icon="📅"), md=3),
            dbc.Col(kpi_card("Total Volume", f"{int(total_volume):,} kg", icon="📦"), md=3),
            dbc.Col(kpi_card("Avg Sessions/Week", f"{avg_sessions_week:.1f}", icon="📊"), md=3),
            dbc.Col(kpi_card("Volume Trend", f"{vol_pct:+.1f}%", icon="📈"), md=3),
        ],
        className="mb-4 g-4 justify-content-center"
    )

    # ------------------------------------------------------------
    # PRs by Exercise + Most Intense Exercises (Row 2)
    # ------------------------------------------------------------

    # PRs
    try:
        prs = pr_by_exercise(df)
        pr_list = [html.P(f"🏋️ {ex}: {int(w)} kg") for ex, w in prs.items()]
    except Exception:
        pr_list = [html.P("No PR data available")]

    pr_card = kpi_card("PRs by Exercise", pr_list, icon="🏆")

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

    intensity_card = kpi_card("Most Intense Exercises", intensity_list, icon="🔥")

    row2 = dbc.Row(
        [
            dbc.Col(pr_card, md=6),
            dbc.Col(intensity_card, md=6),
        ],
        className="mb-4 g-4"
    )

    # ------------------------------------------------------------
    # Charts (Row 3)
    # ------------------------------------------------------------
    charts = dbc.Row(
        [
            dbc.Col(dcc.Graph(figure=sessions_bar_months(df)), md=6),
            dbc.Col(dcc.Graph(figure=volume_area_months(df)), md=6),
        ]
    )

    return html.Div(
        [row1, row2, charts],
        style={"padding": "10px"}
    )