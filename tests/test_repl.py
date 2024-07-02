"""
Tests for the CalculatorREPL class.
"""
import os
import logging
from unittest.mock import patch, MagicMock
import pytest
from calculator.calculations import Calculations
from calculator.repl import CalculatorREPL
from calculator.commands import CommandHandler

#pylint: disable=redefined-outer-name, line-too-long

@pytest.fixture
def repl():
    """Fixture for CalculatorREPL instance."""
    return CalculatorREPL()

def test_repl_load_plugins(repl):  # pylint: disable=redefined-outer-name
    """Testing plugin"""
    assert repl.command_handler is not None
    assert isinstance(repl.command_handler, CommandHandler)

# Helper function to create a temporary environment
@pytest.fixture
def setup_environment(tmp_path):
    """defining setup_environment"""
    os.chdir(tmp_path)
    yield
    os.chdir("..")

def test_log_directory_creation():
    """Test log directory creation"""
    CalculatorREPL()
    assert os.path.exists('logs')

def test_logging_configuration_without_file():
    """Test logging configuration when logging.conf does not exist"""
    with patch('os.path.exists', side_effect=lambda x: x != 'logging.conf'), patch('logging.basicConfig') as mock_basic_config:
        CalculatorREPL()
        mock_basic_config.assert_called_once_with(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_logging_configuration_with_file():
    """Test logging configuration when logging.conf exists"""
    with open('logging.conf', 'w') as f: #pylint: disable=unspecified-encoding
        f.write("[loggers]\nkeys=root\n"
                "[handlers]\nkeys=consoleHandler\n"
                "[formatters]\nkeys=simpleFormatter\n"
                "[logger_root]\nlevel=INFO\nhandlers=consoleHandler\n"
                "[handler_consoleHandler]\nclass=StreamHandler\nlevel=INFO\nformatter=simpleFormatter\nargs=(sys.stdout,)\n"
                "[formatter_simpleFormatter]\nformat=%(asctime)s - %(levelname)s - %(message)s\n")
    with patch('logging.config.fileConfig') as mock_file_config:
        CalculatorREPL()
        mock_file_config.assert_called_once_with('logging.conf', disable_existing_loggers=False)

def test_start_method_exit():
    """Test the start method for exit command"""
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['exit']):
        with patch.object(repl, '_load_plugins'):
            repl.start()

def test_start_method_value_error():
    """Test the start method handling a ValueError"""
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['Add 1 a', 'exit']):
        with patch.object(repl, '_load_plugins'):
            repl.command_handler.execute_command = MagicMock(side_effect=ValueError("Invalid input"))
            repl.start()

def test_start_method_unexpected_error():
    """Test the start method handling an unexpected error"""
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['Add 1 2', 'exit']):
        with patch.object(repl, '_load_plugins'):
            repl.command_handler.execute_command = MagicMock(side_effect=Exception("Unexpected error"))
            repl.start()

def test_save_history_on_exit():
    """Test saving history on exit"""
    repl = CalculatorREPL()
    with patch('builtins.input', side_effect=['exit']):
        with patch.object(Calculations, 'save_history') as mock_save_history:
            with patch.object(repl, '_load_plugins'):
                repl.start()
            mock_save_history.assert_called_once()
