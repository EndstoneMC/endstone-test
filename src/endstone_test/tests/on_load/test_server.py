import pytest
from endstone import Server, __minecraft_version__
from endstone.plugin import Plugin


@pytest.fixture
def server(plugin: Plugin) -> Server:
    return plugin.server


def test_server_version(server: Server) -> None:
    assert server.minecraft_version == __minecraft_version__


def test_server_level(server: Server) -> None:
    level = server.level
    for dimension in level.dimensions:
        assert level.get_dimension(dimension.name) is dimension


def test_dispatch_command(server: Server) -> None:
    server.dispatch_command(server.command_sender, "say Hello, World!")


def test_max_players(server: Server) -> None:
    # get max players
    server.dispatch_command(server.command_sender, "setmaxplayers 5")
    assert server.max_players == 5
    # set max players
    server.max_players = 100
    assert server.max_players == 100
