import logging
import pandas as pd
from decimal import Decimal
from typing import List
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
import os

class Calculations:
    file_path = os.getenv('HISTORY_FILE_PATH', 'calculation_history.csv')
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
        logging.info("Cleared the current instance history")
    
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
        logging.info("Saved current instance history to CSV file.")

    @classmethod
    def load_history(cls):
        """Load the calculation history from a CSV file into the current instance."""
        try:
            if not os.path.exists(cls.file_path) or os.path.getsize(cls.file_path) == 0:
                cls.history = []
                logging.info("No existing history to load from CSV file.")
                return
            df = pd.read_csv(cls.file_path)
            operations = {'add': add, 'subtract': subtract, 'multiply': multiply, 'divide': divide}
            cls.history = [Calculation(Decimal(row['a']), Decimal(row['b']), operations[row['operation']]) for _, row in df.iterrows()]
            logging.info("Loaded history from CSV file.")
        except Exception as e:
            print(f"Failed to load history: {e}")
            logging.error("Failed to load history: %s", e)
            cls.history = []

    @classmethod
    def delete_history(cls):
        """Delete the CSV file containing the history and clear in-memory history."""
        try:
            if os.path.exists(cls.file_path):
                os.remove(cls.file_path)
                print("History deleted successfully.")
                logging.info("Deleted history CSV file.")
                cls.clear_history()  # Clear in-memory history as well
            else:
                logging.warning("No history file found to delete.")
        except Exception as e:
            print(f"Failed to delete history: {e}")
            logging.error("Failed to delete history: %s", e)

    @classmethod
    def print_history(cls):
        """Print the current history of calculations."""
        for calc in cls.history:
            print(calc)
        logging.info("Printed current instance history.")