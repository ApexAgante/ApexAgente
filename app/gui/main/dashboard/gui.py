from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas, PhotoImage, Frame


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def dashboard():
    Dashboard()


class Dashboard(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg="#FFFFFF")

        canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=432,
            width=705,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        canvas.create_image(
            632.2421569824219,
            278.0,
            image=self.image_image_1
        )

        canvas.create_text(
            198.0,
            107.0,
            anchor="nw",
            text="Welcome",
            fill="#E65656",
            font=("Arial", 50 * -1, 'bold')
        )

        canvas.create_text(
            292.0,
            168.0,
            anchor="nw",
            text="To",
            fill="#E65656",
            font=("Arial", 50 * -1, 'bold')
        )

        canvas.create_text(
            160.0,
            229.0,
            anchor="nw",
            text="ApexAgente",
            fill="#E65656",
            font=("Arial", 50 * -1, 'bold')
        )
