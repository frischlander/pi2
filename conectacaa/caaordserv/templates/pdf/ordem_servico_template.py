from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Frame, PageBreak, Flowable, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
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
        self.setStrokeColor(colors.HexColor('#00a652'))
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
        self.width = width or 2.5*inch  # Largura total da pill
        self.height = 0.25 * inch
        self.fontSize = 8
        self.content_width = self.width - 0.4*inch  # Largura do conteúdo (reduzindo as margens laterais)
        
    def draw(self):
        # Desenha o retângulo arredondado
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=0)
        
        # Configura o texto
        self.canv.setFillColor(colors.white)
        self.canv.setFont('Helvetica-Bold', self.fontSize)
        
        # Centraliza o texto considerando a largura do conteúdo
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
            rightMargin=72,  # Aumentado para 72 para manter consistência
            leftMargin=72,
            topMargin=50,
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
    
    def create_status_pill(self, text, color, width=None):
        """Cria uma pill colorida para o status ou tipo"""
        return StatusPill(text, color, width)

    def format_pill_text(self, text):
        """Formata o texto para exibição na pill"""
        if text == "Captura de Animais de Grande Porte":
            return "Captura Grande Porte"
        return text

    def add_header(self, ordem):
        # Primeiro adiciona as pills no topo direito
        tipo_pill = self.create_status_pill(
            self.format_pill_text(ordem.get_tipo_display()),
            colors.HexColor(self.tipo_colors.get(ordem.tipo, '#95a5a6')),
            width=1.8*inch  # Define largura específica para pill de tipo
        )
        status_pill = self.create_status_pill(
            ordem.get_status_display(),
            colors.HexColor(self.status_colors.get(ordem.status, '#95a5a6')),
            width=1.2*inch  # Define largura específica para pill de status
        )
        
        # Criar uma tabela com as pills alinhadas à direita
        pills_table = Table(
            [[tipo_pill, Spacer(1, 0.1*inch), status_pill]],
            colWidths=[1.8*inch, 0.40*inch, 0.5*inch],  # Ajustado para corresponder às larguras das pills
            hAlign='RIGHT'
        )
        pills_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        # Criar uma tabela wrapper para controlar a margem direita
        wrapper_table = Table(
            [[pills_table]],
            colWidths=[self.doc.width - (self.doc.leftMargin + self.doc.rightMargin)],  # Ajustado para considerar ambas as margens
            hAlign='RIGHT'
        )
        wrapper_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        self.elements.append(wrapper_table)
        self.elements.append(Spacer(1, 20))  # Espaço entre as pills e o cabeçalho

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

        # Número do Processo centralizado
        self.elements.append(Paragraph(f"Processo: {ordem.get_processo_display()}", self.processo_style))
    
    def add_solicitante(self, ordem):
        # Adiciona mais espaço antes da seção
        self.elements.append(Spacer(1, 30))  # Aumentado de 12 para 30
        self.elements.append(Paragraph("Dados do Solicitante", self.subtitle_style))
        
        # Criar tabela com fundo cinza claro
        solicitante_data = [
            ["Nome:", ordem.nome_solicitante],
            ["Telefone:", ordem.telefone],
            ["Endereço:", ordem.endereco]
        ]
        
        t = Table(solicitante_data, colWidths=[2*inch, 4.5*inch])  # Aumentado a largura da coluna de labels
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor('#34495e')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 12))
    
    def add_detalhes(self, ordem):
        self.elements.append(Paragraph("Detalhes da Ordem", self.subtitle_style))
        
        # Criar tabela com fundo cinza claro
        ordem_data = [
            ["Tipo:", ordem.get_tipo_display()],
            ["Última Atualização:", ordem.data_atualizacao.strftime("%d/%m/%Y %H:%M")],
            ["Responsável:", ordem.ultimo_usuario.get_full_name() if ordem.ultimo_usuario else "Não informado"]
        ]
        
        t = Table(ordem_data, colWidths=[2*inch, 4.5*inch])  # Aumentado a largura da coluna de labels
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor('#34495e')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        self.elements.append(t)
        self.elements.append(Spacer(1, 12))
    
    def add_descricao(self, ordem):
        # Criar estilo para o texto dentro da tabela
        texto_style = ParagraphStyle(
            'TextoTabela',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#34495e'),
            spaceBefore=0,
            spaceAfter=0,
            leading=12,
            alignment=TA_JUSTIFY  # Alterado para justificado
        )
        
        # Criar o parágrafo com o texto formatado
        texto_formatado = Paragraph(ordem.descricao, texto_style)
        
        # Criar tabela com fundo cinza claro
        descricao_data = [[texto_formatado]]
        
        # Criar a tabela com o título
        elementos_descricao = []
        elementos_descricao.append(Paragraph("Descrição", self.subtitle_style))
        
        t = Table(descricao_data, colWidths=[6.5*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),  # Aumentado o padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),  # Aumentado o padding
            ('TOPPADDING', (0, 0), (-1, -1), 15),  # Aumentado o padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),  # Aumentado o padding
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elementos_descricao.append(t)
        
        # Manter título e conteúdo juntos
        keepTogether = KeepTogether(elementos_descricao)
        self.elements.append(keepTogether)
        self.elements.append(Spacer(1, 30))  # Aumentado o espaço após a descrição
    
    def add_parecer(self, ordem):
        if ordem.status == 'finalizada' and ordem.parecer:
            # Criar estilo para o texto dentro da tabela
            texto_style = ParagraphStyle(
                'TextoTabela',
                parent=self.styles['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#34495e'),
                spaceBefore=0,
                spaceAfter=0,
                leading=12,
                alignment=TA_JUSTIFY  # Alterado para justificado
            )
            
            # Criar o parágrafo com o texto formatado
            texto_formatado = Paragraph(ordem.parecer, texto_style)
            
            # Criar tabela com fundo cinza claro
            parecer_data = [[texto_formatado]]
            
            # Criar a tabela com o título
            elementos_parecer = []
            elementos_parecer.append(Paragraph("Parecer Técnico", self.subtitle_style))
            
            t = Table(parecer_data, colWidths=[6.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                ('LEFTPADDING', (0, 0), (-1, -1), 20),  # Aumentado o padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 20),  # Aumentado o padding
                ('TOPPADDING', (0, 0), (-1, -1), 15),  # Aumentado o padding
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),  # Aumentado o padding
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elementos_parecer.append(t)
            
            # Adicionar espaço antes do parecer técnico
            self.elements.append(Spacer(1, 20))  # Reduzido de 50 para 20
            
            # Manter título e conteúdo juntos
            keepTogether = KeepTogether(elementos_parecer)
            self.elements.append(keepTogether)
            self.elements.append(Spacer(1, 20))  # Reduzido de 50 para 20
            
            # Cria uma tabela com a linha de assinatura e o texto abaixo
            signature_table = Table(
                [[''], ['Responsável do CAA']],
                colWidths=[2.5*inch],
                rowHeights=[15, 8]
            )
            signature_table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (0, 0), 0.5, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, 1), 8),
                ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#666666')),
                ('TOPPADDING', (0, 1), (-1, 1), 0),  # Removido o padding superior
                ('BOTTOMPADDING', (0, 1), (-1, -1), 0),  # Removido o padding inferior
            ]))
            
            signature_wrapper = Table(
                [[signature_table]],
                colWidths=[self.doc.width - 144]
            )
            signature_wrapper.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            
            self.elements.append(signature_wrapper)
            self.elements.append(Spacer(1, 20))
    
    def add_cancelamento(self, ordem):
        if ordem.status == 'cancelada' and ordem.justificativa_cancelamento:
            self.elements.append(Paragraph("Justificativa do Cancelamento", self.subtitle_style))
            
            # Criar tabela com fundo cinza claro
            cancelamento_data = [[ordem.justificativa_cancelamento]]
            
            t = Table(cancelamento_data, colWidths=[5.5*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#dc3545')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            self.elements.append(t)
            self.elements.append(Spacer(1, 12))
    
    def add_anexos(self, ordem):
        # Verifica se existem anexos
        anexos = ordem.anexos.filter(tipo='foto').order_by('data_upload')
        if not anexos:
            return

        # Força uma nova página para os anexos
        self.elements.append(PageBreak())
        
        # Adiciona o título da seção centralizado
        self.elements.append(Spacer(1, 20))
        title_style = ParagraphStyle(
            'AnexosTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#2c3e50')
        )
        self.elements.append(Paragraph("Anexos", title_style))
        
        # Para cada anexo do tipo foto
        for anexo in anexos:
            try:
                # Cria uma lista para os elementos da tabela
                table_elements = []
                
                # Cria um container para a imagem e descrição
                container_elements = []
                
                # Adiciona a imagem
                if anexo.arquivo:
                    img = Image(anexo.arquivo.path)
                    # Calcula as dimensões mantendo a proporção
                    img_width, img_height = img.imageWidth, img.imageHeight
                    aspect = img_height / float(img_width)
                    max_width = self.doc.width - 144  # Margens de 72px
                    max_height = 350  # Reduzido de 450 para 350px
                    
                    # Ajusta as dimensões mantendo a proporção
                    if img_width > max_width:
                        img_width = max_width
                        img_height = img_width * aspect
                    if img_height > max_height:
                        img_height = max_height
                        img_width = img_height / aspect
                    
                    img = Image(anexo.arquivo.path, width=img_width, height=img_height)
                    img.hAlign = 'CENTER'
                    container_elements.append(img)
                    
                    # Adiciona a descrição logo após a imagem
                    if anexo.descricao:
                        desc_style = ParagraphStyle(
                            'AnexoDesc',
                            parent=self.styles['Normal'],
                            fontSize=10,
                            textColor=colors.HexColor('#666666'),
                            alignment=TA_CENTER,
                            spaceBefore=5
                        )
                        container_elements.append(Paragraph(anexo.descricao, desc_style))

                # Adiciona o container à tabela
                table_elements.append([container_elements])

                # Cria a tabela com borda cinza claro
                t = Table(table_elements, colWidths=[self.doc.width - 144])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6')),
                    ('LEFTPADDING', (0, 0), (-1, -1), 15),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                
                # Adiciona a tabela ao documento
                self.elements.append(t)
                
                # Adiciona espaço entre as tabelas, mas não após a última
                if anexo != anexos.last():
                    self.elements.append(Spacer(1, 15))  # Reduzido de 20 para 15

            except Exception as e:
                print(f"Erro ao adicionar anexo {anexo.id}: {str(e)}")
                continue

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
            self.add_anexos(ordem)  # Adiciona os anexos no final
            
            # Gera o PDF com o canvas numerado
            self.doc.build(
                self.elements,
                canvasmaker=NumberedCanvas
            )
            self.buffer.seek(0)
        except Exception as e:
            print(f"Erro ao gerar o PDF: {e}")
            self.buffer.seek(0) 