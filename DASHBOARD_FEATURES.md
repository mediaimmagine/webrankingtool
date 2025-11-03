# 📊 Analytics Dashboard Features

## Overview

The Analytics Dashboard provides **multi-level analytics** with separate tracking for each site in the network.

---

## 🎨 Dashboard Layout

### Top Section - Network Overview (28 Days)
**All Sites Combined:**
- Total Visitors across all properties
- Total Page Views
- Average Session Duration
- Bounce Rate

### Middle Section - Site-Specific Analytics

#### 📍 TRIESTE.NEWS / TRIESTEALLNEWS.IT
- **28-Day Visitor Count Box** (blue background)
- **Traffic Sources Pie Chart** (last 7 days)
- **Multi-Period Overlay Chart** (7/28/90 days)

#### 📍 PORDENONEOGGI.IT
- **28-Day Visitor Count Box** (red/pink background)
- **Traffic Sources Pie Chart** (last 7 days)
- **Multi-Period Overlay Chart** (7/28/90 days)

### Bottom Section
- **Top Pages Table** (last 28 days, all sites)
- Shows which property each page belongs to

---

## 📈 Multi-Period Overlay Charts

### How It Works

All daily visitor charts show **three time periods simultaneously** on the **same x-axis scale (0-90 days)**:

```
Visitors
    │
    │    ╱╲        ●─●─●  ← ORANGE (7 days) - Recent trend
    │   ╱  ╲      ╱      
    │  ╱    ─────╱────   ← BLUE (28 days) - Monthly pattern
    │ ╱    ╱             
    │──────              ← GREEN (90 days) - Long-term trend
    │
    └─────────────────────────
     90   60   30   7   0  (Days Ago)
```

### Color Coding

| Period | Color | Line Style | Markers | Purpose |
|--------|-------|------------|---------|---------|
| **7 days** | 🟠 Orange (#ff9800) | Thick (2.5px) | Yes (●) | Recent activity detail |
| **28 days** | 🔵 Blue (#4285f4) | Medium (2px) | No | Monthly patterns |
| **90 days** | 🟢 Green (#34a853) | Thin (1.5px) | No | Long-term trends |

### Key Features

✅ **Same time scale** - All lines use 0-90 days x-axis  
✅ **Overlaid** - Lines superimposed for easy comparison  
✅ **Different lengths** - Each line only extends to its data range  
✅ **Visual hierarchy** - Orange (recent) on top, green (historical) in back  
✅ **Legend** - Shows which line is which period  

---

## 🎯 Traffic Source Labels

### Improved Labeling

| Original GA Name | Dashboard Label | Explanation |
|------------------|-----------------|-------------|
| Organic Search | **Organic Search** | Google, Bing, etc. search results |
| Organic Social | **Social Media** | Facebook, Twitter, Instagram, etc. |
| Direct | **Direct Traffic** | Direct URL entry, bookmarks |
| Referral | **Referrals** | Links from other websites |
| Cross-network | **Google Network** | Google properties & partner sites |
| Paid Search | **Paid Ads** | Google Ads, paid campaigns |
| Unassigned | **Other** | Uncategorized traffic |

### Google Network Explanation

**"Google Network"** includes:
- Google Discover
- Google News
- Gmail clicks
- Google partner sites
- Cross-property navigation

A tooltip in the chart title explains this.

---

## 🏢 Property Aggregation

### Active Properties

All data aggregates from **2 GA4 properties**:

1. **triesteallnews.it** (Property ID: 476208509)
2. **FVG.news** (Property ID: 257131451)

### Site Filtering

**Trieste Section:**
- Filters pages containing "trieste" in URL or hostname
- Excludes Pordenone pages
- Shows combined data from both properties

**Pordenone Section:**
- Filters pages containing "pordenone" in URL
- Only from FVG.news property
- Isolated from Trieste traffic

---

## 📊 Metrics Explained

### 28-Day Visitor Boxes

**Trieste Box (Blue):**
- Shows total unique visitors to Trieste pages
- Last 28 days period
- Filtered from both properties

**Pordenone Box (Red/Pink):**
- Shows total unique visitors to Pordenone pages
- Last 28 days period
- Filtered from FVG.news property

### Charts Time Periods

| Chart Type | Time Period | Reason |
|------------|-------------|--------|
| **Traffic Sources** | 7 days | Recent source distribution |
| **Daily Overlay** | 7/28/90 days | Multi-period trend comparison |
| **Top Pages** | 28 days | Monthly performance ranking |
| **Metrics Cards** | 28 days | Matches Site Kit default |

---

## 🎨 Visual Design

### Color Themes

**Trieste:**
- Primary: Blue (#4285f4)
- Box background: Light blue (#e3f2fd)
- Chart accent: Blue shades

**Pordenone:**
- Primary: Red (#ea4335)
- Box background: Light red (#ffebee)
- Chart accent: Red shades

### Font Sizes
- Section titles: 12pt bold
- Chart titles: 9-10pt
- Chart labels: 7-8pt
- Metric boxes: 11pt bold
- Legend: 7pt

### Layout
- **Scrollable** - Vertical scrollbar for all content
- **Responsive** - Charts resize with window
- **Organized** - Network → Trieste → Pordenone → Top Pages

---

## 🔄 Refresh & Export

### Refresh Button
- Updates all data from Google Analytics API
- Shows timestamp and property count
- Automatically fetches latest data

### Export Button
- Exports dashboard data to CSV
- Includes all metrics and top pages
- Timestamped filename

---

## 📊 Data Interpretation Tips

### Overlay Charts

**Look for:**
- 🟠 **Orange spike** - Recent traffic increase (last 7 days)
- 🔵 **Blue divergence** - Monthly pattern change
- 🟢 **Green trend** - Overall growth/decline (90 days)

**Patterns:**
- All lines rising = Growing traffic
- Orange above blue = Recent improvement
- Green flat, orange spiky = Stable with recent volatility

### Traffic Sources

- **High Organic Search** = Good SEO
- **High Direct** = Strong brand recognition
- **High Social** = Viral content or good social strategy
- **High Google Network** = Featured in Google News/Discover

---

*Last Updated: November 3, 2025*
*Configuration: Multi-property aggregation enabled*

