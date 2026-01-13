"""
ESG Company Analyzer Dashboard - Enhanced Version
A comprehensive ESG analytics dashboard with advanced features built with Streamlit.

Author: Zakaria El Morabit
Enhanced by: Claude
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import base64
from io import BytesIO

# Import custom modules
from src.data_loader import (
    load_esg_data, get_companies, get_sectors, get_countries,
    get_years, filter_data, get_latest_data, get_esg_rating
)
from src.esg_analyzer import (
    calculate_company_metrics, get_top_performers, get_bottom_performers,
    calculate_sector_benchmark, identify_risks, calculate_improvement_areas,
    generate_summary_stats
)
from src.visualizations import (
    create_esg_gauge, create_esg_breakdown_chart, create_trend_chart,
    create_comparison_radar, create_sector_comparison, create_scatter_bubble,
    create_heatmap, create_ranking_table, create_carbon_emissions_chart,
    set_theme, get_bg_color, get_text_color
)
# Import new enhanced modules
from src.pdf_generator import ESGPDFReporter
from src.esg_simulator import ESGSimulator
from src.peer_benchmark import PeerBenchmarking


# Page configuration
st.set_page_config(
    page_title="ESG Company Analyzer",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'


# Cache data loading
@st.cache_data
def get_data():
    return load_esg_data()


def apply_theme_styles():
    """Apply theme-specific styles dynamically"""
    if st.session_state.theme == 'dark':
        theme_css = """
        <style>
            [data-testid="stAppViewContainer"] {
                background-color: #0f1419;
                color: #e6e6e6;
            }
            [data-testid="stHeader"] {
                background-color: #1a1f2e;
            }
            [data-testid="stSidebar"] {
                background-color: #1a1f2e;
            }
            .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
                color: #e6e6e6 !important;
            }
            div[data-testid="stMetricValue"] {
                color: #e6e6e6;
            }
        </style>
        """
        st.markdown(theme_css, unsafe_allow_html=True)
        set_theme('dark')
    else:
        set_theme('light')


def create_download_link(pdf_bytes, filename):
    """Create a download link for PDF"""
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="pdf-export-btn">Download PDF Report</a>'
    return href


# Main application
def main():
    # Load data
    df = get_data()

    # Apply theme
    apply_theme_styles()
    
    # Header
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1a237e 0%, #0d47a1 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">ESG Company Analyzer Dashboard</h1>
        <p style="color: #bbdefb; margin: 5px 0 0 0;">
            Analyze Environmental, Social & Governance performance across companies and sectors
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")

        # Sector filter
        sectors = get_sectors(df)
        selected_sectors = st.multiselect(
            "Select Sectors",
            options=sectors,
            default=sectors
        )
        
        # Country filter
        countries = get_countries(df)
        selected_countries = st.multiselect(
            "Select Countries",
            options=countries,
            default=countries
        )
        
        # Year filter
        years = get_years(df)
        year_range = st.select_slider(
            "Select Year Range",
            options=years,
            value=(min(years), max(years))
        )
        selected_years = [y for y in years if year_range[0] <= y <= year_range[1]]
        
        st.divider()
        
        # About section
        st.markdown("""
        ### About
        This dashboard analyzes ESG (Environmental, Social, Governance) 
        performance metrics for companies across different sectors.
        
        **Data includes:**
        - ESG scores and ratings
        - Carbon emissions
        - Diversity metrics
        - Governance indicators
        
        ---
        **Built by:** Zakaria El Morabit  
        **Contact:** elmorabitzakaria@gmail.com
        """)
    
    # Filter data
    filtered_df = filter_data(
        df,
        sectors=selected_sectors,
        countries=selected_countries,
        years=selected_years
    )
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Overview",
        "🏢 Company Analysis",
        "📈 Trends & Comparison",
        "⚠️ Risk Assessment",
        "📋 Rankings",
        "🎯 ESG Simulator",
        "🔍 Peer Benchmarking",
        "📄 PDF Reports"
    ])
    
    # Tab 1: Overview
    with tab1:
        st.header("Market Overview")
        
        # Summary statistics
        stats = generate_summary_stats(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Companies Analyzed",
                value=stats['total_companies']
            )
        with col2:
            st.metric(
                label="Sectors Covered",
                value=stats['total_sectors']
            )
        with col3:
            st.metric(
                label="Average ESG Score",
                value=f"{stats['avg_esg_score']:.1f}"
            )
        with col4:
            st.metric(
                label="Top Performer",
                value=stats['top_performer'],
                delta=f"Score: {stats['top_score']:.1f}"
            )
        
        st.divider()
        
        # Charts row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sector ESG Comparison")
            sector_chart = create_sector_comparison(filtered_df)
            st.plotly_chart(sector_chart, use_container_width=True)
        
        with col2:
            st.subheader("ESG vs Market Cap")
            bubble_chart = create_scatter_bubble(filtered_df)
            st.plotly_chart(bubble_chart, use_container_width=True)
        
        # Charts row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("ESG Scores Heatmap")
            heatmap = create_heatmap(filtered_df)
            st.plotly_chart(heatmap, use_container_width=True)
        
        with col2:
            st.subheader("Top Carbon Emitters")
            carbon_chart = create_carbon_emissions_chart(filtered_df)
            st.plotly_chart(carbon_chart, use_container_width=True)
    
    # Tab 2: Company Analysis
    with tab2:
        st.header("Company Deep Dive")
        
        # Company selector
        companies = get_companies(filtered_df)
        selected_company = st.selectbox(
            "Select a Company",
            options=companies,
            index=0 if companies else None
        )
        
        if selected_company:
            metrics = calculate_company_metrics(filtered_df, selected_company)
            
            # Company header
            rating, rating_color = get_esg_rating(metrics['total_esg_score'])
            
            st.markdown(f"""
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
                <h2 style="margin: 0;">{selected_company}</h2>
                <p style="color: #666; margin: 5px 0;">
                    <strong>Sector:</strong> {metrics['sector']} | 
                    <strong>Country:</strong> {metrics['country']} |
                    <strong>Market Cap:</strong> ${metrics['market_cap']:.0f}B
                </p>
                <span style="background-color: {rating_color}; color: white; padding: 5px 15px; 
                            border-radius: 20px; font-weight: bold;">
                    ESG Rating: {rating}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Score gauges
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                gauge = create_esg_gauge(metrics['total_esg_score'], "Total ESG")
                st.plotly_chart(gauge, use_container_width=True)
            
            with col2:
                gauge = create_esg_gauge(metrics['environmental_score'], "Environmental", "#2E7D32")
                st.plotly_chart(gauge, use_container_width=True)
            
            with col3:
                gauge = create_esg_gauge(metrics['social_score'], "Social", "#1565C0")
                st.plotly_chart(gauge, use_container_width=True)
            
            with col4:
                gauge = create_esg_gauge(metrics['governance_score'], "Governance", "#7B1FA2")
                st.plotly_chart(gauge, use_container_width=True)
            
            # YoY Changes
            st.subheader("Year-over-Year Changes")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                delta = metrics['total_trend']
                st.metric("Total ESG", f"{metrics['total_esg_score']:.1f}", f"{delta:+.1f}")
            with col2:
                delta = metrics['e_trend']
                st.metric("Environmental", f"{metrics['environmental_score']:.1f}", f"{delta:+.1f}")
            with col3:
                delta = metrics['s_trend']
                st.metric("Social", f"{metrics['social_score']:.1f}", f"{delta:+.1f}")
            with col4:
                delta = metrics['g_trend']
                st.metric("Governance", f"{metrics['governance_score']:.1f}", f"{delta:+.1f}")
            
            # Sector benchmark
            st.subheader("Sector Benchmark")
            benchmark = calculate_sector_benchmark(filtered_df, selected_company)
            
            if benchmark:
                col1, col2 = st.columns(2)
                
                with col1:
                    benchmark_data = pd.DataFrame({
                        'Dimension': ['Environmental', 'Social', 'Governance', 'Total ESG'],
                        'Company': [benchmark['company_e'], benchmark['company_s'], 
                                   benchmark['company_g'], benchmark['company_total']],
                        'Sector Avg': [benchmark['sector_e'], benchmark['sector_s'],
                                      benchmark['sector_g'], benchmark['sector_total']]
                    })
                    benchmark_data['Difference'] = benchmark_data['Company'] - benchmark_data['Sector Avg']
                    benchmark_data = benchmark_data.round(1)
                    
                    st.dataframe(
                        benchmark_data,
                        use_container_width=True,
                        hide_index=True
                    )
                
                with col2:
                    # Improvement areas
                    improvements = calculate_improvement_areas(filtered_df, selected_company)
                    if improvements:
                        st.markdown("**Areas for Improvement:**")
                        for imp in improvements:
                            st.markdown(f"""
                            - **{imp['area']}** (Gap: {imp['gap']} pts)  
                              {imp['recommendation']}
                            """)
                    else:
                        st.success("✅ Company performs above sector average in all dimensions!")
    
    # Tab 3: Trends & Comparison
    with tab3:
        st.header("Trends & Comparison Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Company selection for trends
            companies = get_companies(filtered_df)
            trend_company = st.selectbox(
                "Select Company for Trend Analysis",
                options=companies,
                key="trend_company"
            )
            
            # Multi-company comparison
            st.markdown("---")
            compare_companies = st.multiselect(
                "Select Companies to Compare (max 5)",
                options=companies,
                default=companies[:3] if len(companies) >= 3 else companies,
                max_selections=5
            )
        
        with col2:
            if trend_company:
                trend_chart = create_trend_chart(filtered_df, trend_company)
                st.plotly_chart(trend_chart, use_container_width=True)
        
        # Comparison radar chart
        if compare_companies:
            st.subheader("Multi-Company Comparison")
            radar_chart = create_comparison_radar(filtered_df, compare_companies)
            st.plotly_chart(radar_chart, use_container_width=True)
    
    # Tab 4: Risk Assessment
    with tab4:
        st.header("Risk Assessment")
        
        companies = get_companies(filtered_df)
        risk_company = st.selectbox(
            "Select Company for Risk Analysis",
            options=companies,
            key="risk_company"
        )
        
        if risk_company:
            risks = identify_risks(filtered_df, risk_company)
            
            if risks:
                st.markdown(f"### Identified Risks for {risk_company}")
                
                # Group risks by severity
                high_risks = [r for r in risks if r['severity'] == 'High']
                medium_risks = [r for r in risks if r['severity'] == 'Medium']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔴 High Severity Risks")
                    if high_risks:
                        for risk in high_risks:
                            st.error(f"**{risk['category']}:** {risk['description']}")
                    else:
                        st.success("No high severity risks identified")
                
                with col2:
                    st.markdown("#### 🟡 Medium Severity Risks")
                    if medium_risks:
                        for risk in medium_risks:
                            st.warning(f"**{risk['category']}:** {risk['description']}")
                    else:
                        st.success("No medium severity risks identified")
                
                # Risk summary
                st.markdown("---")
                st.markdown("### Risk Summary")
                
                risk_summary = pd.DataFrame({
                    'Category': ['Environmental', 'Social', 'Governance', 'Reputation'],
                    'Risk Count': [
                        len([r for r in risks if r['category'] == 'Environmental']),
                        len([r for r in risks if r['category'] == 'Social']),
                        len([r for r in risks if r['category'] == 'Governance']),
                        len([r for r in risks if r['category'] == 'Reputation'])
                    ]
                })
                
                st.bar_chart(risk_summary.set_index('Category'))
            else:
                st.success(f"✅ No significant ESG risks identified for {risk_company}")
    
    # Tab 5: Rankings
    with tab5:
        st.header("ESG Rankings")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            ranking_metric = st.radio(
                "Rank by",
                options=['Total ESG Score', 'Environmental', 'Social', 'Governance'],
                index=0
            )
            
            metric_map = {
                'Total ESG Score': 'total_esg_score',
                'Environmental': 'environmental_score',
                'Social': 'social_score',
                'Governance': 'governance_score'
            }
        
        with col2:
            ranking_table = create_ranking_table(filtered_df, metric_map[ranking_metric])
            st.plotly_chart(ranking_table, use_container_width=True)
        
        # Top and bottom performers
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏆 Top 5 Performers")
            top_df = get_top_performers(filtered_df, n=5, metric=metric_map[ranking_metric])
            st.dataframe(top_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("⚠️ Bottom 5 Performers")
            bottom_df = get_bottom_performers(filtered_df, n=5, metric=metric_map[ranking_metric])
            st.dataframe(bottom_df, use_container_width=True, hide_index=True)

    # Tab 6: ESG Score Simulator
    with tab6:
        st.header("🎯 ESG Score Simulator")
        st.markdown("Model what-if scenarios and project future ESG scores based on improvements.")

        simulator = ESGSimulator()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Select Company")
            sim_company = st.selectbox(
                "Company to simulate",
                options=get_companies(filtered_df),
                key="sim_company"
            )

            if sim_company:
                company_data = filtered_df[filtered_df['company'] == sim_company]
                if not company_data.empty:
                    latest = company_data[company_data['year'] == company_data['year'].max()].iloc[0]

                    st.subheader("Current Scores")
                    st.metric("Environmental", f"{latest['environmental_score']:.1f}")
                    st.metric("Social", f"{latest['social_score']:.1f}")
                    st.metric("Governance", f"{latest['governance_score']:.1f}")
                    st.metric("Total ESG", f"{latest['total_esg_score']:.1f}")

                    st.divider()
                    st.subheader("Improvement Targets (%)")

                    env_improvement = st.slider("Environmental Improvement", 0, 50, 10, key="env_imp")
                    social_improvement = st.slider("Social Improvement", 0, 50, 10, key="soc_imp")
                    gov_improvement = st.slider("Governance Improvement", 0, 50, 10, key="gov_imp")

                    current_scores = {
                        'environmental': latest['environmental_score'],
                        'social': latest['social_score'],
                        'governance': latest['governance_score']
                    }

                    improvements = {
                        'environmental': env_improvement,
                        'social': social_improvement,
                        'governance': gov_improvement
                    }

                    simulation_results = simulator.simulate_improvements(current_scores, improvements)

        with col2:
            if sim_company and not company_data.empty:
                st.subheader("Simulation Results")

                # Comparison chart
                comparison_fig = simulator.create_simulation_comparison_chart(simulation_results)
                st.plotly_chart(comparison_fig, use_container_width=True)

                # Impact metrics
                st.subheader("Impact Analysis")
                metrics_data = simulator.calculate_impact_metrics(simulation_results)

                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric(
                        "Total Score Improvement",
                        f"+{metrics_data['total_improvement']:.1f}",
                        f"{simulation_results['projected']['total']:.1f}"
                    )
                with metric_col2:
                    st.metric(
                        "Current Rating",
                        metrics_data['current_rating']
                    )
                with metric_col3:
                    st.metric(
                        "Projected Rating",
                        metrics_data['projected_rating'],
                        delta="Upgrade" if metrics_data['rating_change'] else "No change"
                    )

                st.divider()

                # Future trajectory
                st.subheader("5-Year Projection")
                st.markdown("Projected scores assuming continuous annual improvements:")

                annual_rates = {
                    'environmental': env_improvement / 5,
                    'social': social_improvement / 5,
                    'governance': gov_improvement / 5
                }

                trajectory = simulator.predict_future_trajectory(current_scores, annual_rates, years=5)
                trajectory_fig = simulator.create_trajectory_chart(trajectory)
                st.plotly_chart(trajectory_fig, use_container_width=True)

    # Tab 7: Peer Benchmarking
    with tab7:
        st.header("🔍 Advanced Peer Benchmarking")
        st.markdown("Compare companies against industry peers with detailed analytics.")

        peer_benchmark = PeerBenchmarking(filtered_df)

        bench_col1, bench_col2 = st.columns([1, 2])

        with bench_col1:
            st.subheader("Configuration")

            bench_company = st.selectbox(
                "Select Company",
                options=get_companies(filtered_df),
                key="bench_company"
            )

            if bench_company:
                company_info = filtered_df[filtered_df['company'] == bench_company]
                if not company_info.empty:
                    sector = company_info.iloc[0]['sector']
                    st.info(f"**Sector:** {sector}")

                    bench_type = st.radio(
                        "Comparison Type",
                        ["Sector Benchmarking", "Custom Peer Group", "Percentile Analysis"]
                    )

                    if bench_type == "Custom Peer Group":
                        peer_companies = st.multiselect(
                            "Select peers to compare",
                            options=[c for c in get_companies(filtered_df) if c != bench_company],
                            default=[],
                            max_selections=4
                        )
                        selected_peers = [bench_company] + peer_companies
                    else:
                        selected_peers = None

        with bench_col2:
            if bench_company and not company_info.empty:
                if bench_type == "Sector Benchmarking":
                    st.subheader(f"Benchmarking vs {sector} Sector")

                    # Peer statistics
                    peer_stats = peer_benchmark.calculate_peer_statistics(bench_company, sector)

                    if peer_stats:
                        stats_df = pd.DataFrame([
                            {
                                'Metric': data['name'],
                                'Company': f"{data['company_value']:.1f}",
                                'Sector Avg': f"{data['sector_mean']:.1f}",
                                'Difference': f"{data['vs_mean']:+.1f}",
                                'Percentile': f"{data['percentile']:.0f}%"
                            }
                            for data in peer_stats.values()
                        ])
                        st.dataframe(stats_df, use_container_width=True, hide_index=True)

                    # Percentile chart
                    percentile_fig = peer_benchmark.create_percentile_ranking_chart(bench_company, sector)
                    st.plotly_chart(percentile_fig, use_container_width=True)

                    # Competitive insights
                    st.subheader("Competitive Insights")
                    insights = peer_benchmark.generate_competitive_insights(bench_company, sector)

                    if insights.get('strengths'):
                        st.success("**Strengths:**")
                        for strength in insights['strengths']:
                            st.write(f"✓ {strength}")

                    if insights.get('weaknesses'):
                        st.warning("**Areas for Improvement:**")
                        for weakness in insights['weaknesses']:
                            st.write(f"• {weakness}")

                elif bench_type == "Custom Peer Group" and selected_peers:
                    st.subheader("Custom Peer Group Comparison")

                    # Heatmap
                    heatmap_fig = peer_benchmark.create_peer_comparison_heatmap(selected_peers)
                    st.plotly_chart(heatmap_fig, use_container_width=True)

                    # Spider chart
                    spider_fig = peer_benchmark.create_spider_comparison(selected_peers)
                    st.plotly_chart(spider_fig, use_container_width=True)

                elif bench_type == "Percentile Analysis":
                    st.subheader("Percentile Analysis")

                    percentile_fig = peer_benchmark.create_percentile_ranking_chart(bench_company, sector)
                    st.plotly_chart(percentile_fig, use_container_width=True)

                    # Quartile analysis
                    st.subheader("Sector Quartile Distribution")
                    quartile_fig = peer_benchmark.create_quartile_analysis(sector)
                    st.plotly_chart(quartile_fig, use_container_width=True)

    # Tab 8: PDF Reports
    with tab8:
        st.header("📄 Generate PDF Reports")
        st.markdown("Export comprehensive ESG reports in PDF format for presentations and documentation.")

        pdf_reporter = ESGPDFReporter()

        report_type = st.radio(
            "Report Type",
            ["Company Report", "Portfolio Report"],
            horizontal=True
        )

        if report_type == "Company Report":
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("Select Company")
                pdf_company = st.selectbox(
                    "Company for report",
                    options=get_companies(filtered_df),
                    key="pdf_company"
                )

                if pdf_company:
                    company_data = filtered_df[filtered_df['company'] == pdf_company]
                    if not company_data.empty:
                        latest = company_data[company_data['year'] == company_data['year'].max()].iloc[0]

                        # Show preview
                        st.subheader("Report Preview")
                        st.write(f"**Company:** {pdf_company}")
                        st.write(f"**Sector:** {latest['sector']}")
                        st.write(f"**ESG Score:** {latest['total_esg_score']:.1f}")

                        # Get rating and color
                        rating_tuple = get_esg_rating(latest['total_esg_score'])
                        rating_text = rating_tuple[0]
                        rating_color = rating_tuple[1]
                        st.markdown(f"**Rating:** <span style='color: {rating_color}; font-weight: bold; font-size: 1.2em;'>{rating_text}</span>", unsafe_allow_html=True)

                        if st.button("📥 Generate PDF Report", use_container_width=True):
                            with st.spinner("Generating PDF report..."):
                                # Prepare company data for PDF
                                report_data = {
                                    'company': pdf_company,
                                    'sector': latest['sector'],
                                    'country': latest['country'],
                                    'year': int(latest['year']),
                                    'market_cap_billion': latest['market_cap_billion'],
                                    'total_esg_score': latest['total_esg_score'],
                                    'environmental_score': latest['environmental_score'],
                                    'social_score': latest['social_score'],
                                    'governance_score': latest['governance_score'],
                                    'esg_rating': get_esg_rating(latest['total_esg_score']),
                                    'environmental_metrics': {
                                        'carbon_emissions_mt': latest['carbon_emissions_mt'],
                                        'energy_intensity': latest['energy_intensity'],
                                        'water_usage_m3': latest['water_usage_m3'],
                                        'waste_recycled_pct': latest['waste_recycled_pct']
                                    },
                                    'social_metrics': {
                                        'employee_turnover_pct': latest['employee_turnover_pct'],
                                        'diversity_score': latest['diversity_score'],
                                        'safety_incidents': latest['safety_incidents'],
                                        'community_investment_usd': latest['community_investment_usd']
                                    },
                                    'governance_metrics': {
                                        'board_independence_pct': latest['board_independence_pct'],
                                        'executive_pay_ratio': latest['executive_pay_ratio'],
                                        'controversy_score': latest['controversy_score']
                                    },
                                    'risks': identify_risks(filtered_df, pdf_company),
                                    'recommendations': calculate_improvement_areas(
                                        filtered_df,
                                        pdf_company
                                    )
                                }

                                pdf_bytes = pdf_reporter.generate_company_report(
                                    report_data,
                                    pdf_company
                                )

                                st.success("✅ PDF Report Generated!")
                                st.download_button(
                                    label="📥 Download PDF Report",
                                    data=pdf_bytes,
                                    file_name=f"ESG_Report_{pdf_company.replace(' ', '_')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )

            with col2:
                if pdf_company:
                    st.subheader("Report Contents")
                    st.markdown("""
                    The generated PDF report will include:

                    **📋 Executive Summary**
                    - Overall ESG performance assessment
                    - Key highlights and rating

                    **📊 ESG Scores Overview**
                    - Environmental, Social, Governance scores
                    - Total ESG score and rating breakdown

                    **🏢 Company Profile**
                    - Sector and market information
                    - Key company metrics

                    **🌍 Environmental Performance**
                    - Carbon emissions
                    - Energy and water usage
                    - Waste management

                    **👥 Social Performance**
                    - Employee metrics
                    - Diversity and inclusion
                    - Community investment

                    **⚖️ Governance Performance**
                    - Board independence
                    - Executive compensation
                    - Controversy assessment

                    **⚠️ Risk Assessment**
                    - Identified risks by category
                    - Severity levels

                    **💡 Recommendations**
                    - Areas for improvement
                    - Action items
                    """)

        else:  # Portfolio Report
            st.subheader("Portfolio Report")
            portfolio_companies = st.multiselect(
                "Select companies for portfolio report",
                options=get_companies(filtered_df),
                default=list(get_companies(filtered_df))[:5]
            )

            if portfolio_companies and st.button("📥 Generate Portfolio Report"):
                with st.spinner("Generating portfolio PDF..."):
                    latest_df = get_latest_data(filtered_df)
                    portfolio_data = []

                    for company in portfolio_companies:
                        comp_data = latest_df[latest_df['company'] == company]
                        if not comp_data.empty:
                            row = comp_data.iloc[0]
                            portfolio_data.append({
                                'company': company,
                                'total_esg_score': row['total_esg_score'],
                                'environmental_score': row['environmental_score'],
                                'social_score': row['social_score'],
                                'governance_score': row['governance_score'],
                                'esg_rating': get_esg_rating(row['total_esg_score'])
                            })

                    pdf_bytes = pdf_reporter.generate_portfolio_report(
                        portfolio_data,
                        title=f"ESG Portfolio Report - {len(portfolio_companies)} Companies"
                    )

                    st.success("✅ Portfolio Report Generated!")
                    st.download_button(
                        label="📥 Download Portfolio Report",
                        data=pdf_bytes,
                        file_name="ESG_Portfolio_Report.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )


if __name__ == "__main__":
    main()
