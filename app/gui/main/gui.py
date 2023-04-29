from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Canvas, Frame, Button, PhotoImage, Toplevel, StringVar
from .dashboard.gui import Dashboard
from .get.gui import Get
from .all.gui import All

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")
MAIN_ASSETS_PATH = OUTPUT_PATH / Path(r"../assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def main_window(user: str, root):
    MainWindow(user, root)


class MainWindow(Toplevel):
    def on_button_enter(self, e, image):
        e.widget.configure(image=image)

    def on_button_leave(self, e, image):
        e.widget.configure(image=image)

    def on_close(self):
        if self.winfo_exists():
            for child in self.root.winfo_children():
                child.destroy()
            self.destroy()
            self.root.destroy()

    def __init__(self, user, root, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.user = user
        self.root = root
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        self.title('ApexAgente')
        self.geometry("911x506")
        self.current_window = None
        self.current_window_label = StringVar()

        self.configure(bg="#E75656")
        logo = PhotoImage(file=MAIN_ASSETS_PATH / "trend.png")
        self.tk.call('wm', 'iconphoto', self._w, logo)
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
            206.0,
            0.0,
            911.0,
            506.0,
            fill="#FFFFFF",
            outline="")

        self.sidebar_indicator = Frame(self, background="#FFFFFF")
        self.sidebar_indicator.place(x=0, y=133, height=47, width=7)

        self.canvas.create_text(
            21.0,
            42.0,
            anchor="nw",
            text="ApexAgente",
            fill="#FFFFFF",
            font=("Helvetica", 24 * -1, 'bold')
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))

        button_image_1_hover = PhotoImage(
            file=relative_to_assets("button_1_hover.png")
        )

        self.dashboard_btn = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handler_btn_press(self.dashboard_btn, "dash"),
            relief="flat"
        )
        self.dashboard_btn.place(
            x=7.0,
            y=133.0,
            width=199.0,
            height=47.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))

        button_image_2_hover = PhotoImage(
            file=relative_to_assets("button_2_hover.png")
        )

        self.get_data_btn = Button(
            self.canvas,
            image=button_image_2,
            background="#E75656",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handler_btn_press(self.get_data_btn, "get"),
            relief="flat"
        )
        self.get_data_btn.place(
            x=7.0,
            y=183.0,
            width=199.0,
            height=47.0,
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png")
        )

        button_image_3_hover = PhotoImage(
            file=relative_to_assets("button_3_hover.png")
        )

        self.all_data_btn = Button(
            self.canvas,
            image=button_image_3,
            background="#E75656",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handler_btn_press(self.all_data_btn, "all"),
            relief="flat"
        )

        self.all_data_btn.place(
            x=7.0,
            y=233.0,
            width=199.0,
            height=47.0
        )

        self.heading = self.canvas.create_text(
            254.0,
            42.0,
            anchor="nw",
            text="Hello",
            fill="#E65656",
            font=("Helvetica", 26 * -1, 'bold')
        )

        self.user = self.canvas.create_text(
            752.0,
            49.0,
            anchor="nw",
            text=self.user,
            fill="#808080",
            font=("Helvetica", 16 * -1, 'bold')
        )

        self.windows = {
            "dash": Dashboard(self),
            "get": Get(self),
            "all": All(self)
        }

        self.handler_btn_press(self.dashboard_btn, "dash")
        self.sidebar_indicator.place(x=0, y=133)
        self.current_window.place(x=215, y=72, width=912.0, height=506.0)
        self.current_window.tkraise()

        self.dashboard_btn.bind(
            "<Enter>", lambda e: self.on_button_enter(e, button_image_1_hover)
        )
        self.dashboard_btn.bind(
            "<Leave>", lambda e: self.on_button_leave(e, button_image_1))

        self.get_data_btn.bind(
            "<Enter>", lambda e: self.on_button_enter(e, button_image_2_hover)
        )
        self.get_data_btn.bind(
            "<Leave>", lambda e: self.on_button_leave(e, button_image_2)
        )

        self.all_data_btn.bind(
            "<Enter>", lambda e: self.on_button_enter(e, button_image_3_hover)
        )

        self.all_data_btn.bind(
            "<Leave>", lambda e: self.on_button_leave(e, button_image_3)
        )

        self.resizable(False, False)
        self.mainloop()

    def handler_btn_press(self, caller, name):
        self.sidebar_indicator.place(x=0, y=caller.winfo_y())
        for window in self.windows.values():
            window.place_forget()

        self.current_window = self.windows.get(name)
        self.windows[name].place(x=215, y=72, width=912.0, height=506.0)
        current_name = self.windows.get(name)._name.split("!")[-1].capitalize()
        self.canvas.itemconfigure(self.heading, text=current_name)
