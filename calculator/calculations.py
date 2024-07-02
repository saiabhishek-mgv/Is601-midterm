import pandas as pd
from decimal import Decimal
from typing import List
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
import os

class Calculations:
    file_path = 'calculation_history.csv'
    history = []
    _cleared = False

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        """Add a new calculation to the history."""
        cls.history.append(calculation)
        cls._cleared = False

    @classmethod
    def get_history(cls) -> List[Calculation]:
        """Retrieve the entire history of calculations."""
        return cls.history
    
    @classmethod
    def clear_history(cls):
        """Clear the history of calculations."""
        cls.history.clear()
        cls._cleared = True
    
    @classmethod
    def get_latest(cls) -> Calculation:
        """Get the latest calculation. Returns None if there is no history."""
        if cls.history:
            return cls.history[-1]
        return None
    
    @classmethod
    def find_by_operation(cls, operation_name: str) -> List[Calculation]:
        """Find and return a list of calculations by name of the operation."""
        return [calc for calc in cls.history if calc.operation.__name__ == operation_name]
    
    @classmethod
    def save_history(cls):
        """Save the current instance history to a CSV file."""
        if cls._cleared:
            return
        
        data = [{
            'a': calc.a,
            'b': calc.b,
            'operation': calc.operation.__name__,
            'result': calc.perform()
        } for calc in cls.history]
        
        if os.path.exists(cls.file_path):
            existing_df = pd.read_csv(cls.file_path)
            new_df = pd.DataFrame(data)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates()
        else:
            combined_df = pd.DataFrame(data)
        
        combined_df.to_csv(cls.file_path, index=False)

    @classmethod
    def load_history(cls):
        """Load the calculation history from a CSV file into the current instance."""
        try:
            if not os.path.exists(cls.file_path) or os.path.getsize(cls.file_path) == 0:
                cls.history = []
                return
            df = pd.read_csv(cls.file_path)
            operations = {'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide}
            cls.history = [Calculation(Decimal(row['a']), Decimal(row['b']), operations[row['operation']]) for _, row in df.iterrows()]
        except Exception as e:
            print(f"Failed to load history: {e}")
            cls.history = []

    @classmethod
    def delete_history(cls):
        """Delete the CSV file containing the history and clear in-memory history."""
        try:
            if os.path.exists(cls.file_path):
                os.remove(cls.file_path)
                print("History deleted successfully.")
                cls.clear_history()  # Clear in-memory history as well
            else:
                print("No history file found to delete.")
        except Exception as e:
            print(f"Failed to delete history: {e}")

    @classmethod
    def print_history(cls):
        """Print the current history of calculations."""
        for calc in cls.history:
            print(calc)
