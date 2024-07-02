from decimal import Decimal, InvalidOperation
from calculator.commands import Command
from calculator import Calculator

class SubtractCommand(Command):
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Subtract command requires exactly two arguments.")
        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
            result = Calculator.subtract(a, b)
            print(f"Result: {result}")
            return result
        except InvalidOperation:
            raise ValueError("Invalid input for Decimal conversion.")
