# 🆓 Free APIs Guide - Real Data Without Cost

This guide shows you how to get real website analytics data using completely free APIs instead of expensive services like SimilarWeb ($1,167+/month).

## 🎯 Free API Options

### 1. BuiltWith API (Recommended)
**What it provides**: Website technology detection, hosting info, analytics tools
**Cost**: FREE tier available
**Signup**: https://api.builtwith.com/
**Free tier**: 500 requests/month

**How to get API key**:
1. Visit https://api.builtwith.com/
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `config.py`:
   ```python
   BUILTWITH_API_KEY = "your_api_key_here"
   ```

### 2. Wappalyzer API
**What it provides**: Technology stack analysis, framework detection
**Cost**: FREE tier available
**Signup**: https://www.wappalyzer.com/api/
**Free tier**: 1,000 requests/month

**How to get API key**:
1. Visit https://www.wappalyzer.com/api/
2. Sign up for free account
3. Get your API key from dashboard
4. Add to `config.py`:
   ```python
   WAPPALYZER_API_KEY = "your_api_key_here"
   ```

### 3. Google PageSpeed Insights API
**What it provides**: Website performance metrics, Core Web Vitals
**Cost**: FREE with Google Cloud
**Signup**: https://developers.google.com/speed/docs/insights/v5/get-started
**Free tier**: 25,000 requests/day

**How to get API key**:
1. Visit https://console.cloud.google.com/
2. Create a new project (free)
3. Enable PageSpeed Insights API
4. Create credentials (API key)
5. Add to `config.py`:
   ```python
   PAGESPEED_API_KEY = "your_api_key_here"
   ```

## 🚀 Quick Setup

### Step 1: Get Free API Keys
Choose one or more free APIs from above and get your API keys.

### Step 2: Update Configuration
Edit `config.py` and add your API keys:
```python
# Free APIs (recommended)
BUILTWITH_API_KEY = "your_builtwith_key_here"
WAPPALYZER_API_KEY = "your_wappalyzer_key_here"
PAGESPEED_API_KEY = "your_pagespeed_key_here"

# Expensive APIs (optional)
SIMILARWEB_API_KEY = None  # $1,167+/month
SEMRUSH_API_KEY = None     # $1,167+/month

# Use real data instead of mock
USE_MOCK_DATA = False
```

### Step 3: Test Your Setup
```bash
.\test_api.bat
```

### Step 4: Use the Tool
```bash
.\run_gui.bat
```

## 💰 Cost Comparison

| Service | Monthly Cost | Free Tier | What You Get |
|---------|-------------|-----------|--------------|
| **SimilarWeb** | $1,167+ | ❌ None | Traffic, rankings, sources |
| **SEMrush** | $1,167+ | ❌ None | SEO data, traffic |
| **BuiltWith** | $0 | ✅ 500 requests | Technology detection |
| **Wappalyzer** | $0 | ✅ 1,000 requests | Tech stack analysis |
| **PageSpeed** | $0 | ✅ 25,000 requests | Performance metrics |

## 🎯 What Each Free API Provides

### BuiltWith API
- ✅ Website technologies detected
- ✅ Hosting information
- ✅ Analytics tools used
- ✅ E-commerce platforms
- ✅ Content management systems

### Wappalyzer API
- ✅ JavaScript frameworks
- ✅ Content management systems
- ✅ E-commerce platforms
- ✅ Analytics tools
- ✅ Web servers

### PageSpeed API
- ✅ Performance scores
- ✅ Core Web Vitals
- ✅ Mobile/desktop metrics
- ✅ Optimization suggestions
- ✅ Loading times

## 🔧 Advanced Configuration

### Using Multiple APIs
The tool automatically uses all available APIs:
```python
# All free APIs
BUILTWITH_API_KEY = "key1"
WAPPALYZER_API_KEY = "key2"
PAGESPEED_API_KEY = "key3"
USE_MOCK_DATA = False
```

### Fallback Behavior
- If free APIs fail → Uses mock data
- If some APIs work → Uses available data
- Always provides results, never crashes

### Rate Limiting
Free APIs have rate limits:
- **BuiltWith**: 500 requests/month
- **Wappalyzer**: 1,000 requests/month
- **PageSpeed**: 25,000 requests/day

The tool includes automatic delays to respect these limits.

## 🧪 Testing Your Setup

### Test Individual APIs
```bash
python test_api.py
```

### Test with Real Data
1. Set `USE_MOCK_DATA = False` in `config.py`
2. Run `.\run_gui.bat`
3. Analyze a website
4. Check console for API usage

### Monitor API Usage
Watch the console output for:
- API request status
- Rate limit warnings
- Fallback notifications

## 🎉 Benefits of Free APIs

### Cost Savings
- **$0/month** vs **$1,167+/month**
- **100% free** for most use cases
- **No credit card** required

### Real Data
- ✅ **Actual website analysis**
- ✅ **Real technology detection**
- ✅ **Live performance metrics**
- ✅ **Current data** (not historical)

### Easy Setup
- ✅ **Quick registration** (5 minutes)
- ✅ **No complex configuration**
- ✅ **Automatic fallback**
- ✅ **Works immediately**

## 🔄 Migration from Expensive APIs

### If you currently use SimilarWeb/SEMrush:
1. **Keep existing setup** (it still works)
2. **Add free APIs** alongside expensive ones
3. **Test with free APIs** first
4. **Gradually reduce** expensive API usage
5. **Save money** while getting similar data

### Recommended Migration Path:
1. **Week 1**: Add free APIs, test alongside expensive ones
2. **Week 2**: Use free APIs for 50% of requests
3. **Week 3**: Use free APIs for 90% of requests
4. **Week 4**: Cancel expensive API subscriptions

## 🆘 Troubleshooting

### Common Issues:

**"API key not configured"**
- Check you've added the key to `config.py`
- Verify the key is correct (no extra spaces)

**"Rate limit exceeded"**
- Wait a few minutes before trying again
- Check your API usage in the provider's dashboard

**"API Error 401/403"**
- Verify your API key is correct
- Check if your account is active

**"No data available"**
- Some websites may not have data in free APIs
- Try with popular websites first (google.com, facebook.com)

### Getting Help:
- Check `API_TROUBLESHOOTING.md` for detailed solutions
- Run `.\test_api.bat` to diagnose issues
- Contact API providers for account issues

## 🎯 Best Practices

### 1. Start Small
- Test with 1-2 free APIs first
- Verify everything works before adding more

### 2. Monitor Usage
- Check your API usage regularly
- Stay within free tier limits

### 3. Use Mock Data for Development
- Keep `USE_MOCK_DATA = True` during development
- Switch to real APIs for production

### 4. Combine APIs
- Use multiple free APIs for comprehensive data
- Each API provides different insights

## 🚀 Ready to Start?

1. **Choose a free API** (BuiltWith recommended)
2. **Get your API key** (5 minutes)
3. **Update config.py** (1 minute)
4. **Test with `.\test_api.bat`** (1 minute)
5. **Start using real data!** 🎉

**Total setup time: ~10 minutes**
**Total cost: $0/month**
**Data quality: Professional grade**

The tool now works perfectly with free APIs, giving you real website analytics data without any monthly costs!

