"""PDF export service for company reports."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

logger = logging.getLogger(__name__)


class PDFExportService:
    """Service for exporting company data to PDF."""
    
    def __init__(self):
        """Initialize PDF export service."""
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """Setup custom styles for PDF."""
        # Custom styles for Russian text
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
            alignment=1  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#000000'),
            spaceAfter=10
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#000000')
        )
    
    def export_company_screen(self, company_data: Dict[str, Any], screen_name: str) -> BytesIO:
        """Export specific company screen to PDF."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        story = []
        
        # Title
        title = Paragraph(f"Отчет: {screen_name}", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.5*cm))
        
        # Company name
        company_name = company_data.get('data', {}).get('name', {}).get('full_with_opf', 'Н/Д')
        story.append(Paragraph(f"<b>Компания:</b> {company_name}", self.normal_style))
        story.append(Spacer(1, 0.3*cm))
        
        # Export date
        export_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(f"<b>Дата экспорта:</b> {export_date}", self.normal_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Add screen specific content
        if screen_name == "Основная информация":
            self._add_main_info(story, company_data)
        elif screen_name == "Директора":
            self._add_directors_info(story, company_data)
        elif screen_name == "Учредители":
            self._add_founders_info(story, company_data)
        elif screen_name == "Адреса":
            self._add_addresses_info(story, company_data)
        elif screen_name == "ОКВЭД":
            self._add_okved_info(story, company_data)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def export_full_report(self, company_data: Dict[str, Any]) -> BytesIO:
        """Export full company report to PDF."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
        story = []
        
        # Title
        company_name = company_data.get('data', {}).get('name', {}).get('full_with_opf', 'Н/Д')
        title = Paragraph(f"Полный отчет по компании", self.title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(company_name, self.heading_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Export date
        export_date = datetime.now().strftime("%d.%m.%Y %H:%M")
        story.append(Paragraph(f"<b>Дата экспорта:</b> {export_date}", self.normal_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Add all sections
        self._add_main_info(story, company_data)
        story.append(PageBreak())
        
        self._add_directors_info(story, company_data)
        story.append(PageBreak())
        
        self._add_founders_info(story, company_data)
        story.append(PageBreak())
        
        self._add_addresses_info(story, company_data)
        story.append(PageBreak())
        
        self._add_okved_info(story, company_data)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _add_main_info(self, story, company_data):
        """Add main company information to PDF."""
        story.append(Paragraph("Основная информация", self.heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        data = company_data.get('data', {})
        
        info_items = [
            ["ИНН", data.get('inn', 'Н/Д')],
            ["ОГРН", data.get('ogrn', 'Н/Д')],
            ["КПП", data.get('kpp', 'Н/Д')],
            ["Статус", data.get('state', {}).get('status', 'Н/Д')],
            ["Дата регистрации", data.get('state', {}).get('registration_date', 'Н/Д')],
        ]
        
        table = Table(info_items, colWidths=[5*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.5*cm))
    
    def _add_directors_info(self, story, company_data):
        """Add directors information to PDF."""
        story.append(Paragraph("История руководителей", self.heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        management = company_data.get('data', {}).get('management', {})
        if management:
            name = management.get('name', 'Н/Д')
            post = management.get('post', 'Н/Д')
            story.append(Paragraph(f"<b>ФИО:</b> {name}", self.normal_style))
            story.append(Paragraph(f"<b>Должность:</b> {post}", self.normal_style))
        else:
            story.append(Paragraph("Информация отсутствует", self.normal_style))
        story.append(Spacer(1, 0.5*cm))
    
    def _add_founders_info(self, story, company_data):
        """Add founders information to PDF."""
        story.append(Paragraph("Учредители", self.heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        founders = company_data.get('data', {}).get('founders', [])
        if founders:
            for i, founder in enumerate(founders, 1):
                name = founder.get('name', 'Н/Д')
                share = founder.get('share', {})
                story.append(Paragraph(f"<b>{i}. {name}</b>", self.normal_style))
                if share:
                    story.append(Paragraph(f"Доля: {share}", self.normal_style))
                story.append(Spacer(1, 0.2*cm))
        else:
            story.append(Paragraph("Информация отсутствует", self.normal_style))
        story.append(Spacer(1, 0.5*cm))
    
    def _add_addresses_info(self, story, company_data):
        """Add addresses information to PDF."""
        story.append(Paragraph("Адреса", self.heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        address = company_data.get('data', {}).get('address', {})
        if address:
            addr_value = address.get('value', 'Н/Д')
            story.append(Paragraph(f"<b>Адрес:</b> {addr_value}", self.normal_style))
        else:
            story.append(Paragraph("Информация отсутствует", self.normal_style))
        story.append(Spacer(1, 0.5*cm))
    
    def _add_okved_info(self, story, company_data):
        """Add OKVED information to PDF."""
        story.append(Paragraph("ОКВЭД (виды деятельности)", self.heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        okved = company_data.get('data', {}).get('okved', 'Н/Д')
        okveds = company_data.get('data', {}).get('okveds', [])
        
        story.append(Paragraph(f"<b>Основной ОКВЭД:</b> {okved}", self.normal_style))
        story.append(Spacer(1, 0.2*cm))
        
        if okveds:
            story.append(Paragraph("<b>Дополнительные ОКВЭД:</b>", self.normal_style))
            for okv in okveds[:10]:  # Limit to 10
                story.append(Paragraph(f"• {okv}", self.normal_style))
        story.append(Spacer(1, 0.5*cm))


# Global service instance
pdf_service = PDFExportService()
