import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from auto_data import year_summary


INK = "#172D37"
BLUE = "#155C9E"
TEAL = "#09685D"
ORIGIN_COLORS = {"United States": BLUE, "Europe": "#9B4615", "Japan": TEAL}
ORIGIN_SYMBOLS = {"United States": "circle", "Europe": "diamond", "Japan": "square"}


def chart_layout(figure: go.Figure, height: int = 390) -> go.Figure:
    figure.update_layout(
        height=height,
        margin=dict(l=12, r=25, t=42, b=14),
        font=dict(color=INK, size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.08, x=0, title_text=""),
    )
    figure.update_xaxes(gridcolor="#DCE6E1", automargin=True, zeroline=False)
    figure.update_yaxes(gridcolor="#DCE6E1", automargin=True, zeroline=False)
    return figure


def brand_bars(summary: pd.DataFrame) -> go.Figure:
    figure = go.Figure(
        go.Bar(
            x=summary["average_mpg"],
            y=summary["brand"],
            orientation="h",
            marker_color=TEAL,
            text=[f"{row.average_mpg:.1f} MPG · n={row.cars}" for row in summary.itertuples()],
            textposition="outside",
            cliponaxis=False,
            customdata=summary[["cars"]],
            hovertemplate="%{y}<br>%{x:.1f} MPG average<br>%{customdata[0]} cars<extra></extra>",
        )
    )
    chart_layout(figure, height=max(330, 36 * len(summary) + 90))
    figure.update_layout(margin=dict(r=92, t=10))
    figure.update_xaxes(title="Average city fuel economy (MPG)", rangemode="tozero")
    figure.update_yaxes(title=None, autorange="reversed", showgrid=False)
    return figure


def horsepower_scatter(complete: pd.DataFrame) -> go.Figure:
    figure = px.scatter(
        complete,
        x="horsepower",
        y="mpg",
        color="origin_label",
        symbol="origin_label",
        category_orders={"origin_label": list(ORIGIN_COLORS)},
        color_discrete_map=ORIGIN_COLORS,
        symbol_map=ORIGIN_SYMBOLS,
        hover_name="car_name",
        hover_data={"model_year": True, "cylinders": True, "origin_label": True},
        labels={
            "horsepower": "Engine power (horsepower)",
            "mpg": "City fuel economy (MPG)",
            "model_year": "Model year",
            "cylinders": "Cylinders",
            "origin_label": "Origin",
        },
    )
    figure.update_traces(marker=dict(size=8, opacity=0.75, line=dict(color=INK, width=0.5)))
    return chart_layout(figure)


def mpg_line(data: pd.DataFrame) -> go.Figure:
    years = year_summary(data)
    figure = go.Figure(
        go.Scatter(
            x=years["model_year"],
            y=years["median_mpg"],
            mode="lines+markers",
            line=dict(color=TEAL, width=3),
            marker=dict(size=8, symbol="circle"),
            customdata=years[["cars"]],
            hovertemplate="Model year %{x}<br>Median %{y:.1f} MPG<br>%{customdata[0]} cars<extra></extra>",
        )
    )
    chart_layout(figure)
    figure.update_xaxes(title="Model year", tickformat="d", dtick=2)
    figure.update_yaxes(title="Median city fuel economy (MPG)", rangemode="tozero")
    return figure


def acceleration_boxes(data: pd.DataFrame) -> go.Figure:
    cylinders = data.groupby("cylinders").size()
    figure = go.Figure()
    for count, size in cylinders.items():
        times = data.loc[data["cylinders"].eq(count), "acceleration"]
        figure.add_trace(
            go.Box(
                y=times,
                name=f"{count} cylinders · n={size}",
                boxpoints="outliers",
                line=dict(color=BLUE, width=2),
                fillcolor="rgba(21,92,158,0.18)",
                quartilemethod="linear",
            )
        )
    chart_layout(figure)
    figure.update_layout(showlegend=False)
    figure.update_xaxes(title="Cylinder count and group size")
    figure.update_yaxes(title="0–60 mph time (seconds)")
    return figure
