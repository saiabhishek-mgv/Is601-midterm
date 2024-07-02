from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, user_input: str):
        if not user_input.strip():
            raise ValueError("No input provided.")
        
        parts = user_input.split()
        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            return self.commands[command_name].execute(*args)
        else:
            raise ValueError(f"No such command: {command_name}")
