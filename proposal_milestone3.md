# Milestone 3 Proposal — NYC 311 Service Dynamics

## Why this matters
NYC’s 311 service requests reveal how residents experience day-to-day city life: noise that keeps neighborhoods awake, sidewalk hazards that impede mobility, and power outages that spark safety concerns. With nearly 3 million requests every year, surfacing where, when, and how issues are reported helps prioritize limited city resources and surfaces inequities between neighborhoods. This milestone focuses on translating those insights into compelling, data-driven stories backed by clean, analysis-ready data.

## Research questions & planned visuals

| Question | Why it’s interesting | Planned D3 visualization |
| --- | --- | --- |
| **Q1. How has the volume of 311 requests evolved since 2020 across boroughs?** | Captures post-pandemic recovery, seasonal surges, and borough-specific spikes (e.g., sanitation complaints in 2023). | Multi-series line/area chart grouped by month with borough + complaint filters (brushing to highlight anomalies). |
| **Q2. What complaint types dominate each borough and how concentrated are they?** | Shows whether boroughs face distinct challenges (noise vs. heating) and identifies service specialization needs. | Stacked/grouped horizontal bars showing % share of top complaint types per borough with tooltips revealing totals. |
| **Q3. When during the week and day do high-impact complaints occur?** | Pinpoints operational staffing opportunities (e.g., noise at night, heat complaints in early morning). | Interactive heatmap (weekday × hour) for selected complaint type; color encodes normalized volume, tooltip quantifies counts. |
| **Q4. Where do residents wait the longest for resolution?** | Highlights service equity concerns; longer waits may correlate with under-resourced neighborhoods. | Binned hex/scatter map of NYC colored by median response time with filter to swap to complaint density. |
| **Q5. Which reporting channels (phone, app, website) are most used per complaint type?** | Informs outreach strategy and accessibility, showing whether digital adoption varies by issue. | Diverging stacked bar or bump chart comparing request channels by complaint type (mobile vs. web vs. phone). |

The final dashboard will link these questions via shared filters (borough, timeframe, complaint type) to encourage multi-faceted exploration.

## Data preparation plan

1. **Column subset:** Extract only high-value fields from the 24.5 GB raw CSV: `Unique Key`, `Created Date`, `Closed Date`, `Agency`, `Agency Name`, `Complaint Type`, `Descriptor`, `Status`, `Borough`, `City`, `Incident Zip`, `Latitude`, `Longitude`, `Location Type`, `Open Data Channel Type`.
2. **Time features:** Parse dates to ISO strings and derive `year`, `month`, `month_name`, `day_of_week`, `hour`, `season`, and `is_weekend` to avoid recomputation in Observable.
3. **Response metrics:** Compute `response_hours` when closed dates exist; cap extreme values (> 45 days) to mitigate anomalies and keep the file tidy.
4. **Filtering:** Keep requests from **Jan 2020 forward**—enough history for trends while trimming file size to ~2–3 GB.
5. **Chunked export:** Stream the raw CSV with `pandas.read_csv(..., chunksize=250_000)` and append to `src/data/311_curated_2020.csv`. Drop rows missing geolocation or borough for map-heavy questions.
6. **Quality checks:** Track row counts per chunk, log duplicates removed by `unique_key`, and emit a JSON metadata summary (row count, time span, null stats) for reproducibility.

## Milestone 3 delivery outline

1. **Intro section:** Short narrative on the importance of 311 data plus dataset snapshot (records, date range, column definitions).
2. **Per-question sections:** Each includes the question prompt, the interactive D3 chart, a short paragraph describing notable patterns, and a direct answer referencing the visualization.
3. **Interaction scaffolding:** Global Inputs (borough/select complaint type/date range) stored in `viewof` cells so that each chart can reference them.
4. **Next steps:** Document polish tasks (storytelling, annotations, responsive layout) and potential additional data (borough population for per-capita metrics).

This plan addresses the instructor’s feedback by centering “why it’s interesting,” specifying D3 encodings for each research question, and laying groundwork for a cohesive, insight-rich dashboard.
