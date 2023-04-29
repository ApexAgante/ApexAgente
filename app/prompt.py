from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import (
    HTML,
    fragment_list_width,
    merge_formatted_text,
    to_formatted_text,
)
from prompt_toolkit.application import get_app
from datetime import datetime


class Prompt:
    def __init__(self):
        self.style = Style.from_dict(
            {
                "username": "#aaaaaa",
                "path": "#1294ff bold",
                "branch": "#5fd700 bold bg:#1c1c1c",
                "env": "bg:#1c1c1c",
                "left-part": "bg:#1c1c1c",
                "right-part": "bg:#1c1c1c",
                "time": "#5f8787",
                "cursor": "ansibrightred blink",
            }
        )
        self.prompt = None

    def get_prompt(self) -> HTML:
        """
        Build the prompt dynamically every time its rendered.
        """
        left_part = HTML(
            "╭─"
            "<left-part>"
            " <username></username>   "
            "<path>/home/apexagente</path>"
            "  on "
            "<branch>   main  </branch>"
            "</left-part>"
        )
        right_part = HTML(
            "<right-part> "
            " <env> python </env> "
            "at"
            " <time>%s  </time>"
            "</right-part>"
        ) % (datetime.now().strftime("%H:%M:%S"),)

        used_width = sum(
            [
                fragment_list_width(to_formatted_text(left_part)),
                fragment_list_width(to_formatted_text(right_part)),
            ]
        )

        total_width = get_app().output.get_size().columns
        padding_size = total_width - used_width

        padding = HTML("<padding>%s</padding>") % (" " * padding_size,)
        self.prompt = merge_formatted_text(
            [left_part, padding, right_part, "\n", "╰─ "]
        )
