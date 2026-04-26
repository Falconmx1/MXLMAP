from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime

class PDFExporter:
    def __init__(self, target_url, vulnerabilities):
        self.target_url = target_url
        self.vulnerabilities = vulnerabilities
        self.filename = f"mxmap_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    def generate(self):
        """Genera reporte profesional en PDF"""
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        story = []
        
        # Estilo personalizado
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.red,
            alignment=1  # Centrado
        )
        
        # Título mamalón
        story.append(Paragraph("🇲🇽 MXlmap Security Report", title_style))
        story.append(Spacer(1, 12))
        
        # Info del objetivo
        story.append(Paragraph(f"<b>Target:</b> {self.target_url}", styles['Normal']))
        story.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"<b>Tool:</b> MXlmap v1.0 - Chingón Mode", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Tabla de vulnerabilidades
        data = [['#', 'Tipo', 'Gravedad', 'Payload']]
        for i, vuln in enumerate(self.vulnerabilities, 1):
            data.append([str(i), vuln['type'], vuln['severity'], vuln['payload'][:50]])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Recomendaciones
        story.append(Paragraph("<b>Recommendations:</b>", styles['Heading2']))
        story.append(Paragraph("• Implement parameterized queries", styles['Normal']))
        story.append(Paragraph("• Use WAF (Web Application Firewall)", styles['Normal']))
        story.append(Paragraph("• Regular security audits", styles['Normal']))
        story.append(Paragraph("• Input validation and sanitization", styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        print(f"[+] Reporte generado: {self.filename}")
        return self.filename
