import pytest
from endstone import Server, __minecraft_version__
from endstone.plugin import Plugin


@pytest.fixture
def server(plugin: Plugin) -> Server:
    return plugin.server


def test_create_block_data(server: Server) -> None:
    block_data = server.create_block_data("minecraft:standing_sign", {"ground_sign_direction": 8})
    assert block_data.type == "minecraft:standing_sign"
    assert "ground_sign_direction" in block_data.block_states
    assert block_data.block_states["ground_sign_direction"] == 8
    assert "block_light_level" not in block_data.block_states
