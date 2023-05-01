class ArgumentsError(Exception):
    def __init__(self, command: str, argument_number: int, argument: int):
        self.command = command
        self.argument_need = argument_number
        self.argument = argument
        super().__init__(command)


class CommandNotFound(Exception):
    def __init__(self):
        super().__init__()
