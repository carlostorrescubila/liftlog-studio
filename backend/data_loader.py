import pandas as pd

# Public Google Sheets CSV export link
LINK = (
    "https://docs.google.com/spreadsheets/d/1Prc4yYiyCRMB43qLxTYlYvTM6Y62fuGBMH8kXhXbVEQ/export?format=csv"
)


def load_lifts(csv_path=LINK) -> pd.DataFrame:
    """
    Load and preprocess the lifts dataset.

    This function:
    - Reads the CSV file (Google Sheets export by default)
    - Parses dates in day-first format
    - Converts numeric fields safely
    - Computes training volume
    - Generates time-based helper columns (Month, MonthLabel, YearMonth)
    - Sorts the dataset chronologically

    Parameters
    ----------
    csv_path : str
        Path or URL to the CSV file containing the lifts data.

    Returns
    -------
    pd.DataFrame
        Cleaned and enriched dataframe ready for filtering,
        KPI calculations, and visualization.
    """

    # --- Load CSV and parse Date column ---
    df = pd.read_csv(
        csv_path,
        parse_dates=["Date"],
        dayfirst=True
    )

    # --- Convert numeric columns safely ---
    df["Series"] = pd.to_numeric(df["Series"], errors="coerce").fillna(0).astype(int)
    df["Repetitions"] = pd.to_numeric(df["Repetitions"], errors="coerce").fillna(0).astype(int)
    df["Weight"] = pd.to_numeric(df["Weight"], errors="coerce").fillna(0.0)

    # --- Compute training volume (Series × Repetitions × Weight) ---
    df["Volume"] = df["Series"] * df["Repetitions"] * df["Weight"]

    # --- Ensure valid dates and drop invalid rows ---
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])

    # --- Month as datetime64[M] (first day of the month) ---
    df["Month"] = df["Date"].values.astype("datetime64[M]")

    # --- Human-readable month label for plots ---
    df["MonthLabel"] = df["Month"].dt.strftime("%b %Y")

    # --- YearMonth key for KPI calculations ---
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

    # --- Sort chronologically ---
    df = df.sort_values("Date").reset_index(drop=True)

    return df