# WordPress REST API Integration Guide

## 📋 Overview

This guide explains how to use WordPress REST API to get **REAL article data** including potentially **real visit counts** from triesteallnews.it.

---

## 🎯 What You'll Get with API Access

### ✅ **Guaranteed Data (Standard WordPress)**
- Real article titles
- Real URLs and slugs
- Exact publication dates (with timestamps)
- Real author names and IDs
- Real categories and tags
- Article content and excerpts
- Featured images
- Comment counts
- Last modified dates

### 🎲 **Potential Data (Depends on Plugins)**
- **Real visit/view counts** ✨ (if WP-PostViews or similar plugin is installed)
- **Real engagement metrics** (if analytics plugin is active)
- **Custom fields** (ACF, meta boxes, etc.)
- **Social share counts** (if tracking plugin installed)

---

## 🔐 Step 1: Create Application Password

### In WordPress Admin:

1. **Log in to WordPress**
   - Go to: `https://www.triesteallnews.it/wp-admin`
   - Use your WordPress username and password

2. **Navigate to Your Profile**
   - Click "Users" in the left sidebar
   - Click "Your Profile" (or "Profile" under your name)

3. **Create Application Password**
   - Scroll down to **"Application Passwords"** section
   - Enter a name: `Article Analytics Tool`
   - Click **"Add New Application Password"**

4. **Copy the Password**
   - WordPress will show a password like: `xxxx xxxx xxxx xxxx xxxx xxxx`
   - **IMPORTANT**: Copy this password immediately!
   - You won't be able to see it again
   - The spaces don't matter (our script removes them)

5. **Save It Securely**
   - Store it in a password manager
   - Or write it down temporarily
   - Never share it or commit it to git

---

## 🚀 Step 2: Test API Access

### Option A: Interactive Setup (Recommended)

```bash
python wordpress_credentials.py
```

This will:
- Ask for your credentials interactively
- Save them securely to `wordpress_api_config.json`
- Set proper file permissions

### Option B: Direct Testing

```bash
python wordpress_api_tester.py
```

This will prompt you for credentials and test the API without saving them.

---

## 📊 Step 3: Run Full API Test

The API tester will:

1. ✅ Test connection to WordPress
2. ✅ Verify authentication
3. ✅ Fetch 10 recent posts
4. ✅ Analyze all available data fields
5. ✅ **Search for view count fields**
6. ✅ Save sample data to `sample_post_data.json`

### Expected Output:

```
================================================================================
WORDPRESS REST API FULL TEST SUITE
================================================================================
Website: https://www.triesteallnews.it
Username: your_username

================================================================================
TESTING WORDPRESS REST API CONNECTION
================================================================================
[OK] API is accessible!
Site Name: TRIESTE.news

================================================================================
TESTING AUTHENTICATION
================================================================================
[OK] Authentication successful!
Username: Your Name
User ID: 123

================================================================================
FETCHING POSTS
================================================================================
[OK] Retrieved 10 posts
Total Posts Available: 1234

================================================================================
SEARCHING FOR VIEW/VISIT COUNT FIELDS
================================================================================
[SUCCESS] Found 1 potential view count field(s):
  ✓ post_views (in meta): 1523
```

---

## 📁 Files Created

### `wordpress_api_config.json` (KEEP SECRET!)
```json
{
  "base_url": "https://www.triesteallnews.it",
  "username": "your_username",
  "app_password": "your_app_password_without_spaces",
  "created_at": "2025-11-03T10:00:00"
}
```

