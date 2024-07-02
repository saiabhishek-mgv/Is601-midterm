from calculator.commands import Command
from calculator.calculations import Calculations

class PrintHistoryCommand(Command):
    def execute(self, *args):
        history = Calculations.print_history()
