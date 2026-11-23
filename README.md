# Auto MPG | Fuel Economy & Performance

**Lifu Deng · DSML 2120 · Project 2**

A Streamlit portfolio and dashboard that explores city fuel economy and performance across the cars in the Auto MPG dataset. Compare brands, explore the relationship between horsepower and MPG, follow model-year trends, and compare 0–60 mph times across cylinder counts. [Professional GitHub profile](https://github.com/lifeoflifu)

## App navigation

- **Bio** introduces my coursework, tools, and visualization philosophy.
- **EDA Gallery** presents four questions with a bar chart, scatter plot, line chart, and box plot. Each chart includes a reading guide, observations, and source credit.
- **Dashboard** filters the same records by model year and origin. The filters update all three KPIs, both charts, and the insights.
- **Future Work** outlines four next steps and reflects on changes from the Lab 4.3 prototype.

## Dataset

The bundled CSV contains **398 vehicles** from model years **1970–1982**. It includes city-cycle MPG, engine horsepower, weight, cylinder count, origin, and 0–60 mph time. These are historical records from a particular mix of cars, so comparisons describe the sample. [Kaggle download](https://www.kaggle.com/datasets/uciml/autompg-dataset) · [Quinlan, R. (1993), Auto MPG, UCI](https://doi.org/10.24432/C5859H) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · [Acceleration documentation](https://search.r-project.org/CRAN/refmans/ISLR2/html/Auto.html)

The app preserves every row, expands two-digit model years, and labels origin codes. It derives brand labels from vehicle names, standardizes obvious variants such as VW and Volkswagen, and retains ambiguous prefixes as source labels. It omits the six records with missing horsepower from horsepower plots. The sidebar and chart labels use plain language, and the scatter plots pair group color with marker shape.

## Run locally

Use Python 3.13, the version used to verify the app. Install the versioned dependencies in [requirements.txt](requirements.txt) and start Streamlit from this directory.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

For Streamlit Community Cloud, select this repository and set the entry point to `app.py`.

## AI assistance

AI assistance was used for question development, wording, and coding support.
