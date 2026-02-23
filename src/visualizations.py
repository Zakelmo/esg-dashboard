"""
Visualizations Module
Contains functions for creating interactive charts and graphs with enhanced styling.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


# SmartDeploy Color scheme for light theme - Orange/Red palette
COLORS = {
    'environmental': '#059669',  # Green (keeping for ESG semantic)
    'social': '#F97316',         # SmartDeploy Orange
    'governance': '#DC2626',     # SmartDeploy Red
    'total': '#1c1917',          # Dark stone
    'positive': '#22c55e',       # Success green
    'negative': '#EF4444',       # SmartDeploy Red
    'neutral': '#a8a29e'         # Warm gray
}

# Dark theme colors - SmartDeploy Orange/Red palette
COLORS_DARK = {
    'environmental': '#34d399',  # Lighter green
    'social': '#FB923C',         # Light orange
    'governance': '#F87171',     # Light red
    'total': '#fafaf9',          # Light stone
    'positive': '#4ade80',       # Light green
    'negative': '#F87171',       # Light red
    'neutral': '#d6d3d1'         # Light warm gray
}

# SmartDeploy sector colors - Orange/Red themed
SECTOR_COLORS = {
    'Technology': '#F97316',      # SmartDeploy Orange
    'Automotive': '#F59E0B',      # Amber
    'Financial Services': '#DC2626',  # SmartDeploy Red
    'Consumer Goods': '#EA580C',  # Orange-red
    'Energy': '#EF4444',          # Red
    'Healthcare': '#FB923C'       # Light orange
}

# Global theme setting
CURRENT_THEME = 'light'


def set_theme(theme='light'):
    """
    Set the global theme for visualizations

    Args:
        theme: 'light' or 'dark'
    """
    global CURRENT_THEME
    CURRENT_THEME = theme


def get_colors():
    """Get current theme colors"""
    return COLORS_DARK if CURRENT_THEME == 'dark' else COLORS


def get_template():
    """Get Plotly template based on current theme"""
    if CURRENT_THEME == 'dark':
        return 'plotly_dark'
    return 'plotly_white'


def get_bg_color():
    """Get background color for current theme - SmartDeploy"""
    return '#0c0a09' if CURRENT_THEME == 'dark' else '#ffffff'  # Warm dark / White


def get_text_color():
    """Get text color for current theme - SmartDeploy"""
    return '#fafaf9' if CURRENT_THEME == 'dark' else '#1c1917'  # Warm light / Dark stone


def create_esg_gauge(score: float, title: str, color: str = None) -> go.Figure:
    """
    Create a gauge chart for ESG score with theme support.

    Args:
        score: ESG score (0-100)
        title: Chart title
        color: Optional color for the gauge

    Returns:
        Plotly figure
    """
    colors = get_colors()

    if color is None:
        if score >= 70:
            color = colors['positive']
        elif score >= 50:
            color = '#F59E0B'  # SmartDeploy amber/orange
        else:
            color = colors['negative']

    # Theme-aware step colors - SmartDeploy warm palette
    if CURRENT_THEME == 'dark':
        steps = [
            {'range': [0, 40], 'color': '#3f1d1d'},    # Dark red
            {'range': [40, 60], 'color': '#3f2a1d'},   # Dark orange
            {'range': [60, 80], 'color': '#2a271d'},   # Dark amber
            {'range': [80, 100], 'color': '#1d2a1f'}   # Dark green
        ]
        threshold_color = get_text_color()
    else:
        steps = [
            {'range': [0, 40], 'color': '#FEF2F2'},    # Light red
            {'range': [40, 60], 'color': '#FFF7ED'},   # Light orange
            {'range': [60, 80], 'color': '#FFFBEB'},   # Light amber
            {'range': [80, 100], 'color': '#F0FDF4'}   # Light green
        ]
        threshold_color = "#1c1917"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': get_text_color()}},
        number={'font': {'size': 40, 'color': get_text_color()}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': get_text_color()},
            'bar': {'color': color},
            'bgcolor': get_bg_color(),
            'borderwidth': 2,
            'bordercolor': get_text_color(),
            'steps': steps,
            'threshold': {
                'line': {'color': threshold_color, 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor=get_bg_color(),
        font=dict(color=get_text_color())
    )

    return fig


def create_esg_breakdown_chart(e_score: float, s_score: float, g_score: float) -> go.Figure:
    """
    Create a bar chart showing E, S, G breakdown with theme support.

    Args:
        e_score: Environmental score
        s_score: Social score
        g_score: Governance score

    Returns:
        Plotly figure
    """
    colors = get_colors()
    categories = ['Environmental', 'Social', 'Governance']
    scores = [e_score, s_score, g_score]
    bar_colors = [colors['environmental'], colors['social'], colors['governance']]

    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=scores,
            marker_color=bar_colors,
            text=[f'{s:.1f}' for s in scores],
            textposition='outside',
            textfont=dict(size=14, color=get_text_color()),
            hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='ESG Score Breakdown',
        yaxis_title='Score',
        yaxis=dict(range=[0, 110]),
        height=350,
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),
        template=get_template(),
        paper_bgcolor=get_bg_color(),
        plot_bgcolor=get_bg_color(),
        font=dict(color=get_text_color())
    )

    return fig


def create_trend_chart(df: pd.DataFrame, company: str) -> go.Figure:
    """
    Create a line chart showing ESG score trends over time with theme support.

    Args:
        df: DataFrame with ESG data
        company: Company name

    Returns:
        Plotly figure
    """
    colors = get_colors()
    company_df = df[df['company'] == company].sort_values('year')

    fig = go.Figure()

    # Add traces for each score
    fig.add_trace(go.Scatter(
        x=company_df['year'],
        y=company_df['environmental_score'],
        name='Environmental',
        line=dict(color=colors['environmental'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate='<b>Environmental</b><br>Year: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=company_df['year'],
        y=company_df['social_score'],
        name='Social',
        line=dict(color=colors['social'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate='<b>Social</b><br>Year: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=company_df['year'],
        y=company_df['governance_score'],
        name='Governance',
        line=dict(color=colors['governance'], width=3),
        mode='lines+markers',
        marker=dict(size=8),
        hovertemplate='<b>Governance</b><br>Year: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=company_df['year'],
        y=company_df['total_esg_score'],
        name='Total ESG',
        line=dict(color=colors['total'], width=4, dash='dash'),
        mode='lines+markers',
        marker=dict(size=10),
        hovertemplate='<b>Total ESG</b><br>Year: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))

    fig.update_layout(
        title=f'ESG Score Trends - {company}',
        xaxis_title='Year',
        yaxis_title='Score',
        yaxis=dict(range=[0, 100]),
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        template=get_template(),
        paper_bgcolor=get_bg_color(),
        plot_bgcolor=get_bg_color(),
        font=dict(color=get_text_color()),
        hovermode='x unified'
    )

    return fig


def create_comparison_radar(df: pd.DataFrame, companies: list) -> go.Figure:
    """
    Create a radar chart comparing multiple companies.
    
    Args:
        df: DataFrame with ESG data
        companies: List of company names to compare
        
    Returns:
        Plotly figure
    """
    categories = ['Environmental', 'Social', 'Governance', 'Controversy', 'Board Independence']
    
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, company in enumerate(companies):
        company_data = df[df['company'] == company]
        if company_data.empty:
            continue
        latest = company_data[company_data['year'] == company_data['year'].max()].iloc[0]
        
        values = [
            latest['environmental_score'],
            latest['social_score'],
            latest['governance_score'],
            latest['controversy_score'],
            latest['board_independence_pct']
        ]
        values.append(values[0])  # Close the radar
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=company,
            line_color=colors[i % len(colors)],
            opacity=0.6
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Company Comparison - ESG Dimensions',
        height=500,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig


def create_sector_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Create a grouped bar chart comparing sectors.
    
    Args:
        df: DataFrame with ESG data
        
    Returns:
        Plotly figure
    """
    # Get latest year data and calculate sector averages
    latest_year = df['year'].max()
    sector_avg = df[df['year'] == latest_year].groupby('sector').agg({
        'environmental_score': 'mean',
        'social_score': 'mean',
        'governance_score': 'mean'
    }).round(1).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Environmental',
        x=sector_avg['sector'],
        y=sector_avg['environmental_score'],
        marker_color=COLORS['environmental']
    ))
    
    fig.add_trace(go.Bar(
        name='Social',
        x=sector_avg['sector'],
        y=sector_avg['social_score'],
        marker_color=COLORS['social']
    ))
    
    fig.add_trace(go.Bar(
        name='Governance',
        x=sector_avg['sector'],
        y=sector_avg['governance_score'],
        marker_color=COLORS['governance']
    ))
    
    fig.update_layout(
        title=f'Sector ESG Comparison ({latest_year})',
        xaxis_title='Sector',
        yaxis_title='Average Score',
        yaxis=dict(range=[0, 100]),
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=80, b=80)
    )
    
    return fig


