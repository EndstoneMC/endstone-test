import pytest
from endstone import Player, Server
from endstone.inventory import ItemStack


@pytest.fixture
def server(player: Player) -> Server:
    return player.server


def test_inventory_sizes(player: Player):
    assert player.inventory.size == 36
    assert player.inventory.max_stack_size == 254


def test_set_invalid_item(player: Player):
    player.inventory.set_item(35, ItemStack("item_that_does_not_exist", 1))
    assert player.inventory.get_item(35) is None


def test_set_empty_item(player: Player):
    player.inventory.set_item(35, None)
    assert player.inventory.get_item(35) is None


def test_set_item(player: Player):
    player.inventory.set_item(35, ItemStack("minecraft:clock", 7))

    item = player.inventory.get_item(35)
    assert item.type == "minecraft:clock"
    assert item.amount == 7

    player.inventory.set_item(35, item)
    item = player.inventory.get_item(35)
    assert item.type == "minecraft:clock"
    assert item.amount == 7
