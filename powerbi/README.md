# Power BI build kit

Everything needed to build a Power BI report from this analysis without redoing any of it. Power BI Desktop is free — [download it here](https://powerbi.microsoft.com/desktop/).

The three CSVs in this folder come out of `notebooks/cape_town_rental_market.ipynb`, so they carry the same cleaning as the notebook and the web dashboard: price parsed from its formatted string, listings outside R50–R50,000 excluded, host portfolios already bucketed.

## The model

A star schema — one fact table, two dimensions.

```
        dim_ward                     dim_host
     (ward, 85 rows)            (host_id, 13,978 rows)
            │                            │
            │ 1                        1 │
            │                            │
            └────────► fact_listings ◄───┘
                        (27,381 rows)
```

| File | Grain | Key |
|---|---|---|
| `fact_listings.csv` | One row per listing | `listing_id` |
| `dim_ward.csv` | One row per City of Cape Town ward | `ward` |
| `dim_host.csv` | One row per host account | `host_id` |

### Relationships to create

In **Model view**, drag to create both:

| From | To | Cardinality | Direction |
|---|---|---|---|
| `fact_listings[ward]` | `dim_ward[ward]` | Many to one | Single |
| `fact_listings[host_id]` | `dim_host[host_id]` | Many to one | Single |

Set both dimension tables' key columns to **Don't summarize** so Power BI stops trying to sum them.

## Steps

1. **Get data → Text/CSV**, load all three files. Set `price_zar`, `latitude`, `longitude` to Decimal Number; `accommodates`, `bedrooms`, `reviews_total` to Whole Number; `is_superhost`, `is_licensed` to True/False.
2. Create the two relationships above.
3. Paste the measures below (**Modeling → New measure**, one at a time).
4. Build the visuals.

## Measures

```dax
Listings = COUNTROWS ( fact_listings )

Hosts = DISTINCTCOUNT ( fact_listings[host_id] )

Median Price =
MEDIAN ( fact_listings[price_zar] )

Entire Homes % =
DIVIDE (
    CALCULATE ( [Listings], fact_listings[room_type] = "Entire home/apt" ),
    [Listings]
)

Commercial Listings % =
DIVIDE (
    CALCULATE ( [Listings], dim_host[host_profile] <> "Single listing" ),
    [Listings]
)

Licensed % =
DIVIDE ( CALCULATE ( [Listings], fact_listings[is_licensed] = TRUE () ), [Listings] )

Superhost % =
DIVIDE ( CALCULATE ( [Listings], fact_listings[is_superhost] = "t" ), [Listings] )

-- Wards with a thin sample give unstable medians. Blank them rather than show noise.
Median Price (ranked) =
IF ( [Listings] >= 30, [Median Price] )

-- Share of all listings held by the largest hosts, ignoring the ward filter
Top Host Share % =
VAR TopHosts =
    TOPN ( 100, ALL ( dim_host ), dim_host[listings_held], DESC )
RETURN
    DIVIDE (
        CALCULATE ( [Listings], KEEPFILTERS ( TopHosts ) ),
        CALCULATE ( [Listings], ALL ( dim_host ) )
    )

Avg Listings per Host =
DIVIDE ( [Listings], [Hosts] )
```

## Visuals worth building

| Visual | Fields |
|---|---|
| **Filled map** — the centrepiece | Location `dim_ward[ward]`, Colour saturation `[Median Price (ranked)]`. Use latitude/longitude from `dim_ward` if the ward names do not geocode |
| **KPI cards** | `[Listings]`, `[Median Price]`, `[Commercial Listings %]`, `[Entire Homes %]`, `[Licensed %]` |
| **Bar chart** | Axis `dim_ward[ward]`, Value `[Median Price (ranked)]`, Top-N filter 15 |
| **Clustered bar** | Axis `dim_host[host_profile]`, Values `[Listings]` and `[Hosts]` — the ownership asymmetry |
| **Scatter** | X `fact_listings[accommodates]`, Y `[Median Price]`, Legend `fact_listings[room_type]` |
| **Slicers** | `fact_listings[room_type]`, `dim_host[host_profile]`, `fact_listings[price_zar]` as a numeric range |

## A note on the map visual

Power BI's filled map geocodes by name, and "Ward 62" is not a place it recognises. Two options:

- Set the ward field's **Data category** to *Place* and add a `dim_ward[lat]` / `dim_ward[lon]` bubble map instead — reliable, no geocoding needed.
- Or import `data/neighbourhoods.geojson` (converted to TopoJSON) into a **Shape Map** visual, which draws the actual ward boundaries. This matches what the web dashboard shows.

The bubble map is the faster route; the shape map is the better-looking one.

## Why there is a web dashboard too

`.pbix` files cannot be shared live without a Power BI Pro licence, so the interactive version people can actually click lives at
[siya990808.github.io/dashboards/cape-town-rentals](https://siya990808.github.io/dashboards/cape-town-rentals/).
Both are driven by the same exported figures, so they agree.
