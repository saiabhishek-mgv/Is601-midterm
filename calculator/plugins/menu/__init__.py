from calculator.commands import Command

class MenuCommand(Command):
    def __init__(self, command_handler):
        self.command_handler = command_handler

    def execute(self, *args):
        print("Available commands:")
        # Get and sort commands by length and then alphabetically
        sorted_commands = sorted(
            [cmd for cmd in self.command_handler.commands if cmd != 'menu'],
            key=lambda cmd: (len(cmd), cmd)
        )
        
        # Print sorted commands
        for command_name in sorted_commands:
            print(f"- {command_name.capitalize()}")
