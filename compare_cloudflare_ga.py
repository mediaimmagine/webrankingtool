#!/usr/bin/env python3
"""
Compare Cloudflare Analytics with Google Analytics
to understand data coverage and potential gaps
"""

import json
import requests
from datetime import datetime, timedelta
from google_analytics_fetcher import GoogleAnalyticsFetcher, load_config

def get_cloudflare_analytics(zone_id, api_token, days_back=7):
    """
    Get overall analytics from Cloudflare GraphQL
    """
    print(f"\n[INFO] Fetching Cloudflare Zone Analytics (last {days_back} days)...")
    
    try:
        url = "https://api.cloudflare.com/client/v4/graphql"
        
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # GraphQL query for zone-level analytics
        query = """
        query GetZoneAnalytics($zoneTag: string, $start: string, $end: string) {
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
                  threats
                  bytes
                }
                uniq {
                  uniques
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
                print(f"[ERROR] GraphQL errors: {data['errors']}")
                return None
            
            # Extract and aggregate data
            try:
                zones = data['data']['viewer']['zones']
                if zones and len(zones) > 0:
                    groups = zones[0]['httpRequests1dGroups']
                    
                    # Aggregate totals
                    total_requests = sum(g['sum'].get('requests', 0) for g in groups if 'sum' in g)
                    total_pageviews = sum(g['sum'].get('pageViews', 0) for g in groups if 'sum' in g)
                    total_threats = sum(g['sum'].get('threats', 0) for g in groups if 'sum' in g)
                    total_bytes = sum(g['sum'].get('bytes', 0) for g in groups if 'sum' in g)
                    total_uniques = sum(g['uniq'].get('uniques', 0) for g in groups if 'uniq' in g)
                    
                    print(f"[OK] Cloudflare data retrieved ({len(groups)} days)")
                    
                    return {
                        'requests': total_requests,
                        'pageviews': total_pageviews,
                        'threats': total_threats,
                        'bandwidth': total_bytes,
                        'uniques': total_uniques,
                        'period_days': days_back,
                        'actual_days': len(groups),
                        'source': 'Cloudflare GraphQL'
                    }
                else:
                    print(f"[ERROR] No zone data returned")
                    return None
            except Exception as e:
                print(f"[ERROR] Parsing data: {e}")
                return None
        else:
            print(f"[ERROR] API status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Request failed: {str(e)}")
        return None

def get_ga_analytics(property_id, credentials_file, days_back=7):
    """
    Get overall analytics from Google Analytics
    """
    print(f"\n[INFO] Fetching Google Analytics (last {days_back} days)...")
    
    try:
        fetcher = GoogleAnalyticsFetcher(
            credentials_file=credentials_file,
            property_id=property_id
        )
        
        from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric
        
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="sessions"),
                Metric(name="totalUsers")
            ]
        )
        
        response = fetcher.client.run_report(request)
        
        if response.rows:
            row = response.rows[0]
            
            print(f"[OK] Google Analytics data retrieved")
            
            return {
                'pageviews': int(row.metric_values[0].value),
                'active_users': int(row.metric_values[1].value),
                'sessions': int(row.metric_values[2].value),
                'total_users': int(row.metric_values[3].value),
                'period_days': days_back,
                'source': 'Google Analytics 4'
            }
        else:
            print(f"[WARN] No Google Analytics data for this period")
            return None
            
    except Exception as e:
        print(f"[ERROR] Google Analytics request failed: {str(e)}")
        return None

def compare_data(cloudflare_data, ga_data, days):
    """
    Compare Cloudflare and Google Analytics data
    """
    print(f"\n{'='*80}")
    print(f"DATA COMPARISON - Last {days} Days")
    print(f"{'='*80}")
    
    if not cloudflare_data:
        print("\n[ERROR] Cloudflare data not available")
        return
    
    if not ga_data:
        print("\n[ERROR] Google Analytics data not available")
        return
    
    # Display data side by side
    print(f"\n{'Metric':<25} {'Cloudflare':<20} {'Google Analytics':<20} {'Difference':<15}")
    print("-" * 80)
    
    # Page Views / Requests
    cf_requests = cloudflare_data.get('requests', 0)
    cf_pageviews = cloudflare_data.get('pageviews', 0)
    ga_pageviews = ga_data.get('pageviews', 0)
    
    # Use Cloudflare pageviews if available, otherwise requests
    cf_metric_to_use = cf_pageviews if cf_pageviews > 0 else cf_requests
    cf_label = "Pageviews" if cf_pageviews > 0 else "Requests"
    
    print(f"{'Page Views':<25} {cf_metric_to_use:<20,} {ga_pageviews:<20,}", end='')
    
    if cf_metric_to_use > 0 and ga_pageviews > 0:
        diff_pct = ((cf_metric_to_use - ga_pageviews) / cf_metric_to_use * 100)
        ratio = ga_pageviews / cf_metric_to_use
        print(f"{diff_pct:>+6.1f}%")
        print(f"{'  (GA captures)':<25} {'':<20} {ratio*100:>19.1f}%")
    else:
        print()
    
    # Unique Visitors / Users
    cf_uniques = cloudflare_data.get('uniques', 0)
    ga_users = ga_data.get('active_users', 0)
    
    print(f"{'Unique Visitors/Users':<25} {cf_uniques:<20,} {ga_users:<20,}", end='')
    
    if cf_uniques > 0 and ga_users > 0:
        diff_pct = ((cf_uniques - ga_users) / cf_uniques * 100)
        ratio = ga_users / cf_uniques
        print(f"{diff_pct:>+6.1f}%")
        print(f"{'  (GA captures)':<25} {'':<20} {ratio*100:>19.1f}%")
    else:
        print()
    
    # Sessions (GA only)
    ga_sessions = ga_data.get('sessions', 0)
    print(f"{'Sessions':<25} {'N/A':<20} {ga_sessions:<20,}")
    
    # Bandwidth (Cloudflare only)
    cf_bandwidth = cloudflare_data.get('bandwidth', 0)
    bandwidth_gb = cf_bandwidth / (1024**3) if cf_bandwidth > 0 else 0
    print(f"{'Bandwidth':<25} {bandwidth_gb:<19.2f}GB {'N/A':<20}")
    
    # Analysis
    print(f"\n{'='*80}")
    print("ANALYSIS")
    print(f"{'='*80}")
    
    if cf_metric_to_use > 0 and ga_pageviews > 0:
        coverage_pct = (ga_pageviews / cf_metric_to_use * 100)
        
        print(f"\n[COVERAGE] Google Analytics captures {coverage_pct:.1f}% of Cloudflare traffic")
        
        if coverage_pct > 95:
            print(f"  Status: Excellent - GA is capturing nearly all traffic")
        elif coverage_pct > 80:
            print(f"  Status: Good - GA is capturing most traffic")
            print(f"  Missing: ~{100-coverage_pct:.1f}% could be bots, ad blockers, or JS disabled")
        elif coverage_pct > 60:
            print(f"  Status: Fair - GA is missing significant traffic")
            print(f"  Missing: ~{100-coverage_pct:.1f}% - Check GA tracking code installation")
        else:
            print(f"  Status: Poor - GA is missing majority of traffic")
            print(f"  Missing: ~{100-coverage_pct:.1f}% - Possible tracking code issues")
        
        # Estimate "real human traffic"
        print(f"\n[ESTIMATION] Traffic Breakdown:")
        print(f"  Cloudflare Total Requests: {cf_metric_to_use:,}")
        print(f"  Google Analytics (JS-enabled): {ga_pageviews:,} ({coverage_pct:.1f}%)")
        print(f"  Estimated bots/blockers: {cf_metric_to_use - ga_pageviews:,} ({100-coverage_pct:.1f}%)")
        
        print(f"\n[RECOMMENDATION]:")
        if coverage_pct > 80:
            print(f"  Google Analytics data is reliable for your use case")
            print(f"  The {100-coverage_pct:.1f}% difference is likely bots, crawlers, and ad blockers")
            print(f"  Use GA data as your primary source")
        else:
            print(f"  Consider investigating why GA is missing {100-coverage_pct:.1f}% of traffic")
            print(f"  Check if GA tracking code is properly installed on all pages")
    
    # User comparison
    if cf_uniques > 0 and ga_users > 0:
        user_coverage = (ga_users / cf_uniques * 100)
        print(f"\n[USERS] GA captures {user_coverage:.1f}% of Cloudflare unique visitors")

def main():
    print("="*80)
    print("Cloudflare vs Google Analytics - Data Comparison")
    print("triesteallnews.it (Property 476208509)")
    print("="*80)
    
    # Load Cloudflare config
    from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID
    from cloudflare_overall_analytics import get_cloudflare_zone_analytics
    
    # Load GA config
    ga_config = load_config()
    
    if not ga_config:
        print("[ERROR] Google Analytics not configured")
        return
    
    # Test different time periods
    time_periods = [7, 28]
    
    for days in time_periods:
        # Get Cloudflare data using GraphQL
        cf_data = get_cloudflare_zone_analytics(CLOUDFLARE_ZONE_ID, CLOUDFLARE_API_TOKEN, days)
        
        # Get GA data for primary property (triesteallnews.it)
        ga_data = get_ga_analytics(
            property_id="476208509",  # triesteallnews.it only
            credentials_file=ga_config['credentials_file'],
            days_back=days
        )
        
        # Compare
        if cf_data and ga_data:
            compare_data(cf_data, ga_data, days)
        elif cf_data:
            print(f"\n[WARN] Only Cloudflare data available for {days} days")
        elif ga_data:
            print(f"\n[WARN] Only Google Analytics data available for {days} days")
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\n[INFO] This comparison helps you understand:")
    print("  1. How much traffic Google Analytics is capturing")
    print("  2. What percentage might be bots/crawlers/ad blockers")
    print("  3. Whether GA data is reliable for your analytics")
    print("\n[NOTE] Cloudflare sees ALL requests at the edge")
    print("[NOTE] Google Analytics only tracks JS-enabled, non-blocked page views")
    print("[NOTE] The difference is normal and expected (typically 10-30%)")

if __name__ == "__main__":
    main()

