#!/usr/bin/env python3
"""
Detailed analysis of Cloudflare traffic to understand the discrepancy
"""

import requests
import json
from datetime import datetime, timedelta
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID

def get_cloudflare_traffic_breakdown(zone_id, api_token, days_back=7):
    """
    Get detailed breakdown of Cloudflare traffic
    """
    print(f"\n[INFO] Analyzing Cloudflare traffic breakdown...")
    
    try:
        url = "https://api.cloudflare.com/client/v4/graphql"
        
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Query for content type breakdown
        query = """
        query GetContentTypeBreakdown($zoneTag: string, $start: string, $end: string) {
          viewer {
            zones(filter: {zoneTag: $zoneTag}) {
              httpRequests1dGroups(
                limit: 1000,
                filter: {
                  date_geq: $start,
                  date_leq: $end
                }
              ) {
                sum {
                  requests
                  pageViews
                  bytes
                }
                dimensions {
                  contentType
                }
              }
            }
          }
        }
        """
        
        variables = {
            'zoneTag': zone_id,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
        
        payload = {
            'query': query,
            'variables': variables
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'errors' in data and data['errors']:
                # Content type might not be available, try simpler query
                print(f"[INFO] Content type breakdown not available with Pro plan")
                return None
            
            return data
        else:
            print(f"[WARN] Could not get traffic breakdown: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[WARN] Traffic breakdown failed: {str(e)}")
        return None

def main():
    print("="*80)
    print("Cloudflare Traffic Analysis - Understanding the Numbers")
    print("="*80)
    
    from cloudflare_overall_analytics import get_cloudflare_zone_analytics
    from google_analytics_fetcher import GoogleAnalyticsFetcher, load_config
    
    # Get Cloudflare data (7 days)
    cf_data = get_cloudflare_zone_analytics(CLOUDFLARE_ZONE_ID, CLOUDFLARE_API_TOKEN, days_back=7)
    
    # Get ALL GA properties combined
    ga_config = load_config()
    
    print(f"\n{'='*80}")
    print("CLOUDFLARE DATA (ENTIRE ZONE)")
    print(f"{'='*80}")
    
    if cf_data:
        print(f"  Total Requests: {cf_data['requests']:,}")
        print(f"  Page Views (CF): {cf_data['pageviews']:,}")
        print(f"  Unique Visitors (CF): {cf_data['uniques']:,}")
        print(f"  Threats Blocked: {cf_data['threats']:,}")
        print(f"  Bandwidth: {cf_data['bandwidth'] / (1024**3):.2f} GB")
    
    print(f"\n{'='*80}")
    print("GOOGLE ANALYTICS DATA (INDIVIDUAL PROPERTIES)")
    print(f"{'='*80}")
    
    properties = [
        ("476208509", "triesteallnews.it"),
        ("257131451", "FVG.news")
    ]
    
    ga_total_pageviews = 0
    ga_total_users = 0
    
    for prop_id, label in properties:
        try:
            fetcher = GoogleAnalyticsFetcher(
                credentials_file=ga_config['credentials_file'],
                property_id=prop_id
            )
            
            from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
            
            request = RunReportRequest(
                property=f"properties/{prop_id}",
                date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="activeUsers")
                ]
            )
            
            response = fetcher.client.run_report(request)
            
            if response.rows:
                row = response.rows[0]
                pageviews = int(row.metric_values[0].value)
                users = int(row.metric_values[1].value)
                
                print(f"\n[{label}] Property {prop_id}:")
                print(f"  Page Views: {pageviews:,}")
                print(f"  Users: {users:,}")
                
                ga_total_pageviews += pageviews
                ga_total_users += users
        except Exception as e:
            print(f"\n[ERROR] {label}: {str(e)[:100]}")
    
    print(f"\n{'='*80}")
    print("COMBINED GOOGLE ANALYTICS (ALL PROPERTIES)")
    print(f"{'='*80}")
    print(f"  Total Page Views: {ga_total_pageviews:,}")
    print(f"  Total Users: {ga_total_users:,}")
    
    print(f"\n{'='*80}")
    print("ANALYSIS")
    print(f"{'='*80}")
    
    if cf_data and ga_total_pageviews > 0:
        # Page views comparison
        coverage_pv = (ga_total_pageviews / cf_data['pageviews'] * 100)
        coverage_req = (ga_total_pageviews / cf_data['requests'] * 100)
        
        print(f"\n[PAGE VIEWS]")
        print(f"  Cloudflare Page Views: {cf_data['pageviews']:,}")
        print(f"  GA Page Views (combined): {ga_total_pageviews:,}")
        print(f"  GA captures {coverage_pv:.1f}% of CF page views")
        
        print(f"\n[REQUESTS]")
        print(f"  Cloudflare Total Requests: {cf_data['requests']:,}")
        print(f"  GA captures {coverage_req:.1f}% of all CF requests")
        
        # Users comparison
        coverage_users = (ga_total_users / cf_data['uniques'] * 100)
        print(f"\n[VISITORS]")
        print(f"  Cloudflare Uniques: {cf_data['uniques']:,}")
        print(f"  GA Users (combined): {ga_total_users:,}")
        print(f"  GA captures {coverage_users:.1f}% of CF uniques")
        
        print(f"\n{'='*80}")
        print("INTERPRETATION")
        print(f"{'='*80}")
        
        if coverage_pv < 10:
            print(f"\n[CRITICAL] Only {coverage_pv:.1f}% coverage is very low!")
            print(f"\n[POSSIBLE CAUSES]:")
            print(f"  1. Cloudflare 'pageViews' includes ALL HTTP requests")
            print(f"     - Images, CSS, JS files, fonts, API calls, etc.")
            print(f"     - Each page load generates 20-50+ requests")
            print(f"     - This inflates Cloudflare numbers significantly")
            print(f"\n  2. Cloudflare zone covers multiple sites/subdomains")
            print(f"     - FVG.news might be on same zone")
            print(f"     - All *.triesteallnews.it subdomains")
            print(f"     - Admin panels, APIs, etc.")
            print(f"\n  3. Bot/Crawler traffic (normal)")
            print(f"     - Search engine bots")
            print(f"     - Monitoring services")
            print(f"     - Malicious scrapers (blocked by CF)")
            
            print(f"\n[MORE REALISTIC METRIC]: User coverage = {coverage_users:.1f}%")
            print(f"  This is more reasonable and expected")
            print(f"  Suggests GA is capturing ~{coverage_users:.0f}% of real human traffic")
            
        else:
            print(f"\n[OK] {coverage_pv:.1f}% coverage is within normal range")

if __name__ == "__main__":
    main()

