from prompt_toolkit.shortcuts import set_title, clear
import colorama
from colorama import Fore, Style as ColorStyle
from prompt_toolkit import PromptSession

from .data import Data
from .completer import TerminalCompleter
from .commands import Commands
from .prompt import Prompt

app = Commands(name="Commands")
prompt = Prompt()
colorama.init()
session = PromptSession()

data = Data({
    'headers': '',
    'query': '?hostname',
    'body': '',
    'http_method': 'GET'
})


@app.command(name="clear", help="Clear console")
def clear_command():
    clear()


@app.command(name="all", help="Get all data")
def all_command():
    global data
    data.get_all_data()


@app.command(name="get", help="Get a data from host name")
def get_command(host):
    global data
    data.get_data_by_host(host)


@app.command(name="help", help="Display all available commands")
def help_command():
    print(Fore.GREEN + "Available commands")
    for command, help in app.registered_help.items():
        print(f" - {command}: {help}")
    print(ColorStyle.RESET_ALL)


prompt.get_prompt()


def run():
    try:
        clear()
        set_title("Simple-ApexAgente")
        while True:
            # Prompt user for command input using prompt-toolkit
            command_input = session.prompt(prompt.prompt, style=prompt.style,
                                           refresh_interval=1,
                                           completer=TerminalCompleter(),
                                           complete_while_typing=True,
                                           complete_in_thread=True)
            # Look up and execute the corresponding command function
            command_input_split = command_input.split()
            try:
                if command_input_split[0] in app.registered_commands:
                    if len(command_input_split) == 1:
                        app.registered_commands[command_input_split[0]]()
                    elif len(command_input_split) == 2 and command_input_split[0] == 'get':
                        app.registered_commands[command_input_split[0]](
                            command_input_split[1])
                    else:
                        raise ValueError
                else:
                    raise KeyError
            except (KeyError, ValueError):
                error_msg = "Invalid command. Type 'help' for a list of available commands."
                print(f"{Fore.RED}{error_msg}{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Fore.RED} ❯")


if __name__ == "__main__":
    run()
