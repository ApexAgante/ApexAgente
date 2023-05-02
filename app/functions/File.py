import pandas as pd

from os import path, remove
from ..classes.PDFManager import PDF
from fpdf.fonts import FontFace

pdf = PDF()
pdf.add_page(format="a3")
pdf.set_author('Apex Agente')
pdf.set_creator('Apex Agente')
pdf.set_title('Apex Agente')
pdf.set_font("Helvetica")

fg = (255, 255, 255)
bg = (231, 86, 86)
headings_style = FontFace(emphasis="BOLD", color=fg,
                          fill_color=bg)


def check_config():
    if path.isfile('config.json'):
        remove('config.json')


def test_write_pdf():
    data = {
        "First Name": ["Jo", "Es"],
        "Last Name": ["Son", "Co"]
    }

    headers = [key for key in data]
    d = []
    for key in data:
        value = data[key]
        d.append(value)

    data = [list(a) for a in zip(*d)]
    
    with pdf.table(headings_style=headings_style, col_widths=(20, 20)) as table:
        row = table.row()
        for h in headers:
            row.cell(h)
        
        for da in data:
            ros = table.row()
            for d in da:
                pdf.set_text_color(233, 200, 20)
                ros.cell(d)

    pdf.output('a.pdf')


def write_excel(data):
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter("output/data_result.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    (max_row, max_col) = df.shape
    column_settings = [{"header": column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})
    worksheet.set_column(0, 1, 5)
    worksheet.set_column(1, 1, 50)
    worksheet.set_column(2, max_col - 1, 30)
    writer.close()


def write_pdf(data):
    if data and isinstance(data, list):

        with pdf.table(headings_style=headings_style, line_height=6,col_widths=(8, 30, 30, 30, 20, 15), width=277) as table:
            row = table.row()
            for header in data[0]:
                row.cell(header)

            for data_row in data[1:]:
                row = table.row()
                for d in data_row:
                    pdf.set_font("Times", size=10)
                    row.cell(d)

        pdf.output('output/data_result.pdf')
