# Advanced Python Calculator

This project is an advanced Python-based calculator application developed as part of a software engineering graduate course. It demonstrates professional software development practices, including clean and maintainable code, the use of design patterns, comprehensive logging, dynamic configuration via environment variables, sophisticated data handling with Pandas, and a command-line interface (REPL) for real-time user interaction.

## Project Overview

The Advanced Python Calculator supports the following core functionalities:

- **Command-Line Interface (REPL)**: Facilitates direct interaction with the calculator, supporting arithmetic operations (Add, Subtract, Multiply, and Divide) and calculation history management.
- **Plugin System**: Allows seamless integration of new commands or features, dynamically loading and integrating plugins without modifying the core application code.
- **Calculation History Management**: Utilizes Pandas to manage a robust calculation history, enabling users to load, save, clear, and delete history records through the REPL interface.
- **Professional Logging Practices**: Establishes a comprehensive logging system to record detailed application operations, data manipulations, errors, and informational messages, with dynamic logging configuration through environment variables.
- **Advanced Data Handling with Pandas**: Employs Pandas for efficient data reading and writing to CSV files, managing calculation history.
- **Design Patterns**: Incorporates key design patterns to address software design challenges, including Facade Pattern, Command Pattern, Factory Method, Singleton, and Strategy Patterns.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Usage Examples](#usage-examples)
- [Architectural Decisions](#architectural-decisions)
  - [Design Patterns](#design-patterns)
  - [Logging Strategy](#logging-strategy)

## Setup Instructions

### Installation

1. Clone the repo
2. Install virtual environment
3. Activate the virtual environment
4. pip install -r requirements.txt
5. Create and add the following to the .env file
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
[View code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/25a5de89f5fbbf0b0c39e99eede753738d7ab870/calculator/calculations.py#L9C1-L30C61)

### Command Pattern:

Used to encapsulate all calculator commands as objects.
Each command (e.g., AddCommand, SubtractCommand) implements the Command interface, allowing for easy addition of new commands without modifying the core application logic.
[View code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/6d9694dfb9a2f3919d349f89fcd6688a9c934907/calculator/commands/__init__.py#L3)

### Factory Method:

Used to create instances of calculation commands dynamically.
The plugin system dynamically loads and registers commands found in the calculator/plugins directory.
[View code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/20d6c592590a067d78111d1c9fd0ce8c091ffe15/calculator/repl.py#L34)

### Strategy Pattern:

Used to encapsulate arithmetic operations as individual strategies.
The Calculator class delegates arithmetic operations to specific strategy functions (e.g., add, subtract).

## Logging Strategy
The project employs a comprehensive logging strategy to record detailed application operations, data manipulations, errors, and informational messages. The logging configuration is managed through a logging.conf file.

### Logging Levels:

DEBUG: Detailed information, typically of interest only when diagnosing problems.
INFO: Confirmation that things are working as expected. [view code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/20d6c592590a067d78111d1c9fd0ce8c091ffe15/calculator/repl.py#L28)
WARNING: An indication that something unexpected happened, or indicative of some problem in the near future.
ERROR: Due to a more serious problem, the software has not been able to perform some function. [view code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/20d6c592590a067d78111d1c9fd0ce8c091ffe15/calculator/repl.py#L74)

### Configuration:

Logging configurations are loaded from logging.conf if it exists, otherwise default configurations are applied.

Logs are written to a log file located in the logs directory.
The console output is minimized to only display critical information, while detailed logs are maintained in the log file.

## Exception Handling
The project uses both "Look Before You Leap" (LBYL) and "Easier to Ask for Forgiveness than Permission" (EAFP) approaches for exception handling. Here are some examples:

### LBYL: Checking conditions before performing operations.

[View Code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/20d6c592590a067d78111d1c9fd0ce8c091ffe15/calculator/repl.py#L24)

### EAFP: Trying to perform an operation and handling exceptions if it fails.

[View Code](https://github.com/saiabhishek-mgv/Is601-midterm/blob/20d6c592590a067d78111d1c9fd0ce8c091ffe15/calculator/repl.py#L67)


## Video Demonstration
[view demo]()

