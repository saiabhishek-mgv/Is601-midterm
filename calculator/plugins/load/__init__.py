from calculator.commands import Command
from calculator.calculations import Calculations

class LoadHistoryCommand(Command):
    def execute(self, *args):
        try:
            Calculations.load_history()
            print("History loaded successfully.")
        except Exception as e:
            print(f"Failed to load history: {e}")
