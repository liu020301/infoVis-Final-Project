---
title: Milestone 3 — NYC 311 Service Dynamics
files:
  - ../data/exports/q1_monthly_trends.csv
  - ../data/exports/q2_complaints_by_borough.csv
  - ../data/exports/q3_hourly_patterns.csv
  - ../data/exports/q4_response_by_location.csv
  - ../data/exports/q5_channels_by_complaint.csv
toc: true
---

# NYC 311 Service Dynamics

NYC's 311 service handles nearly 3 million requests annually, revealing how residents experience daily city life—noise disturbances, infrastructure hazards, and service outages. This analysis explores post-2010 patterns to surface operational insights and potential equity concerns across NYC's five boroughs.

```js
import * as d3 from "npm:d3";
```

```js

const q1Data = await FileAttachment("../data/exports/q1_monthly_trends.csv").csv({typed: true});
```

```js
const q2Data = await FileAttachment("../data/exports/q2_complaints_by_borough.csv").csv({typed: true});
```

```js
const q3Data = await FileAttachment("../data/exports/q3_hourly_patterns.csv").csv({typed: true});
```

```js
const q4Data = await FileAttachment("../data/exports/q4_response_by_location.csv").csv({typed: true});
```

```js
const q5Data = await FileAttachment("../data/exports/q5_channels_by_complaint.csv").csv({typed: true});
```

---

## Q1. How has the volume of 311 requests evolved since 2020 across boroughs?


```js
const q1Filtered = q1Data.filter(d => new Date(d.date) >= new Date("2014-01-01"));
```

```js
const boroughs = [...new Set(q1Filtered.map(d => d.borough))].filter(b => b !== "UNSPECIFIED");
```

```js
const selectedBorough = view(Inputs.select(["All", ...boroughs], {label: "Borough", value: "All"}));
```

```js
const width = 928;
const height = 500;
const marginTop = 40;
const marginRight = 150;
const marginBottom = 40;
const marginLeft = 60;

const q1ChartData = selectedBorough === "All"
  ? q1Filtered.filter(d => d.borough !== "UNSPECIFIED")
  : q1Filtered.filter(d => d.borough === selectedBorough);

// const parseDate = d3.timeParse("%Y-%m-%d");
// q1ChartData.forEach(d => d.parsedDate = parseDate(d.date));

const nested = d3.group(q1ChartData, d => d.borough);

const x = d3.scaleTime()
  // CHANGE d.parsedDate TO d.date HERE:
  .domain(d3.extent(q1ChartData, d => d.date)) 
  .range([marginLeft, width - marginRight]);

const y = d3.scaleLinear()
  .domain([0, d3.max(q1ChartData, d => d.count)])
  .nice()
  .range([height - marginBottom, marginTop]);

const color = d3.scaleOrdinal()
  .domain(boroughs)
  .range(d3.schemeTableau10);

const line = d3.line()
  // CHANGE d.parsedDate TO d.date HERE:
  .x(d => x(d.date)) 
  .y(d => y(d.count))
  .curve(d3.curveMonotoneX);

const svg = d3.create("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height])
  .attr("style", "max-width: 100%; height: auto;");

svg.append("g")
  .attr("transform", `translate(0,${height - marginBottom})`)
  .call(d3.axisBottom(x).ticks(width / 80))
  .call(g => g.select(".domain").remove());

svg.append("g")
  .attr("transform", `translate(${marginLeft},0)`)
  .call(d3.axisLeft(y).ticks(height / 40).tickFormat(d => `${d / 1000}k`))
  .call(g => g.select(".domain").remove())
  .call(g => g.selectAll(".tick line").clone()
    .attr("x2", width - marginLeft - marginRight)
    .attr("stroke-opacity", 0.1));

svg.append("text")
  .attr("x", marginLeft)
  .attr("y", marginTop - 10)
  .attr("font-weight", "bold")
  .text(`Monthly 311 Requests${selectedBorough !== "All" ? ` — ${selectedBorough}` : " — All Boroughs"}`);

nested.forEach((values, borough) => {
  svg.append("path")
    .datum(values)
    .attr("fill", "none")
    .attr("stroke", color(borough))
    .attr("stroke-width", 2)
    .attr("d", line);

  const last = values[values.length - 1];
  svg.append("text")
    .attr("x", width - marginRight + 10)
    .attr("y", y(last.count))
    .attr("dy", "0.35em")
    .attr("font-size", 11)
    .attr("fill", color(borough))
    .text(borough);
});

display(svg.node());
```


---

## Q2. What complaint types dominate each borough and how concentrated are they?


```js
const selectedBoroughQ2 = view(Inputs.select(boroughs, {label: "Borough", value: "Brooklyn"}));
```

```js
const q2Width = 928;
const q2Height = 600;
const q2MarginTop = 40;
const q2MarginRight = 40;
const q2MarginBottom = 40;
const q2MarginLeft = 280;

const q2BoroughData = q2Data.filter(d => d.borough === selectedBoroughQ2);
const q2BoroughTotal = d3.sum(q2BoroughData, d => d.count);

const q2ChartData = q2BoroughData
  .map(d => ({
    ...d,
    percentage: (d.count / q2BoroughTotal) * 100
  }))
  .sort((a, b) => b.count - a.count)
  .slice(0, 12);

const q2X = d3.scaleLinear()
  .domain([0, d3.max(q2ChartData, d => d.percentage)])
  .range([q2MarginLeft, q2Width - q2MarginRight]);

const q2Y = d3.scaleBand()
  .domain(q2ChartData.map(d => d.complaint_type))
  .range([q2MarginTop, q2Height - q2MarginBottom])
  .padding(0.2);

const q2Color = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, d3.max(q2ChartData, d => d.percentage)]);

const q2Svg = d3.create("svg")
  .attr("width", q2Width)
  .attr("height", q2Height)
  .attr("viewBox", [0, 0, q2Width, q2Height])
  .attr("style", "max-width: 100%; height: auto;");

q2Svg.append("g")
  .attr("transform", `translate(0,${q2Height - q2MarginBottom})`)
  .call(d3.axisBottom(q2X).ticks(q2Width / 80).tickFormat(d => `${d.toFixed(0)}%`))
  .call(g => g.select(".domain").remove());

q2Svg.append("g")
  .attr("transform", `translate(${q2MarginLeft},0)`)
  .call(d3.axisLeft(q2Y))
  .call(g => g.select(".domain").remove());

q2Svg.append("text")
  .attr("x", q2MarginLeft)
  .attr("y", q2MarginTop - 10)
  .attr("font-weight", "bold")
  .text(`Top Complaint Types — ${selectedBoroughQ2}`);

q2Svg.append("g")
  .selectAll("rect")
  .data(q2ChartData)
  .join("rect")
    .attr("x", q2MarginLeft)
    .attr("y", d => q2Y(d.complaint_type))
    .attr("width", d => q2X(d.percentage) - q2MarginLeft)
    .attr("height", q2Y.bandwidth())
    .attr("fill", d => q2Color(d.percentage));

q2Svg.append("g")
  .selectAll("text")
  .data(q2ChartData)
  .join("text")
    .attr("x", d => q2X(d.percentage) + 5)
    .attr("y", d => q2Y(d.complaint_type) + q2Y.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("font-size", 11)
    .attr("fill", "black")
    .text(d => `${d.count.toLocaleString()}`);

display(q2Svg.node());
```


---

## Q3. When during the week and day do high-impact complaints occur?


```js
const topComplaintTypes = [...new Set(q3Data.map(d => d.complaint_type))]
  .map(type => ({
    type,
    total: d3.sum(q3Data.filter(d => d.complaint_type === type), d => d.count)
  }))
  .sort((a, b) => b.total - a.total)
  .slice(0, 10)
  .map(d => d.type);
```

```js
const selectedComplaint = view(Inputs.select(topComplaintTypes, {
  label: "Complaint Type",
  value: topComplaintTypes[0]
}));
```

