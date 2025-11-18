---
title: Milestone 2 — NYC 311 Data Transformation & Sketches
files:
  - ../data/311_clean.csv
toc: false
pagefind: true
---

# 🧹 Step 1 — Data Transformation

We cleaned the NYC 311 Service Request dataset by:
- Removing unused columns (bridge, taxi, park, address fields, etc.)
- Renaming columns to consistent snake_case format  
- Parsing `created_date` into date objects and deriving `year`, `month`, `hour`, `day of week`, and `season`
- Cleaning text fields (trim + title case)
- Normalizing borough names and removing missing coordinates
- Filtering data from Oct 2024 onward for better performance

```js
import * as d3 from "npm:d3";

// Load the cleaned dataset
const rows = await FileAttachment("../data/311_clean.csv").csv();

display(Inputs.table(rows.slice(0, 10), {
  label: "Preview of First 10 Rows",
  rows: 10
}));