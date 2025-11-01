import pytest
from endstone import Server


@pytest.mark.parametrize(
    "registry,key,expected",
    [
        (
            "enchantment",
            "protection",
            {"start_level": 1, "max_level": 4},
        ),
        (
            "enchantment",
            "sharpness",
            {"start_level": 1, "max_level": 5},
        ),
        (
            "item",
            "minecraft:diamond",
            {"max_stack_size": 64, "max_durability": 0},
        ),
        (
            "item",
            "minecraft:diamond_sword",
            {"max_stack_size": 1, "max_durability": 1561},
        ),
    ],
)
def test_get_valid(server: Server, registry: str, key: str, expected: dict):
    reg = getattr(server, f"{registry}_registry")
    assert reg.get(key) is not None
    assert reg[key] is not None
    assert key in reg
    assert reg.get_or_throw(key) is not None
    for attr, expected_value in expected.items():
        assert getattr(reg.get(key), attr) == expected_value


@pytest.mark.parametrize(
    "registry,key",
    [
        ("enchantment", "not_an_enchant"),
        ("enchantment", "bogus_enchantment"),
        ("item", "not_an_item"),
        ("item", "bogus_item"),
    ],
)
def test_get_invalid(server: Server, registry: str, key: str):
    reg = getattr(server, f"{registry}_registry")
    assert reg.get(key) is None
    assert key not in reg
    with pytest.raises(KeyError):
        reg.get_or_throw(key)
    with pytest.raises(KeyError):
        _ = reg[key]
