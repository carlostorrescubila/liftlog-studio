from dash import html
import dash_bootstrap_components as dbc


def kpi_card(
    title,
    value,
    subtitle="",
    icon=None,
    bg_color="#FFCC00",
    border_color="#000000",
    text_color="#000000"
):
    """
    Build a KPI card component with optional icon, title, value and subtitle.

    Parameters
    ----------
    title : str
        Title displayed at the top of the card.
    value : str or list
        Main KPI value. Can be a string or a list of HTML elements.
    subtitle : str, optional
        Additional text displayed below the value.
    icon : str, optional
        Emoji or icon displayed above the title.
    bg_color : str
        Background color of the card.
    border_color : str
        Border color of the card.
    text_color : str
        Text color used for title and value.

    Returns
    -------
    dbc.Card
        A styled KPI card component.
    """

    # Optional icon displayed at the top
    icon_component = None
    if icon:
        icon_component = html.Div(
            icon,
            style={
                "fontSize": "2.2rem",
                "textAlign": "center",
                "marginBottom": "0.3rem",
                "lineHeight": "1"
            }
        )

    # Value can be a string or a list of HTML elements
    if isinstance(value, list):
        # Render list items with consistent styling
        value_component = html.Div(
            [
                html.P(
                    item.children if hasattr(item, "children") else item,
                    style={
                        "margin": "2px 0",
                        "fontSize": "1.35rem",
                        "lineHeight": "1.2",
                        "color": text_color
                    }
                )
                for item in value
            ],
            style={"textAlign": "left"}
        )
    else:
        # Simple string value → render as H3
        value_component = html.H3(
            value,
            className="card-value",
            style={
                "textAlign": "center",
                "color": text_color,
                "marginBottom": "0.5rem"
            }
        )

    # Final card layout
    return dbc.Card(
        dbc.CardBody(
            [
                icon_component,
                html.H5(
                    title,
                    className="card-title",
                    style={
                        "textAlign": "center",
                        "color": text_color,
                        "fontWeight": "700"
                    }
                ),
                value_component,
                html.Small(
                    subtitle,
                    className="text-muted",
                    style={
                        "textAlign": "center",
                        "display": "block",
                        "marginTop": "0.3rem"
                    }
                )
            ]
        ),
        className="shadow-sm h-100",
        style={
            "backgroundColor": bg_color,
            "border": f"2px solid {border_color}",
            "borderRadius": "12px",
            "padding": "10px",
            "minWidth": "250px",
        }
    )


def kpi_card_trend(
    title,
    value,
    diff,
    pct,
    subtitle="",
    bg_color="#FFCC00",
    border_color="#000000",
    text_color="#000000"
):
    """
    Build a KPI card with trend information (arrow, diff, percentage).

    Parameters
    ----------
    title : str
        Title displayed at the top of the card.
    value : str or list
        Main KPI value.
    diff : float
        Absolute difference vs previous period.
    pct : float
        Percentage difference vs previous period.
    subtitle : str, optional
        Additional text displayed below the value.
    bg_color : str
        Background color of the card.
    border_color : str
        Border color of the card.
    text_color : str
        Text color used for title and value.

    Returns
    -------
    dbc.Card
        A styled KPI card with trend indicators.
    """

    # Determine arrow and color based on trend direction
    if diff > 0:
        arrow = "▲"
        trend_color = "green"
    elif diff < 0:
        arrow = "▼"
        trend_color = "red"
    else:
        arrow = "■"
        trend_color = "gray"

    trend_text = f"{arrow} {abs(diff):.0f} ({pct:.1f}%) vs last month"

    # Value can be a string or a list
    if isinstance(value, list):
        value_component = html.Div(
            [
                html.P(
                    item.children if hasattr(item, "children") else item,
                    style={
                        "margin": "2px 0",
                        "fontSize": "1.35rem",
                        "lineHeight": "1.2",
                        "color": text_color
                    }
                )
                for item in value
            ],
            style={"textAlign": "left"}
        )
    else:
        value_component = html.H3(
            value,
            className="card-value",
            style={
                "textAlign": "center",
                "color": text_color,
                "marginBottom": "0.5rem"
            }
        )

    # Final card layout
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    title,
                    className="card-title",
                    style={
                        "textAlign": "center",
                        "color": text_color,
                        "fontWeight": "700"
                    }
                ),
                value_component,
                html.Small(
                    subtitle,
                    className="text-muted",
                    style={
                        "textAlign": "center",
                        "display": "block",
                        "marginTop": "0.3rem"
                    }
                ),
                html.Small(
                    trend_text,
                    style={
                        "textAlign": "center",
                        "display": "block",
                        "marginTop": "0.3rem",
                        "fontWeight": "700",
                        "color": trend_color
                    }
                )
            ]
        ),
        className="shadow-sm h-100",
        style={
            "backgroundColor": bg_color,
            "border": f"2px solid {border_color}",
            "borderRadius": "12px",
            "padding": "10px"
        }
    )