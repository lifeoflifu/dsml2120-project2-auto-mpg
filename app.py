from base64 import b64encode
from pathlib import Path

import pandas as pd
import streamlit as st

from auto_data import DATA_PATH, KAGGLE_URL, ORIGINS, UCI_URL, brand_summary, load_data, year_summary
from charts import acceleration_boxes, brand_bars, horsepower_scatter, mpg_line


st.set_page_config(page_title="Auto MPG · Lifu Deng", page_icon="🚘", layout="wide")
st.html("""
<style>
[data-testid="stMainBlockContainer"] {max-width: 1180px; padding-top: 2.75rem;}
[data-testid="stHeading"] h1 {letter-spacing: -0.045em;}
[data-testid="stMetric"] {
    background: #E9F2EE; border: 1px solid #CEDFD7;
    border-radius: 0.65rem; padding: 0.8rem 1rem;
}
</style>
""")
DATA_SOURCE = f"[Kaggle Auto MPG]({KAGGLE_URL}) · [Original UCI dataset]({UCI_URL})"
CHART_CONFIG = {"displaylogo": False}
data, refreshed_at = load_data(DATA_PATH.stat().st_mtime_ns)


def bullets(items: list[str]) -> None:
    st.markdown("\n".join(f"- {item}" for item in items))


def chart_and_notes(figure, how_to_read: list[str], observations: list[str]) -> None:
    st.plotly_chart(figure, theme=None, config=CHART_CONFIG)
    st.caption(f"Source · {DATA_SOURCE}")
    reading, findings = st.columns(2, gap="large")
    with reading:
        st.markdown("**How to read this chart**")
        bullets(how_to_read)
    with findings:
        st.markdown("**What stands out**")
        bullets(observations)


def bio_page() -> None:
    st.caption("DSML 2120 DATA VISUALIZATION · PROJECT 2")
    st.title("Lifu Deng")
    st.write("Data science and machine learning student · MSU Denver")
    picture, introduction = st.columns([1, 3], gap="large", vertical_alignment="center")
    with picture:
        image_path = Path(__file__).resolve().parent / "assets" / "lifu_deng.jpeg"
        image_data = b64encode(image_path.read_bytes()).decode("ascii")
        st.html(
            '<figure style="margin:0;max-width:190px">'
            f'<img src="data:image/jpeg;base64,{image_data}" alt="Portrait of Lifu Deng" '
            'style="width:100%;height:auto;border-radius:0.65rem">'
            '<figcaption style="margin-top:0.35rem;font-size:0.85rem">Lifu Deng</figcaption>'
            '</figure>'
        )
    with introduction:
        st.write(
            "I study data science and machine learning at Metropolitan State University of Denver "
            "with a minor in computer security. I use Python, pandas, Plotly, and Streamlit in my "
            "coursework. I’m interested in making data easier to explore and communicating what "
            "the evidence shows."
        )
        st.link_button("GitHub · lifeoflifu", "https://github.com/lifeoflifu")
    st.subheader("Highlights")
    bullets([
        "Built a Streamlit dashboard to help readers explore an e-commerce funnel.",
        "Use pandas to check, clean, and summarize datasets for visualization.",
        "Explore interactive charts with Plotly and Streamlit.",
    ])
    st.subheader("Visualization philosophy")
    st.write(
        "I want the chart to answer the reader’s question at a glance. I label measures and units, "
        "pair color with text or shape, and explain where the data limits the conclusion."
    )


