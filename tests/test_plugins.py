import pytest
from calculator.calculations import Calculations
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.multiply import MultiplyCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.load import LoadHistoryCommand
from calculator.plugins.save import SaveHistoryCommand
from calculator.plugins.clear import ClearHistoryCommand
from calculator.plugins.print import PrintHistoryCommand
from calculator.plugins.menu import MenuCommand
from calculator.commands import CommandHandler
from decimal import Decimal

@pytest.fixture
def handler():
    return CommandHandler()

def test_add_command(handler):
    command = AddCommand()
    handler.register_command('add', command)
    result = handler.execute_command('add 1 2')
    assert result == Decimal('3')

def test_subtract_command(handler):
    command = SubtractCommand()
    handler.register_command('subtract', command)
    result = handler.execute_command('subtract 5 2')
    assert result == Decimal('3')

def test_multiply_command(handler):
    command = MultiplyCommand()
    handler.register_command('multiply', command)
    result = handler.execute_command('multiply 3 4')
    assert result == Decimal('12')

def test_divide_command(handler):
    command = DivideCommand()
    handler.register_command('divide', command)
    result = handler.execute_command('divide 8 2')
    assert result == Decimal('4')

def test_divide_by_zero(handler):
    command = DivideCommand()
    handler.register_command('Divide', command)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        handler.execute_command('Divide 8 0')

def test_load_command(handler):
    Calculations.clear_history()
    command = LoadHistoryCommand()
    handler.register_command('Loadhistory', command)
    Calculations.add_calculation(Calculations.get_latest())
    command2 = SaveHistoryCommand()
    handler.register_command('Savehistory', command2)   
    handler.execute_command('Savehistory')
    Calculations.clear_history()
    handler.execute_command('Loadhistory')
    assert len(Calculations.get_history()) == 0

def test_save_command(handler):
    Calculations.clear_history()
    command = SaveHistoryCommand()
    handler.register_command('Savehistory', command)
    result = handler.execute_command('Savehistory')
    assert result is None  # save command does not return a result

def test_clear_command(handler):
    Calculations.clear_history()
    command = ClearHistoryCommand()
    handler.register_command('clear', command)
    handler.execute_command('clear')
    assert len(Calculations.get_history()) == 0

def test_print_history_command(handler, capsys):
    Calculations.clear_history()
    # Add a calculation to the history
    add_command = AddCommand()
    handler.register_command('Add', add_command)
    handler.execute_command('Add 1 2')

    command = PrintHistoryCommand()
    handler.register_command('Printhistory', command)
    handler.execute_command('Printhistory')
    captured = capsys.readouterr()
    assert "Calculation" in captured.out

def test_menu_command(handler, capsys):
    command = MenuCommand(handler)
    handler.register_command('menu', command)
    handler.execute_command('menu')
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out
