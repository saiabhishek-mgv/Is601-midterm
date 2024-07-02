import pytest
from calculator.commands import Command, CommandHandler

class TestCommand(Command):
    def execute(self, *args):
        return "Executed"

def test_register_command():
    handler = CommandHandler()
    command = TestCommand()
    handler.register_command('test', command)
    assert 'test' in handler.commands
    assert handler.commands['test'] is command

def test_execute_command():
    handler = CommandHandler()
    command = TestCommand()
    handler.register_command('test', command)
    result = handler.execute_command('test')
    assert result == "Executed"

def test_execute_unknown_command():
    handler = CommandHandler()
    with pytest.raises(ValueError, match="No such command: unknown"):
        handler.execute_command('unknown')

def test_execute_command_with_args():
    class TestCommandWithArgs(Command):
        def execute(self, *args):
            return args

    handler = CommandHandler()
    command = TestCommandWithArgs()
    handler.register_command('testargs', command)
    result = handler.execute_command('testargs arg1 arg2')
    assert result == ('arg1', 'arg2')
