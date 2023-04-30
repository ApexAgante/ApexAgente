from prompt_toolkit.shortcuts import set_title, clear
import colorama
import click
from os import path, remove
from colorama import Fore, Style as ColorStyle
from prompt_toolkit import PromptSession
from rich.tree import Tree
from rich.console import Console

from .classes import TerminalCompleter, Commands, Prompt
from .functions import write_config, create_data, get_data

# Init colorama
colorama.init()

console = Console()
app = Commands(name="Commands")
prompt = Prompt()
session = PromptSession()


@click.command()
@click.option('--api', '-api', default=None, help="Your API key")
@click.option('--id', '-id', default=None, help="Your application ID")
@click.option('--url', '-url', default=None, help="Server URL")
@click.option('--n', is_flag=True, help="Use default Configuration")
def main(api, id, url, n):
    if path.isfile('config.json'):
        remove('config.json')

    if not n:
        if api is None:
            api = click.prompt("API Key")
        if id is None:
            id = click.prompt("Application ID")
        if url is None:
            url = click.prompt("Server URL")
        write_config(api, id, url)

    create_data()
    run()


@app.command(name="clear", help="Clear console")
def clear_command():
    clear()


@app.command(name="all", help="Get all data")
def all_command():
    data = get_data()
    data.get_all_data()


@app.command(name="get", help="Get a data from host name")
def get_command(host):
    data = get_data()
    data.get_data_by_host(host)


@app.command(name="quit", help="Quit from app")
def quit_command():
    raise KeyboardInterrupt


@app.command(name="help", help="Display all available commands")
def help_command():
    tree = Tree(":open_file_folder: Available commands",
                guide_style="bold bright_blue")
    for command, help in app.registered_help.items():
        tree.add(f"{command}").add(help)
    console.print(tree)
    print(ColorStyle.RESET_ALL)


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
    except (KeyboardInterrupt, EOFError):
        print(f"{Fore.RED} ❯")


if __name__ == "__main__":
    main()
