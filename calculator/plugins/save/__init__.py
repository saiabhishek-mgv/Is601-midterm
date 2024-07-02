from calculator.commands import Command
from calculator.calculations import Calculations

class SaveHistoryCommand(Command):
    def execute(self, *args):
        Calculations.save_history()
        print("History saved successfully.")

