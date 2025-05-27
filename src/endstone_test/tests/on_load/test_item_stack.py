import pytest
from endstone.inventory import ItemStack


@pytest.mark.parametrize("type,max_durability,max_stack_size", [
    ("minecraft:diamond_sword", 1561, 1),
    ("minecraft:apple", 0, 64),
])
def test_create_item(type: str, max_durability, max_stack_size):
    item = ItemStack(type)
    assert item.type == type
    assert item.type.id == type
    assert item.type.max_durability == max_durability
    assert item.type.max_stack_size == max_stack_size


def test_create_item_bad_type():
    with pytest.raises(RuntimeError) as err_info:
        _ = ItemStack("non_existent_item")

    assert "Unknown item type: non_existent_item" == str(err_info.value)


@pytest.mark.parametrize("amount", [-1, 0, 256])
def test_create_item_bad_amount(amount):
    with pytest.raises(RuntimeError) as err_info:
        _ = ItemStack("minecraft:apple", amount)

    assert f"Item stack amount must be between 1 to 255, got {amount}." == str(err_info.value)


def test_set_lore():
    item = ItemStack("minecraft:diamond_sword")
    lore = ["A powerful blade", "of destiny"]

    meta = item.item_meta
    meta.lore = lore

    assert item.set_item_meta(meta)

    meta = item.item_meta
    assert meta.has_lore
    assert meta.lore == lore


def test_remove_lore():
    item = ItemStack("minecraft:diamond_sword")
    lore = ["A powerful blade", "of destiny"]

    meta = item.item_meta
    meta.lore = lore
    assert item.set_item_meta(meta)

    meta = item.item_meta
    meta.lore = []
    assert item.set_item_meta(meta)

    meta = item.item_meta
    assert meta.has_lore == False
    assert meta.lore is None


def test_clear_item_meta():
    item = ItemStack("minecraft:diamond_sword")
    lore = ["A powerful blade", "of destiny"]

    meta = item.item_meta
    meta.lore = lore
    assert item.set_item_meta(meta)

    assert item.set_item_meta(None)
    meta = item.item_meta
    assert meta.has_lore == False
