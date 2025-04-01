from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Frame, PageBreak, Flowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os

class StatusPill(Flowable):
    def __init__(self, text, color, width=None):
        Flowable.__init__(self)
        self.text = text
        self.color = color
        self.width = width or (len(text) * 0.15 * inch)
        self.height = 0.25 * inch
        self.fontSize = 8
        
    def draw(self):
        # Desenha o retângulo arredondado
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)  # Reduzido para 4 e removida a borda
        
        # Configura o texto
        self.canv.setFillColor(colors.white)
        self.canv.setFont('Helvetica-Bold', self.fontSize)
        
        # Centraliza o texto
        text_width = self.canv.stringWidth(self.text, 'Helvetica-Bold', self.fontSize)
        x = (self.width - text_width) / 2
        y = (self.height - self.fontSize) / 2
        
        # Desenha o texto
        self.canv.drawString(x, y, self.text)

class OrdemServicoTemplate:
    def __init__(self, buffer):
        self.buffer = buffer
        self.doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        self.elements = []
        self.styles = getSampleStyleSheet()
        
        # Dicionário de cores para os status
        self.status_colors = {
            'aberta': '#373a3c',     
            'em_andamento': '#17a2b8', 
            'finalizada': '#27ae60',  
            'cancelada': '#dc3545',   
            'pendente': '#f1c40f',     
            'aguardando_parecer': '#e98604',
        }
        
        # Estilos personalizados
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.HexColor('#34495e')
        )
        
        self.header_style = ParagraphStyle(
            'Header',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_RIGHT,
            textColor=colors.HexColor('#7f8c8d')
        )
        
        self.table_style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor('#34495e')),
        ])
        
        # Frame para o conteúdo principal
        self.main_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin + 100,  # Espaço para o footer
            self.doc.width - 2*self.doc.leftMargin,
            self.doc.height - 2*self.doc.bottomMargin - 100
        )
        
        # Frame para o footer
        self.footer_frame = Frame(
            self.doc.leftMargin,
            self.doc.bottomMargin,
            self.doc.width - 2*self.doc.leftMargin,
            100
        )
    
    def create_status_pill(self, status):
        """Cria uma pill colorida para o status"""
        status_display = status.get_status_display()
        color = colors.HexColor(self.status_colors.get(status.status, '#95a5a6'))
        return StatusPill(status_display, color)

    def add_header(self, ordem):
        # Tabela para o cabeçalho com logo e informações
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
        self.elements.append(Paragraph("ORDEM DE SERVIÇO", title_style))
        self.elements.append(Spacer(1, 10))

        # Dados da tabela
        data = [['Processo', 'Tipo', 'Status']]
        data.append([
            ordem.get_processo_display(),  # Usa o método get_processo_display para remover zeros à esquerda
            ordem.get_tipo_display(),
            ordem.get_status_display()
        ])
        
        # Se tiver logo, adiciona uma coluna para ela
        if logo:
            data[0].insert(0, logo)
        
        # Ajusta as larguras das colunas baseado na presença da logo
        col_widths = [2*inch, 4*inch] if not logo else [100, 4*inch]
        
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor('#34495e')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        self.elements.append(t)
        self.elements.append(Spacer(1, 20))
    
    def add_solicitante(self, ordem):
        self.elements.append(Paragraph("Dados do Solicitante", self.subtitle_style))
        
        solicitante_data = [
            ["Nome:", ordem.nome_solicitante],
            ["Telefone:", ordem.telefone],
            ["Endereço:", ordem.endereco]
        ]
        
        t = Table(solicitante_data, colWidths=[1.5*inch, 4*inch])
        t.setStyle(self.table_style)
        self.elements.append(t)
        self.elements.append(Spacer(1, 12))
    
    def add_detalhes(self, ordem):
        self.elements.append(Paragraph("Detalhes da Ordem", self.subtitle_style))
        
        ordem_data = [
            ["Tipo:", ordem.get_tipo_display()],
            ["Última Atualização:", ordem.data_atualizacao.strftime("%d/%m/%Y %H:%M")],
            ["Responsável:", ordem.ultimo_usuario.get_full_name() if ordem.ultimo_usuario else "Não informado"]
        ]
        
        t = Table(ordem_data, colWidths=[1.5*inch, 4*inch])
        t.setStyle(self.table_style)
        self.elements.append(t)
        self.elements.append(Spacer(1, 12))
    
    def add_descricao(self, ordem):
        self.elements.append(Paragraph("Descrição", self.subtitle_style))
        self.elements.append(Paragraph(ordem.descricao, self.styles['Normal']))
        self.elements.append(Spacer(1, 12))
    
    def add_parecer(self, ordem):
        if ordem.status == 'finalizada' and ordem.parecer:
            self.elements.append(Paragraph("Parecer Técnico", self.subtitle_style))
            self.elements.append(Paragraph(ordem.parecer, self.styles['Normal']))
            self.elements.append(Spacer(1, 12))
    
    def add_cancelamento(self, ordem):
        if ordem.status == 'cancelada' and ordem.justificativa_cancelamento:
            self.elements.append(Paragraph("Justificativa do Cancelamento", self.subtitle_style))
            self.elements.append(Paragraph(ordem.justificativa_cancelamento, self.styles['Normal']))
            self.elements.append(Spacer(1, 12))
    
    def add_footer(self):
        # Adiciona o rodapé com informações de contato
        footer_data = [
            ['Centro de Acolhimento Animal "São Francisco de Assis"'],
            ["Endereço: Estrada Municipal Vitorio Celso Cisoto, Km 1,5"],
            ["Telefone: (17) 3279-4886"],
            ["Email: luciano.terazima@olimpia.sp.gov.br"],
            ["Site: www.olimpia.sp.gov.br"]
        ]
        
        t = Table(footer_data, colWidths=[6*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#7f8c8d')),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        self.elements.append(t)
    
    def build(self, ordem):
        try:
            # Adiciona todos os elementos na ordem correta
            self.add_header(ordem)
            self.add_solicitante(ordem)
            self.add_detalhes(ordem)
            self.add_descricao(ordem)
            self.add_parecer(ordem)
            self.add_cancelamento(ordem)
            
            # Adiciona espaço para empurrar o footer para baixo
            self.elements.append(Spacer(1, 230))
            
            # Adiciona o footer no final
            self.add_footer()
            
            # Gera o PDF
            self.doc.build(self.elements)
            self.buffer.seek(0)
        except Exception as e:
            print(f"Erro ao gerar o PDF: {e}")
            self.buffer.seek(0) 