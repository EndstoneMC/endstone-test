from babel import Locale
from endstone import Player, Server, GameMode
from endstone.plugin import Plugin
import pytest


@pytest.fixture
def server(player: Player) -> Server:
    return player.server


def test_player_in_online_players(player: Player, server: Server):
    assert player in server.online_players
    assert server.get_player(player.name) is player
    assert server.get_player(player.unique_id) is player


def test_player_inventory(player: Player):
    assert player.inventory.size == 36
    assert player.inventory.max_stack_size == 254


def test_player_permissions(player: Player, plugin: Plugin):
    assert player.has_permission("minecraft.command.me") is True
    player.add_attachment(plugin, "minecraft.command.me", False)

    assert player.has_permission("minecraft.command.me") is False
    player.update_commands()


def test_player_experience(player: Player):
    current_exp_lvl = player.exp_level
    current_exp_progress = player.exp_progress

    player.give_exp_levels(2)
    assert player.exp_level == current_exp_lvl + 2

    assert 0.0 <= player.exp_progress <= 1.0
    player.exp_level = current_exp_lvl + 1
    assert player.exp_level == current_exp_lvl + 1

    player.exp_progress = 1.0 - player.exp_progress
    assert abs(player.exp_progress + current_exp_progress - 1.0) <= 0.00001

    player.exp_level = current_exp_lvl
    player.exp_progress = current_exp_progress
    assert player.exp_level == current_exp_lvl
    assert player.exp_progress == current_exp_progress


def test_player_attributes(player: Player):
    assert abs(player.fly_speed - 0.05) <= 0.00001
    assert abs(player.walk_speed - 0.10) <= 0.00001


def test_player_locale(player: Player):
    assert Locale.parse(player.locale) is not None


def test_player_skin(player: Player):
    skin = player.skin
    assert skin.skin_data.shape[2] == 4
    if skin.cape_data is not None:
        assert skin.cape_data.shape[2] == 4


def test_player_game_mode(player: Player):
    current_game_mode = player.game_mode
    player.game_mode = GameMode.SPECTATOR
    assert player.game_mode == GameMode.SPECTATOR
    player.game_mode = current_game_mode
    assert player.game_mode == current_game_mode


def test_player_scoreboard(player: Player, server: Server):
    assert player.scoreboard is server.scoreboard

    new_scoreboard = server.create_scoreboard()
    player.scoreboard = new_scoreboard
    assert player.scoreboard is new_scoreboard
    assert player.scoreboard is not server.scoreboard

    player.scoreboard = server.scoreboard
    assert player.scoreboard is server.scoreboard


def test_player_tags(player: Player, server: Server):
    server.dispatch_command(server.command_sender, f'tag "{player.name}" add test_tag')
    assert "test_tag" in player.scoreboard_tags
    server.dispatch_command(
        server.command_sender, f'tag "{player.name}" remove test_tag'
    )
    assert "test_tag" not in player.scoreboard_tags
