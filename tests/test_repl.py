"""
Tests for the CalculatorREPL class.
"""

import pytest
from calculator.repl import CalculatorREPL
from calculator.commands import CommandHandler

@pytest.fixture
def repl():
    """Fixture for CalculatorREPL instance."""
    return CalculatorREPL()

def test_repl_load_plugins(repl):  # pylint: disable=redefined-outer-name
    """Testing plugin"""
    assert repl.command_handler is not None
    assert isinstance(repl.command_handler, CommandHandler)
