import pytest
from calculator.repl import CalculatorREPL
from calculator.commands import CommandHandler

@pytest.fixture
def repl():
    return CalculatorREPL()

def test_repl_load_plugins(repl):
    assert repl.command_handler is not None
    assert isinstance(repl.command_handler, CommandHandler)

