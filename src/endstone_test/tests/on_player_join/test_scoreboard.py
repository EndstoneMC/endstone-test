import pytest
from endstone import Player, Server
from endstone.scoreboard import Scoreboard


@pytest.fixture
def server(player: Player) -> Server:
    return player.server


@pytest.fixture
def scoreboard(server: Server) -> Scoreboard:
    return server.scoreboard


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(server: Server, scoreboard: Scoreboard):
    # Before each test run
    server.dispatch_command(server.command_sender, "scoreboard objectives remove test_objective")
    objective = scoreboard.get_objective("test_objective")
    assert objective is None

    yield

    # After each test run
    server.dispatch_command(server.command_sender, "scoreboard objectives remove test_objective")
    objective = scoreboard.get_objective("test_objective")
    assert objective is None


def test_scoreboard_value(player: Player, server: Server, scoreboard: Scoreboard) -> None:
    server.dispatch_command(server.command_sender, "scoreboard objectives add test_objective dummy")
    objective = scoreboard.get_objective("test_objective")
    assert objective is not None

    server.dispatch_command(server.command_sender, f"scoreboard players set {player.name} test_objective 3")
    score = objective.get_score(player)
    assert score.is_score_set
    assert score.value == 3
