---
toc: false
---

<div class="hero">
  <h1>FinalProject</h1>
</div>

<br>

# NYC 311 Service Dynamics
---

Group Members:
- Zehao Liu		zl6194
- Junyuan Wang	jw9178
- Jiangnan Li		jl18011

## Problem Space
---

NYC’s 311 system receives millions of service requests every year. These requests say a lot about what residents experience in daily life—noise, broken infrastructure, heating issues, parking conflicts, and more. Understanding these patterns is valuable not only for operational planning but also for uncovering disparities in how different communities experience city services.
In this analysis, we look at several common patterns:
- How has the volume of 311 requests evolved since 2010 across boroughs

- Which complaints are most common in each borough

- When major problems happen during the week

- Where people wait longer for a response

- Which channels (web, phone, mobile) residents use most often

The goal is to understand both behavior patterns and possible service gaps across NYC.

## Data Description
---
The dataset we used is “311 Service Requests from 2010 to Present” from NYC Open Data. It is one of the city’s largest public datasets and is updated every day. It contains every 311 service request reported by New Yorkers since 2010, including issues like noise, heating complaints, illegal parking, broken street lights, and many others. 
For this project, we focused mainly on:
- the complaint type

- created date

- borough

- location coordinates

- response time

- reporting channel

## Questions and Findings
---
### Q1. How has the volume of 311 requests evolved since 2010 across boroughs?
From 2010 to 2024, the volume of 311 requests shows a clear upward trend across the city, although each borough grows at a different pace. Brooklyn sees the strongest and most consistent increase, reaching some of the highest monthly counts in the dataset. Queens and the Bronx also rise steadily over time, with the Bronx having more up and down changes from month to month. Manhattan grows more slowly, and Staten Island stays much lower throughout the entire period. Around 2020, there is a noticeable drop followed by a quick rebound, which likely reflects the early months of the pandemic when city activity temporarily slowed and reporting behavior shifted. After that period, request levels return quickly and remain high, continuing the overall growth pattern that has been developing since the early 2010s.

### Q2. What complaint types dominate each borough and how concentrated are they?
Each borough has a unique mix of high-volume complaint types, but there are also several patterns that repeat across the city. “Illegal Parking” and “Noise – Residential” are consistently among the top issues in most boroughs, especially Brooklyn, Queens, and Staten Island. The Bronx stands out with a very high volume of heat and hot water complaints, making it the second-largest category there. Manhattan shows a different mix, where noise related complaints (both residential and street/sidewalk) appear more frequently than parking issues. Some complaint types, like blocked driveways, bulky item collection, and street condition, appear in the top ten lists of most boroughs but at different ranks depending on local priorities. Overall, while each borough has its own top concerns, the data suggests that noise and parking remain citywide issues, while heating problems and street infrastructure vary more by neighborhood.

### Q3. When during the week and day do high-impact complaints occur?
The timing of complaints differs a lot depending on the type of issue. Noise related complaints, especially residential and street/sidewalk noise, peak late at night and early in the morning, particularly on weekends. Saturday and Sunday show the highest activity around midnight to 2 a.m., which matches typical nightlife patterns. Illegal parking follows a very different rhythm, with strong peaks during weekday mornings around 7–10 a.m. and again in the evening around 8–10 p.m., which reflecting commuting and work hour parking pressures. Heating and hot water complaints tend to spike early in the morning, especially on weekdays, when people first notice temperature issues at home (often while showering or getting ready for the day). Infrastructure-related complaints like street condition, water system, and bulky item collection follow a much more “business-hours” pattern, with peaks between 9 a.m. and 3 p.m. Overall, the heatmaps show that different problems emerge at different times of day, and many of the most disruptive issues are concentrated during late night hours, especially on weekends.

### Q4. Where do residents wait the longest for resolution?
Across these recent years from 2019 to 2024, the maps show a similar divide: central areas such as Lower Manhattan, Midtown, Downtown Brooklyn, and parts of western Queens usually receive faster responses, while neighborhoods farther from the core (especially Staten Island, eastern Queens, the Rockaways, and parts of the Bronx) tend to wait noticeably longer. 
The All-Years view (2010–2024) shows a very similar picture. Manhattan isn’t uniformly fast, but areas around downtown and the west side consistently receive quicker responses than most outer-borough neighborhoods. In contrast, Staten Island, eastern Queens, and several slower-responding areas in the Bronx continue to stand out even after averaging fifteen years of data. The Bronx is especially noticeable because it has both a high request density and relatively long response times, suggesting that heavier demand may be putting more pressure on available resources there. Overall, both the year-by-year maps and the long-term view point to a stable pattern: response times are shaped not only by geography and service coverage but also by how much volume each area has to absorb.


### Q5. Which reporting channels are most used per complaint type?
Looking at the year-by-year view, the mix of reporting channels changes quite noticeably over time. In the early years of the dataset, most complaint types were dominated by the “Other” category, but not all of them—certain issues such as blocked driveways, residential noise, and damaged trees were reported mainly by phone in 2010. As the timeline moves forward, phone use becomes more common across a wider range of complaint types and gradually turns into the primary channel for many household or urgent problems.
The All-Years view reflects these long-term tendencies. Phone is still the dominant channel overall, especially for maintenance and infrastructure complaints, but web and mobile now make up a meaningful portion of reports for several high-volume categories. Meanwhile, the “Other” category stays fairly large for some types of issues, especially things like street-light problems, sewer complaints, and construction-related reports, which are often handled through channels that aren’t recorded as phone, web, or mobile. Taken together, the data suggests that while phone has stayed a central part of 311 reporting, residents have increasingly adopted web and mobile options as these channels became more accessible and convenient over time.


## Conclusion
---
Overall, the 311 data shows that request patterns differ across boroughs but follow a few clear themes. Across the full period from 2010 to 2024, activity has remained high, with Brooklyn, Queens, and the Bronx driving most of the volume. Noise and parking complaints consistently dominate, while heating, water, and street-related issues vary more by area. Timing patterns also differ by complaint type: noise peaks late at night, parking issues rise during commute hours, and most infrastructure complaints happen during the day. Spatially, some outer-borough neighborhoods experience noticeably longer response times, even though they don’t always have the highest request counts. Reporting channels reflect the nature of the issue — urgent household problems are usually reported by phone, while noise and illegal parking are more often submitted by mobile or web.<br><br>
These findings suggest a few possible improvements. Late-night noise issues and early-morning heating problems may benefit from better targeted staffing or automated screening. Areas with long response times, especially in parts of the Bronx and Queens, could gain from additional field resources or more efficient routing. Strengthening mobile and web tools may also help reduce phone-dependent bottlenecks.<br><br>
It’s also important to note the dataset’s limitations. 311 requests reflect what residents choose to report, not all actual incidents, and reporting behavior varies by neighborhood and demographic factors. Some categories are broad or inconsistently used, and response-time data can be influenced by agency processes not captured in the dataset. Despite these limits, the data still offers a useful view of service needs across the city and highlights where attention and resources could make the biggest difference.<br><br>
