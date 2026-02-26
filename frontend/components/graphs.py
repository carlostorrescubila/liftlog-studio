import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

SCALABLE_PALETTE = [
    "#FFCC00",  # Bright Yellow
    "#000000",  # Black
    "#555555",  # Dark Gray
    "#999999",  # Medium Gray
    "#CCCCCC",  # Light Gray
    "#66C2A5",  # Soft Green
    "#FC8D62",  # Soft Orange
    "#8DA0CB",  # Soft Blue
    "#E78AC3",  # Soft Pink
    "#A6D854",  # Lime Green
    "#FFD92F",  # Soft Yellow
    "#E5C494",  # Soft Brown
]

EXERCISE_COLORS = {
    "Squat": "#34A853",        # Azul Google
    "Deadlift": "#1A73E8",     # Verde moderno
    "Press militar": "#FBBC04", # Amarillo oscuro
    "Bench Press": "#EA4335",  # Rojo suave
}

def color_sequence_for(df):
    """
    Return a list of colors matching the order of exercises present
    in the dataframe, ensuring consistent color mapping across plots.
    """
    exercises = df["Exercises"].unique()
    return [EXERCISE_COLORS.get(e, "#333333") for e in exercises]

def sessions_bar_months(df: pd.DataFrame, exercise: str | None = None):

    d = df.copy()

    # Optional filtering by exercise
    if exercise:
        d = d[d["Exercises"] == exercise]

    if d.empty:
        return px.bar(title="No session data available")

    monthly_freq = (
        d.groupby(["Month", "Exercises"], observed=True)
        .size()
        .reset_index(name="Sessions")
        .sort_values("Month")
    )

    # FIX: MonthLabel is lost after groupby → recreate it
    monthly_freq["MonthLabel"] = monthly_freq["Month"].dt.strftime("%b %Y")

    fig = px.bar(
        monthly_freq,
        x="MonthLabel",
        y="Sessions",
        color="Exercises",
        text="Sessions",
        title=f"Training Frequency per Month{' - ' + exercise if exercise else ''}",
        color_discrete_sequence=color_sequence_for(monthly_freq)
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        barmode="stack",
        xaxis_title="Date",
        yaxis_title="Sessions",
        legend_title="Exercise",
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
        yaxis=dict(showgrid=True, gridcolor="#e5e5e5", rangemode="tozero"),
        font=dict(color="#000000"),
        title_x=0.5,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_color="black",
            bordercolor="black"
        ),
        margin=dict(t=60, b=40)
    )

    return fig

def volume_area_months(df: pd.DataFrame, exercise: str | None = None):

    d = df.copy()

    # Optional filtering
    if exercise:
        d = d[d["Exercises"] == exercise]

    if d.empty:
        return px.area(title="No volume data available")

    # Group monthly volume
    monthly_volume = (
        d.groupby(["Month", "Exercises"], observed=True)["Volume"]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    # FIX: MonthLabel is lost after groupby → recreate it
    monthly_volume["MonthLabel"] = monthly_volume["Month"].dt.strftime("%b %Y")

    # Build stacked area chart
    fig = px.area(
        monthly_volume,
        x="MonthLabel",
        y="Volume",
        color="Exercises",
        title=f"Total Monthly Volume{' - ' + exercise if exercise else ''}",
        color_discrete_sequence=color_sequence_for(monthly_volume)
    )

    # Total line
    total_monthly = (
        monthly_volume.groupby("Month")["Volume"]
        .sum()
        .reset_index()
    )
    total_monthly["MonthLabel"] = total_monthly["Month"].dt.strftime("%b %Y")

    fig.add_scatter(
        x=total_monthly["MonthLabel"],
        y=total_monthly["Volume"],
        mode="lines+markers",
        name="Total Volume",
        line=dict(color="black", width=2),
        marker=dict(size=6)
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Month",
        yaxis_title="Volume (kg)",
        legend_title="Exercise",
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
        yaxis=dict(showgrid=True, gridcolor="#e5e5e5", rangemode="tozero"),
        font=dict(color="#000000"),
        title_x=0.5,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_color="black",
            bordercolor="black"
        ),
        margin=dict(t=60, b=40)
    )

    return fig

def progress_line(df: pd.DataFrame, exercise: str | None = None):
    d = df.copy()
    if exercise:
        d = d[d["Exercises"] == exercise]

    if d.empty:
        return px.line(title="Sin datos")

    # Asegurar orden temporal
    d = d.sort_values("Date")

    fig = px.line(
        d,
        x="Date",
        y="Weight",
        markers=True,
        title=f"Progreso - {exercise}",
    )

    # --- Layout: centrado, sin fondo gris, estilo limpio ---
    fig.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22, "color": "black"},
        },
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(
            title="Fecha",
            showgrid=True,
            gridcolor="#E5E5E5"
        ),
        yaxis=dict(
            title="Weight (kg)",
            showgrid=True,
            gridcolor="#E5E5E5"
        ),
        margin=dict(l=40, r=20, t=60, b=40)
    )

    # --- Línea amarilla consistente con tu branding ---
    fig.update_traces(
        line=dict(width=3, color="#FFCC00"),
        marker=dict(size=8, color="#FFCC00")
    )

    return fig


