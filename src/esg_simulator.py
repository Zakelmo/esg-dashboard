"""
ESG Score Simulator - What-If Analysis Tool
Allows users to model different scenarios and predict future ESG scores
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ESGSimulator:
    """Simulate and predict ESG scores based on improvements"""

    def __init__(self):
        self.weights = {
            'environmental': 0.33,
            'social': 0.33,
            'governance': 0.34
        }

    def calculate_total_score(self, env_score, social_score, gov_score):
        """Calculate total ESG score from components"""
        return (env_score * self.weights['environmental'] +
                social_score * self.weights['social'] +
                gov_score * self.weights['governance'])

    def simulate_improvements(self, current_scores, improvements):
        """
        Simulate ESG score improvements

        Parameters:
        -----------
        current_scores : dict
            Dictionary with current E, S, G scores
        improvements : dict
            Dictionary with improvement percentages for each pillar

        Returns:
        --------
        dict
            Dictionary with current, projected, and delta scores
        """
        results = {
            'current': current_scores.copy(),
            'projected': {},
            'delta': {},
            'improvement_pct': improvements.copy()
        }

        # Calculate projected scores
        for pillar in ['environmental', 'social', 'governance']:
            current = current_scores.get(pillar, 0)
            improvement_pct = improvements.get(pillar, 0)

            # Calculate improvement (capped at 100)
            projected = min(100, current + (current * improvement_pct / 100))
            results['projected'][pillar] = projected
            results['delta'][pillar] = projected - current

        # Calculate total scores
        results['current']['total'] = self.calculate_total_score(
            current_scores.get('environmental', 0),
            current_scores.get('social', 0),
            current_scores.get('governance', 0)
        )

        results['projected']['total'] = self.calculate_total_score(
            results['projected']['environmental'],
            results['projected']['social'],
            results['projected']['governance']
        )

        results['delta']['total'] = results['projected']['total'] - results['current']['total']

        return results

    def predict_future_trajectory(self, current_scores, annual_improvement_rate, years=5):
        """
        Predict future ESG score trajectory

        Parameters:
        -----------
        current_scores : dict
            Current E, S, G scores
        annual_improvement_rate : dict
            Annual improvement rate for each pillar (%)
        years : int
            Number of years to project

        Returns:
        --------
        pd.DataFrame
            DataFrame with projected scores over time
        """
        projections = []

        for year in range(years + 1):
            year_data = {'year': year}

            for pillar in ['environmental', 'social', 'governance']:
                current = current_scores.get(pillar, 0)
                rate = annual_improvement_rate.get(pillar, 0)

                # Compound growth with diminishing returns as score approaches 100
                score = current
                for _ in range(year):
                    improvement = (100 - score) * (rate / 100) * 0.5  # Diminishing returns
                    score = min(100, score + improvement)

                year_data[pillar] = round(score, 1)

            year_data['total'] = self.calculate_total_score(
                year_data['environmental'],
                year_data['social'],
                year_data['governance']
            )

            projections.append(year_data)

        return pd.DataFrame(projections)

    def create_simulation_comparison_chart(self, simulation_results):
        """
        Create comparison chart for simulation results

        Parameters:
        -----------
        simulation_results : dict
            Results from simulate_improvements

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        pillars = ['environmental', 'social', 'governance', 'total']
        pillar_names = ['Environmental', 'Social', 'Governance', 'Total ESG']

        current_scores = [simulation_results['current'].get(p, 0) for p in pillars]
        projected_scores = [simulation_results['projected'].get(p, 0) for p in pillars]

        fig = go.Figure(data=[
            go.Bar(
                name='Current',
                x=pillar_names,
                y=current_scores,
                marker_color='#9E9E9E',
                text=[f"{v:.1f}" for v in current_scores],
                textposition='outside'
            ),
            go.Bar(
                name='Projected',
                x=pillar_names,
                y=projected_scores,
                marker_color='#4CAF50',
                text=[f"{v:.1f}" for v in projected_scores],
                textposition='outside'
            )
        ])

        fig.update_layout(
            title='Current vs Projected ESG Scores',
            xaxis_title='Pillar',
            yaxis_title='Score',
            barmode='group',
            height=400,
            template='plotly_white',
            yaxis=dict(range=[0, 110]),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    def create_trajectory_chart(self, trajectory_df):
        """
        Create trajectory projection chart

        Parameters:
        -----------
        trajectory_df : pd.DataFrame
            DataFrame with projected scores over time

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        fig = go.Figure()

        colors = {
            'environmental': '#2E7D32',
            'social': '#1565C0',
            'governance': '#7B1FA2',
            'total': '#424242'
        }

        for pillar in ['environmental', 'social', 'governance', 'total']:
            fig.add_trace(go.Scatter(
                x=trajectory_df['year'],
                y=trajectory_df[pillar],
                mode='lines+markers',
                name=pillar.capitalize(),
                line=dict(color=colors.get(pillar), width=3),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title='ESG Score Trajectory Projection',
            xaxis_title='Years from Now',
            yaxis_title='Score',
            height=450,
            template='plotly_white',
            hovermode='x unified',
            yaxis=dict(range=[0, 105]),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig

    def create_improvement_gauge(self, current_score, projected_score, pillar_name):
        """
        Create gauge chart showing improvement

        Parameters:
        -----------
        current_score : float
            Current score
        projected_score : float
            Projected score
        pillar_name : str
            Name of the pillar

        Returns:
        --------
        plotly.graph_objects.Figure
        """
        delta = projected_score - current_score

        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=projected_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{pillar_name}<br>Projected Score", 'font': {'size': 16}},
            delta={'reference': current_score, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#4CAF50"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 50], 'color': '#FFCDD2'},
                    {'range': [50, 70], 'color': '#FFF9C4'},
                    {'range': [70, 100], 'color': '#C8E6C9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': current_score
                }
            }
        ))

        fig.update_layout(
            height=250,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        return fig

    def calculate_impact_metrics(self, simulation_results):
        """
        Calculate impact metrics from simulation

        Parameters:
        -----------
        simulation_results : dict
            Results from simulate_improvements

        Returns:
        --------
        dict
            Dictionary with impact metrics
        """
        metrics = {}

        # Overall improvement
        metrics['total_improvement'] = simulation_results['delta']['total']

        # Best performing pillar
        deltas = {k: v for k, v in simulation_results['delta'].items() if k != 'total'}
        metrics['best_pillar'] = max(deltas, key=deltas.get)
        metrics['best_improvement'] = deltas[metrics['best_pillar']]

        # Rating change
        current_rating = self._score_to_rating(simulation_results['current']['total'])
        projected_rating = self._score_to_rating(simulation_results['projected']['total'])
        metrics['current_rating'] = current_rating
        metrics['projected_rating'] = projected_rating
        metrics['rating_change'] = projected_rating != current_rating

        # Percentile improvement (approximate)
        current_percentile = min(99, int(simulation_results['current']['total']))
        projected_percentile = min(99, int(simulation_results['projected']['total']))
        metrics['percentile_gain'] = projected_percentile - current_percentile

        return metrics

    def _score_to_rating(self, score):
        """Convert score to ESG rating"""
        if score >= 80:
            return 'AAA'
        elif score >= 75:
            return 'AA'
        elif score >= 70:
            return 'A'
        elif score >= 65:
            return 'BBB'
        elif score >= 60:
            return 'BB'
        elif score >= 55:
            return 'B'
        elif score >= 50:
            return 'CCC'
        elif score >= 40:
            return 'CC'
        else:
            return 'C'

    def generate_recommendations(self, current_scores, target_score=80):
        """
        Generate recommendations to reach target score

        Parameters:
        -----------
        current_scores : dict
            Current E, S, G scores
        target_score : float
            Target total ESG score

        Returns:
        --------
        dict
            Dictionary with recommendations for each pillar
        """
        recommendations = {}

        current_total = self.calculate_total_score(
            current_scores.get('environmental', 0),
            current_scores.get('social', 0),
            current_scores.get('governance', 0)
        )

        if current_total >= target_score:
            recommendations['message'] = f"Current score ({current_total:.1f}) already meets or exceeds target ({target_score})!"
            return recommendations

        gap = target_score - current_total

        # Calculate required improvements for each pillar
        for pillar in ['environmental', 'social', 'governance']:
            current = current_scores.get(pillar, 0)
            weight = self.weights[pillar]

            # Calculate points needed from this pillar to close the gap
            points_needed = gap / 3  # Distribute evenly
            score_increase = points_needed / weight

            recommendations[pillar] = {
                'current': current,
                'target': min(100, current + score_increase),
                'increase_needed': score_increase,
                'increase_pct': (score_increase / current * 100) if current > 0 else 0
            }

        recommendations['gap'] = gap
        recommendations['current_total'] = current_total
        recommendations['target_total'] = target_score

        return recommendations

    def benchmark_simulation(self, company_scores, sector_avg_scores):
        """
        Simulate improvements needed to match sector average

        Parameters:
        -----------
        company_scores : dict
            Company's current scores
        sector_avg_scores : dict
            Sector average scores

        Returns:
        --------
        dict
            Simulation results to match sector performance
        """
        improvements = {}

        for pillar in ['environmental', 'social', 'governance']:
            current = company_scores.get(pillar, 0)
            target = sector_avg_scores.get(pillar, 0)

            if current < target:
                improvement_needed = ((target - current) / current * 100) if current > 0 else 0
                improvements[pillar] = improvement_needed
            else:
                improvements[pillar] = 0

        # Run simulation with calculated improvements
        return self.simulate_improvements(company_scores, improvements)