```js
const q3Width = 928;
const q3Height = 400;
const q3MarginTop = 60;
const q3MarginRight = 120;
const q3MarginBottom = 40;
const q3MarginLeft = 100;

const q3WeekdayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const q3Hours = d3.range(0, 24);

const q3FilteredData = q3Data.filter(d => d.complaint_type === selectedComplaint && d.count > 0);

const q3HeatmapData = q3WeekdayOrder.flatMap(day =>
  q3Hours.map(hour => {
    const match = q3FilteredData.find(d => d.day_of_week === day && d.hour === hour);
    return {
      day,
      hour,
      count: match ? match.count : 0
    };
  })
);

const q3X = d3.scaleBand()
  .domain(q3Hours)
  .range([q3MarginLeft, q3Width - q3MarginRight])
  .padding(0.05);

const q3Y = d3.scaleBand()
  .domain(q3WeekdayOrder)
  .range([q3MarginTop, q3Height - q3MarginBottom])
  .padding(0.05);

const q3Color = d3.scaleSequential(d3.interpolateYlOrRd)
  .domain([0, d3.max(q3HeatmapData, d => d.count)]);

const q3Svg = d3.create("svg")
  .attr("width", q3Width)
  .attr("height", q3Height)
  .attr("viewBox", [0, 0, q3Width, q3Height])
  .attr("style", "max-width: 100%; height: auto;");

q3Svg.append("text")
  .attr("x", q3MarginLeft)
  .attr("y", 20)
  .attr("font-weight", "bold")
  .attr("font-size", 14)
  .text(`${selectedComplaint} — Weekday vs Hour`);

q3Svg.append("g")
  .attr("transform", `translate(0,${q3Height - q3MarginBottom})`)
  .call(d3.axisBottom(q3X).tickFormat(d => `${d}:00`))
  .selectAll("text")
    .attr("transform", "rotate(-45)")
    .style("text-anchor", "end");

q3Svg.append("g")
  .attr("transform", `translate(${q3MarginLeft},0)`)
  .call(d3.axisLeft(q3Y));

q3Svg.append("g")
  .selectAll("rect")
  .data(q3HeatmapData)
  .join("rect")
    .attr("x", d => q3X(d.hour))
    .attr("y", d => q3Y(d.day))
    .attr("width", q3X.bandwidth())
    .attr("height", q3Y.bandwidth())
    .attr("fill", d => d.count > 0 ? q3Color(d.count) : "#f0f0f0")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1)
  .append("title")
    .text(d => `${d.day}, ${d.hour}:00\n${d.count.toLocaleString()} requests`);

// Legend
const q3LegendWidth = 200;
const q3LegendHeight = 10;
const q3LegendX = q3Width - q3MarginRight + 20;
const q3LegendY = q3MarginTop;

const q3LegendScale = d3.scaleLinear()
  .domain([0, d3.max(q3HeatmapData, d => d.count)])
  .range([0, q3LegendWidth]);

const q3LegendAxis = d3.axisBottom(q3LegendScale)
  .ticks(5)
  .tickFormat(d => d.toLocaleString());

const q3Defs = q3Svg.append("defs");
const q3Gradient = q3Defs.append("linearGradient")
  .attr("id", "q3-legend-gradient")
  .attr("x1", "0%")
  .attr("x2", "100%");

q3Gradient.selectAll("stop")
  .data(d3.range(0, 1.01, 0.1))
  .join("stop")
    .attr("offset", d => `${d * 100}%`)
    .attr("stop-color", d => q3Color(d * d3.max(q3HeatmapData, d => d.count)));

q3Svg.append("rect")
  .attr("x", q3LegendX)
  .attr("y", q3LegendY)
  .attr("width", q3LegendWidth)
  .attr("height", q3LegendHeight)
  .style("fill", "url(#q3-legend-gradient)");

q3Svg.append("g")
  .attr("transform", `translate(${q3LegendX},${q3LegendY + q3LegendHeight})`)
  .call(q3LegendAxis);

display(q3Svg.node());
```

---

## Q4. Where do residents wait the longest for resolution?


```js
const responseMetric = view(Inputs.radio(["median_response_hours", "count"], {
  label: "Show",
  value: "median_response_hours",
  format: x => x === "median_response_hours" ? "Response Time" : "Request Density"
}));
```

