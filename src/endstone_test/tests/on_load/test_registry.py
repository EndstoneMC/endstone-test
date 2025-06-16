import pytest
from endstone import Server, NamespacedKey
from endstone.plugin import Plugin


@pytest.fixture
def server(plugin: Plugin) -> Server:
    return plugin.server


def test_enchantment_registry(server: Server):
    registry = server.enchantment_registry
    assert "protection" in registry
    assert NamespacedKey.from_string("protection") in registry
    assert "minecraft:protection" in registry
    assert NamespacedKey.from_string("minecraft:protection") in registry
    assert "bad_enchantment" not in registry


def test_item_registry(server: Server):
    registry = server.item_registry
    assert "apple" in registry
    assert "minecraft:apple" in registry
    assert "non_existent_item" not in registry
