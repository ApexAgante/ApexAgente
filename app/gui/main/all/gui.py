from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage
from tkinter.ttk import Treeview, Style
from model import Data

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def all():
    All()


class All(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg="#FFFFFF")
        self.data_parent = Data({
            'headers': '',
            'query': '?hostname',
            'body': '',
            'http_method': 'GET'
        })
        self.host = None
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
        canvas.create_rectangle(
            40.0,
            14.0,
            656.0,
            16.0,
            fill="#EFEFEF",
            outline="")

        canvas.create_rectangle(
            47.0,
            415.0,
            656.0,
            417.0,
            fill="#EFEFEF",
            outline="")

        canvas.create_text(
            49.0,
            33.0,
            anchor="nw",
            text="All Data",
            fill="#E65656",
            font=("Montserrat Bold", 26 * -1)
        )

        canvas.create_text(
            49.0,
            65.0,
            anchor="nw",
            text="Obtain every data",
            fill="#808080",
            font=("Montserrat SemiBold", 16 * -1)
        )

        canvas.create_rectangle(
            49.0,
            101.0,
            656.0,
            400.0,
            fill="#EFEFEF",
            outline="")

        self.reload_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.reload = Button(
            self,
            image=self.reload_image_1,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.reload.place(
            x=603.0,
            y=33.0,
            width=53.0,
            height=53.0
        )

        self.columns = {
            "ID": ["ID", 15],
            "Entity ID": ["Entity ID", 200],
            "Host Name": ["Host Name", 140],
            "IP Address": ["IP Address", 120],
            "Status": ["Status", 40]
        }

        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview",
                             background="#EFEFEF",
                             foreground="black",
                             fieldbackground="#EFEFEF")
        self.style.configure("Treeview.Heading",
                             background="#E75656",
                             foreground="#EFEFEF",
                             relief="flat")

        self.style.map("Treeview",
                       background=[('selected', '#E75656'),
                                   ('active', '#151515')]
                       )

        self.style.map("Treeview.Heading",
                       background=[('active', '#E75656')]
                       )

        self.treeview = Treeview(
            self,
            columns=list(self.columns.keys()),
            show="headings",
            height=200,
            selectmode="browse"
        )

        for idx, txt in self.columns.items():
            self.treeview.heading(idx, text=txt[0])
            self.treeview.column(idx, width=txt[1])

        self.treeview.place(x=49, y=101, width=607, height=299)
        self.treeview.tag_configure('focus', background="#d9d7d7")
        self.treeview.bind("<Motion>", self.on_motion)
        self.treeview.bind("<1>", self.on_select)
        self.reload.bind("<Enter>", lambda e: self.on_reload_click(e))
        self.last_focus = None

    def on_select(self, e):
        selection = e.widget.selection()
        _iid = e.widget.identify_row(e.y)
        if _iid in selection:
            e.widget.selection_remove(_iid)
            return "break"

    def on_motion(self, e):
        _iid = self.treeview.identify_row(e.y)
        if _iid != self.last_focus:
            if self.last_focus:
                self.treeview.item(self.last_focus, tags=[])
            self.treeview.item(_iid, tags=['focus'])
            self.last_focus = _iid

    def get_data(self):
        data = self.data_parent.fetch_data()
        if data:
            return data

    def on_reload_click(self, e):
        self.refresh_data()

    def refresh_data(self):
        data = self.get_data()
        if data:
            self.treeview.delete(*self.treeview.get_children())
            count = 0
            for d in data:
                count += 1
                entity_id = d['entity_id']
                host_name = d['host_name']
                ip = d['ip_address_list']
                status = d['connection_status']
                row = (count, entity_id, host_name, ip, status)
                self.treeview.insert("", "end", values=row)
