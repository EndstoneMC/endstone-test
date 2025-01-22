import pytest
from endstone import Player, Server


@pytest.fixture
def server(player: Player) -> Server:
    return player.server


def test_get_block_at_xyz(player: Player) -> None:
    location = player.location
    block = player.dimension.get_block_at(location.block_x, -64, location.block_z)
    assert block.type == "minecraft:bedrock"
    block = player.dimension.get_block_at(location.block_x, 320, location.block_z)
    assert block.type == "minecraft:air"


def test_get_block_at_location(player: Player) -> None:
    location = player.location
    block = player.dimension.get_block_at(location)
    assert block.data.type == block.type
