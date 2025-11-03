#!/usr/bin/env python3
"""
Test what Cloudflare Analytics API endpoints work with Pro plan
"""

import requests
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID
from datetime import datetime, timedelta

zone_id = CLOUDFLARE_ZONE_ID
headers = {
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json'
}

print("="*80)
print("TESTING CLOUDFLARE PRO PLAN - AVAILABLE ANALYTICS")
print("="*80)

# Test 1: Zone Analytics Dashboard (should work with Pro)
print("\n[TEST 1] Zone-level Analytics Dashboard")
print("-"*80)

try:
    # Last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/analytics/dashboard"
    params = {
        'since': start_date.isoformat(),
        'until': end_date.isoformat()
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=15)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            result = data.get('result', {})
            timeseries = result.get('timeseries', [])
            totals = result.get('totals', {})
            
            print(f"[OK] Zone Analytics Available!")
            print(f"\nTotal Metrics (last 7 days):")
            print(f"  Requests: {totals.get('requests', {}).get('all', 'N/A'):,}")
            print(f"  Page Views: {totals.get('pageviews', {}).get('all', 'N/A'):,}")
            print(f"  Unique Visitors: {totals.get('uniques', {}).get('all', 'N/A'):,}")
            print(f"  Bandwidth: {totals.get('bandwidth', {}).get('all', 'N/A'):,} bytes")
            
            print(f"\n[INFO] This gives zone-level totals, NOT per-URL data")
        else:
            print(f"[ERROR] {data.get('errors')}")
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(response.text[:200])
        
except Exception as e:
    print(f"[ERROR] {str(e)}")

# Test 2: Try simpler GraphQL query (zone-level only)
print("\n[TEST 2] GraphQL Analytics - Zone Level (Pro Compatible)")
print("-"*80)

try:
    graphql_url = "https://api.cloudflare.com/client/v4/graphql"
    
    # Simpler query - just zone totals, no per-URL breakdown
    query = """
    query GetZoneAnalytics($zoneTag: string, $startDate: string, $endDate: string) {
      viewer {
        zones(filter: {zoneTag: $zoneTag}) {
          httpRequests1dGroups(
            filter: {
              date_geq: $startDate
              date_lt: $endDate
            }
            limit: 100
          ) {
            sum {
              requests
              pageViews
            }
            uniq {
              uniques
            }
          }
        }
      }
    }
    """
    
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    
    variables = {
        "zoneTag": zone_id,
        "startDate": start_date_str,
        "endDate": end_date_str
    }
    
    payload = {
        "query": query,
        "variables": variables
    }
    
    response = requests.post(graphql_url, headers=headers, json=payload, timeout=15)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if 'errors' in data:
            print(f"[ERROR] GraphQL Errors:")
            for error in data['errors']:
                print(f"  - {error.get('message')}")
        else:
            print(f"[OK] GraphQL Query Successful!")
            
            zones = data.get('data', {}).get('viewer', {}).get('zones', [])
            if zones:
                groups = zones[0].get('httpRequests1dGroups', [])
                
                total_requests = sum(g.get('sum', {}).get('requests', 0) for g in groups)
                total_pageviews = sum(g.get('sum', {}).get('pageViews', 0) for g in groups)
                
                print(f"\nZone-Level Data (last 7 days):")
                print(f"  Total Requests: {total_requests:,}")
                print(f"  Total Page Views: {total_pageviews:,}")
                
                print(f"\n[INFO] Pro plan provides zone totals only")
                print(f"[INFO] Per-URL data requires Business plan")
    else:
        print(f"[ERROR] Status {response.status_code}")
        print(response.text[:200])
        
except Exception as e:
    print(f"[ERROR] {str(e)}")

# Test 3: Check available fields in GraphQL schema
print("\n[TEST 3] Query GraphQL Schema - What Fields Are Available")
print("-"*80)

try:
    # Introspection query to see available fields
    schema_query = """
    {
      __type(name: "ZoneHttpRequests1dGroups") {
        fields {
          name
          description
        }
      }
    }
    """
    
    payload = {"query": schema_query}
    response = requests.post(graphql_url, headers=headers, json=payload, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('__type'):
            fields = data['data']['__type'].get('fields', [])
            print(f"[OK] Available fields in httpRequests1dGroups:")
            for field in fields[:20]:  # Show first 20
                name = field.get('name')
                desc = field.get('description', 'No description')
                print(f"  - {name}: {desc[:60]}")
        else:
            print(f"[INFO] Schema introspection not available")
    
except Exception as e:
    print(f"[INFO] Schema query not supported: {str(e)}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("\nWith Cloudflare Pro Plan:")
print("  ✅ Zone-level analytics (total traffic)")
print("  ❌ Per-URL analytics (article-by-article)")
print("\nTo get per-URL page view data:")
print("  → Upgrade to Business Plan ($200/month)")
print("  → Or use alternative method (WordPress plugin)")

