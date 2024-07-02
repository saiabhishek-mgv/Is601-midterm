import os
import importlib.util
from calculator.commands import CommandHandler, Command
from calculator.calculations import Calculations

class CalculatorREPL:
    def __init__(self, plugin_dir='plugins'):
        self.command_handler = CommandHandler()
        self.plugin_dir = plugin_dir
        self._load_plugins()
        Calculations.load_history()  # Load history on startup

    def _load_plugins(self):
        plugins_path = os.path.join(os.path.dirname(__file__), self.plugin_dir)
        if not os.path.exists(plugins_path):
            print(f"Plugin directory does not exist: {plugins_path}")
            return

        for subdir in os.listdir(plugins_path):
            subdir_path = os.path.join(plugins_path, subdir)
            if os.path.isdir(subdir_path):
                init_path = os.path.join(subdir_path, '__init__.py')
                if os.path.exists(init_path):
                    module_name = f"calculator.plugins.{subdir}"
                    spec = importlib.util.spec_from_file_location(module_name, init_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attr in dir(module):
                        if attr.endswith("Command"):
                            command_class = getattr(module, attr)
                            if callable(command_class) and issubclass(command_class, Command):
                                if command_class.__module__ == module_name:
                                    if attr == "MenuCommand":
                                        instance = command_class(self.command_handler)
                                    else:
                                        instance = command_class()
                                    command_name = instance.__class__.__name__.replace('Command', '').replace('_',' ').title()
                                    self.command_handler.register_command(command_name, instance)

    def start(self):
        print("Type 'Menu' to see the list of available commands or 'exit' to exit.")
        while True:
            try:
                user_input = input(">>> ").strip()
                if user_input.lower() == 'exit':
                    print("Exiting the calculator. Goodbye!")
                    break
                self.command_handler.execute_command(user_input)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            finally:
                 Calculations.save_history()  # Save history on exit

