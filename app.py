from dash import Dash
import dash_bootstrap_components as dbc

from backend.data_loader import load_lifts
from frontend.layout import make_layout
from callbacks.register_callbacks import register_callbacks


def create_app():
    """
    Create and configure the Dash application.

    This function:
    - Initializes the Dash app with Bootstrap styling
    - Loads the lifts dataset
    - Builds the main layout
    - Registers all callbacks

    Returns:
    - app : Dash
        Fully configured Dash application.
    - server : Flask
        Underlying Flask server for deployment.
    """

    # Initialize app with Bootstrap theme + Bootstrap Icons (required for icons)
    external_stylesheets = [
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"
    ]

    app = Dash(__name__, external_stylesheets=external_stylesheets)
    server = app.server

    # Load dataset
    df = load_lifts()

    # Apply main layout
    app.layout = make_layout(app, df["Exercises"].unique())

    # Register callbacks
    register_callbacks(app, df)

    return app, server


# Run the application
if __name__ == "__main__":
    app, server = create_app()
    app.run(debug=True, port=8050)