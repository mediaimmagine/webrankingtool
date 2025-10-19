# 🔧 API Troubleshooting Guide

This guide helps you resolve common API issues with the MediaImmagine Web Ranking Tool.

## 🚨 Common Issues and Solutions

### 1. SimilarWeb API 404 Errors

**Problem**: Getting 404 errors from SimilarWeb API endpoints

**Possible Causes**:
- API endpoints have changed
- Incorrect API key format
- API key doesn't have required permissions
- Domain not supported by SimilarWeb

**Solutions**:

#### Option A: Check API Key Format
```python
# In config.py, ensure your API key looks like this:
SIMILARWEB_API_KEY = "your_32_character_api_key_here"
```

#### Option B: Test Different Endpoints
The tool now automatically tries multiple SimilarWeb endpoints:
- `/total-traffic-and-engagement/visits`
- `/traffic-and-engagement/visits`
- `/visits`
- `/overview`
- `/traffic-sources/overview`

#### Option C: Verify API Key Permissions
1. Log into your SimilarWeb account
2. Check if your API key has access to:
   - Website traffic data
   - Traffic sources
   - Geographic data

#### Option D: Use Alternative Data Sources
If SimilarWeb continues to fail, consider:
- **SEMrush API** (usually more reliable)
- **BuiltWith API**
- **Wappalyzer API**
- **Custom web scraping**

### 2. SEMrush API Issues

**Problem**: SEMrush API not working

**Solutions**:
1. Verify your API key is correct
2. Check your SEMrush account has API access
3. Ensure you have remaining API calls in your quota

### 3. Authentication Errors (401/403)

**Problem**: Getting 401 (Unauthorized) or 403 (Forbidden) errors

**Solutions**:
1. **Check API Key**: Ensure it's copied correctly without extra spaces
2. **Verify Account Status**: Make sure your account is active
3. **Check Permissions**: Ensure your API key has required permissions
4. **Rate Limits**: Wait if you've exceeded rate limits

### 4. No Data Available

**Problem**: APIs work but return no data for certain websites

**Solutions**:
1. **Try Popular Websites**: Test with google.com, facebook.com first
2. **Check Domain Format**: Ensure domain is correct (no http://, www.)
3. **API Coverage**: Some APIs don't have data for all websites
4. **Use Mock Data**: The tool falls back to mock data automatically

## 🧪 Testing Your Setup

### Step 1: Run the API Test
```bash
.\test_api.bat
```

This will test all configured APIs and show you exactly what's working.

### Step 2: Check Console Output
When running the tool, watch the console for:
- API endpoint attempts
- Error messages
- Fallback notifications

### Step 3: Verify Configuration
Check your `config.py`:
```python
# Make sure these are set correctly
SIMILARWEB_API_KEY = "your_actual_key_here"
SEMRUSH_API_KEY = "your_actual_key_here"
USE_MOCK_DATA = False  # Set to False for real APIs
```

## 🔄 Fallback Behavior

The tool is designed to be robust:

1. **Primary**: Tries real APIs first
2. **Fallback**: Uses mock data if APIs fail
3. **Graceful**: Always provides some data, never crashes

## 📊 Alternative Data Sources

If SimilarWeb doesn't work, consider these alternatives:

### BuiltWith API
- Website technology detection
- Traffic estimates
- Contact information

### Wappalyzer API
- Technology stack analysis
- Framework detection
- Plugin identification

### Custom Web Scraping
- Public data sources
- Website analysis
- Custom metrics

## 🆘 Getting Help

### 1. Check Error Messages
Look for specific error codes:
- **404**: Endpoint not found
- **401**: Unauthorized (wrong API key)
- **403**: Forbidden (no permissions)
- **429**: Rate limit exceeded

### 2. Test with Simple Tools
Use curl or Postman to test APIs directly:
```bash
curl -H "api-key: YOUR_KEY" \
     "https://api.similarweb.com/v1/website/google.com/visits"
```

### 3. Contact API Providers
- **SimilarWeb**: https://support.similarweb.com/
- **SEMrush**: https://www.semrush.com/support/

### 4. Use Mock Data
If all else fails, the tool works perfectly with mock data:
```python
# In config.py
USE_MOCK_DATA = True
```

## 💡 Pro Tips

1. **Start with Mock Data**: Test the tool with mock data first
2. **Test Popular Sites**: Use well-known websites for testing
3. **Check Quotas**: Monitor your API usage limits
4. **Keep Backups**: Save working API keys securely
5. **Update Regularly**: APIs change, keep the tool updated

## 🔧 Quick Fixes

### Reset to Mock Data
```python
# In config.py
USE_MOCK_DATA = True
SIMILARWEB_API_KEY = None
SEMRUSH_API_KEY = None
```

### Test Single API
```python
# In config.py - test only SimilarWeb
USE_MOCK_DATA = False
SIMILARWEB_API_KEY = "your_key"
SEMRUSH_API_KEY = None
```

### Debug Mode
The tool shows detailed error messages in the console. Watch for:
- Endpoint testing results
- API response codes
- Fallback notifications

Remember: The tool is designed to always work, even when APIs fail!

