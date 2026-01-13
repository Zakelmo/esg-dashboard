"""
Peer Benchmarking Module
Advanced comparison and benchmarking analysis for ESG performance
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


class PeerBenchmarking:
    """Advanced peer benchmarking and comparison analytics"""

    def __init__(self, data):
        """
        Initialize with ESG data

        Parameters:
        -----------
        data : pd.DataFrame
            DataFrame with ESG data
        """
        self.data = data

    def create_benchmark_matrix(self, companies, metrics=None):
        """
        Create comprehensive benchmark comparison matrix

        Parameters:
        -----------
        companies : list
            List of company names to compare
        metrics : list, optional
            List of metrics to include. If None, uses default metrics.

        Returns:
        --------
        pd.DataFrame
            Benchmark matrix with scores and rankings
        """
        if metrics is None:
            metrics = [
                'total_esg_score',
                'environmental_score',
                'social_score',
                'governance_score',
                'carbon_emissions_mt',
                'diversity_score',
                'board_independence_pct'
            ]

        # Filter data for selected companies (latest year)
        latest_year = self.data['year'].max()
        company_data = self.data[
            (self.data['company'].isin(companies)) &
            (self.data['year'] == latest_year)
        ].copy()

        if company_data.empty:
            return pd.DataFrame()

        # Create matrix
        matrix = []
        for _, row in company_data.iterrows():
            company_metrics = {'Company': row['company']}

            for metric in metrics:
                if metric in row:
                    value = row[metric]
                    company_metrics[metric] = value

                    # Calculate percentile rank
                    all_values = self.data[self.data['year'] == latest_year][metric].dropna()
                    if len(all_values) > 0:
                        percentile = (all_values < value).sum() / len(all_values) * 100
                        company_metrics[f'{metric}_percentile'] = percentile

            matrix.append(company_metrics)

        return pd.DataFrame(matrix)

    def create_peer_comparison_heatmap(self, companies, metrics=None):
        """
        Create heatmap comparing companies across metrics

        Parameters:
        -----------
        companies : list
            List of company names
        metrics : list, optional
            Metrics to display

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        if metrics is None:
            metrics = [
                'total_esg_score',
                'environmental_score',
                'social_score',
                'governance_score'
            ]

        matrix = self.create_benchmark_matrix(companies, metrics)

        if matrix.empty:
            return go.Figure()

        # Prepare data for heatmap
        heatmap_data = matrix[['Company'] + metrics].set_index('Company')

        # Normalize scores to 0-100 scale for better visualization
        heatmap_normalized = heatmap_data.copy()

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_normalized.values,
            x=[self._format_metric_name(m) for m in heatmap_normalized.columns],
            y=heatmap_normalized.index,
            colorscale='RdYlGn',
            text=heatmap_normalized.values.round(1),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Score")
        ))

        fig.update_layout(
            title='Peer Benchmark Comparison Matrix',
            xaxis_title='Metrics',
            yaxis_title='Companies',
            height=max(400, len(companies) * 80),
            template='plotly_white'
        )

        return fig

    def create_percentile_ranking_chart(self, company, sector=None):
        """
        Create percentile ranking visualization for a company

        Parameters:
        -----------
        company : str
            Company name
        sector : str, optional
            Sector for comparison. If None, compares against all companies.

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        latest_year = self.data['year'].max()
        company_data = self.data[
            (self.data['company'] == company) &
            (self.data['year'] == latest_year)
        ]

        if company_data.empty:
            return go.Figure()

        company_data = company_data.iloc[0]

        # Comparison dataset
        if sector:
            comparison_data = self.data[
                (self.data['sector'] == sector) &
                (self.data['year'] == latest_year)
            ]
        else:
            comparison_data = self.data[self.data['year'] == latest_year]

        metrics = {
            'Total ESG': 'total_esg_score',
            'Environmental': 'environmental_score',
            'Social': 'social_score',
            'Governance': 'governance_score',
            'Diversity': 'diversity_score',
            'Board Independence': 'board_independence_pct'
        }

        percentiles = []
        metric_names = []

        for name, metric in metrics.items():
            if metric in company_data and pd.notna(company_data[metric]):
                value = company_data[metric]
                all_values = comparison_data[metric].dropna()

                if len(all_values) > 0:
                    percentile = (all_values < value).sum() / len(all_values) * 100
                    percentiles.append(percentile)
                    metric_names.append(name)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=percentiles,
            y=metric_names,
            orientation='h',
            marker=dict(
                color=percentiles,
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Percentile")
            ),
            text=[f"{p:.0f}%" for p in percentiles],
            textposition='outside'
        ))

        comparison_label = f"vs {sector} Sector" if sector else "vs All Companies"
        fig.update_layout(
            title=f'{company} - Percentile Rankings ({comparison_label})',
            xaxis_title='Percentile',
            yaxis_title='Metric',
            height=400,
            template='plotly_white',
            xaxis=dict(range=[0, 110])
        )

        return fig

    def create_spider_comparison(self, companies, metrics=None):
        """
        Create spider/radar chart comparing multiple companies

        Parameters:
        -----------
        companies : list
            List of company names (max 5)
        metrics : list, optional
            Metrics to display

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        if metrics is None:
            metrics = [
                'environmental_score',
                'social_score',
                'governance_score',
                'diversity_score',
                'board_independence_pct'
            ]

        latest_year = self.data['year'].max()
        company_data = self.data[
            (self.data['company'].isin(companies)) &
            (self.data['year'] == latest_year)
        ]

        fig = go.Figure()

        colors = ['#2196F3', '#FF9800', '#4CAF50', '#9C27B0', '#F44336']

        for idx, company in enumerate(companies):
            c_data = company_data[company_data['company'] == company]

            if c_data.empty:
                continue

            c_data = c_data.iloc[0]

            values = []
            for metric in metrics:
                if metric in c_data and pd.notna(c_data[metric]):
                    values.append(c_data[metric])
                else:
                    values.append(0)

            # Close the radar chart
            values.append(values[0])

            metric_labels = [self._format_metric_name(m) for m in metrics]
            metric_labels.append(metric_labels[0])

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=metric_labels,
                fill='toself',
                name=company,
                line=dict(color=colors[idx % len(colors)], width=2)
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title='Multi-Company ESG Comparison',
            height=500,
            template='plotly_white'
        )

        return fig

    def calculate_peer_statistics(self, company, sector):
        """
        Calculate comprehensive peer statistics

        Parameters:
        -----------
        company : str
            Company name
        sector : str
            Sector name

        Returns:
        --------
        dict
            Dictionary with peer statistics
        """
        latest_year = self.data['year'].max()

        # Get company data
        company_data = self.data[
            (self.data['company'] == company) &
            (self.data['year'] == latest_year)
        ]

        # Get sector data
        sector_data = self.data[
            (self.data['sector'] == sector) &
            (self.data['year'] == latest_year)
        ]

        if company_data.empty or sector_data.empty:
            return {}

        company_data = company_data.iloc[0]

        stats = {}

        metrics = {
            'total_esg_score': 'Total ESG',
            'environmental_score': 'Environmental',
            'social_score': 'Social',
            'governance_score': 'Governance'
        }

        for metric, name in metrics.items():
            company_value = company_data[metric]
            sector_mean = sector_data[metric].mean()
            sector_median = sector_data[metric].median()
            sector_std = sector_data[metric].std()

            # Calculate percentile
            percentile = (sector_data[metric] < company_value).sum() / len(sector_data) * 100

            # Calculate z-score
            z_score = (company_value - sector_mean) / sector_std if sector_std > 0 else 0

            stats[metric] = {
                'name': name,
                'company_value': company_value,
                'sector_mean': sector_mean,
                'sector_median': sector_median,
                'sector_std': sector_std,
                'percentile': percentile,
                'z_score': z_score,
                'vs_mean': company_value - sector_mean,
                'vs_median': company_value - sector_median
            }

        return stats

    def create_quartile_analysis(self, sector, metric='total_esg_score'):
        """
        Create quartile analysis for a sector

        Parameters:
        -----------
        sector : str
            Sector name
        metric : str
            Metric to analyze

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        latest_year = self.data['year'].max()
        sector_data = self.data[
            (self.data['sector'] == sector) &
            (self.data['year'] == latest_year)
        ].copy()

        if sector_data.empty:
            return go.Figure()

        # Calculate quartiles
        q1 = sector_data[metric].quantile(0.25)
        q2 = sector_data[metric].quantile(0.5)
        q3 = sector_data[metric].quantile(0.75)

        # Assign quartiles
        sector_data['quartile'] = pd.cut(
            sector_data[metric],
            bins=[0, q1, q2, q3, 100],
            labels=['Q1 (Bottom 25%)', 'Q2', 'Q3', 'Q4 (Top 25%)']
        )

        # Count companies in each quartile
        quartile_counts = sector_data['quartile'].value_counts().sort_index()

        fig = go.Figure(data=[
            go.Bar(
                x=quartile_counts.index.astype(str),
                y=quartile_counts.values,
                marker_color=['#F44336', '#FF9800', '#FFC107', '#4CAF50'],
                text=quartile_counts.values,
                textposition='outside'
            )
        ])

        fig.update_layout(
            title=f'{sector} Sector - Quartile Distribution ({self._format_metric_name(metric)})',
            xaxis_title='Quartile',
            yaxis_title='Number of Companies',
            height=400,
            template='plotly_white',
            showlegend=False
        )

        return fig

    def generate_competitive_insights(self, company, sector):
        """
        Generate competitive insights and recommendations

        Parameters:
        -----------
        company : str
            Company name
        sector : str
            Sector name

        Returns:
        --------
        dict
            Dictionary with insights and recommendations
        """
        stats = self.calculate_peer_statistics(company, sector)

        if not stats:
            return {}

        insights = {
            'strengths': [],
            'weaknesses': [],
            'opportunities': [],
            'recommendations': []
        }

        for metric, data in stats.items():
            percentile = data['percentile']
            vs_mean = data['vs_mean']

            # Identify strengths (top 25%)
            if percentile >= 75:
                insights['strengths'].append(
                    f"{data['name']}: Top quartile performance ({percentile:.0f}th percentile)"
                )

            # Identify weaknesses (bottom 25%)
            elif percentile <= 25:
                insights['weaknesses'].append(
                    f"{data['name']}: Below peer average (only {percentile:.0f}th percentile)"
                )

                # Generate recommendations
                gap = abs(vs_mean)
                insights['recommendations'].append(
                    f"Improve {data['name']} score by {gap:.1f} points to reach sector average"
                )

            # Opportunities (between 25-50%)
            elif 25 < percentile < 50:
                insights['opportunities'].append(
                    f"{data['name']}: Room for improvement to reach sector median"
                )

        return insights

    def _format_metric_name(self, metric):
        """Format metric name for display"""
        name_map = {
            'total_esg_score': 'Total ESG',
            'environmental_score': 'Environmental',
            'social_score': 'Social',
            'governance_score': 'Governance',
            'carbon_emissions_mt': 'Carbon Emissions',
            'diversity_score': 'Diversity',
            'board_independence_pct': 'Board Independence',
            'employee_turnover_pct': 'Employee Turnover',
            'safety_incidents': 'Safety Incidents'
        }
        return name_map.get(metric, metric.replace('_', ' ').title())

    def create_trend_comparison(self, companies, metric='total_esg_score'):
        """
        Create trend comparison chart for multiple companies

        Parameters:
        -----------
        companies : list
            List of company names
        metric : str
            Metric to compare

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        fig = go.Figure()

        colors = ['#2196F3', '#FF9800', '#4CAF50', '#9C27B0', '#F44336']

        for idx, company in enumerate(companies):
            company_data = self.data[self.data['company'] == company].sort_values('year')

            if company_data.empty:
                continue

            fig.add_trace(go.Scatter(
                x=company_data['year'],
                y=company_data[metric],
                mode='lines+markers',
                name=company,
                line=dict(color=colors[idx % len(colors)], width=3),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title=f'Peer Comparison: {self._format_metric_name(metric)} Trends',
            xaxis_title='Year',
            yaxis_title=self._format_metric_name(metric),
            height=450,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig
