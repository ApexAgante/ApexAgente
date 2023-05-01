from typing import Optional, Dict
from inspect import signature


class Commands:
    def __init__(self, *, name: Optional[str] = 'Command'):
        self.name = name
        self.registered_commands: Dict[str, any] = {}
        self.registered_help: Dict[str, Optional[str]] = {}
        self.registered_command_parameters: Dict[str, int] = {}

    def command(self,
                name: Optional[str] = None,
                *,
                help: Optional[str] = None):
        def decorator(f):
            parameter_total = len(signature(f).parameters)
            self.registered_commands[name] = f
            self.registered_command_parameters[name] = parameter_total
            self.registered_help[name] = help
            return f
        return decorator
