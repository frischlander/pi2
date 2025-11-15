from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageBreak, Flowable, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from django.conf import settings
import os

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self._total_ordens = kwargs.get('total_ordens', 0)

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_footer(self._pageNumber, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_footer(self, page_num, total_pages):
        width, height = landscape(A4)
        
        # Desenha a linha verde clara
        self.setStrokeColor(colors.HexColor('#90EE90'))
        self.setLineWidth(1)
        self.line(30, 35, width - 30, 35)  # Margens de 30px e posição Y ajustada
        
        # Texto do rodapé
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#666666'))
        
        # Ajusta a posição Y do texto para ficar abaixo da linha verde
        footer_text = f'Total de ordens: {self._total_ordens}'
        self.drawString(30, 20, footer_text)
        self.drawRightString(width - 30, 20, f'Página {page_num} de {total_pages}')

class StatusPill(Flowable):
    def __init__(self, text, color, width=None):
        Flowable.__init__(self)
        self.text = text
        self.color = color
        self.width = 1.3 * inch
        self.height = 0.18 * inch
        self.fontSize = 7
        
    def draw(self):
        padding = 0.02 * inch
        pill_width = self.width - (2 * padding)
        pill_height = self.height - (2 * padding)
        
        self.canv.setFillColor(self.color)
        self.canv.roundRect(padding, padding, pill_width, pill_height, 3, fill=1, stroke=0)
        
        self.canv.setFillColor(colors.white)
        self.canv.setFont('Helvetica-Bold', self.fontSize)
        
        text_width = self.canv.stringWidth(self.text, 'Helvetica-Bold', self.fontSize)
        x = (self.width - text_width) / 2
        y = padding + (pill_height / 2) - (self.fontSize / 4)
        
        self.canv.drawString(x, y, self.text)

class ListaOrdensTemplate:
    def __init__(self, buffer):
        self.buffer = buffer
        self.doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=50
        )
        self.styles = getSampleStyleSheet()
        self.elements = []

    def get_status_color(self, status):
        status_colors = {
            'finalizada': colors.green,
            'em_andamento': colors.blue,
            'aguardando_parecer': colors.orange,
            'cancelada': colors.red,
            'nao_iniciada': colors.grey
        }
        return status_colors.get(status, colors.grey)

    def build(self, ordens):
        try:
            # Adiciona a logo
            logo_path = os.path.join(settings.BASE_DIR, 'conectacaa', 'static', 'img', 'logo.png')
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=100, height=100)
                logo.hAlign = 'CENTER'
                self.elements.append(logo)
                self.elements.append(Spacer(1, 10))

            # Título em verde
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=14,
                spaceAfter=15,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#00a652')
            )
            self.elements.append(Paragraph("LISTA DE ORDENS DE SERVIÇO", title_style))
            self.elements.append(Spacer(1, 10))

            # Dados da tabela
            data = [['Processo', 'Nome', 'Tipo', 'Endereço', 'Status']]
            
            # Adiciona os dados das ordens
            for ordem in ordens:
                status_color = self.get_status_color(ordem.status)
                status_pill = StatusPill(ordem.get_status_display(), status_color)
                
                data.append([
                    ordem.get_processo_display(),
                    ordem.nome_solicitante,
                    ordem.get_tipo_display(),
                    ordem.endereco,
                    status_pill
                ])

            # Estilo da tabela
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00a652')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#00a652')),
            ])

            # Adiciona as linhas alternadas em verde claro
            for i in range(len(data)):
                if i > 0 and i % 2 == 1:
                    table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#e6f3ed'))

            # Cria a tabela com larguras ajustadas
            table = Table(data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch, 3.5*inch, 1.5*inch])
            table.setStyle(table_style)
            self.elements.append(table)

            # Gera o PDF com o canvas numerado
            self.doc.build(
                self.elements,
                canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, total_ordens=len(ordens), **kwargs)
            )
            
            # Garante que o buffer está no início
            self.buffer.seek(0)
            
        except Exception as e:
            raise Exception(f"Erro ao gerar PDF: {str(e)}") 