#!/usr/bin/env python3
"""
Configuration file for MediaImmagine Web Ranking Tool
"""

# API Configuration
# Free alternatives for real data integration

# BuiltWith API (Free tier available)
BUILTWITH_API_KEY = None  # Get free API key from https://api.builtwith.com/
BUILTWITH_BASE_URL = "https://api.builtwith.com/v20/api.json"

# Wappalyzer API (Free tier available)
WAPPALYZER_API_KEY = None  # Get free API key from https://www.wappalyzer.com/api/
WAPPALYZER_BASE_URL = "https://api.wappalyzer.com/v2/lookup"

# Google PageSpeed Insights API (Free with Google Cloud)
PAGESPEED_API_KEY = "AIzaSyCSBFykUBziUgL-iY0b37_-CFFz263AxwM"  # Google PageSpeed API key
PAGESPEED_BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

# SEOZoom API (Paid subscription - Real traffic data)
SEOZOOM_API_KEY = "AK-c8713689b856896216114ac25e2bb7a4"  # SEOZoom API key
SEOZOOM_BASE_URL = "https://apiv2.seozoom.com/api/v2"

# Cloudflare Browser Rendering API (Official API for content access)
CLOUDFLARE_API_TOKEN = "IvzQIqq_sEVeIv-aoDO8wzD4QW-4bRS62LNo3-QB"  # Your Cloudflare API token
CLOUDFLARE_ACCOUNT_ID = "cdf6203660960b5ce0404a772a7d04c5"  # Your Cloudflare account ID
CLOUDFLARE_BROWSER_RENDERING_URL = "https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/content"

# SimilarWeb API (Expensive - kept for reference)
SIMILARWEB_API_KEY = None  # Expensive: ~$1,167/month minimum
SIMILARWEB_BASE_URL = "https://api.similarweb.com/v1/website"

# SEMrush API (Expensive - kept for reference)
SEMRUSH_API_KEY = None  # Expensive: ~$1,167/month minimum
SEMRUSH_BASE_URL = "https://api.semrush.com"

# Alexa API (Historical - service discontinued)
ALEXA_API_KEY = None
ALEXA_BASE_URL = "https://awis.api.alexa.com"

# Application Settings
DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Mock Data Settings (for development/demo)
USE_MOCK_DATA = False  # Set to False when using real APIs - NOW USING REAL DATA!
NEVER_USE_MOCK_DATA = True  # Never display mock data, only real data
MOCK_DATA_VARIATION = 0.2  # 20% variation in mock data

# Export Settings
DEFAULT_EXPORT_FORMAT = "csv"
EXPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# GUI Settings
GUI_THEME = "clam"
GUI_WINDOW_SIZE = "1400x900"
GUI_FONT_FAMILY = "Arial"
GUI_FONT_SIZE = 10

# Web Interface Settings
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = True
