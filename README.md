# Cape Town's Short-Term Rental Market

**How much of "home sharing" in Cape Town is actually a commercial industry?**

### 🔗 [Open the interactive dashboard →](https://siya990808.github.io/dashboards/cape-town-rentals/)

Filterable choropleth of all 116 City of Cape Town wards — slice by room type, host portfolio size and price band, and every figure recomputes exactly.

> Postgraduate Diploma in Data Analytics · IIE Varsity College · Siyabonga Mfusi

---

## The question

Airbnb's founding story is a spare room. Cape Town has a serious housing shortage, so whether that story still describes what is happening is not an abstract question — it decides whether short-term rentals are a household income supplement or an industry withdrawing housing stock.

That is empirical. This analyses **27,381 active listings** and **10 million rows** of forward availability from an Inside Airbnb snapshot dated 29 June 2026.

## Findings

**84.5% of listings are entire homes or apartments.** Whole properties, not spare rooms — dwellings removed from the residential rental pool.

**A quarter of hosts control almost two-thirds of the listings.**

| Hosts with… | Share of hosts | Share of listings |
|---|---:|---:|
| 2+ listings | 25.6% | **62.0%** |
| 5+ listings | 5.9% | 37.0% |
| 20+ listings | **0.7%** | 16.3% |
| 50+ listings | 0.2% | 8.0% |

That is the distribution of an industry with professional operators, not a neighbourhood of residents letting a room. And the largest operators skew harder still: filter the dashboard to hosts with 20+ listings and **93.3%** of their stock is entire homes, against 84.2% overall.

**Location premiums are extreme** — median nightly rates run from **R701 to R4,265** across wards, a 6.1× spread.

**Almost nothing is licensed** — 0.6% of listings display a licence number. That figure needs care, and the limitations section below explains why.

### What drives the nightly rate

| Feature | Spearman ρ with price |
|---|---:|
| Accommodates | **0.706** |
| Bedrooms | 0.699 |
| Review score | 0.193 |
| Availability (365d) | −0.119 |
| Number of reviews | −0.134 |

Capacity dominates. A good deal of "Cape Town is expensive" is really "Cape Town lists large houses".

## Why the map matters

Inside Airbnb reports Cape Town location as **City of Cape Town ward numbers** — the `neighbourhood` field is null for all 27,381 listings. "Ward 62" means nothing to a reader on its own.

Rather than invent suburb names the data cannot support, this project ships a map. On the dashboard you can *see* that Ward 62 is the Atlantic Seaboard and which wards are the Cape Flats, instead of being told.

## Method

**Two cleaning decisions carry the analysis.**

Price arrives as a formatted string (`$1,231.00`) and must be parsed. Despite the dollar sign these are **rand** — Inside Airbnb formats local currency with `$`. A median of R1,735 a night for a Cape Town entire home is plausible; $1,735 would not be.

The top of the distribution is not real: the maximum reported rate is R999,537 a night. Listings outside R50–R50,000 are excluded from price analysis (109 listings) while still counting toward market size and ownership structure.

| Step | Listings | % of snapshot |
|---|---:|---:|
| In snapshot | 27,381 | 100.0% |
| With a published price | 24,542 | 89.6% |
| Price in a credible range | 24,433 | 89.2% |

## Three artefacts, one pipeline

The notebook is the single source of the cleaned figures and exports both downstream artefacts, so they cannot drift apart.

| | |
|---|---|
| **Notebook** | `notebooks/cape_town_rental_market.ipynb` — full analysis with static figures |
| **Web dashboard** | [live here](https://siya990808.github.io/dashboards/cape-town-rentals/) · source in `dashboard/` |
| **Power BI kit** | `powerbi/` — star schema CSVs, DAX measures, build guide |

The dashboard ships the **listing-level values**, not pre-aggregated cells. A weighted median of group medians lands about 15% below the true median on this distribution, so every figure it shows under any filter combination is exact rather than approximate. The notebook asserts that its own median matches the dashboard payload before writing it.

## Figures

| | |
|---|---|
| `figure_1_market_shape.png` | Price distribution and room-type mix |
| `figure_2_ownership.png` | Host portfolio sizes and the concentration curve |
| `figure_3_ward_prices.png` | The 18 most expensive wards |
| `figure_4_availability.png` | Forward availability by month |

## Reproducing

```bash
pip install -r requirements.txt
python src/download_data.py
jupyter notebook notebooks/cape_town_rental_market.ipynb
```

Data is ~85 MB compressed and not committed; the download script fetches it.

## Limitations

**A snapshot, not a history.** One scrape cannot show whether concentration is rising or falling — which is the question a policymaker would actually ask.

**Listed price is not achieved price.** This is the advertised nightly rate, before discounts, cleaning fees and commission, with no evidence anyone paid it.

**Availability is not occupancy.** An unavailable night is either booked or blocked by the host, and the two are indistinguishable here. A booking curve also inflates near-term months — nights close to the scrape date are likelier to be taken simply because they are nearer. The monthly series is a shape, not a measurement, and the notebook says so where it is plotted.

**The licence figure records disclosure, not compliance.** The field captures what a host published on the listing, not whether a licence exists. A 0.6% rate is consistent with widespread non-compliance *or* with hosts not publishing numbers they hold. The data cannot separate the two and this project does not claim to.

**Host identity is per account.** One operator running several accounts appears as several small hosts, so the concentration measured here is a **floor**, not a ceiling.

## Data

[Inside Airbnb](https://insideairbnb.com/get-the-data/) — Cape Town, 29 June 2026 snapshot, CC BY 4.0. Basemap © OpenStreetMap contributors.

## Tech

Python · pandas · NumPy · Matplotlib · Jupyter · Leaflet · Power BI