def gallery_page() -> None:
    st.title("EDA Gallery")
    st.write("Four questions about fuel economy and performance in the 1970–1982 Auto MPG sample.")

    st.header("Which brands averaged the most MPG?")
    st.write("Compare average city fuel economy for the brands represented in the dataset.")
    brands = brand_summary(data)
    thresholds = {"All brands": 1, "At least 3 cars": 3, "At least 5 cars": 5, "At least 10 cars": 10}
    brand_filter = st.selectbox("Minimum cars per brand", list(thresholds), key="gallery_min_brand")
    ranked = brands.loc[brands["cars"].ge(thresholds[brand_filter])].head(10)
    leader = ranked.iloc[0]
    five_car_leader = brands.loc[brands["cars"].ge(5)].iloc[0]
    largest = brands.loc[brands["cars"].idxmax()]
    chart_and_notes(
        brand_bars(ranked),
        [
            "Up to ten qualifying brands appear, ordered by average MPG.",
            "A longer bar represents more miles per gallon in city-cycle testing.",
            "The value marked n is the number of cars behind the average.",
        ],
        [
            f"**{leader.brand}** leads this view at **{leader.average_mpg:.1f} MPG** "
            f"based on {leader.cars} {'car' if leader.cars == 1 else 'cars'}.",
            f"Among brands with five or more cars, **{five_car_leader.brand}** leads at "
            f"**{five_car_leader.average_mpg:.1f} MPG**.",
            f"**{largest.brand}** has the broadest coverage ({largest.cars} cars). "
            "Group sizes vary considerably across brands.",
        ],
    )

    st.divider()
    st.header("How does MPG vary with horsepower?")
    st.write("Look for an association between fuel economy and engine power.")
    complete = data.dropna(subset=["horsepower"])
    horsepower = complete["horsepower"]
    lower_mpg = complete.loc[horsepower.le(horsepower.quantile(0.25)), "mpg"].median()
    upper_mpg = complete.loc[horsepower.ge(horsepower.quantile(0.75)), "mpg"].median()
    association = complete["horsepower"].corr(complete["mpg"])
    chart_and_notes(
        horsepower_scatter(complete),
        [
            "Read engine horsepower left to right and city MPG bottom to top.",
            "Each dot is one vehicle. Color and shape identify its origin.",
            "Hover for the vehicle name, model year, and cylinder count.",
        ],
        [
            f"The overall association is negative (**Pearson r = {association:.2f}**).",
            f"The bottom horsepower quarter had a median of **{lower_mpg:.1f} MPG**, "
            f"versus **{upper_mpg:.1f} MPG** in the top quarter, including ties.",
            f"The plot includes **{len(complete)} cars**. "
            f"**{len(data) - len(complete)}** have no recorded horsepower.",
        ],
    )

    st.divider()
    st.header("How did typical MPG change by model year?")
    st.write("Compare the typical city fuel economy of the sampled cars across 13 model years.")
    years = year_summary(data)
    first, last = years.iloc[0], years.iloc[-1]
    best = years.loc[years["median_mpg"].idxmax()]
    year_1973 = years.set_index("model_year").loc[1973, "median_mpg"]
    chart_and_notes(
        mpg_line(data),
        [
            "Each point represents the median MPG of one model year.",
            "A rising line shows an increase in median MPG between model years.",
            "Hover to see how many vehicles contributed to each median.",
        ],
        [
            f"Median MPG rose from **{first.median_mpg:.1f}** in {int(first.model_year)} "
            f"to **{last.median_mpg:.1f}** in {int(last.model_year)}.",
            f"The upward trend includes setbacks. Median MPG returned to **{year_1973:.1f}** in 1973.",
            f"**{int(best.model_year)}** had the highest median at **{best.median_mpg:.1f} MPG**, "
            f"based on **{int(best.cars)} cars**.",
        ],
    )

    st.divider()
    st.header("How did acceleration times vary by cylinder count?")
    st.write("Compare typical 0–60 mph times and their spread across cylinder groups.")
    groups = data.groupby("cylinders")["acceleration"].agg(["size", "median", "min", "max"])
    eight, four, six = (groups.loc[number] for number in (8, 4, 6))
    chart_and_notes(
        acceleration_boxes(data),
        [
            "The vertical axis is seconds to reach 60 mph. Lower is faster.",
            "The line inside each box marks the median. The box covers the middle half.",
            "Whiskers and separate points show how far times extend beyond the box.",
        ],
        [
            f"Eight-cylinder cars had a median of **{eight['median']:.1f} s**, compared with "
            f"**{four['median']:.1f} s** for four cylinders and **{six['median']:.1f} s** for six.",
            f"Eight-cylinder times ranged from **{eight['min']:.1f}** to **{eight['max']:.1f} s**, "
            "overlapping times in the four- and six-cylinder groups.",
            f"There are only **{int(groups.loc[3, 'size'])} three-cylinder** and "
            f"**{int(groups.loc[5, 'size'])} five-cylinder** cars, so their boxes summarize few observations.",
        ],
    )


