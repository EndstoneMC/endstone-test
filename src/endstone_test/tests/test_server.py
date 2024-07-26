import pytest
from endstone import Server, __minecraft_version__
from endstone.plugin import Plugin


@pytest.fixture
def server(plugin: Plugin) -> Server:
    return plugin.server


def test_server_version(server: Server) -> None:
    assert server.minecraft_version == f"v{__minecraft_version__}"


def test_server_levels(server: Server) -> None:
    assert len(server.levels) == 1
    for level in server.levels:
        assert server.get_level(level.name) is level

        for dimension in level.dimensions:
            assert level.get_dimension(dimension.name) is dimension


def test_dispatch_command(server: Server) -> None:
    server.dispatch_command(server.command_sender, "say Hello, World!")
