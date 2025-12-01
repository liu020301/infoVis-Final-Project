---
toc: false
---

<div class="hero">
  <h1>FinalProject</h1>
</div>

<br>

# NYC 311 Service Dynamics
---

## Introduction

New York City’s 311 system processes millions of requests every year, serving as a real-time barometer of urban conditions—ranging from noise and heat complaints to street maintenance and public service failures. Understanding these patterns is valuable not only for operational planning but also for uncovering disparities in how different communities experience city services.
In this analysis, we look at several common patterns:
- how the number of requests changed after 2020

- which complaints are most common in each borough

- when major problems happen during the week

- where people wait longer for a response

- and which channels (web, phone, mobile) residents use most often

The goal is to understand both behavior patterns and possible service gaps across NYC.

## Data Description
The dataset we used is “311 Service Requests from 2010 to Present” from NYC Open Data. It is one of the city’s largest public datasets and is updated every day. It contains every 311 service request reported by New Yorkers since 2010, including issues like noise, heating complaints, illegal parking, broken street lights, and many others. 
For this project, we focused mainly on:
- the complaint type

- created date

- borough

- location coordinates

- response time

- reporting channel

## Questions and Findings
### Q1. How has the volume of 311 requests changed since 2020?
From 2020 onward, the volume of 311 requests has stayed consistently high across all boroughs, but each borough shows its own pattern. Brooklyn has the largest number of monthly requests throughout the period and shows a steady increase after the initial drop at the start of the pandemic. Queens and the Bronx follow a similar trend, with noticeable spikes around late 2020 and early 2021 before stabilizing at slightly higher levels than before. Manhattan’s request volume is more moderate and fluctuates less sharply, while Staten Island remains consistently much lower than the other boroughs. Overall, every borough experienced a major disruption around early 2020, but by 2021 the request volume returned to normal seasonal patterns, with Brooklyn and Queens driving most of the citywide activity.

### Q2. What complaint types dominate each borough and how concentrated are they?
Each borough has a unique mix of high-volume complaint types, but there are also several patterns that repeat across the city. “Illegal Parking” and “Noise – Residential” are consistently among the top issues in most boroughs, especially Brooklyn, Queens, and Staten Island. The Bronx stands out with a very high volume of heat and hot water complaints, making it the second-largest category there. Manhattan shows a different mix, where noise-related complaints — both residential and street/sidewalk — appear more frequently than parking issues. Some complaint types, like blocked driveways, bulky item collection, and street condition, appear in the top ten lists of most boroughs but at different ranks depending on local priorities. Overall, while each borough has its own top concerns, the data suggests that noise and parking remain citywide issues, while heating problems and street infrastructure vary more by neighborhood.

### Q3. When during the week and day do high-impact complaints occur?
The timing of complaints differs a lot depending on the type of issue. Noise-related complaints, especially residential and street/sidewalk noise, peak late at night and early in the morning, particularly on weekends. Saturday and Sunday show the highest activity around midnight to 2 a.m., which matches typical nightlife patterns. Illegal parking follows a very different rhythm, with strong peaks during weekday mornings around 7–10 a.m. and again in the evening around 8–10 p.m., likely reflecting commuting and work-hour parking pressures. Heating and hot water complaints tend to spike early in the morning, especially on weekdays, when people first notice temperature issues at home. Infrastructure-related complaints like street condition, water system, and bulky item collection follow a much more “business-hours” pattern, with peaks between 9 a.m. and 3 p.m. Overall, the heatmaps show that different problems emerge at different times of day, and many of the most disruptive issues — like noise — are concentrated during late-night hours, especially on weekends.

### Q4. Where do residents wait the longest for resolution?
The spatial patterns of response time vary across the city. Longer average response times appear in several outer-borough areas, particularly parts of the Bronx, eastern Queens, and pockets of southern Brooklyn. Meanwhile, areas with very high request density — such as Midtown Manhattan, central Brooklyn, and western Queens — do not necessarily have long response times, suggesting that higher volume does not always lead to slower service. On the other hand, neighborhoods with fewer requests sometimes show longer response times, which may indicate slower resource allocation or logistical challenges. Overall, the map suggests that response time is influenced more by geography and agency logistics than by raw request volume, with some low-density regions waiting notably longer for service.

### Q5. Which reporting channels are most used per complaint type?
Different complaint types rely on different reporting channels, and some patterns stand out clearly. Phone reporting remains the dominant method for many issues, especially those related to plumbing, unsanitary conditions, water system problems, and heating complaints. These categories are more urgent or complex, so residents may prefer speaking to someone directly. Web and mobile submissions are more common for noise-related issues, illegal parking, and blocked driveways — all problems that residents may report quickly from their phone. A few categories, such as street light condition and heating, show unusually high proportions of “Other” channels, which may include automated systems or referrals from other agencies. Overall, the mix of reporting channels reflects how different types of problems are experienced: urgent household issues push people to call, while everyday neighborhood nuisances are more often reported online.

## Conclusion
Overall, the 311 data shows that request patterns differ across boroughs but follow a few clear themes. Since 2020, activity has remained high, with Brooklyn, Queens, and the Bronx driving most of the volume. Noise and parking complaints consistently dominate, while heating, water, and street-related issues vary more by area. Timing patterns also differ by complaint type: noise peaks late at night, parking issues rise during commute hours, and most infrastructure complaints happen during the day. Spatially, some outer-borough neighborhoods experience noticeably longer response times, even though they don’t always have the highest request counts. Reporting channels reflect the nature of the issue — urgent household problems are usually reported by phone, while noise and parking are more often submitted online.<br><br>
These findings suggest a few possible improvements. Late-night noise issues and early-morning heating problems may benefit from better targeted staffing or automated triage. Areas with long response times, especially in parts of the Bronx and Queens, could gain from additional field resources or more efficient routing. Strengthening mobile and web tools may also help reduce phone-dependent bottlenecks.<br><br>
It’s also important to note the dataset’s limitations. 311 requests reflect what residents choose to report, not all actual incidents, and reporting behavior varies by neighborhood and demographic factors. Some categories are broad or inconsistently used, and response-time data can be influenced by agency processes not captured in the dataset. Despite these limits, the data still offers a useful view of service needs across the city and highlights where attention and resources could make the biggest difference.<br><br>