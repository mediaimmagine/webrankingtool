# 🔑 API Setup Guide - Real Data Integration

This guide will help you configure the MediaImmagine Web Ranking Tool to use real data from actual APIs instead of mock data.

## 📋 Prerequisites

- Internet connection
- Valid API keys from the data providers
- Basic understanding of API keys and configuration

## 🚀 Step-by-Step Setup

### Step 1: Get API Keys

#### SimilarWeb API (Recommended)
1. Visit: https://www.similarweb.com/corp/api/
2. Sign up for a free trial or paid plan
3. Navigate to your dashboard
4. Copy your API key

#### SEMrush API (Optional)
1. Visit: https://www.semrush.com/api/
2. Sign up for a SEMrush account
3. Go to API section in your account
4. Copy your API key

### Step 2: Configure API Keys

1. Open `config.py` in a text editor
2. Replace the placeholder values with your actual API keys:

```python
# SimilarWeb API
SIMILARWEB_API_KEY = "your_actual_similarweb_api_key_here"

# SEMrush API  
SEMRUSH_API_KEY = "your_actual_semrush_api_key_here"

# Mock Data Settings
USE_MOCK_DATA = False  # Set to False to use real APIs
```

### Step 3: Test Your API Configuration

1. Run the API test script to verify your keys work:
   ```bash
   python test_api.py
   ```

2. This will test both APIs and show you if they're working correctly

### Step 4: Test the Configuration

1. Run the GUI application:
   ```bash
   .\run_gui.bat
   ```

2. Try analyzing a website (e.g., `triesteallnews.it`)
3. Check if you get real data instead of mock data

## 🔧 API Features

### SimilarWeb API Provides:
- ✅ Real monthly visit data
- ✅ Global and country rankings
- ✅ Traffic source breakdown
- ✅ Geographic distribution
- ✅ Bounce rate and engagement metrics

### SEMrush API Provides:
- ✅ SEO-focused rankings
- ✅ Organic search traffic
- ✅ Paid traffic data
- ✅ Domain authority metrics

## ⚠️ Important Notes

### Rate Limits
- APIs have rate limits (requests per minute/hour)
- The tool includes automatic delays to respect limits
- Free tiers may have limited requests per month

### API Costs
- SimilarWeb: Free tier available, paid plans for more data
- SEMrush: Paid service, various pricing tiers
- Check current pricing on their websites

### Fallback Behavior
- If API fails, the tool automatically falls back to mock data
- Error messages will be displayed in the console
- This ensures the tool always works, even with API issues

## 🐛 Troubleshooting

### Common Issues:

1. **"API Key Invalid" Error**
   - Double-check your API key is correct
   - Ensure you've copied the entire key without extra spaces

2. **"Rate Limit Exceeded" Error**
   - Wait a few minutes before trying again
   - Consider upgrading your API plan

3. **"No Data Available" Error**
   - Some websites may not have data in the APIs
   - Try with more popular websites first

4. **Still Getting Mock Data**
   - Check that `USE_MOCK_DATA = False` in config.py
   - Verify your API keys are properly set
   - Check the console for error messages

### Getting Help:
- Check the console output for detailed error messages
- Verify your API keys are active and have remaining quota
- Test with well-known websites first (google.com, facebook.com)

## 🎯 Recommended Configuration

For best results, we recommend:
1. **SimilarWeb API** - Most comprehensive data
2. **SEMrush API** - Good for SEO analysis
3. **Alexa API** - Leave as None (service discontinued)

## 📊 Data Quality

Real API data provides:
- ✅ Accurate, up-to-date metrics
- ✅ Professional-grade analytics
- ✅ Reliable for business decisions
- ✅ Consistent with industry standards

Mock data is useful for:
- 🧪 Testing and development
- 📚 Learning the tool features
- 💰 Avoiding API costs during development
