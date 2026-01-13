"""
ESG Analyzer Module
Contains functions for analyzing ESG data and generating insights.
"""

import pandas as pd
import numpy as np


def calculate_company_metrics(df: pd.DataFrame, company: str) -> dict:
    """
    Calculate comprehensive metrics for a specific company.
    
    Args:
        df: Source DataFrame
        company: Company name
        
    Returns:
        Dictionary with company metrics
    """
    company_df = df[df['company'] == company].sort_values('year')
    latest = company_df.iloc[-1]
    
    # Calculate trends (comparing latest year to previous)
    if len(company_df) > 1:
        prev = company_df.iloc[-2]
        e_trend = latest['environmental_score'] - prev['environmental_score']
        s_trend = latest['social_score'] - prev['social_score']
        g_trend = latest['governance_score'] - prev['governance_score']
        total_trend = latest['total_esg_score'] - prev['total_esg_score']
    else:
        e_trend = s_trend = g_trend = total_trend = 0
    
    return {
        'company': company,
        'sector': latest['sector'],
        'country': latest['country'],
        'year': latest['year'],
        'environmental_score': latest['environmental_score'],
        'social_score': latest['social_score'],
        'governance_score': latest['governance_score'],
        'total_esg_score': latest['total_esg_score'],
        'e_trend': e_trend,
        's_trend': s_trend,
        'g_trend': g_trend,
        'total_trend': total_trend,
        'carbon_emissions': latest['carbon_emissions_mt'],
        'controversy_score': latest['controversy_score'],
        'market_cap': latest['market_cap_billion']
    }


def get_top_performers(df: pd.DataFrame, n: int = 5, metric: str = 'total_esg_score') -> pd.DataFrame:
    """
    Get top performing companies by ESG metric.
    
    Args:
        df: Source DataFrame
        n: Number of top companies to return
        metric: Score metric to rank by
        
    Returns:
        DataFrame with top performers
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    return latest_df.nlargest(n, metric)[['company', 'sector', metric]]


def get_bottom_performers(df: pd.DataFrame, n: int = 5, metric: str = 'total_esg_score') -> pd.DataFrame:
    """
    Get bottom performing companies by ESG metric.
    
    Args:
        df: Source DataFrame
        n: Number of bottom companies to return
        metric: Score metric to rank by
        
    Returns:
        DataFrame with bottom performers
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    return latest_df.nsmallest(n, metric)[['company', 'sector', metric]]


def calculate_sector_benchmark(df: pd.DataFrame, company: str) -> dict:
    """
    Calculate how a company performs vs its sector average.
    
    Args:
        df: Source DataFrame
        company: Company name
        
    Returns:
        Dictionary with benchmark comparisons
    """
    company_data = df[df['company'] == company]
    if company_data.empty:
        return {}
    
    latest_year = company_data['year'].max()
    company_latest = company_data[company_data['year'] == latest_year].iloc[0]
    sector = company_latest['sector']
    
    # Get sector averages for the latest year
    sector_data = df[(df['sector'] == sector) & (df['year'] == latest_year)]
    
    return {
        'company_e': company_latest['environmental_score'],
        'sector_e': sector_data['environmental_score'].mean(),
        'company_s': company_latest['social_score'],
        'sector_s': sector_data['social_score'].mean(),
        'company_g': company_latest['governance_score'],
        'sector_g': sector_data['governance_score'].mean(),
        'company_total': company_latest['total_esg_score'],
        'sector_total': sector_data['total_esg_score'].mean(),
        'sector': sector
    }


