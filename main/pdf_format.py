from import_export.formats.base_formats import Format
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import io

class PDF(Format):
    """
    Classe que implementa a formatação de exportação de dados em formato PDF.

    Métodos:
        get_title(): Retorna o título do formato.
        get_extension(): Retorna a extensão do arquivo.
        get_content_type(): Retorna o tipo de conteúdo MIME.
        export_data(dataset, **kwargs): Exporta os dados do dataset para um arquivo PDF.
        import_data(dataset, stream, **kwargs): Importação via PDF não é suportada.
    """

    def get_title(self):
        """
        Retorna o título do formato.

        Retorna:
            str: O título do formato.
        """
        return "pdf"

    def get_extension(self):
        """
        Retorna a extensão do arquivo.

        Retorna:
            str: A extensão do arquivo.
        """
        return "pdf"

    def get_content_type(self):
        """
        Retorna o tipo de conteúdo MIME.

        Retorna:
            str: O tipo de conteúdo MIME.
        """
        return "application/pdf"

    def export_data(self, dataset, **kwargs):
        """
        Exporta os dados do dataset para um arquivo PDF.

        Parâmetros:
            dataset: O dataset contendo os dados a serem exportados.
            **kwargs: Argumentos adicionais.

        Retorna:
            bytes: O conteúdo do arquivo PDF em bytes.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))  # Página horizontal
        elements = []

        # Obter cabeçalhos e linhas do dataset
        headers = dataset.headers
        rows = dataset.dict  # Obtém os dados como uma lista de dicionários

        # Se não houver dados, exibir uma mensagem
        if not rows:
            data = [["Nenhum dado disponível"]]
        else:
            # Converter dados em um formato que permita quebra de linhas
            data = [headers] + [list(row.values()) for row in rows]
            data = [
                [Paragraph(str(cell), ParagraphStyle(name='Normal', wordWrap='CJK')) for cell in row]
                for row in data
            ]

        # Calcular larguras dinâmicas das colunas
        page_width = landscape(A4)[0] - 2 * doc.leftMargin
        num_columns = len(headers)
        col_widths = [page_width / num_columns] * num_columns

        # Criar tabela
        table = Table(data, colWidths=col_widths, repeatRows=1)

        # Estilizar tabela
        table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ])
        )

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer.read()

    def import_data(self, dataset, stream, **kwargs):
        """
        Levanta uma exceção, pois a importação via PDF não é suportada.

        Lança:
            NotImplementedError: Sempre, pois a importação via PDF não é suportada.
        """
        raise NotImplementedError("Importação via PDF não é suportada.")
