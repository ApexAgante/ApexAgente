from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "b", size=26)
        self.ln(10)
        width = self.get_string_width("Apex Agente") + 6
        self.set_x((190 + width) / 2)
        self.cell(
            width,
            9,
            "Apex Agente",
            border=0,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )
        self.ln(10)