def dashboard_page() -> None:
    st.title("Auto MPG Dashboard")
    st.write("Explore how city fuel economy and performance change across model years and origins.")
    year_control, origin_control = st.columns([1, 1], gap="large")
    first_year, last_year = int(data["model_year"].min()), int(data["model_year"].max())
    with year_control:
        low, high = st.slider(
            "Model year range", first_year, last_year, (first_year, last_year),
            key="dashboard_year", format="%d",
        )
    with origin_control:
        origins = st.multiselect("Vehicle origin", list(ORIGINS.values()),
                                 default=list(ORIGINS.values()), key="dashboard_origins")
    selection = data.loc[data["model_year"].between(low, high) & data["origin_label"].isin(origins)]
    st.caption(
        f"Source · {DATA_SOURCE}  |  Data last refreshed {refreshed_at:%Y-%m-%d %H:%M UTC}"
    )
    if selection.empty:
        st.info("No cars match this selection. Choose an origin or widen the model year range.")
        return

    count, fuel, acceleration = st.columns(3)
    count.metric("Vehicles", f"{len(selection):,}")
    fuel.metric("Median city fuel economy", f"{selection['mpg'].median():.1f} MPG")
    acceleration.metric("Median 0–60 mph time", f"{selection['acceleration'].median():.1f} s")

    line_column, scatter_column = st.columns(2, gap="large")
    complete = selection.dropna(subset=["horsepower"])
    with line_column:
        st.subheader("Median MPG by model year")
        st.plotly_chart(mpg_line(selection), theme=None, config=CHART_CONFIG)
    with scatter_column:
        st.subheader("Horsepower and fuel economy")
        if complete.empty:
            st.info("The selected cars have no recorded horsepower.")
        else:
            st.plotly_chart(horsepower_scatter(complete), theme=None, config=CHART_CONFIG)

    st.subheader("What this selection shows")
    years = year_summary(selection)
    first, last = years.iloc[0], years.iloc[-1]
    if len(years) > 1:
        year_insight = (
            f"Median MPG was **{first.median_mpg:.1f}** in {int(first.model_year)} "
            f"and **{last.median_mpg:.1f}** in {int(last.model_year)} across the selected cars."
        )
    else:
        year_insight = f"The selection covers **{int(first.model_year)}** with a median of **{first.median_mpg:.1f} MPG**."
    by_origin = selection["origin_label"].value_counts()
    origin_details = ", ".join(f"{name} ({size})" for name, size in by_origin.items())
    association = (
        complete["horsepower"].corr(complete["mpg"])
        if complete["horsepower"].nunique() > 1 and complete["mpg"].nunique() > 1 else None
    )
    power_insight = (
        f"The horsepower plot uses **{len(complete)}** selected cars. "
        f"The horsepower–MPG association is **r = {association:.2f}**."
        if association is not None else
        f"The horsepower plot has **{len(complete)}** selected cars with both measurements."
    )
    bullets([
        year_insight,
        f"The selected cars come from {origin_details}. Group sizes affect the medians.",
        power_insight,
        "These are historical city-cycle measurements. Changes in which vehicles were sampled "
        "can contribute to the differences you see.",
    ])


def future_page() -> None:
    st.title("Future Work")
    st.subheader("What I’d explore next")
    bullets([
        "Compare fuel economy within the same cylinder group to see how much the overall horsepower pattern changes.",
        "Use a newer fuel-economy dataset with documented test methods to investigate later model years.",
        "Add a vehicle comparison view for two models with MPG, horsepower, and 0–60 mph time side by side.",
        "Test the charts with a keyboard and screen reader, and add a compact data table as an alternative view.",
    ])
    st.subheader("What changed from the Lab 4.3 prototype")
    bullets([
        "I kept the prototype’s metrics-first layout so readers can see the selected group before examining detailed charts.",
        "I changed the shared filter controls from website traffic and devices to model year and vehicle origin.",
        "I added a separate gallery for chart-reading guides and observations so the dashboard can stay focused on exploration.",
    ])


pages = {"Bio": bio_page, "EDA Gallery": gallery_page, "Dashboard": dashboard_page, "Future Work": future_page}
st.sidebar.title("Auto MPG")
st.sidebar.caption("Lifu Deng · DSML 2120")
page = st.sidebar.radio("Go to", list(pages), label_visibility="collapsed")
pages[page]()
