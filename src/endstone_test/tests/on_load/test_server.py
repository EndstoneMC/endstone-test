import time
from pathlib import Path

import pytest
from endstone import Server, __minecraft_version__
from endstone.command import CommandSenderWrapper
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
    assert server.dispatch_command(
        server.command_sender, "scriptevent endstone:test Hello World!"
    )


def test_max_players(server: Server) -> None:
    # get max players
    server.dispatch_command(server.command_sender, "setmaxplayers 5")
    assert server.max_players == 5
    # set max players
    server.max_players = 100
    assert server.max_players == 100


def test_online_mode(plugin: Plugin, server: Server) -> None:
    properties_file = Path(plugin.data_folder, "..", "..", "server.properties").resolve()
    with properties_file.open(mode="r") as file:
        for line in file:
            if line.startswith("online-mode="):
                value = line.split("=", 1)[1].strip()
                assert (value.lower() == "true") == server.online_mode
                return

    assert False


def test_command_sender_wrapper(server: Server):
    messages = []

    def on_message(message):
        messages.append(server.language.translate(message, locale="zh_CN"))

    sender = CommandSenderWrapper(server.command_sender, on_message=on_message)
    assert server.dispatch_command(sender, "listd")
    assert "玩家在线" in "".join(messages)
