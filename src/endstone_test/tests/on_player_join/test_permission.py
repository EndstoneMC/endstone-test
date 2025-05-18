import pytest
from babel import Locale
from endstone import GameMode, Player, Server
from endstone.plugin import Plugin


@pytest.fixture
def server(player: Player) -> Server:
    return player.server


def test_non_op_permissions(player: Player, plugin: Plugin):
    op_status = player.is_op

    player.is_op = False
    assert player.has_permission("minecraft.command.me") is True
    assert player.has_permission("minecraft.command.kick") is False
    assert player.has_permission("minecraft.command.ban") is False

    player.is_op = op_status


def test_op_permissions(player: Player, plugin: Plugin):
    op_status = player.is_op

    player.is_op = True
    assert player.has_permission("minecraft.command.me") is True
    assert player.has_permission("minecraft.command.kick") is True
    assert player.has_permission("minecraft.command.ban") is True

    player.is_op = op_status
