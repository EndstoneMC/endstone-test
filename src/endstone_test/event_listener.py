import datetime
from functools import partial

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

        self.server.scheduler.run_task_later(self._plugin, partial(send_welcome_message, event.player.name), delay=20)

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
        self._plugin.logger.info("===========================")

        assert event.player.inventory.size == 36
        assert event.player.inventory.max_stack_size == 254

        assert event.player.has_permission("minecraft.command.me") is True
        event.player.add_attachment(self._plugin, "minecraft.command.me", False)
        assert event.player.has_permission("minecraft.command.me") is False
        event.player.update_commands()

        event.player.allow_flight = True
        assert event.player.allow_flight is True

    @event_handler
    def on_player_death(self, event: PlayerDeathEvent):
        # TODO: add player.is_dead check
        pass

    @event_handler
    def on_actor_death(self, event: ActorDeathEvent):
        self._plugin.logger.info(f"{event.actor.name} died.")

    @property
    def server(self) -> Server:
        return self._plugin.server