def volume_bar_by_period(
        df: pd.DataFrame,
        exercise: str | None = None,
        period_label: str | None = None
):
    """

    :param df:
    :param exercise:
    :return:
    """

    # Copy of dataframe
    d = df.copy()

    # Filter excercise
    if exercise:
        d = d[d["Exercises"] == exercise]

    # Dataframe empty
    if d.empty:
        return px.bar(title="No Data")

    # Sum of volume by week
    week_sum = d.groupby("Date")["Volume"].sum().reset_index()

    # Sort data
    week_sum = week_sum.sort_values("Date")

    # Convert week number to string (for x axis)
    if period_label in ["Month", "YearMonth"]:
        week_sum["Date"] = week_sum["Date"]#.dt.to_period("M")


    # Figure
    fig = px.bar(
        week_sum,
        x="Date",
        y="Volume",
        title=f"Weekly volume{' - ' + exercise if exercise else ''}",
        labels={"Date": period_label, "Volume": "Volume (kg)"},
        text="Volume",
        color_discrete_sequence=["#FFCC00"]
    )

    # Layout
    fig.update_layout(
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22, "color": "black"},
        },
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
        yaxis=dict(showgrid=True, gridcolor="#e5e5e5", rangemode="tozero"),
        font=dict(color="#000000"),
    )

    return fig


def avg_series_reps(df, exercise=None):
    """

    :param df:
    :param exercise:
    :return:
    """

    # Copy of dataframe
    df_copy = df.copy()

    # Filter excercise
    if exercise:
        df_copy = df_copy[df_copy["Exercises"] == exercise]

    # Dataframe empty
    if df_copy.empty:
        return px.line(title="No Data")

    # Select data
    df_avg = df_copy.groupby("Date")[["Series","Repetitions"]].mean().reset_index()

    # Figure
    fig = px.line(
        df_avg,
        x="Date",
        y=["Series","Repetitions"],
        markers=True,
        title=f"Average sets and reps - {exercise}" if exercise else "Average sets and reps",
        labels={"Date": "Date", "value": "Count"},
        color_discrete_sequence=SCALABLE_PALETTE
    )

    # Layout
    fig.update_layout(
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
        yaxis=dict(showgrid=True, gridcolor="#e5e5e5", rangemode="tozero"),
        font=dict(color="#000000"),
        title={
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22, "color": "black"},
        },
    )

    return fig


def weight_distribution(df, exercise=None, kind="histogram"):
    """

    :param df:
    :param exercise:
    :param kind:
    :return:
    """

    # Copy of dataframe
    df_copy = df.copy()

    # Filter excercise
    if exercise:
        df_copy = df_copy[df_copy["Exercises"] == exercise]

    # Dataframe empty
    if df_copy.empty:
        return px.line(title="No Data")

    # Calculate PR
    df_copy = df_copy.sort_values("Date")
    df_copy["PR_to_date"] = df_copy.groupby("Exercises")["Weight"].cummax()

    # Intensity weighted by volume
    df_copy["Intensity"] = df_copy["Weight"] / df_copy["PR_to_date"] * 100

    # Add daily intensity (average per day if there ara various sets)
    daily_intensity = df_copy.groupby("Date")["Intensity"].mean().reset_index()

    # Figure
    fig = go.Figure()

    # Area
    fig.add_trace(
        go.Scatter(
            x=daily_intensity["Date"],
            y=daily_intensity["Intensity"],
            fill='tozeroy',
            mode='lines',
            line_color="#FFCC00",
            name="Intensity"
        )
    )

    # Marker
    fig.add_trace(
        go.Scatter(
            x=daily_intensity["Date"],
            y=daily_intensity["Intensity"],
            mode='markers+text',
            marker=dict(size=8, symbol='star', color="#000000"),
            text=[f"{int(v)}%" for v in daily_intensity["Intensity"]],
            textposition="top center",
            name="Sessions"
        )
    )

    # Update trace
    fig.update_traces(
        hovertemplate="Date: %{x|%d %b %Y}<br>Intensity: %{y:.1f}%<extra></extra>"
    )

    # Layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Intensity (% of PR)",
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        xaxis=dict(showgrid=True, gridcolor="#e5e5e5"),
        yaxis=dict(showgrid=True, gridcolor="#e5e5e5", rangemode="tozero"),
        font=dict(color="#000000"),
        title={
            "text": "Daily Intensity",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 22, "color": "black"},
        },
    )

    return fig