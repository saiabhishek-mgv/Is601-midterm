# Advanced Python Calculator

This project is an advanced Python-based calculator application designed to demonstrate professional software development practices. The application integrates clean, maintainable code, the application of design patterns, logging, dynamic configuration via environment variables, data handling with Pandas, and a command-line interface (REPL) for real-time user interaction.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Usage Examples](#usage-examples)
- [Architectural Decisions](#architectural-decisions)
  - [Design Patterns](#design-patterns)
  - [Logging Strategy](#logging-strategy)

## Setup Instructions

### Prerequisites

- Python 
- `pip` (Python package installer)

### Installation

1. Clone the repo
2. Install virtual environment
3. pip install -r requirements.txt
4. Create and add the following to the .env file
    HISTORY_FILE_PATH=calculation_history.csv
    PLUGIN_DIR=plugins

## Usage Examples
#### Running the Calculator
1. Start the interface by  running the command: python main.py
2. Add <num1> <num2>: Adds two numbers.
3. Subtract <num1> <num2>: Subtracts the second number from the first.
4. Multiply <num1> <num2>: Multiplies two numbers.
5. Divide <num1> <num2>: Divides the first number by the second.
6. Loadhistory: Loads calculation history from the CSV file.
7. Savehistory: Saves the current instance history to the CSV file.
8. Clearhistory: Clears the current instance history.
9. Deletehistory: Deletes the CSV file containing the history.
10. Menu: Displays a list of available commands.
11. Exit: Exits the calculator.

## Architectural Decisions
### Design Patterns
This project leverages several design patterns to enhance code structure, flexibility, and scalability:

### Facade Pattern:

Used to provide a simplified interface for complex Pandas data manipulations.
The CalculationsFacade class encapsulates all interactions with the Pandas library, providing simple methods for loading, saving, and manipulating calculation history.
https://github.com/saiabhishek-mgv/Is601-midterm/blob/main/calculator/calculations.py

### Command Pattern:

Used to encapsulate all calculator commands as objects.
Each command (e.g., AddCommand, SubtractCommand) implements the Command interface, allowing for easy addition of new commands without modifying the core application logic.

### Factory Method:

Used to create instances of calculation commands dynamically.
The plugin system dynamically loads and registers commands found in the calculator/plugins directory.

### Singleton Pattern:

Ensures a single instance of the CommandHandler and Calculator classes.
These classes manage the registration and execution of commands, ensuring consistent behavior across the application.

### Strategy Pattern:

Used to encapsulate arithmetic operations as individual strategies.
The Calculator class delegates arithmetic operations to specific strategy functions (e.g., add, subtract).
