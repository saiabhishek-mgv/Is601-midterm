from calculator.commands import Command
from calculator.calculations import Calculations

class PrintHistoryCommand(Command):
    def execute(self, *args):
        history = Calculations.get_history()
        if not history:
            print("No history available.")
        else:
            for calc in history:
                print(calc)
