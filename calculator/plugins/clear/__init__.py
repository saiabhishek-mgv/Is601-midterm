from calculator.commands import Command
from calculator.calculations import Calculations

class ClearHistoryCommand(Command):
    def execute(self, *args):
        try:
            Calculations.clear_history()
            print("History cleared successfully.")
        except Exception as e:
            print(f"Failed to clear history: {e}")

