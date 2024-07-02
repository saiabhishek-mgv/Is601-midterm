from calculator.commands import Command
from calculator.calculations import Calculations
import logging

class DeleteHistoryCommand(Command):
    def execute(self, *args):
        try:
            Calculations.delete_history()
        except Exception as e:
            print(f"Failed to delete history: {e}")
