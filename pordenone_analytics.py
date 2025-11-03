#!/usr/bin/env python3
"""
Pordenone-specific analytics filtering
"""

from typing import Dict, List
from datetime import datetime, timedelta
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension, FilterExpression, Filter, OrderBy

def get_pordenone_metrics(fetcher, days_back: int = 7) -> Dict:
    """Get metrics specifically for pordenoneoggi.it pages"""
    try:
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Filter for pordenoneoggi pages
        dimension_filter = FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="pordenoneoggi"
                )
            )
        )
        
        request = RunReportRequest(
            property=fetcher.property_id,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            metrics=[
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
                Metric(name="sessions")
            ],
            dimension_filter=dimension_filter
        )
        
        response = fetcher.client.run_report(request)
        
        if response.rows:
            row = response.rows[0]
            return {
                'views': int(row.metric_values[0].value),
                'users': int(row.metric_values[1].value),
                'sessions': int(row.metric_values[2].value)
            }
        return {'views': 0, 'users': 0, 'sessions': 0}
        
    except Exception as e:
        print(f"[WARN] Pordenone metrics: {str(e)[:80]}")
        return {'views': 0, 'users': 0, 'sessions': 0}

def get_pordenone_traffic_sources(fetcher, days_back: int = 7) -> Dict:
    """Get traffic sources for pordenoneoggi.it"""
    try:
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Filter for pordenoneoggi pages
        dimension_filter = FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="pordenoneoggi"
                )
            )
        )
        
        request = RunReportRequest(
            property=fetcher.property_id,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            metrics=[Metric(name="sessions")],
            dimension_filter=dimension_filter
        )
        
        response = fetcher.client.run_report(request)
        
        sources = {}
        for row in response.rows:
            channel = row.dimension_values[0].value
            sessions = int(row.metric_values[0].value)
            sources[channel] = sessions
        
        return sources
        
    except Exception as e:
        print(f"[WARN] Pordenone sources: {str(e)[:80]}")
        return {}

def get_pordenone_daily_traffic(fetcher, days_back: int = 7) -> Dict:
    """Get daily traffic for pordenoneoggi.it"""
    try:
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Filter for pordenoneoggi pages
        dimension_filter = FilterExpression(
            filter=Filter(
                field_name="pagePath",
                string_filter=Filter.StringFilter(
                    match_type=Filter.StringFilter.MatchType.CONTAINS,
                    value="pordenoneoggi"
                )
            )
        )
        
        request = RunReportRequest(
            property=fetcher.property_id,
            date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
            dimensions=[Dimension(name="date")],
            metrics=[Metric(name="activeUsers")],
            dimension_filter=dimension_filter,
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="date"))]
        )
        
        response = fetcher.client.run_report(request)
        
        daily_data = {}
        for row in response.rows:
            date = row.dimension_values[0].value
            users = int(row.metric_values[0].value)
            daily_data[date] = users
        
        return daily_data
        
    except Exception as e:
        print(f"[WARN] Pordenone daily: {str(e)[:80]}")
        return {}

