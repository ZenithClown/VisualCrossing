<h1 align = "center">
  Visual-Crossing Weather API <img src = "./assets/logo.png" height = "190" width = "175" align = "right" /><br>
  <a href = "https://www.linkedin.com/in/dpramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/linkedin.svg"/></a>
  <a href = "https://github.com/ZenithClown"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/github.svg"/></a>
  <a href = "https://gitlab.com/ZenithClown/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/gitlab.svg"/></a>
  <a href = "https://www.researchgate.net/profile/Debmalya_Pramanik2"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/researchgate.svg"/></a>
  <a href = "https://www.kaggle.com/dPramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/kaggle.svg"/></a>
  <a href = "https://app.pluralsight.com/profile/Debmalya-Pramanik/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/pluralsight.svg"/></a>
  <a href = "https://stackoverflow.com/users/6623589/"><img height="16" width="16" src="https://unpkg.com/simple-icons@v3/icons/stackoverflow.svg"/></a>
</h1>

<div align = "justify">

In collaboration with [VisualCrossing](https://www.visualcrossing.com/weather-data) as a Weather Ambassador, I am creating a *python wrapper* that can fetch the historical, latest, and forecast weather data. The Visual Crossing Weather API provides developers with weather data for any programming language or script, using simple `.get()` requests. The Weather API provides instant and scalable access to historical weather reports and forecast data in an easy-to-use JSON or text format.

## Plans & Pricing

VisualCrossing provides five different types of subscriptions, with either *monthly* or *annual* payable plans. The annual payable plans offer *two months* of free data usage, i.e., about 16% cheaper than the monthly plan. The table below highlights the plan details (which may change over time), for more details visit [VisualCrossing/pricing](https://www.visualcrossing.com/weather-data-editions).

<div align = "center">

| Plan Name | Costing Details | No. API Calls |
| :---: | :---: | :---: |
| Free Tier | $ 0.00 / month | 1,000 (1k) Records/Month |
| Professional Tier | $ 35.00 / month | 10,000,000 (10M) Records/Month |
| Metered Connection (pay as you use) | $ 0.0001 / record | *unlimited* |
| Corporate Tier | $ 150.00 / month | *unlimited* |

</div>

In addition, you can contact the support for enterprise solutions. The `free` and `professional` tier has a single concurrency usage, while the `metered` connection has unlimited concurrency while the corporate account has a team concurrency and is billed together. The API service provided historical data of the last 50 years (currently, the data is available from 1975, as of 21.01.2024), while a **15-Days forecast** data is available under each tier.

## Getting Started

Weather data is a critical parameter in various forecasting projects ([1](https://www.britannica.com/science/weather-forecasting/Practical-applications), [2](https://www.vedantu.com/geography/weather-forecasting)) due to its widespread impact. Popular tools like **VisualCrossing** fetch data from various weather stations and provide an API-based service to query onto. A weather data record is typically divided into two tables/files - (I) `daily`: where the day-level information of a particular *"location"* is stored, and (II) an `hourly` value for the location.

### World Location DB

To fetch the data easily, a **`WorldDB.db`** file is provided with basic location information like - countries, states, and city names. The data is sourced and parsed from [OSS World-DB Site](https://countrystatecity.in/) and the data can be read and used in `python` using [`SQLite`](https://www.sqlite.org/index.html) engine.

```python
import sqlite3

con = sqlite3.connect("WorldDB.db")
records = pd.read_sql("SELECT * FROM vwWorldDB", con) # using pandas
records.sample()
```

The table `vwWorldDB` is the combined view of the `mwCountries`, `mwStates`, and `mwCities` tables, and the location of states/cities are in the format `latitude,longitude` and thus can be easily parsed using the `eval` statement in python. This is specifically done, because VisualCrossing accepts location information in `lat,lon` format, and thus the table can be easily used to fetch the data.

Thus said, it is recommended to integrate the data into your own database using an already existing key, or creating a new key for the use. Also, it is recommended to not use SQLite3 as database to save weather data as for large tables the query can be slow.

## Contributing

Contributions are welcomed. Do check our [contributing guide](CONTRIBUTING.md) for more information.

</div>
