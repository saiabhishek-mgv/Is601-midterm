"""
Tests for command plugins.
"""

from decimal import Decimal
import pytest
from calculator.calculations import Calculations
from calculator.plugins.add import AddCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.multiply import MultiplyCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.save import SaveHistoryCommand
from calculator.plugins.clear import ClearHistoryCommand
from calculator.plugins.print import PrintHistoryCommand
from calculator.plugins.menu import MenuCommand
from calculator.commands import CommandHandler

@pytest.fixture
def handler():
    """Fixture to create a CommandHandler instance."""
    return CommandHandler()

def test_add_command(handler):  # pylint: disable=redefined-outer-name
    """Test the add command."""
    command = AddCommand()
    handler.register_command('add', command)
    result = handler.execute_command('add 1 2')
    assert result == Decimal('3')

def test_subtract_command(handler):  # pylint: disable=redefined-outer-name
    """Test the subtract command."""
    command = SubtractCommand()
    handler.register_command('subtract', command)
    result = handler.execute_command('subtract 5 2')
    assert result == Decimal('3')

def test_subtract_command_valid():
    """Test the subtract command with valid inputs."""
    command = SubtractCommand()
    result = command.execute('5', '3')
    assert result == Decimal('2')

def test_subtract_command_invalid_args_count():
    """Test the subtract command with incorrect number of arguments."""
    command = SubtractCommand()
    with pytest.raises(ValueError, match="Subtract command requires exactly two arguments."):
        command.execute('5')

def test_subtract_command_decimal_error():
    """Test handling of InvalidOperation in decimal conversion."""
    command = SubtractCommand()
    with pytest.raises(ValueError, match="Invalid input for Decimal conversion."):
        command.execute('5', 'invalid')

def test_multiply_command(handler):  # pylint: disable=redefined-outer-name
    """Test the multiply command."""
    command = MultiplyCommand()
    handler.register_command('multiply', command)
    result = handler.execute_command('multiply 3 4')
    assert result == Decimal('12')

def test_multiply_command_invalid_args_count():
    """Test the multiply command with incorrect number of arguments."""
    command = MultiplyCommand()
    with pytest.raises(ValueError, match="Multiply command requires exactly two arguments."):
        command.execute('2')

def test_multiply_command_invalid_decimal_conversion():
    """Test the multiply command with invalid decimal inputs."""
    command = MultiplyCommand()
    with pytest.raises(ValueError, match="Invalid input for Decimal conversion."):
        command.execute('invalid', '3')

def test_divide_command(handler):  # pylint: disable=redefined-outer-name
    """Test the divide command."""
    command = DivideCommand()
    handler.register_command('divide', command)
    result = handler.execute_command('divide 8 2')
    assert result == Decimal('4')

def test_divide_by_zero(handler):  # pylint: disable=redefined-outer-name
    """Test division by zero."""
    command = DivideCommand()
    handler.register_command('Divide', command)
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        handler.execute_command('Divide 8 0')

def test_save_command(handler):  # pylint: disable=redefined-outer-name
    """Test the save command."""
    Calculations.clear_history()
    command = SaveHistoryCommand()
    handler.register_command('Savehistory', command)
    result = handler.execute_command('Savehistory')
    assert result is None  # save command does not return a result

def test_clear_command(handler):  # pylint: disable=redefined-outer-name
    """Test the clear command."""
    Calculations.clear_history()
    command = ClearHistoryCommand()
    handler.register_command('clear', command)
    handler.execute_command('clear')
    assert len(Calculations.get_history()) == 0

def test_print_history_command(handler, capsys):  # pylint: disable=redefined-outer-name
    """Test the print history command."""
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

def test_menu_command(handler, capsys):  # pylint: disable=redefined-outer-name
    """Test the menu command."""
    command = MenuCommand(handler)
    handler.register_command('menu', command)
    handler.execute_command('menu')
    captured = capsys.readouterr()
    assert "Available commands:" in captured.out
