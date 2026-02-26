from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from frontend.components.overview import layout_overview
from frontend.components.exercises import layout_exercises
from frontend.components.compare import layout_compare
from frontend.components.data import layout_data
from frontend.components.kpi_card import kpi_card
from frontend.components.graphs import (
    volume_bar_by_period,
    avg_series_reps,
    weight_distribution,
)
from backend.calculations import (
    add_derived_columns,
    get_pr,
    get_pr_trend,
    get_last_session,
    get_consistency,
    get_volume_trend,
    get_best_quality,
)
from .sidebar_callbacks import *


def register_callbacks(app, df_raw):

    # Prepare dataframe with derived columns
    df = add_derived_columns(df_raw)

    # 1) TAB ROUTING (Overview / Exercises / Compare / Data)
    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def render_page(pathname):
        """Render the page based on the URL path."""

        if pathname == "/":
            return layout_overview(df)

        if pathname == "/exercises":
            return layout_exercises(df)

        if pathname == "/compare":
            return layout_compare(df)

        if pathname == "/data":
            return layout_data(df)

        return html.Div("404 - Page not found")

    # 2) MAIN CALLBACK FOR EXERCISE TAB
    @app.callback(
        Output("exercise-date-range", "start_date"),
        Output("exercise-date-range", "end_date"),
        Output("exercise-kpis", "children"),
        Output("exercise-weekly-volume", "figure"),
        Output("exercise-average-sets-reps", "figure"),
        Output("exercise-weight-distribution", "figure"),
        Input("exercise-selector", "value"),
        Input("exercise-date-range", "start_date"),
        Input("exercise-date-range", "end_date"),
        prevent_initial_call=False,
    )
    def update_exercise_tab(exercise, start_date, end_date):
        """Update KPIs and graphs when exercise or date range changes."""

        if not exercise:
            raise PreventUpdate

        # Filter selected exercise
        d = df[df["Exercises"] == exercise]
        if d.empty:
            raise PreventUpdate

        # Determine available date range
        min_date = d["Date"].min().date()
        max_date = d["Date"].max().date()

        # If no date selected → use full range
        if start_date is None or end_date is None:
            start_date, end_date = min_date, max_date

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter by date range
        df_filtered = d[(d["Date"] >= start_date) & (d["Date"] <= end_date)]

        # Compute KPIs
        pr = get_pr(df_filtered)
        pr_trend = get_pr_trend(df_filtered, end_date)
        last_str, last_str_date = get_last_session(df_filtered)
        consistency, consistency_label = get_consistency(df_filtered)
        avg_volume = df_filtered["Volume"].mean() if not df_filtered.empty else 0
        volume_trend = get_volume_trend(df_filtered, end_date)
        best_quality, best_quality_date = get_best_quality(df_filtered)
        sessions_count = df_filtered.shape[0]

        # KPI layout
        kpis = html.Div(
            [
                # Row 1
                dbc.Row(
                    [
                        dbc.Col(kpi_card("PR", f"{pr} kg", icon="🏆"), md=3),
                        dbc.Col(kpi_card("PR Trend", f"{pr_trend:+} kg", icon="📈"), md=3),
                        dbc.Col(kpi_card("Last Session", last_str, icon="🔄", subtitle=last_str_date), md=3),
                        dbc.Col(kpi_card("Consistency", f"{consistency} {consistency_label}", icon="📅"), md=3),
                    ],
                    className="mb-4 g-4 justify-content-center"
                ),
                # Row 2
                dbc.Row(
                    [
                        dbc.Col(kpi_card("Avg Volume", f"{avg_volume:.0f} kg", icon="📦"), md=3),
                        dbc.Col(kpi_card("Volume Trend", f"{volume_trend:+.1f}%", icon="🔥"), md=3),
                        dbc.Col(kpi_card("Best Set", best_quality, icon="🎯", subtitle=best_quality_date), md=3),
                        dbc.Col(kpi_card("Sessions", f"{sessions_count}", icon="🔢"), md=3),
                    ],
                    className="g-4 justify-content-center"
                )
            ]
        )

        # Compute graphs
        fig1 = volume_bar_by_period(df_filtered, exercise, period_label="Month")
        fig2 = avg_series_reps(df_filtered, exercise)
        fig3 = weight_distribution(df_filtered, exercise)

        return (
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            kpis,
            fig1,
            fig2,
            fig3
        )

    # 3) CALLBACK FOR EXERCISE COMPARISON TAB
    @app.callback(
        Output("compare-graph", "figure"),
        Input("compare-a", "value"),
        Input("compare-b", "value"),
    )
    def update_compare(a, b):
        """Update comparison graph between two exercises."""

        if not a or not b:
            return {}

        df_copy = df[df["Exercises"].isin([a, b])].copy()
        df_copy["CumMax"] = df_copy.groupby("Exercises")["Weight"].cummax()

        import plotly.express as px
        return px.line(
            df_copy,
            x="Date",
            y="CumMax",
            color="Exercises",
            markers=True,
            title=f"PR Comparison: {a} vs {b}",
        )