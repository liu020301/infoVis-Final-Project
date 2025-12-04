# NYC 311 Service Dynamics — Final Project

Summary
- Exploratory InfoVis analysis of NYC 311 service requests (2010–present) using D3 and prepared CSV exports.  

Group
- Zehao Liu (zl6194)  
- Junyuan Wang (jw9178)  
- Jiangnan Li (jl18011)

Key files
- Source pages: `src/index.md`, `src/pages/milestone3.md`  
- Data exports: `src/data/exports/`
  - q1_monthly_trends.csv
  - q2_complaints_by_borough.csv
  - q3_hourly_patterns.csv
  - q4_response_by_location.csv
  - q5_channels_by_complaint.csv

Main questions (Q1–Q5)
- Q1: How has the volume of 311 requests evolved since 2010 across boroughs??  
- Q2: What complaint types dominate each borough and how concentrated are they??  
- Q3: When during the week and day do high-impact complaints occur? 
- Q4: Where do residents wait the longest for resolution?
- Q5: Which reporting channels are most used per complaint type?

How to run (Mac)
- Requirements: Node.js, pnpm or npm.  
- Install:
  - pnpm: `pnpm install`
  - npm: `npm install`
- Dev/preview:
  - `pnpm dev` or `npm run dev`

Data source and license
- Data: "311 Service Requests from 2010 to Present" — NYC Open Data.  
    https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/about_data 
- Visualizations implemented with D3.js.