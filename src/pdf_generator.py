"""
PDF Report Generator for ESG Dashboard
Generates professional PDF reports with charts, tables, and analytics
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import plotly.graph_objects as go
import pandas as pd


class ESGPDFReporter:
    """Generate comprehensive ESG PDF reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()

    def _wrap_cell_content(self, content, style=None):
        """Wrap cell content in Paragraph for proper rendering"""
        if style is None:
            style = self.styles['Normal']
        if isinstance(content, (Paragraph, Table, Image)):
            return content
        return Paragraph(str(content), style)

    def _create_custom_styles(self):
        """Create custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1565C0'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#666666'),
            spaceAfter=12,
            alignment=TA_CENTER
        ))

        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1565C0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leading=14
        ))

    def generate_company_report(self, company_data, company_name, charts_data=None):
        """
        Generate a comprehensive company ESG report

        Parameters:
        -----------
        company_data : dict
            Dictionary containing company ESG metrics
        company_name : str
            Name of the company
        charts_data : dict, optional
            Dictionary containing chart figures

        Returns:
        --------
        bytes
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        story = []

        # Title Page
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"ESG Performance Report", self.styles['CustomTitle']))
        story.append(Paragraph(f"{company_name}", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}",
                              self.styles['CustomBody']))
        story.append(Spacer(1, 0.5*inch))

        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(self._create_executive_summary(company_data))
        story.append(Spacer(1, 0.3*inch))

        # ESG Scores Overview
        story.append(Paragraph("ESG Scores Overview", self.styles['SectionHeader']))
        story.append(self._create_scores_table(company_data))
        story.append(Spacer(1, 0.3*inch))

        # Company Profile
        story.append(Paragraph("Company Profile", self.styles['SectionHeader']))
        story.append(self._create_company_profile(company_data))
        story.append(Spacer(1, 0.3*inch))

        # Environmental Metrics
        if 'environmental_metrics' in company_data:
            story.append(PageBreak())
            story.append(Paragraph("Environmental Performance", self.styles['SectionHeader']))
            story.append(self._create_environmental_section(company_data))
            story.append(Spacer(1, 0.3*inch))

        # Social Metrics
        if 'social_metrics' in company_data:
            story.append(Paragraph("Social Performance", self.styles['SectionHeader']))
            story.append(self._create_social_section(company_data))
            story.append(Spacer(1, 0.3*inch))

        # Governance Metrics
        if 'governance_metrics' in company_data:
            story.append(Paragraph("Governance Performance", self.styles['SectionHeader']))
            story.append(self._create_governance_section(company_data))
            story.append(Spacer(1, 0.3*inch))

        # Risk Assessment
        if 'risks' in company_data and company_data['risks']:
            story.append(PageBreak())
            story.append(Paragraph("Risk Assessment", self.styles['SectionHeader']))
            story.append(self._create_risk_section(company_data['risks']))
            story.append(Spacer(1, 0.3*inch))

        # Recommendations
        if 'recommendations' in company_data and company_data['recommendations']:
            story.append(Paragraph("Recommendations", self.styles['SectionHeader']))
            story.extend(self._create_recommendations_section(company_data['recommendations']))

        # Build PDF
        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    def _create_executive_summary(self, data):
        """Create executive summary paragraph"""
        total_score = data.get('total_esg_score', 0)
        rating_data = data.get('esg_rating', 'N/A')

        # Extract rating text and color if it's a tuple (rating, color)
        if isinstance(rating_data, tuple):
            rating_text = rating_data[0]
            rating_color = rating_data[1]
        else:
            rating_text = rating_data
            rating_color = '#000000'

        summary_text = f"""
        This report provides a comprehensive analysis of the company's Environmental, Social,
        and Governance (ESG) performance. The company has achieved an overall ESG score of
        <b>{total_score:.1f}/100</b>, earning a rating of <b><font color="{rating_color}">{rating_text}</font></b>. This assessment is based
        on multiple factors including environmental impact, social responsibility initiatives,
        and governance practices.
        """

        return Paragraph(summary_text, self.styles['CustomBody'])

    def _create_scores_table(self, data):
        """Create ESG scores table"""
        # Extract rating text and color if it's a tuple (rating, color)
        rating_data = data.get('esg_rating', 'N/A')
        if isinstance(rating_data, tuple):
            rating_text = rating_data[0]
            rating_color = rating_data[1]
        else:
            rating_text = rating_data
            rating_color = '#000000'

        raw_data = [
            ['Metric', 'Score', 'Rating'],
            ['Environmental Score', f"{data.get('environmental_score', 0):.1f}", self._get_rating_text(data.get('environmental_score', 0))],
            ['Social Score', f"{data.get('social_score', 0):.1f}", self._get_rating_text(data.get('social_score', 0))],
            ['Governance Score', f"{data.get('governance_score', 0):.1f}", self._get_rating_text(data.get('governance_score', 0))],
            ['Total ESG Score', f"{data.get('total_esg_score', 0):.1f}", f'<font color="{rating_color}"><b>{rating_text}</b></font>'],
        ]

        # Wrap all cells in Paragraphs
        table_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E3F2FD')),
        ]))

        return table

    def _create_company_profile(self, data):
        """Create company profile table"""
        raw_data = [
            ['Sector', data.get('sector', 'N/A')],
            ['Country', data.get('country', 'N/A')],
            ['Market Cap', f"${data.get('market_cap_billion', 0):.2f}B"],
            ['Year', str(data.get('year', 'N/A'))],
        ]

        # Wrap all cells in Paragraphs
        profile_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(profile_data, colWidths=[2*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5F5F5')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))

        return table

    def _create_environmental_section(self, data):
        """Create environmental metrics section"""
        env_metrics = data.get('environmental_metrics', {})

        raw_data = [
            ['Metric', 'Value'],
            ['Carbon Emissions', f"{env_metrics.get('carbon_emissions_mt', 0):.2f} MT"],
            ['Energy Intensity', f"{env_metrics.get('energy_intensity', 0):.2f}"],
            ['Water Usage', f"{env_metrics.get('water_usage_m3', 0):.0f} m³"],
            ['Waste Recycled', f"{env_metrics.get('waste_recycled_pct', 0):.1f}%"],
        ]

        # Wrap all cells in Paragraphs
        metrics_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(metrics_data, colWidths=[3*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F1F8E9')),
        ]))

        return table

    def _create_social_section(self, data):
        """Create social metrics section"""
        social_metrics = data.get('social_metrics', {})

        raw_data = [
            ['Metric', 'Value'],
            ['Employee Turnover', f"{social_metrics.get('employee_turnover_pct', 0):.1f}%"],
            ['Diversity Score', f"{social_metrics.get('diversity_score', 0):.1f}/100"],
            ['Safety Incidents', str(social_metrics.get('safety_incidents', 0))],
            ['Community Investment', f"${social_metrics.get('community_investment_usd', 0):,.0f}"],
        ]

        # Wrap all cells in Paragraphs
        metrics_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(metrics_data, colWidths=[3*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E3F2FD')),
        ]))

        return table

    def _create_governance_section(self, data):
        """Create governance metrics section"""
        gov_metrics = data.get('governance_metrics', {})

        raw_data = [
            ['Metric', 'Value'],
            ['Board Independence', f"{gov_metrics.get('board_independence_pct', 0):.1f}%"],
            ['Executive Pay Ratio', f"{gov_metrics.get('executive_pay_ratio', 0):.1f}:1"],
            ['Controversy Score', f"{gov_metrics.get('controversy_score', 0):.1f}/100"],
        ]

        # Wrap all cells in Paragraphs
        metrics_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(metrics_data, colWidths=[3*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7B1FA2')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3E5F5')),
        ]))

        return table

    def _create_risk_section(self, risks):
        """Create risk assessment section"""
        risk_data = [['Risk Type', 'Severity', 'Description']]

        for risk in risks:
            category = risk.get('category', 'N/A')
            severity = risk.get('severity', 'N/A')
            description = risk.get('description', 'N/A')

            # Wrap text in Paragraph objects for proper rendering
            risk_data.append([
                Paragraph(str(category), self.styles['CustomBody']),
                Paragraph(str(severity), self.styles['CustomBody']),
                Paragraph(str(description), self.styles['CustomBody'])
            ])

        table = Table(risk_data, colWidths=[1.5*inch, 1*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        return table

    def _create_recommendations_section(self, recommendations):
        """Create recommendations section"""
        story = []

        for i, rec in enumerate(recommendations, 1):
            # Handle both dict and string formats
            if isinstance(rec, dict):
                area = rec.get('area', 'N/A')
                gap = rec.get('gap', 0)
                recommendation = rec.get('recommendation', 'N/A')
                text = f"<b>{i}. {area}</b> (Gap: {gap} points): {recommendation}"
            else:
                text = f"<b>{i}.</b> {rec}"

            story.append(Paragraph(text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.1*inch))

        return story

    def _get_rating_text(self, score):
        """Convert score to rating text"""
        if score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Average"
        elif score >= 50:
            return "Fair"
        else:
            return "Poor"

    def generate_portfolio_report(self, companies_data, title="ESG Portfolio Report"):
        """
        Generate a portfolio report comparing multiple companies

        Parameters:
        -----------
        companies_data : list of dict
            List of company data dictionaries
        title : str
            Report title

        Returns:
        --------
        bytes
            PDF file as bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)

        story = []

        # Title
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}",
                              self.styles['CustomBody']))
        story.append(Spacer(1, 0.5*inch))

        # Portfolio Summary Table
        story.append(Paragraph("Portfolio Summary", self.styles['SectionHeader']))
        story.append(self._create_portfolio_table(companies_data))

        # Build PDF
        doc.build(story)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        return pdf_bytes

    def _create_portfolio_table(self, companies_data):
        """Create portfolio comparison table"""
        raw_data = [['Company', 'ESG Score', 'E', 'S', 'G', 'Rating']]

        for company in companies_data:
            # Extract rating text and color if it's a tuple (rating, color)
            rating_data = company.get('esg_rating', 'N/A')
            if isinstance(rating_data, tuple):
                rating_text = rating_data[0]
                rating_color = rating_data[1]
                rating_display = f'<font color="{rating_color}"><b>{rating_text}</b></font>'
            else:
                rating_display = rating_data

            raw_data.append([
                company.get('company', 'N/A'),
                f"{company.get('total_esg_score', 0):.1f}",
                f"{company.get('environmental_score', 0):.1f}",
                f"{company.get('social_score', 0):.1f}",
                f"{company.get('governance_score', 0):.1f}",
                rating_display
            ])

        # Wrap all cells in Paragraphs
        table_data = [[self._wrap_cell_content(cell) for cell in row] for row in raw_data]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1565C0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
        ]))

        return table
