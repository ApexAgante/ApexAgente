from fpdf import FPDF
from fpdf.fonts import FontFace

data = [
    ["Name", "Age"],
    ["JW", "20"],
    ["John", "18"]
]

pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica", size=12)

fg = (255, 255, 255)
bg = (231, 86, 86)
headings_style = FontFace(emphasis="BOLD", color=fg,
                          fill_color=bg)


def main():
    with pdf.table(headings_style=headings_style) as table:
        for data_row in data:
            row = table.row()
            for d in data_row:
                row.cell(d)
    pdf.output('Testing.pdf')