```js
const nycGeoJson = await d3.json("https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson");

const q4Width = 928;
const q4Height = 600;

// 2. Filter q4Data (renamed from q4ChartData)
// We use a local variable 'plotData' for the filtered set to keep q4Data intact
const plotData = q4Data.filter(d =>
  d.count >= 100 &&
  d.lat > 40.4 && d.lat < 41.0 &&
  d.lng > -74.3 && d.lng < -73.7 &&
  d.borough !== "UNSPECIFIED"
);

// 3. Setup Projection
const projection = d3.geoConicConformal()
  .parallels([40 + 40 / 60, 41 + 2 / 60])
  .rotate([74, 0])
  .fitSize([q4Width, q4Height], nycGeoJson);

const path = d3.geoPath().projection(projection);

// 4. Scales
const q4ColorScale = responseMetric === "median_response_hours"
  ? d3.scaleSequential(d3.interpolateViridis)
      .domain([0, d3.quantile(plotData.map(d => d.median_response_hours).sort(d3.ascending), 0.9)])
  : d3.scaleSequential(d3.interpolatePlasma)
      .domain([0, d3.quantile(plotData.map(d => d.count).sort(d3.ascending), 0.95)]);

const q4SizeScale = d3.scaleSqrt()
  .domain([0, d3.max(plotData, d => d.count)])
  .range([2, 12]);

// 5. Create SVG
const q4Svg = d3.create("svg")
  .attr("width", q4Width)
  .attr("height", q4Height)
  .attr("viewBox", [0, 0, q4Width, q4Height])
  .attr("style", "max-width: 100%; height: auto;");

// --- LEGEND IMPLEMENTATION ---
const legendWidth = 200;
const legendHeight = 12;
const legendPosition = { x: q4Width - legendWidth - 30, y: 30 };

// Create a unique ID for the gradient
const gradientId = "legend-gradient";

// Append defs and gradient
const defs = q4Svg.append("defs");
const gradient = defs.append("linearGradient")
  .attr("id", gradientId)
  .attr("x1", "0%")
  .attr("x2", "100%");

// Generate stops for the gradient based on the current color scale
const stopCount = 10;
for (let i = 0; i <= stopCount; i++) {
  const t = i / stopCount;
  gradient.append("stop")
    .attr("offset", `${t * 100}%`)
    .attr("stop-color", q4ColorScale.interpolator()(t));
}

// Legend Group
const legendG = q4Svg.append("g")
  .attr("transform", `translate(${legendPosition.x}, ${legendPosition.y})`);

// Legend Title
legendG.append("text")
  .attr("x", 0)
  .attr("y", -8)
  .attr("font-size", "12px")
  .attr("font-weight", "bold")
  .text(responseMetric === "median_response_hours" ? "Avg Response (Hours)" : "Request Count");

// Legend Color Bar
legendG.append("rect")
  .attr("width", legendWidth)
  .attr("height", legendHeight)
  .attr("fill", `url(#${gradientId})`)
  .attr("stroke", "#ccc")
  .attr("stroke-width", 0.5);

// Legend Axis
const legendScale = d3.scaleLinear()
  .domain(q4ColorScale.domain())
  .range([0, legendWidth]);

const legendAxis = d3.axisBottom(legendScale)
  .ticks(5)
  .tickSize(5)
  .tickFormat(d => d3.format(".0f")(d));

legendG.append("g")
  .attr("transform", `translate(0, ${legendHeight})`)
  .call(legendAxis)
  .select(".domain").remove(); // Hide the main axis line for a cleaner look
// -----------------------------

// Title
q4Svg.append("text")
  .attr("x", 40)
  .attr("y", 30)
  .attr("font-weight", "bold")
  .attr("font-size", 16)
  .text(`NYC 311 Response by Location`);

// Draw Background Map
q4Svg.append("g")
  .selectAll("path")
  .data(nycGeoJson.features)
  .join("path")
    .attr("d", path)
    .attr("fill", "#e6e6e6")
    .attr("stroke", "#ffffff")
    .attr("stroke-width", 1);

// Draw Data Points
q4Svg.append("g")
  .selectAll("circle")
  .data(plotData)
  .join("circle")
    .attr("cx", d => projection([d.lng, d.lat])[0])
    .attr("cy", d => projection([d.lng, d.lat])[1])
    .attr("r", responseMetric === "median_response_hours" ? 4 : d => q4SizeScale(d.count))
    .attr("fill", d => q4ColorScale(d[responseMetric]))
    .attr("opacity", 0.7)
    .attr("stroke", "#333")
    .attr("stroke-width", 0.5)
  .append("title")
    .text(d => `${d.borough} (${d.zip})\nMedian Response: ${d.median_response_hours.toFixed(1)} hrs\nRequests: ${d.count.toLocaleString()}`);

display(q4Svg.node());
```



---

## Q5. Which reporting channels are most used per complaint type?


```js
const topComplaintTypesQ5 = [...new Set(q5Data.map(d => d.complaint_type))]
  .map(type => ({
    type,
    total: d3.sum(q5Data.filter(d => d.complaint_type === type), d => d.count)
  }))
  .sort((a, b) => b.total - a.total)
  .slice(0, 15)
  .map(d => d.type);
```

```js
const q5Width = 928;
const q5Height = 600;
const q5MarginTop = 40;
const q5MarginRight = 150;
const q5MarginBottom = 40;
const q5MarginLeft = 280;

const q5ChartData = q5Data.filter(d => topComplaintTypesQ5.includes(d.complaint_type));

const q5ComplaintTotals = d3.rollup(q5ChartData, v => d3.sum(v, d => d.count), d => d.complaint_type);

const q5Nested = Array.from(d3.group(q5ChartData, d => d.complaint_type), ([type, values]) => {
  const total = q5ComplaintTotals.get(type);
  const channels = ["Mobile", "Web", "Phone", "Other"];
  const channelData = channels.map(channel => {
    const match = values.find(v => v.channel_group === channel);
    return {
      channel,
      count: match ? match.count : 0,
      percentage: match ? (match.count / total) * 100 : 0
    };
  });
  return { type, total, channels: channelData };
})
.sort((a, b) => b.total - a.total);

const q5Y = d3.scaleBand()
  .domain(q5Nested.map(d => d.type))
  .range([q5MarginTop, q5Height - q5MarginBottom])
  .padding(0.2);

const q5X = d3.scaleLinear()
  .domain([0, 100])
  .range([q5MarginLeft, q5Width - q5MarginRight]);

const q5Color = d3.scaleOrdinal()
  .domain(["Mobile", "Web", "Phone", "Other"])
  .range(["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]);

const q5Svg = d3.create("svg")
  .attr("width", q5Width)
  .attr("height", q5Height)
  .attr("viewBox", [0, 0, q5Width, q5Height])
  .attr("style", "max-width: 100%; height: auto;");

q5Svg.append("text")
  .attr("x", q5MarginLeft)
  .attr("y", 20)
  .attr("font-weight", "bold")
  .attr("font-size", 14)
  .text("Reporting Channel Mix by Complaint Type");

q5Svg.append("g")
  .attr("transform", `translate(0,${q5Height - q5MarginBottom})`)
  .call(d3.axisBottom(q5X).tickFormat(d => `${d}%`))
  .call(g => g.select(".domain").remove());

q5Svg.append("g")
  .attr("transform", `translate(${q5MarginLeft},0)`)
  .call(d3.axisLeft(q5Y))
  .call(g => g.select(".domain").remove());

const q5Groups = q5Svg.append("g")
  .selectAll("g")
  .data(q5Nested)
  .join("g");

q5Groups.each(function(d) {
  let cumulative = 0;
  d3.select(this)
    .selectAll("rect")
    .data(d.channels)
    .join("rect")
      .attr("x", ch => {
        const xPos = q5X(cumulative);
        cumulative += ch.percentage;
        return xPos;
      })
      .attr("y", q5Y(d.type))
      .attr("width", ch => q5X(ch.percentage) - q5MarginLeft)
      .attr("height", q5Y.bandwidth())
      .attr("fill", ch => q5Color(ch.channel));
});

// Legend
const q5Legend = q5Svg.append("g")
  .attr("transform", `translate(${q5Width - q5MarginRight + 20}, ${q5MarginTop})`);

["Mobile", "Web", "Phone", "Other"].forEach((channel, i) => {
  const legendRow = q5Legend.append("g")
    .attr("transform", `translate(0, ${i * 20})`);

  legendRow.append("rect")
    .attr("width", 15)
    .attr("height", 15)
    .attr("fill", q5Color(channel));

  legendRow.append("text")
    .attr("x", 20)
    .attr("y", 12)
    .attr("font-size", 12)
    .text(channel);
});

display(q5Svg.node());
```


---


