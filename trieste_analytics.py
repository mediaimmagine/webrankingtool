#!/usr/bin/env python3
"""
Trieste-specific analytics filtering
Includes triesteallnews.it and trieste.news
"""

from typing import Dict, List
from datetime import datetime, timedelta
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension, FilterExpression, Filter, OrderBy, FilterExpressionList

def get_trieste_metrics(fetchers_dict, days_back: int = 7) -> Dict:
    """Get metrics specifically for Trieste pages across all properties"""
    total_views = 0
    total_users = 0
    total_sessions = 0
    
    for prop_id, fetcher in fetchers_dict.items():
        try:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Filter for trieste pages (excluding pordenone)
            dimension_filter = FilterExpression(
                and_group=FilterExpressionList(
                    expressions=[
                        FilterExpression(
                            or_group=FilterExpressionList(
                                expressions=[
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="pagePath",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    ),
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="hostname",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    )
                                ]
                            )
                        ),
                        # Exclude pordenone
                        FilterExpression(
                            not_expression=FilterExpression(
                                filter=Filter(
                                    field_name="pagePath",
                                    string_filter=Filter.StringFilter(
                                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                                        value="pordenone"
                                    )
                                )
                            )
                        )
                    ]
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
                total_views += int(row.metric_values[0].value)
                total_users += int(row.metric_values[1].value)
                total_sessions += int(row.metric_values[2].value)
                
        except Exception as e:
            print(f"[WARN] Trieste metrics for {prop_id}: {str(e)[:80]}")
    
    return {'views': total_views, 'users': total_users, 'sessions': total_sessions}

def get_trieste_traffic_sources(fetchers_dict, days_back: int = 7) -> Dict:
    """Get traffic sources for Trieste pages"""
    combined_sources = {}
    
    for prop_id, fetcher in fetchers_dict.items():
        try:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Filter for trieste pages (excluding pordenone)
            dimension_filter = FilterExpression(
                and_group=FilterExpressionList(
                    expressions=[
                        FilterExpression(
                            or_group=FilterExpressionList(
                                expressions=[
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="pagePath",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    ),
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="hostname",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    )
                                ]
                            )
                        ),
                        FilterExpression(
                            not_expression=FilterExpression(
                                filter=Filter(
                                    field_name="pagePath",
                                    string_filter=Filter.StringFilter(
                                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                                        value="pordenone"
                                    )
                                )
                            )
                        )
                    ]
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
            
            for row in response.rows:
                channel = row.dimension_values[0].value
                sessions = int(row.metric_values[0].value)
                
                if channel in combined_sources:
                    combined_sources[channel] += sessions
                else:
                    combined_sources[channel] = sessions
                    
        except Exception as e:
            print(f"[WARN] Trieste sources for {prop_id}: {str(e)[:80]}")
    
    return combined_sources

def get_trieste_daily_traffic(fetchers_dict, days_back: int = 7) -> Dict:
    """Get daily traffic for Trieste pages"""
    combined_daily = {}
    
    for prop_id, fetcher in fetchers_dict.items():
        try:
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            # Filter for trieste pages (excluding pordenone)
            dimension_filter = FilterExpression(
                and_group=FilterExpressionList(
                    expressions=[
                        FilterExpression(
                            or_group=FilterExpressionList(
                                expressions=[
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="pagePath",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    ),
                                    FilterExpression(
                                        filter=Filter(
                                            field_name="hostname",
                                            string_filter=Filter.StringFilter(
                                                match_type=Filter.StringFilter.MatchType.CONTAINS,
                                                value="trieste"
                                            )
                                        )
                                    )
                                ]
                            )
                        ),
                        FilterExpression(
                            not_expression=FilterExpression(
                                filter=Filter(
                                    field_name="pagePath",
                                    string_filter=Filter.StringFilter(
                                        match_type=Filter.StringFilter.MatchType.CONTAINS,
                                        value="pordenone"
                                    )
                                )
                            )
                        )
                    ]
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
            
            for row in response.rows:
                date = row.dimension_values[0].value
                users = int(row.metric_values[0].value)
                
                if date in combined_daily:
                    combined_daily[date] += users
                else:
                    combined_daily[date] = users
                    
        except Exception as e:
            print(f"[WARN] Trieste daily for {prop_id}: {str(e)[:80]}")
    
    return combined_daily

