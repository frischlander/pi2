from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Frame, PageBreak, Flowable
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
        width, height = A4
        
        # Desenha a linha verde clara
        self.setStrokeColor(colors.HexColor('#90EE90'))
        self.setLineWidth(1)
        self.line(72, 35, width - 72, 35)  # Margens de 72px e posição Y ajustada
        
        # Texto do rodapé
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#666666'))
        
        # Ajusta a posição Y do texto para ficar abaixo da linha verde
        footer_text = f'Centro de Acolhimento Animal "São Francisco de Assis"'
        self.drawString(72, 20, footer_text)
        self.drawRightString(width - 72, 20, f'Página {page_num} de {total_pages}')

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
            topMargin=30,  # Reduzindo a margem superior
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

        # Dicionário de cores para os tipos
        self.tipo_colors = {
            'manutencao': '#3498db',    # Azul
            'limpeza': '#2ecc71',       # Verde
            'outros': '#9b59b6',        # Roxo
            'emergencia': '#e74c3c',    # Vermelho
            'preventiva': '#f39c12',    # Laranja
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

        # Estilo para o número do processo
        self.processo_style = ParagraphStyle(
            'Processo',
            parent=self.styles['Heading1'],
            fontSize=14,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#00a652'),
            borderWidth=1,
            borderColor=colors.HexColor('#00a652'),
            borderPadding=(10, 5),
            borderRadius=5
        )

        # Estilo para os detalhes do processo
        self.processo_details_style = ParagraphStyle(
            'ProcessoDetails',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#666666')
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
    
    def create_status_pill(self, text, color):
        """Cria uma pill colorida para o status ou tipo"""
        return StatusPill(text, color)

    def add_header(self, ordem):
        # Tabela para o cabeçalho com logo e informações
        logo_path = os.path.join(settings.BASE_DIR, 'conectacaa', 'static', 'img', 'logo.png')
        
        # Estilo para o texto do cabeçalho
        header_text_style = ParagraphStyle(
            'HeaderText',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#666666'),
            spaceAfter=0,
            spaceBefore=0,
            leading=10
        )

        # Estilo para o nome do centro
        center_name_style = ParagraphStyle(
            'CenterName',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#00a652'),
            spaceAfter=0,
            spaceBefore=0,
            leading=12,
            fontName='Helvetica-Bold'
        )

        # Criar o cabeçalho principal
        header_elements = []
        
        # Adiciona a logo e informações em uma tabela
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=80, height=80)
            
            # Criar os parágrafos de informações
            info_elements = [
                Paragraph("Centro de Acolhimento Animal", center_name_style),
                Paragraph('"São Francisco de Assis"', center_name_style),
                Spacer(1, 5),
                Paragraph("Estrada Municipal Vitorio Celso Cisoto, Km 1,5", header_text_style),
                Paragraph("Telefone: (17) 3279-4886", header_text_style),
                Paragraph("Email: luciano.terazima@olimpia.sp.gov.br", header_text_style),
                Paragraph("Site: www.olimpia.sp.gov.br", header_text_style)
            ]

            # Criar uma tabela com duas colunas: logo e informações
            header_table = Table(
                [[logo, info_elements]],
                colWidths=[90, self.doc.width - 162]
            )
            
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),  # Alinha a logo ao centro
                ('ALIGN', (1, 0), (1, 0), 'LEFT'),    # Alinha o texto à esquerda
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (1, 0), (1, 0), 20),  # Aumenta o espaço entre a logo e o texto
            ]))

            self.elements.append(header_table)
            self.elements.append(Spacer(1, 20))

        # Adiciona uma linha decorativa
        line = Table([['']], colWidths=[self.doc.width - 144])
        line.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#00a652')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        self.elements.append(line)
        self.elements.append(Spacer(1, 20))

        # Número do Processo centralizado
        self.elements.append(Paragraph(f"Processo: {ordem.get_processo_display()}", self.processo_style))
        
        # Detalhes do processo em texto com tipo e status em pill
        tipo_pill = self.create_status_pill(
            ordem.get_tipo_display(),
            colors.HexColor(self.tipo_colors.get(ordem.tipo, '#95a5a6'))
        )
        status_pill = self.create_status_pill(
            ordem.get_status_display(),
            colors.HexColor(self.status_colors.get(ordem.status, '#95a5a6'))
        )
        
        details_table = Table(
            [[tipo_pill, status_pill]],
            colWidths=[self.doc.width/2 - 72, self.doc.width/2 - 72]
        )
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        self.elements.append(details_table)
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
            # Estilo para o título do parecer
            parecer_title_style = ParagraphStyle(
                'ParecerTitle',
                parent=self.subtitle_style,
                spaceBefore=10,
                spaceAfter=5,
            )
            
            self.elements.append(Paragraph("Parecer Técnico", parecer_title_style))
            self.elements.append(Paragraph(ordem.parecer, self.styles['Normal']))
            self.elements.append(Spacer(1, 30))  # Espaço entre o parecer e a assinatura
            
            # Cria uma tabela com a linha de assinatura e o texto abaixo
            signature_table = Table(
                [[''], ['Veterinário(a) Responsável']],
                colWidths=[2.5*inch],  # Reduzindo um pouco a largura da linha
                rowHeights=[15, 12]  # Reduzindo a altura da linha e do texto
            )
            signature_table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (0, 0), 0.5, colors.HexColor('#00a652')),  # Linha mais fina
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, 1), 8),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#666666')),
                ('TOPPADDING', (0, 1), (-1, 1), 2),  # Reduz o espaço entre a linha e o texto
            ]))
            
            # Centraliza a tabela de assinatura
            signature_wrapper = Table(
                [[signature_table]],
                colWidths=[self.doc.width - 144]
            )
            signature_wrapper.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            
            self.elements.append(signature_wrapper)
            self.elements.append(Spacer(1, 20))  # Reduzindo o espaço após a assinatura
    
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
            
            # Gera o PDF com o canvas numerado
            self.doc.build(
                self.elements,
                canvasmaker=NumberedCanvas
            )
            self.buffer.seek(0)
        except Exception as e:
            print(f"Erro ao gerar o PDF: {e}")
            self.buffer.seek(0) 