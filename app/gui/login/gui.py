from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas, Entry, Button, PhotoImage, Toplevel
from controller import check_user
from ..main.gui import main_window

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")
MAIN_ASSETS_PATH = OUTPUT_PATH / Path(r"../assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def login_window(root):
    Login(root)


class Login(Toplevel):
    def on_button_click(self):
        res = check_user(self.username.get(), self.password.get())
        if res:
            self.destroy()
            main_window(res, self.root)

    def on_close(self):
        if self.winfo_exists():
            for child in self.root.winfo_children():
                child.destroy()
            self.destroy()
            self.root.destroy()

    def __init__(self, root, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.root = root
        self.geometry("911x506")
        self.configure(bg="#E75656")
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.title("Login - ApexAgente")
        self.canvas = Canvas(
            self,
            bg="#E75656",
            height=506,
            width=911,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            508.00000000000006,
            0.0,
            911.0,
            506.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            62.00000000000006,
            68.99999999999997,
            anchor="nw",
            text="ApexAgente",
            fill="#FFFFFF",
            font=("Helvetica", 50 * -1, 'bold')
        )

        self.canvas.create_text(
            62.00000000000006,
            447.0,
            anchor="nw",
            text="© ApexAgente, 2023",
            fill="#FFFFFF",
            font=("Helvetica", 18 * -1, 'bold')
        )

        self.canvas.create_text(
            62.00000000000006,
            156.99999999999997,
            anchor="nw",
            text="ApexAgente is a software system",
            fill="#FFFFFF",
            font=("Helvetica", 20 * -1)
        )

        self.canvas.create_text(
            62.00000000000006,
            180.99999999999997,
            anchor="nw",
            text="designed to obtain data for",
            fill="#FFFFFF",
            font=("Helvetica", 20 * -1)
        )

        self.canvas.create_text(
            62.00000000000006,
            204.99999999999997,
            anchor="nw",
            text="the Apex agent on Trend Micro.",
            fill="#FFFFFF",
            font=("Helvetica", 20 * -1)
        )

        self.canvas.create_text(
            537.0,
            63.99999999999997,
            anchor="nw",
            text="Enter your login details.",
            fill="#E65656",
            font=("Helvetica", 26 * -1, 'bold')
        )

        self.canvas.create_text(
            537.0,
            103.99999999999997,
            anchor="nw",
            text="Enter the credentials that the admin gave",
            fill="#CCCCCC",
            font=("Helvetica", 16 * -1)
        )

        self.canvas.create_text(
            537.0,
            124.99999999999997,
            anchor="nw",
            text="you while signing up for the program",
            fill="#CCCCCC",
            font=("Helvetica", 16 * -1)
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_click(),
            relief="flat"
        )
        button_1.place(
            x=615.0,
            y=437.0,
            width=190.0,
            height=48.0
        )

        self.canvas.create_rectangle(
            527.0,
            223.99999999999997,
            893.0,
            264.0,
            fill="#EFEFEF",
            outline="")

        self.canvas.create_rectangle(
            527.0,
            312.0,
            893.0,
            352.0,
            fill="#EFEFEF",
            outline="")

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        self.canvas.create_image(
            709.5,
            244.49999999999997,
            image=entry_image_1
        )
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            fg="#000716",
            highlightthickness=0
        )
        self.username.place(
            x=568.0,
            y=235.99999999999997,
            width=283.0,
            height=15.0
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        self.canvas.create_image(
            709.5,
            331.5,
            image=entry_image_2
        )
        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#EFEFEF",
            fg="#000716",
            highlightthickness=0
        )
        self.password.place(
            x=568.0,
            y=323.0,
            width=283.0,
            height=15.0
        )

        self.canvas.create_text(
            537.0,
            294.0,
            anchor="nw",
            text="Password",
            fill="#E65656",
            font=("Helvetica", 14 * -1, 'bold')
        )

        self.canvas.create_text(
            537.0,
            204.99999999999997,
            anchor="nw",
            text="Username",
            fill="#E65656",
            font=("Helvetica", 14 * -1, 'bold')
        )
        self.resizable(False, False)
        self.mainloop()
