# 🚀 Quick Start: Analytics Dashboard

## What's Configured

**Multi-Property Aggregation for triesteallnews.it**

Your dashboard combines data from **3 GA4 properties**:

| Property | GA4 ID | Purpose |
|----------|--------|---------|
| triesteallnews.it | `476208509` | Main site (non-www) |
| www.triesteallnews.it | `316181048` | Main site (www) |
| FVG.news | `257131451` | Regional network |

**Why?** These properties track the same website network, so we aggregate them for complete analytics.

---

## 🎯 Launch Dashboard

```bash
python gui_app.py
```

Or double-click: `run_gui.bat`

Then click the **"📈 Analytics Dashboard"** tab.

---

## 📊 What You'll See

### Info Banner (Top):
```
ℹ️ Multi-Property Aggregation: Combining data from 3 GA4 properties
   triesteallnews.it (GA4: 476208509) | 
   www.triesteallnews.it (GA4: 316181048) | 
   FVG.news (GA4: 257131451)
```

### Metrics (Combined):
- **All Visitors** - Total unique users across all properties
- **Page Views** - Total views across all properties  
- **Avg. Session** - Weighted average session duration
- **Bounce Rate** - Weighted average bounce rate

### Charts:
- **Traffic Sources** - Pie chart of combined traffic channels
- **Daily Visitors** - Line graph of last 7 days

### Top Pages Table:
Shows pages from all properties with property labels:
- `[triesteallnews.it] Article title...`
- `[FVG.news] Article title...`
- etc.

---

## 🔄 Refresh Data

Click the **"🔄 Refresh Analytics Data"** button to update with latest data.

Status shows: `"Last updated: HH:MM:SS - Aggregated from 3 properties"`

---

## 📁 Files Reference

- `google_analytics_config.json` - Multi-property configuration
- `MULTI_PROPERTY_INFO.md` - Detailed aggregation info
- `ANALYTICS_SETUP_COMPLETE.md` - Full setup documentation

---

**That's it! Your dashboard is ready to use.** 🎉

