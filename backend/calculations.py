import pandas as pd


def session_volume(row):
    """
    Compute volume for a single training row.

    Volume = Series * Repetitions * Weight
    """
    return row["Series"] * row["Repetitions"] * row["Weight"]


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived helper columns to the dataframe:
    - Volume: total load per row
    - YearMonth: YYYY-MM period string
    - Week: ISO week period string
    """
    df = df.copy()
    df["Volume"] = df.apply(session_volume, axis=1)
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    df["Week"] = df["Date"].dt.to_period("W").astype(str)
    return df


def pr_by_exercise(df: pd.DataFrame) -> dict:
    """
    Return a dictionary mapping each exercise to its max recorded weight.
    """
    return df.groupby("Exercises")["Weight"].max().to_dict()


def get_pr(df: pd.DataFrame):
    """
    Return the max weight in the dataframe.
    If empty, return 0.
    """
    return df["Weight"].max() if not df.empty else 0


def get_pr_trend(df: pd.DataFrame, end_date):
    """
    Compute PR trend over the last 30 days vs the previous 30 days.

    Returns:
        difference (float): PR_last_30_days - PR_previous_30_days
    """
    last_30 = df[df["Date"] >= end_date - pd.Timedelta(days=30)]
    prev_30 = df[
        (df["Date"] < end_date - pd.Timedelta(days=30)) &
        (df["Date"] >= end_date - pd.Timedelta(days=60))
    ]

    pr_last = last_30["Weight"].max() if not last_30.empty else 0
    pr_prev = prev_30["Weight"].max() if not prev_30.empty else 0

    return pr_last - pr_prev


def get_last_session(df: pd.DataFrame):
    """
    Return the last session summary and its date.

    Returns:
        last_session (str)
        last_session_date (str)
    """
    if df.empty:
        return "No data", ""

    last = df.sort_values("Date").iloc[-1]
    last_session = f"{last['Series']}x{last['Repetitions']} @ {last['Weight']} kg"
    last_session_date = f"{last['Date'].date()}"

    return last_session, last_session_date


def get_consistency(df: pd.DataFrame):
    """
    Compute consecutive training weeks.

    Returns:
        consistency (int): number of consecutive weeks
        consistency_label (str): "week" or "weeks"
    """
    if df.empty:
        consistency = 0
    else:
        weeks = df["Date"].dt.isocalendar().week.unique()
        weeks_sorted = sorted(weeks)

        consistency = 1
        for i in range(len(weeks_sorted) - 1, 0, -1):
            if weeks_sorted[i] - weeks_sorted[i - 1] == 1:
                consistency += 1
            else:
                break

    consistency_label = "weeks" if consistency > 1 else "week"
    return consistency, consistency_label


def get_volume_trend(df: pd.DataFrame, end_date):
    """
    Compute volume trend comparing the last 30 days vs the previous 30 days.

    Returns:
        percentage change (float)
    """
    this_month = df[df["Date"] >= end_date - pd.Timedelta(days=30)]
    prev_month = df[
        (df["Date"] < end_date - pd.Timedelta(days=30)) &
        (df["Date"] >= end_date - pd.Timedelta(days=60))
    ]

    vol_this = this_month["Volume"].sum() if not this_month.empty else 0
    vol_prev = prev_month["Volume"].sum() if not prev_month.empty else 0

    return ((vol_this - vol_prev) / vol_prev * 100) if vol_prev > 0 else 0


def get_best_quality(df: pd.DataFrame):
    """
    Return the best set based on highest weight and reps.

    Returns:
        best_quality (str)
        best_quality_date (str)
    """
    if df.empty:
        return "No data", ""

    best_set = df.sort_values(
        ["Weight", "Repetitions"], ascending=False
    ).iloc[0]

    best_quality = f"{best_set['Series']}x{best_set['Repetitions']} @ {best_set['Weight']} kg"
    best_quality_date = f"{best_set['Date'].date()}"

    return best_quality, best_quality_date


def weekly_volume_timeseries(df: pd.DataFrame, exercise: str | None = None) -> pd.DataFrame:
    """
    Return weekly volume timeseries for all exercises or a specific one.

    Returns:
        DataFrame with columns:
        - Week
        - Volume
        - WeekStart (converted to datetime)
    """
    d = df.copy()
    if exercise:
        d = d[d["Exercises"] == exercise]

    s = d.groupby("Week")["Volume"].sum().reset_index()

    # Convert period string to representative date (first day of the week)
    s["WeekStart"] = pd.to_datetime(
        s["Week"].str.replace("W", "").str.split("/").str[0],
        errors="coerce"
    )

    return s.sort_values("WeekStart")


def month_comparison(df, metric_col):
    """
    Compare a metric between the current month and the previous month.

    Returns:
        current_value (float)
        diff (float): absolute difference
        pct (float): percentage difference
    """
    months = sorted(df["YearMonth"].unique())
    if len(months) < 2:
        return 0, 0, 0

    current = months[-1]
    previous = months[-2]

    cur_val = df[df["YearMonth"] == current][metric_col].sum()
    prev_val = df[df["YearMonth"] == previous][metric_col].sum()

    diff = cur_val - prev_val
    pct = (diff / prev_val * 100) if prev_val > 0 else 0

    return cur_val, diff, pct