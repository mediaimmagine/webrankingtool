# 📊 Multi-Property Analytics Configuration

## Overview

The Analytics Dashboard **aggregates data from 3 separate GA4 properties** that track the same website network (triesteallnews.it and related sites).

---

## 🏢 Configured Properties

### Property 1: triesteallnews.it (non-www)
- **GA4 Property ID:** `476208509`
- **URL:** https://triesteallnews.it
- **Purpose:** Tracks non-www version of main site
- **Measurement ID:** G-KCD0PGWV1N

### Property 2: www.triesteallnews.it (www)
- **GA4 Property ID:** `316181048`
- **URL:** https://www.triesteallnews.it
- **Purpose:** Tracks www version of main site
- **Note:** Same content as Property 1, different subdomain

### Property 3: FVG.news
- **GA4 Property ID:** `257131451`
- **URL:** Regional news network
- **Purpose:** Tracks Friuli-Venezia Giulia news network
- **Note:** Part of triesteallnews.it media network

---

## ❓ Why Multi-Property Aggregation?

### The Problem:
The same website content is tracked by **multiple GA4 properties** due to:
1. **URL variations** (www vs non-www)
2. **Related sites** in the same network (FVG.news)
3. **Historical setup** with separate tracking codes

### The Solution:
**Aggregate all properties** to get complete, unified analytics showing total traffic across all variations.

### Benefits:
- ✅ **Complete data** - No traffic is missed
- ✅ **Single view** - One dashboard for all properties
- ✅ **Accurate totals** - Combined metrics reflect true site performance
- ✅ **Property breakdown** - Still see which property/site contributed what

---

## 🔧 Technical Details

### Configuration File:
`google_analytics_config.json`

```json
{
  "use_aggregation": true,
  "aggregate_properties": [
    "476208509",
    "316181048",
    "257131451"
  ],
  "property_labels": {
    "476208509": "triesteallnews.it",
    "316181048": "www.triesteallnews.it",
    "257131451": "FVG.news"
  }
}
```

### How It Works:
1. **Parallel data fetching** from all 3 properties
2. **Metric aggregation** (views, users, sessions summed)
3. **Weighted averages** (session duration, bounce rate)
4. **Combined traffic sources** (all channels merged)
5. **Unified top pages** (pages from all properties sorted by views)

---

## 📈 Example Dashboard View

```
╔════════════════════════════════════════════════════════════╗
║  ℹ️ Multi-Property Aggregation: 3 GA4 Properties         ║
║  triesteallnews.it (476208509) |                          ║
║  www.triesteallnews.it (316181048) |                      ║
║  FVG.news (257131451)                                      ║
╚════════════════════════════════════════════════════════════╝

┌─────────────────┬─────────────────┬─────────────────┐
│  All Visitors   │   Page Views    │  Avg. Session   │
│     54,617      │     164,178     │    4.3 min      │
│                 │                 │                 │
│   (Combined)    │   (Combined)    │   (Weighted)    │
└─────────────────┴─────────────────┴─────────────────┘

Top Pages (Last 7 Days):
 1. [FVG.news] Notizie TRIESTE.news - 7,878 views
 2. [triesteallnews.it] Notizie TRIESTE.news - 7,054 views
 3. [FVG.news] Treno Trieste-Vienna - 5,140 views
    ...
```

---

## 🛠️ Managing Properties

### To Add a New Property:
1. Add service account to the property in Google Analytics
2. Edit `google_analytics_config.json`:
   ```json
   "aggregate_properties": [..., "NEW_PROPERTY_ID"],
   "property_labels": {
     "NEW_PROPERTY_ID": "Site Name"
   }
   ```
3. Restart the dashboard

### To Remove a Property:
1. Remove from `aggregate_properties` array in config
2. Remove from `property_labels` object
3. Restart the dashboard

### To Disable Aggregation:
Set `"use_aggregation": false` in config file

---

## 📊 Data Accuracy

### Deduplication:
- **Not performed** - Each property tracks independently
- **User overlap** - Same user visiting both www and non-www counts twice
- **Rationale:** Shows true property-level traffic, important for understanding distribution

### Metrics:
- **Additive:** Page Views, Users, Sessions
- **Averaged:** Session Duration, Bounce Rate (weighted by sessions)
- **Combined:** Traffic Sources (merged by channel name)

### Trade-offs:
- ✅ **Pro:** Complete picture of all traffic
- ⚠️ **Note:** User counts may include duplicates if same person visits multiple properties

---

## 📞 Support

### Test Configuration:
```bash
python test_all_properties.py
```

### Test Aggregation:
```bash
python multi_property_analytics.py
```

### View in GUI:
```bash
python gui_app.py
# Click "Analytics Dashboard" tab
```

---

*Configuration File: `google_analytics_config.json`*
*Module: `multi_property_analytics.py`*
*Last Updated: November 3, 2025*