def identify_risks(df: pd.DataFrame, company: str) -> list:
    """
    Identify ESG-related risks for a company.
    
    Args:
        df: Source DataFrame
        company: Company name
        
    Returns:
        List of identified risks
    """
    company_data = df[df['company'] == company]
    if company_data.empty:
        return []
    
    latest = company_data[company_data['year'] == company_data['year'].max()].iloc[0]
    risks = []
    
    # Environmental risks
    if latest['environmental_score'] < 50:
        risks.append({
            'category': 'Environmental',
            'severity': 'High' if latest['environmental_score'] < 40 else 'Medium',
            'description': f"Environmental score ({latest['environmental_score']}) below industry threshold"
        })
    
    if latest['carbon_emissions_mt'] > 50:
        risks.append({
            'category': 'Environmental',
            'severity': 'High' if latest['carbon_emissions_mt'] > 100 else 'Medium',
            'description': f"High carbon emissions ({latest['carbon_emissions_mt']} MT)"
        })
    
    # Social risks
    if latest['social_score'] < 50:
        risks.append({
            'category': 'Social',
            'severity': 'High' if latest['social_score'] < 40 else 'Medium',
            'description': f"Social score ({latest['social_score']}) indicates workforce or community concerns"
        })
    
    if latest['safety_incidents'] > 20:
        risks.append({
            'category': 'Social',
            'severity': 'High' if latest['safety_incidents'] > 40 else 'Medium',
            'description': f"Elevated safety incidents ({latest['safety_incidents']} reported)"
        })
    
    # Governance risks
    if latest['governance_score'] < 60:
        risks.append({
            'category': 'Governance',
            'severity': 'High' if latest['governance_score'] < 50 else 'Medium',
            'description': f"Governance score ({latest['governance_score']}) suggests oversight concerns"
        })
    
    if latest['board_independence_pct'] < 60:
        risks.append({
            'category': 'Governance',
            'severity': 'Medium',
            'description': f"Low board independence ({latest['board_independence_pct']}%)"
        })
    
    # Controversy risk
    if latest['controversy_score'] < 60:
        risks.append({
            'category': 'Reputation',
            'severity': 'High' if latest['controversy_score'] < 50 else 'Medium',
            'description': f"Controversy score ({latest['controversy_score']}) indicates reputational risks"
        })
    
    return risks


def calculate_improvement_areas(df: pd.DataFrame, company: str) -> list:
    """
    Identify areas where a company can improve.
    
    Args:
        df: Source DataFrame
        company: Company name
        
    Returns:
        List of improvement recommendations
    """
    benchmark = calculate_sector_benchmark(df, company)
    if not benchmark:
        return []
    
    improvements = []
    
    # Compare to sector averages
    if benchmark['company_e'] < benchmark['sector_e']:
        diff = benchmark['sector_e'] - benchmark['company_e']
        improvements.append({
            'area': 'Environmental',
            'gap': round(diff, 1),
            'recommendation': 'Focus on reducing carbon emissions and improving energy efficiency'
        })
    
    if benchmark['company_s'] < benchmark['sector_s']:
        diff = benchmark['sector_s'] - benchmark['company_s']
        improvements.append({
            'area': 'Social',
            'gap': round(diff, 1),
            'recommendation': 'Enhance workforce diversity, safety programs, and community engagement'
        })
    
    if benchmark['company_g'] < benchmark['sector_g']:
        diff = benchmark['sector_g'] - benchmark['company_g']
        improvements.append({
            'area': 'Governance',
            'gap': round(diff, 1),
            'recommendation': 'Strengthen board independence and improve executive compensation alignment'
        })
    
    return improvements


def generate_summary_stats(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics for the dataset.
    
    Args:
        df: Source DataFrame
        
    Returns:
        Dictionary with summary statistics
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    
    return {
        'total_companies': len(latest_df),
        'total_sectors': latest_df['sector'].nunique(),
        'total_countries': latest_df['country'].nunique(),
        'avg_esg_score': round(latest_df['total_esg_score'].mean(), 1),
        'avg_e_score': round(latest_df['environmental_score'].mean(), 1),
        'avg_s_score': round(latest_df['social_score'].mean(), 1),
        'avg_g_score': round(latest_df['governance_score'].mean(), 1),
        'top_performer': latest_df.loc[latest_df['total_esg_score'].idxmax(), 'company'],
        'top_score': latest_df['total_esg_score'].max(),
        'years_covered': f"{df['year'].min()} - {df['year'].max()}"
    }
