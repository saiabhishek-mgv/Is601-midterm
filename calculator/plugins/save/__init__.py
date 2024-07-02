from calculator.commands import Command
from calculator.calculations import Calculations

class SaveHistoryCommand(Command):
    def execute(self, *args):
        try:
            Calculations.save_history()
            print("History saved successfully.")
        except Exception as e:
            print(f"Failed to save history: {e}")
