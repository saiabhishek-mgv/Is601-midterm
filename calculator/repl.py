import logging
import logging.config
import os
import importlib.util
from dotenv import load_dotenv
from calculator.commands import CommandHandler, Command
from calculator.calculations import Calculations

class CalculatorREPL:
    def __init__(self, plugin_dir='plugins'):
        if not os.path.exists('logs'):
            os.makedirs('logs')
        self.configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.plugin_dir = self.settings.get('PLUGIN_DIR', 'plugins')
        self._load_plugins()
        #Calculations.load_history()  # Load history on startup
    
    def configure_logging(self):
        logging_conf_path = 'logging.conf'
        if os.path.exists(logging_conf_path):
            logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)
        else:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info("Logging configured.")
    def load_environment_variables(self):
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

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
                                    command_name = instance.__class__.__name__.replace('Command', '').replace('_', ' ').title()
                                    self.command_handler.register_command(command_name, instance)

    def start(self):
        print("Type 'Menu' to see the list of available commands or 'Exit' to exit.")
        try:
            while True:
                user_input = input(">>> ").strip()
                if user_input.lower() == 'exit':
                    print("Exiting the calculator. Goodbye!")
                    logging.info("Exiting the calculator.")
                    break
                try:
                    self.command_handler.execute_command(user_input)
                except ValueError as e:
                    print(f"Error: {e}")
                    logging.error("Error executing command: %s", e)
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    logging.error("An unexpected error occurred: %s", e)
        finally:
            Calculations.save_history()  # Save history on exit
