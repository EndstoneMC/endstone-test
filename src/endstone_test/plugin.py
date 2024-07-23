import datetime
import uuid

from endstone import Translatable as tr
from endstone import __minecraft_version__, Player
from endstone.command import Command, CommandSender, ConsoleCommandSender
from endstone.form import ActionForm, MessageForm, Button
from endstone.plugin import Plugin
from endstone.scoreboard import Criteria, DisplaySlot

from endstone_test.event_listener import EventListener


class TestPlugin(Plugin):
    name = "EndstoneTest"
    api_version = "0.4"

    commands = {
        "test": {
            "description": "Run the test command",
            "usages": ["/test"],
            "permissions": ["endstone_test.command.test"],
        }
    }

    permissions = {
        "endstone_test.command.test": {
            "description": "Allow users to use the /test command.",
            "default": True,
        }
    }

    def on_load(self) -> None:
        self.logger.info("on_load is called!")
        assert len(self.server.levels) == 0
        assert self.server.minecraft_version == f"v{__minecraft_version__}"

    def on_enable(self) -> None:
        self._listener = EventListener(self)
        self.register_events(self._listener)

        assert self.get_command("test") is not None
        assert self.get_command("test").plugin is self

        self.logger.info("on_enable is called!")

        assert len(self.server.levels) == 1
        assert self.server.max_players == 10
        self.server.max_players = 100
        assert self.server.max_players == 100

        assert self.server.get_player("non-existent") is None
        assert self.server.get_player(uuid.uuid4()) is None

        for level in self.server.levels:
            self.logger.info(f"Level: {level.name}")
            assert self.server.get_level(level.name) is level

            for dimension in level.dimensions:
                self.logger.info(f"\tDimension: {dimension.name}")
                assert level.get_dimension(dimension.name) is dimension

        self.server.broadcast_message("Hello!")
        self.server.scheduler.run_task_timer(self, self.send_debug_message, delay=0, period=10)
        self.server.scheduler.run_task_timer(self, self.update_player_pings, delay=0, period=20)

        self.objective = self.server.scoreboard.get_objective("ping")
        if not self.objective:
            self.objective = self.server.scoreboard.add_objective("ping", Criteria.DUMMY, "Player Ping")
        self.objective.set_display(DisplaySlot.SIDE_BAR)

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if isinstance(sender, ConsoleCommandSender):
            sender.send_message("You are the console!")
        elif isinstance(sender, Player):
            sender.send_message("You are the player!")
            sender.send_form(
                MessageForm(
                    title=tr("permissions.removeplayer"),
                    content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                    button1="Yes",
                    button2="No",
                )
            )

            sender.send_form(
                ActionForm(
                    title=tr("permissions.removeplayer"),
                    content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                    buttons=[
                        Button("Endstone",
                               icon="https://avatars.githubusercontent.com/u/142812342"),
                        Button("Instagram"),
                        Button("Twitter"),
                    ]
                )
            )
        else:
            assert False, f"Unknown command sender: {sender.__class__}"

        return True

    def send_debug_message(self):
        for player in self.server.online_players:
            player.send_tip(
                f"Level: {player.level.name}, Time: {player.level.time}, Ping: {player.ping / datetime.timedelta(milliseconds=1)}\n"
                f"Velocity: {player.velocity}\n"
                f"InWater: {player.is_in_water}, InLava: {player.is_in_lava}\n"
                f"OnGround: {player.is_on_ground}, MayFly: {player.allow_flight}, Flying: {player.is_flying}\n"
                f"FlySpeed: {player.fly_speed:.2f}, WalkSpeed: {player.walk_speed:.2f}\n"
                f"Exp: {player.exp_progress}, Lv: {player.exp_level}, Total: {player.total_exp}"
            )

    def update_player_pings(self):
        for player in self.server.online_players:
            score = self.objective.get_score(player)
            score.value = int(player.ping / datetime.timedelta(milliseconds=1))
