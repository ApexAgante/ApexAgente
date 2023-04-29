from typing import Optional, Dict


class Commands:
    def __init__(self, *, name: Optional[str] = 'Command'):
        self.name = name
        self.registered_commands: Dict[str, any] = {}
        self.registered_help: Dict[str, Optional[str]] = {}

    def command(self,
                name: Optional[str] = None,
                *,
                help: Optional[str] = None):
        def decorator(f):
            self.registered_commands[name] = f
            self.registered_help[name] = help
            return f
        return decorator