**⚠️ SECURITY WARNING:**
- This file contains your credentials
- Never commit it to git (it's in `.gitignore`)
- Keep it secure
- Only readable by file owner (Unix)

### `sample_post_data.json`
- Complete data structure of one post
- Shows all available fields
- Use for reference when building scrapers

---

## 🔍 Step 4: Check for View Count Plugins

### Common WordPress View Counter Plugins:

1. **WP-PostViews**
   - Field name: `views` or `post_views_count`
   - Very popular, likely installed

2. **Post Views Counter**
   - Field name: `post_views_count`
   - Modern, actively maintained

3. **Simple View Counter**
   - Field name: `view_count`
   - Lightweight option

4. **Google Analytics Counter Tracker**
   - Field name: `ga_pageviews`
   - Uses real GA data

### How to Check:

After running `wordpress_api_tester.py`, look for this section:

```
SEARCHING FOR VIEW/VISIT COUNT FIELDS
```

If it shows:
- ✅ **Field found** → You have real visit data! 🎉
- ❌ **No fields found** → Ask site admin to install a plugin

---

## 🛠️ Step 5: What If No View Counts Available?

### Option 1: Install a WordPress Plugin (Recommended)

Ask the site administrator to install one of these:

```
WP-PostViews (Free)
https://wordpress.org/plugins/wp-postviews/

Post Views Counter (Free)
https://wordpress.org/plugins/post-views-counter/
```

### Option 2: Use Google Analytics

If the site uses Google Analytics:
- Some plugins can sync GA data to WordPress
- Look for `ga_pageviews` or similar fields

### Option 3: Continue with Estimates

If real data is not available:
- Use the improved scraper we built
- Clearly label data as "estimated"
- Focus on relative comparisons rather than absolute numbers

---

## 📚 Step 6: Next Steps After Successful Test

Once API access is confirmed:

1. **Review `sample_post_data.json`**
   - Understand the complete data structure
   - Identify which fields have the data you need

2. **Update Article Analytics System**
   - Replace HTML scraping with API calls
   - Use real data for all available fields
   - Much more reliable and faster!

3. **Build Production Scraper**
   - Use authenticated API requests
   - Get structured, clean data
   - No HTML parsing needed

4. **If View Counts Found**
   - 🎉 Celebrate! You have real traffic data!
   - Update the GUI to show "Real Visits" not "Estimated"
   - Build trend analysis with historical data

---

## 🔒 Security Best Practices

### ✅ DO:
- Use Application Passwords (not your main password)
- Store credentials in `wordpress_api_config.json`
- Keep the config file out of git
- Revoke Application Passwords you don't use
- Use read-only API access when possible

### ❌ DON'T:
- Never commit credentials to git
- Never share your Application Password
- Never use your main WordPress password in scripts
- Never hardcode credentials in Python files

---

## 🐛 Troubleshooting

### "401 Unauthorized"
**Cause:** Wrong credentials or Application Passwords not enabled

**Fix:**
1. Verify username is correct
2. Check Application Password is copied correctly (no extra spaces at start/end)
3. Ensure Application Passwords are enabled in WordPress settings
4. Try creating a new Application Password

### "403 Forbidden"
**Cause:** Your user account doesn't have permission

**Fix:**
- Ensure your WordPress user has at least "Editor" role
- Some endpoints require "Administrator" role

### "Connection Timeout"
**Cause:** Network issues or server problems

**Fix:**
1. Check your internet connection
2. Verify the website is accessible in a browser
3. Try again later (server might be busy)

### "No View Count Fields Found"
**Cause:** No view counter plugin installed

**Fix:**
1. Ask site administrator to install WP-PostViews
2. Or continue using estimated data (clearly labeled)
3. Check `sample_post_data.json` manually for custom fields

---

## 📊 Expected Performance

### API vs HTML Scraping:

| Feature | HTML Scraping | WordPress API |
|---------|---------------|---------------|
| **Speed** | 2-3 sec/category | < 1 sec/request |
| **Reliability** | 80% (breaks if HTML changes) | 99% (stable API) |
| **Data Quality** | Parsed (some errors) | Structured (perfect) |
| **Visit Counts** | ❌ Not available | ✅ Available (if plugin installed) |
| **Authentication** | Not needed | Required |
| **Maintenance** | High (HTML changes) | Low (stable API) |

**Recommendation:** Use WordPress API for production!

---

## 📞 Need Help?

### Created Files:
- `wordpress_api_tester.py` - Test API access and explore data
- `wordpress_credentials.py` - Secure credentials manager
- `WORDPRESS_API_GUIDE.md` - This guide

### Next Step:
```bash
python wordpress_credentials.py
```

Then provide the WordPress username and Application Password when prompted.

---

## 🎉 Success Checklist

- [ ] Created Application Password in WordPress
- [ ] Ran `wordpress_credentials.py` to save credentials
- [ ] Ran `wordpress_api_tester.py` successfully
- [ ] Reviewed `sample_post_data.json`
- [ ] Identified available data fields
- [ ] Checked if view count fields exist
- [ ] Ready to build production API scraper!

---

**Last Updated:** November 3, 2025  
**Status:** Ready for Testing  
**Next:** Run `python wordpress_credentials.py`

