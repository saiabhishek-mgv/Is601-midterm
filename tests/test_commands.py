"""
Tests for commands.
"""

import pytest
from calculator.commands import Command, CommandHandler

class TestCommand(Command):
    """A test command that implements the execute method."""
    def execute(self, *args):
        """Execute the test command."""
        return "Executed"

def test_command_handler_init():
    """Test the initialization of CommandHandler."""
    handler = CommandHandler()
    assert not handler.commands

def test_register_and_execute_command():
    """Test registering and executing a command."""
    handler = CommandHandler()
    command = TestCommand()
    handler.register_command('test', command)
    assert 'test' in handler.commands
    result = handler.execute_command('test')
    assert result == "Executed"

def test_execute_unknown_command():
    """Test executing an unknown command."""
    handler = CommandHandler()
    with pytest.raises(ValueError, match="No such command: unknown"):
        handler.execute_command('unknown')

def test_execute_command_with_args():
    """Test executing a command with arguments."""
    class TestCommandWithArgs(Command):
        """A test command that takes arguments and returns them."""
        def execute(self, *args):
            """Execute the command with arguments."""
            return args

    handler = CommandHandler()
    command = TestCommandWithArgs()
    handler.register_command('testargs', command)
    result = handler.execute_command('testargs arg1 arg2')
    assert result == ('arg1', 'arg2')
