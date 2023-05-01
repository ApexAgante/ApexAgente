class ArgumentsError(Exception):
    def __init__(self, command: str, argument_number: int):
        self.command = command
        self.argument_total = argument_number
        super().__init__(command)


class CommandNotFound(Exception):
    def __init__(self):
        super().__init__()
