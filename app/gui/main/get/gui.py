from pathlib import Path
from tkinter import Frame, Canvas, Button, PhotoImage, Entry
from tkinter.ttk import Treeview, Style
from model import Data

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def get():
    Get()


class Get(Frame):

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
            text="View Data",
            fill="#E65656",
            font=("Arial", 26 * -1, "bold")
        )

        canvas.create_text(
            49.0,
            65.0,
            anchor="nw",
            text="Check data",
            fill="#808080",
            font=("Arial", 16 * -1, "bold")
        )

        canvas.create_rectangle(
            49.0,
            101.0,
            656.0,
            400.0,
            fill="#EFEFEF",
            outline="")

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.reload = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.reload.place(
            x=393.0,
            y=33.0,
            width=53.0,
            height=53.0
        )

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            556.0,
            59.0,
            image=self.image_image_1
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            594.5,
            60.0,
            image=self.entry_image_1
        )
        self.search_box = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            fg="#000716",
            highlightthickness=0
        )
        self.search_box.place(
            x=501.0,
            y=48.0,
            width=147.0,
            height=22.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.search = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.search.place(
            x=470.0,
            y=48.0,
            width=24.0,
            height=25.0
        )

        self.columns = {
            "Name": ["Name", 150],
            "Value": ["Value", 150]
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
        self.last_focus = None

        self.search.bind("<Enter>", lambda e: self.on_search_click(e))

    def get_data(self, host: str):
        data = self.data_parent.fetch_data_from_host_name(host)
        return data

    def on_reload_click(self, e):
        if self.host is not None:
            data = self.get_data(self.host)
            if data:
                self.refresh_data(data)

    def on_search_click(self, e):
        host = self.search_box.get()
        if self.host is None or self.host != host:
            self.host = host
        self.search_box.delete(first=0, last=len(host) - 1)
        data = self.get_data(self.host)
        if data:
            self.refresh_data(data)

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

    def refresh_data(self, data):
        self.treeview.delete(*self.treeview.get_children())
        data_res = [
            {
                "key": "ID",
                "value": data['entity_id']
            },
            {
                "key": "Host Name",
                "value": data['host_name']
            },
            {
                "key": "IP Address",
                "value": data['ip_address_list']
            },
            {
                "key": "Status",
                "value": data['connection_status']
            }
        ]
        for data in data_res:
            key = data['key']
            value = data['value']
            row = (key, value)
            self.treeview.insert("", "end", values=row)
