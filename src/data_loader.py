"""
Data Loader Module
Handles loading, cleaning, and preprocessing of ESG data.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_esg_data(file_path: str = "data/esg_data.csv") -> pd.DataFrame:
    """
    Load ESG data from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with ESG data
    """
    df = pd.read_csv(file_path)
    df = clean_data(df)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess the ESG data.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Ensure proper data types
    df['year'] = df['year'].astype(int)
    df['company'] = df['company'].astype(str)
    df['sector'] = df['sector'].astype(str)
    df['country'] = df['country'].astype(str)
    
    # Round scores to 1 decimal place
    score_columns = ['environmental_score', 'social_score', 'governance_score', 'total_esg_score']
    for col in score_columns:
        df[col] = df[col].round(1)
    
    return df


def get_companies(df: pd.DataFrame) -> list:
    """Get unique list of companies."""
    return sorted(df['company'].unique().tolist())


def get_sectors(df: pd.DataFrame) -> list:
    """Get unique list of sectors."""
    return sorted(df['sector'].unique().tolist())


def get_countries(df: pd.DataFrame) -> list:
    """Get unique list of countries."""
    return sorted(df['country'].unique().tolist())


def get_years(df: pd.DataFrame) -> list:
    """Get unique list of years."""
    return sorted(df['year'].unique().tolist())


def filter_data(
    df: pd.DataFrame,
    companies: list = None,
    sectors: list = None,
    countries: list = None,
    years: list = None
) -> pd.DataFrame:
    """
    Filter DataFrame based on criteria.
    
    Args:
        df: Source DataFrame
        companies: List of companies to include
        sectors: List of sectors to include
        countries: List of countries to include
        years: List of years to include
        
    Returns:
        Filtered DataFrame
    """
    filtered_df = df.copy()
    
    if companies:
        filtered_df = filtered_df[filtered_df['company'].isin(companies)]
    if sectors:
        filtered_df = filtered_df[filtered_df['sector'].isin(sectors)]
    if countries:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    if years:
        filtered_df = filtered_df[filtered_df['year'].isin(years)]
    
    return filtered_df


def get_latest_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the most recent data for each company.
    
    Args:
        df: Source DataFrame
        
    Returns:
        DataFrame with only the latest year data for each company
    """
    return df.loc[df.groupby('company')['year'].idxmax()]


def calculate_sector_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average ESG scores by sector.
    
    Args:
        df: Source DataFrame
        
    Returns:
        DataFrame with sector averages
    """
    score_columns = ['environmental_score', 'social_score', 'governance_score', 'total_esg_score']
    
    sector_avg = df.groupby(['sector', 'year'])[score_columns].mean().round(1).reset_index()
    
    return sector_avg


def calculate_yoy_change(df: pd.DataFrame, company: str) -> pd.DataFrame:
    """
    Calculate year-over-year change for a company.
    
    Args:
        df: Source DataFrame
        company: Company name
        
    Returns:
        DataFrame with YoY changes
    """
    company_df = df[df['company'] == company].sort_values('year')
    
    score_columns = ['environmental_score', 'social_score', 'governance_score', 'total_esg_score']
    
    for col in score_columns:
        company_df[f'{col}_change'] = company_df[col].diff()
    
    return company_df


def get_esg_rating(score: float) -> tuple:
    """
    Convert ESG score to rating.
    
    Args:
        score: ESG score (0-100)
        
    Returns:
        Tuple of (rating, color)
    """
    if score >= 80:
        return ('AAA', '#006400')  # Dark green
    elif score >= 70:
        return ('AA', '#228B22')   # Forest green
    elif score >= 60:
        return ('A', '#32CD32')    # Lime green
    elif score >= 50:
        return ('BBB', '#FFD700')  # Gold
    elif score >= 40:
        return ('BB', '#FFA500')   # Orange
    elif score >= 30:
        return ('B', '#FF6347')    # Tomato
    elif score >= 20:
        return ('CCC', '#FF4500')  # Orange red
    else:
        return ('CC', '#DC143C')   # Crimson
