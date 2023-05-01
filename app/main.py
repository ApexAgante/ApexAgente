import click

from os import path, remove
from colorama import Fore, Style as ColorStyle, init
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import set_title, clear
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from rich.tree import Tree
from rich.console import Console

from .classes import (TerminalCompleter, Commands, Prompt,
                      ArgumentsError, CommandNotFound)
from .functions import write_config, create_data, get_data

# Init colorama
init()

console = Console()
app = Commands(name="Commands")
prompt = Prompt()
session = PromptSession()
keys = KeyBindings()


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
    run_cli()


@app.command(name="clear", help="Clear console")
def clear_command():
    clear()


@app.command(name="all", help="Get all data")
def all_command():
    data = get_data()
    data.get_all_data()


@app.command(name="get", help="Get a data from host name")
def get_command(host=None):
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


@keys.add(Keys.ControlZ)
def _(event):
    raise KeyboardInterrupt


def run_cli():
    try:
        clear()
        set_title("Apex Agente")
        while True:
            command_input = session.prompt(prompt.prompt, style=prompt.style,
                                           refresh_interval=1,
                                           completer=TerminalCompleter(),
                                           complete_while_typing=True,
                                           complete_in_thread=True,
                                           key_bindings=keys)

            command_input_split = command_input.split()
            try:
                name = command_input_split[0]
                length = len(command_input_split)
                if name in app.registered_commands:
                    parameter_need = (app.registered_command_parameters[name])
                    if length > 0:
                        if length == parameter_need + 1:
                            parameter = command_input_split[1:]
                            app.registered_commands[name](*parameter)
                        else:
                            raise ArgumentsError(name, parameter_need)
                    else:
                        raise CommandNotFound
                else:
                    raise CommandNotFound
            except CommandNotFound:
                error_msg = "Invalid command. Type 'help' for a list of available commands"
                print(f"{Fore.RED}{error_msg}{Fore.RESET}")
            except ArgumentsError as a:
                error_msg = f"Invalid parameters. You need {a.argument_total} parameter(s) for {a.command}"
                print(f"{Fore.RED}{error_msg}{Fore.RESET}")
    except (KeyboardInterrupt, EOFError):
        print(f"{Fore.RED} ❯")
        raise SystemExit


if __name__ == "__main__":
    main()
