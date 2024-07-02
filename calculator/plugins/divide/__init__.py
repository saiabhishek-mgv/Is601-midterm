from decimal import Decimal, InvalidOperation
from calculator.commands import Command
from calculator import Calculator

class DivideCommand(Command):
    def execute(self, *args):
        if len(args) != 2:
            raise ValueError("Divide command requires exactly two arguments.")
        try:
            a = Decimal(args[0])
            b = Decimal(args[1])
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero.")
            result = Calculator.divide(a, b)
            print(f"Result: {result}")
            return result
        except InvalidOperation:
            raise ValueError("Invalid input for Decimal conversion.")
        except ZeroDivisionError as e:
            print(e)
            raise e  # Re-raise the ZeroDivisionError
