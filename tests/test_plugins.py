"""
Tests for command plugins.
"""
from decimal import Decimal
from unittest.mock import MagicMock, patch
import pytest
from calculator import Calculator
from calculator.calculations import Calculations
from calculator.plugins.add import AddCommand
from calculator.plugins.delete import DeleteHistoryCommand
from calculator.plugins.load import LoadHistoryCommand
from calculator.plugins.subtract import SubtractCommand
from calculator.plugins.multiply import MultiplyCommand
from calculator.plugins.divide import DivideCommand
from calculator.plugins.save import SaveHistoryCommand
from calculator.plugins.clear import ClearHistoryCommand
from calculator.plugins.print import PrintHistoryCommand
from calculator.plugins.menu import MenuCommand
from calculator.commands import CommandHandler
# pylint: disable =missing-function-docstring
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

def test_add_command_invalid_arguments():
    # Test invalid number of arguments
    command = AddCommand()
    with pytest.raises(ValueError, match="Add command requires exactly two arguments."):
        command.execute('1')

def test_add_command_invalid_decimal():
    # Test invalid decimal conversion
    command = AddCommand()
    with pytest.raises(ValueError, match="Invalid input for Decimal conversion."):
        command.execute('1', 'invalid')

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

def test_divide_command_success():
    # Test successful division
    with patch.object(Calculator, 'divide', return_value=Decimal('2')):
        command = DivideCommand()
        with patch('builtins.print') as mock_print:
            result = command.execute('4', '2')
            assert result == Decimal('2')
            mock_print.assert_called_with("Result: 2")

def test_divide_command_invalid_arguments():
    # Test invalid number of arguments
    command = DivideCommand()
    with pytest.raises(ValueError, match="Divide command requires exactly two arguments."):
        command.execute('4')

def test_divide_command_invalid_decimal():
    # Test invalid decimal conversion
    command = DivideCommand()
    with pytest.raises(ValueError, match="Invalid input for Decimal conversion."):
        command.execute('4', 'invalid')

def test_divide_command_zero_division():
    # Test division by zero
    command = DivideCommand()
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero."):
        command.execute('4', '0')

def test_divide_command_other_value_error():
    # Test other value errors
    command = DivideCommand()
    with pytest.raises(ValueError, match="Divide command requires exactly two arguments."):
        command.execute('4', '2', 'extra')

def test_save_command(handler):  # pylint: disable=redefined-outer-name
    """Test the save command."""
    Calculations.clear_history()
    command = SaveHistoryCommand()
    handler.register_command('Savehistory', command)
    result = handler.execute_command('Savehistory')
    assert result is None  # save command does not return a result

def test_clear_command(handler):  #pylint: disable=redefined-outer-name
    """Test the clear command."""
    Calculations.clear_history()
    command = ClearHistoryCommand()
    handler.register_command('clear', command)
    handler.execute_command('clear')
    assert len(Calculations.get_history()) == 0

def test_print_history_command(handler, capsys):  #pylint: disable=redefined-outer-name
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

def test_menu_command():
    # Mock the command handler with some commands
    mock_command_handler = MagicMock()
    mock_command_handler.commands = {
        'add': MagicMock(),
        'subtract': MagicMock(),
        'multiply': MagicMock(),
        'divide': MagicMock(),
        'menu': MagicMock()
    }
    # Instantiate the MenuCommand with the mock command handler
    command = MenuCommand(mock_command_handler)
    # Capture the output
    with patch('builtins.print') as mock_print:
        command.execute()
        # Check that the output contains the expected commands, excluding 'menu'
        mock_print.assert_any_call("Available commands:")
        mock_print.assert_any_call("- add")
        mock_print.assert_any_call("- subtract")
        mock_print.assert_any_call("- multiply")
        mock_print.assert_any_call("- divide")
        #mock_print.assert_any_call("- menu")

def test_load_history_success():
    # Test successful loading of history
    with patch.object(Calculations, 'load_history') as mock_load_history:
        command = LoadHistoryCommand()
        with patch('builtins.print') as mock_print:
            command.execute()
            mock_load_history.assert_called_once()
            mock_print.assert_called_with("History loaded successfully.")

def test_load_history_failure():
    # Test failure to load history
    with patch.object(Calculations, 'load_history', side_effect=Exception("Error loading history")):
        command = LoadHistoryCommand()
        with patch('builtins.print') as mock_print:
            command.execute()
            mock_print.assert_called_with("Failed to load history: Error loading history")

def test_delete_history_success():
    # Test successful deletion of history
    with patch.object(Calculations, 'delete_history') as mock_delete_history:
        command = DeleteHistoryCommand()
        command.execute()
        mock_delete_history.assert_called_once()

def test_delete_history_failure():
    # Test failure to delete history
    with patch.object(Calculations, 'delete_history', side_effect=Exception("Error deleting history")): #pylint: disable=line-too-long
        command = DeleteHistoryCommand()
        with patch('builtins.print') as mock_print:
            command.execute()
            mock_print.assert_called_with("Failed to delete history: Error deleting history")

def test_clear_history_success():
    # Test successful clearing of history
    with patch.object(Calculations, 'clear_history') as mock_clear_history:
        command = ClearHistoryCommand()
        with patch('builtins.print') as mock_print:
            command.execute()
            mock_clear_history.assert_called_once()
            mock_print.assert_called_with("History cleared successfully.")

def test_clear_history_failure():
    # Test failure to clear history
    with patch.object(Calculations, 'clear_history', side_effect=Exception("Error clearing history")): #pylint: disable=line-too-long
        command = ClearHistoryCommand()
        with patch('builtins.print') as mock_print:
            command.execute()
            mock_print.assert_called_with("Failed to clear history: Error clearing history")
