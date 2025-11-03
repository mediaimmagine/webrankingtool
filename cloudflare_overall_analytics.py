#!/usr/bin/env python3
"""
Get overall Cloudflare analytics using GraphQL
(We can get zone-level totals even with Pro plan)
"""

import requests
import json
from datetime import datetime, timedelta

def get_cloudflare_zone_analytics(zone_id, api_token, days_back=7):
    """
    Get overall zone analytics from Cloudflare GraphQL
    This works with Pro plan for overall metrics (not per-URL)
    """
    print(f"\n[INFO] Fetching Cloudflare Zone Analytics via GraphQL (last {days_back} days)...")
    
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
                print(f"[ERROR] GraphQL errors: {json.dumps(data['errors'], indent=2)}")
                return None
            
            # Debug: show structure
            print(f"[DEBUG] Response structure: {json.dumps(data, indent=2)[:500]}")
            
            # Extract data
            try:
                zones = data['data']['viewer']['zones']
                if zones and len(zones) > 0:
                    groups = zones[0]['httpRequests1dGroups']
                    
                    # Aggregate totals
                    total_requests = 0
                    total_pageviews = 0
                    total_threats = 0
                    total_bytes = 0
                    total_uniques = 0
                    
                    for group in groups:
                        if 'sum' in group:
                            total_requests += group['sum'].get('requests', 0)
                            total_pageviews += group['sum'].get('pageViews', 0)
                            total_threats += group['sum'].get('threats', 0)
                            total_bytes += group['sum'].get('bytes', 0)
                        
                        if 'uniq' in group:
                            # Note: uniques are already deduplicated per day
                            total_uniques += group['uniq'].get('uniques', 0)
                    
                    print(f"[OK] Cloudflare GraphQL data retrieved")
                    print(f"  Days retrieved: {len(groups)}")
                    
                    return {
                        'requests': total_requests,
                        'pageviews': total_pageviews,
                        'threats': total_threats,
                        'bandwidth': total_bytes,
                        'uniques': total_uniques,
                        'period_days': days_back,
                        'actual_days': len(groups),
                        'source': 'Cloudflare GraphQL (Zone-level)'
                    }
                else:
                    print(f"[ERROR] No zone data returned")
                    return None
            
            except KeyError as e:
                print(f"[ERROR] Unexpected data structure: {e}")
                print(f"Data: {json.dumps(data, indent=2)[:500]}")
                return None
        else:
            print(f"[ERROR] GraphQL API status: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"[ERROR] Cloudflare GraphQL request failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Test Cloudflare zone analytics"""
    from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ZONE_ID
    
    print("="*80)
    print("Testing Cloudflare Zone Analytics (GraphQL)")
    print("="*80)
    print(f"\nZone ID: {CLOUDFLARE_ZONE_ID}")
    
    # Test 7 days
    data = get_cloudflare_zone_analytics(CLOUDFLARE_ZONE_ID, CLOUDFLARE_API_TOKEN, days_back=7)
    
    if data:
        print(f"\n{'='*80}")
        print("RESULTS - Last 7 Days")
        print(f"{'='*80}")
        print(f"  Total Requests: {data['requests']:,}")
        print(f"  Page Views: {data['pageviews']:,}")
        print(f"  Unique Visitors: {data['uniques']:,}")
        print(f"  Threats Blocked: {data['threats']:,}")
        print(f"  Bandwidth: {data['bandwidth'] / (1024**3):.2f} GB")
        print(f"  Days with data: {data['actual_days']}")

if __name__ == "__main__":
    main()

