import pytest
from endstone.plugin import Plugin, PluginCommand

from endstone_test.command_executor import TestCommandExecutor


@pytest.fixture
def command(plugin: Plugin) -> PluginCommand:
    return plugin.get_command("test")


def test_command(plugin: Plugin, command: PluginCommand) -> None:
    assert command is not None
    assert command.plugin is plugin


def test_command_executor(plugin: Plugin, command: PluginCommand) -> None:
    assert command.executor is plugin
    command.executor = TestCommandExecutor()
    assert command.executor is not plugin
    assert isinstance(command.executor, TestCommandExecutor)
    command.executor = plugin
    assert command.executor is plugin
    assert not isinstance(command.executor, TestCommandExecutor)


def test_server_command_sender(plugin: Plugin) -> None:
    server = plugin.server
    assert server.command_sender.name == "Server"
