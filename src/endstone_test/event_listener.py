import datetime
from functools import partial
from pathlib import Path

from babel import Locale
from endstone import ColorFormat, Server, Translatable
from endstone.event import *
from endstone.plugin import Plugin


class EventListener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._should_kick = True

    @event_handler
    def on_player_login(self, event: PlayerLoginEvent) -> None:
        if self._should_kick:
            event.kick_message = "Player::kick is working. Please join again."
            event.cancelled = True
            self._should_kick = False

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        def send_welcome_message(player_name: str) -> None:
            self.server.broadcast_message(ColorFormat.YELLOW + f"{player_name} joined the game.")
            player = self.server.get_player(player_name)
            assert player is not None
            player.send_message(Translatable("commands.give.success", ["Secret Item", "233", "Secret Man"]))
            player.send_title("Welcome!", player_name)

        self.server.scheduler.run_task(self._plugin, partial(send_welcome_message, event.player.name), delay=20)

        assert event.player in self.server.online_players
        assert self.server.get_player(event.player.name) is event.player
        assert self.server.get_player(event.player.unique_id) is event.player

        self._plugin.logger.info("===========================")
        self._plugin.logger.info(f"Name: {event.player.name}")
        self._plugin.logger.info(f"UUID: {event.player.unique_id}")
        self._plugin.logger.info(f"Entity Id: {event.player.runtime_id}")
        self._plugin.logger.info(f"Address: {event.player.address}")
        self._plugin.logger.info(f"Game mode: {event.player.game_mode}")
        self._plugin.logger.info(f"Location: {event.player.location}")
        self._plugin.logger.info(f"Velocity: {event.player.velocity}")
        self._plugin.logger.info(f"Op status: {event.player.is_op}")
        self._plugin.logger.info(f"Ping: {event.player.ping / datetime.timedelta(milliseconds=1)}")
        self._plugin.logger.info(f"Locale: {event.player.locale}")
        self._plugin.logger.info(f"Device: {event.player.device_os} {event.player.device_id}")
        self._plugin.logger.info("===========================")

        assert event.player.inventory.size == 36
        assert event.player.inventory.max_stack_size == 254

        assert event.player.has_permission("minecraft.command.me") is True
        event.player.add_attachment(self._plugin, "minecraft.command.me", False)
        assert event.player.has_permission("minecraft.command.me") is False
        event.player.update_commands()

        event.player.allow_flight = True
        assert event.player.allow_flight is True

        current_exp_lvl = event.player.exp_level
        event.player.give_exp_levels(2)
        assert event.player.exp_level == current_exp_lvl + 2
        assert 0.0 <= event.player.exp_progress <= 1.0
        event.player.exp_level = current_exp_lvl + 1
        assert event.player.exp_level == current_exp_lvl + 1

        event.player.fly_speed = 0.5
        event.player.walk_speed = 0.05
        assert abs(event.player.fly_speed - 0.5) <= 0.00001
        assert abs(event.player.walk_speed - 0.05) <= 0.00001
        event.player.fly_speed = 0.05
        event.player.walk_speed = 0.10

        assert Locale.parse(event.player.locale) is not None, event.player.locale

        skin = event.player.skin
        self._plugin.logger.info(f"Skin Id: {skin.skin_id}, Cape Id: {skin.cape_id}")
        assert skin.skin_data.shape[2] == 4, f"Bad shape for skin data: {skin.skin_data.shape}"
        skin_path = Path(self._plugin.data_folder) / "skins"
        skin_path.mkdir(parents=True, exist_ok=True)
        if skin.cape_data is not None:
            assert skin.cape_data.shape[2] == 4, f"Bad shape for cape data: {skin.cape_data.shape}"

    @event_handler
    def on_player_death(self, event: PlayerDeathEvent):
        # TODO: add player.is_dead check
        pass

    @event_handler
    def on_actor_death(self, event: ActorDeathEvent):
        self._plugin.logger.info(f"{event.actor.name} died.")

    @event_handler
    def on_actor_teleport(self, event: ActorTeleportEvent):
        self._plugin.logger.info(f"{event.actor.name} teleported from {event.from_location} to {event.to_location}")

    @property
    def server(self) -> Server:
        return self._plugin.server
