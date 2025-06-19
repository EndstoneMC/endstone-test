from endstone import Player, Server
from endstone.inventory import ItemStack


def test_inventory_sizes(player: Player):
    assert player.inventory.size == 36
    assert player.inventory.max_stack_size == 254


def test_get_item(player: Player, server: Server):
    player.inventory.clear()
    assert player.inventory.is_empty

    server.dispatch_command(
        server.command_sender, f'give "{player.name}" minecraft:clock'
    )
    assert not player.inventory.is_empty

    item1 = player.inventory.get_item(0)
    item2 = player.inventory.contents[0]
    assert item1.type == "minecraft:clock"
    assert item1.amount == 1
    assert item1.type == item2.type
    assert item1.amount == item2.amount

    player.inventory.clear()
    assert player.inventory.is_empty


def test_add_item(player: Player):
    player.inventory.add_item(ItemStack("minecraft:clock", 7))
    item = player.inventory.get_item(0)
    assert item.type == "minecraft:clock"
    assert item.amount == 7


def test_set_item(player: Player):
    player.inventory.set_item(35, ItemStack("minecraft:diamond", 7))

    item = player.inventory.get_item(35)
    assert item.type == "minecraft:diamond"
    assert item.amount == 7

    player.inventory.set_item(35, item)
    item = player.inventory.get_item(35)
    assert item.type == "minecraft:diamond"
    assert item.amount == 7

    assert player.inventory.first(item) == 35


def test_set_empty_item(player: Player):
    player.inventory.set_item(35, None)
    assert player.inventory.get_item(35) is None


def test_update_item_meta(player: Player, server: Server):
    player.inventory.clear()
    server.dispatch_command(
        server.command_sender, f'give "{player.name}" minecraft:clock'
    )

    # Set the lore
    item = player.inventory.contents[0]
    meta = item.item_meta
    assert meta.lore is None
    lore = ["This is a test lore", "And another line of lore:)"]
    meta.lore = lore
    assert meta.lore == lore
    item.set_item_meta(meta)
    assert item.item_meta.lore == lore

    # Update the inventory
    player.inventory.set_item(0, item)
    item = player.inventory.get_item(0)
    assert item.item_meta.lore == lore

    # Remove the lore
    meta = item.item_meta
    meta.lore = None
    item.set_item_meta(meta)
    assert item.item_meta.lore is None


def test_add_item_with_meta(player: Player):
    item = ItemStack("minecraft:diamond_sword", 1)
    meta = item.item_meta
    assert meta.lore is None
    lore = ["A powerful blade", "of destiny"]
    meta.display_name = "Excalibur"
    meta.lore = lore
    meta.damage = 500
    assert not meta.add_enchant("sharpness", 66, force=False)
    assert meta.add_enchant("sharpness", 66, force=True)

    assert item.set_item_meta(meta)

    player.inventory.set_item(1, item)
    item = player.inventory.get_item(1)
    assert item.item_meta.display_name == "Excalibur"
    assert item.item_meta.lore == lore
    assert item.item_meta.damage == 500
    assert item.item_meta.has_enchant("sharpness")
    assert item.item_meta.get_enchant_level("sharpness") == 66
    assert not item.item_meta.has_enchant("protection")