def create_scatter_bubble(df: pd.DataFrame) -> go.Figure:
    """
    Create a bubble chart showing ESG vs Market Cap.
    
    Args:
        df: DataFrame with ESG data
        
    Returns:
        Plotly figure
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    
    fig = px.scatter(
        latest_df,
        x='environmental_score',
        y='social_score',
        size='market_cap_billion',
        color='sector',
        hover_name='company',
        color_discrete_map=SECTOR_COLORS,
        size_max=60
    )
    
    fig.update_layout(
        title='ESG Performance vs Market Cap',
        xaxis_title='Environmental Score',
        yaxis_title='Social Score',
        height=500,
        xaxis=dict(range=[30, 100]),
        yaxis=dict(range=[40, 90])
    )
    
    return fig


def create_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create a heatmap of ESG scores by company.
    
    Args:
        df: DataFrame with ESG data
        
    Returns:
        Plotly figure
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    latest_df = latest_df.sort_values('total_esg_score', ascending=True)
    
    heatmap_data = latest_df[['company', 'environmental_score', 'social_score', 'governance_score']].set_index('company')
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=['Environmental', 'Social', 'Governance'],
        y=heatmap_data.index,
        colorscale='RdYlGn',
        zmin=30,
        zmax=90,
        text=heatmap_data.values.round(1),
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='ESG Scores Heatmap',
        height=600,
        margin=dict(l=150, r=40, t=60, b=40)
    )
    
    return fig


def create_ranking_table(df: pd.DataFrame, metric: str = 'total_esg_score') -> go.Figure:
    """
    Create a table showing company rankings.
    
    Args:
        df: DataFrame with ESG data
        metric: Metric to rank by
        
    Returns:
        Plotly figure
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    ranked_df = latest_df.sort_values(metric, ascending=False).reset_index(drop=True)
    ranked_df['Rank'] = range(1, len(ranked_df) + 1)
    
    display_cols = ['Rank', 'company', 'sector', 'environmental_score', 'social_score', 
                    'governance_score', 'total_esg_score']
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Rank', 'Company', 'Sector', 'E', 'S', 'G', 'Total'],
            fill_color='#F97316',  # SmartDeploy Orange
            font=dict(color='white', size=12),
            align='left'
        ),
        cells=dict(
            values=[ranked_df[col] for col in display_cols],
            fill_color=[['white', '#f5f5f5'] * (len(ranked_df) // 2 + 1)],
            align='left',
            font=dict(size=11)
        )
    )])
    
    fig.update_layout(
        title='ESG Rankings',
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_carbon_emissions_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a bar chart of carbon emissions by company.
    
    Args:
        df: DataFrame with ESG data
        top_n: Number of companies to show
        
    Returns:
        Plotly figure
    """
    latest_df = df.loc[df.groupby('company')['year'].idxmax()]
    top_emitters = latest_df.nlargest(top_n, 'carbon_emissions_mt')
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_emitters['company'],
            y=top_emitters['carbon_emissions_mt'],
            marker_color=top_emitters['environmental_score'].apply(
                lambda x: COLORS['positive'] if x >= 60 else (
                    '#F59E0B' if x >= 40 else COLORS['negative']  # SmartDeploy Amber
                )
            ),
            text=top_emitters['carbon_emissions_mt'].round(1),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Carbon Emitters (MT)',
        xaxis_title='Company',
        yaxis_title='Carbon Emissions (Million Tonnes)',
        height=400,
        margin=dict(l=40, r=40, t=60, b=100),
        xaxis_tickangle=-45
    )
    
    return fig
