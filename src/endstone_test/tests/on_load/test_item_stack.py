from endstone.inventory import ItemStack


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
