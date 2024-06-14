from functools import partial
from uuid import UUID

from endstone import ColorFormat, Server
from endstone.event import event_handler, PlayerJoinEvent
from endstone.plugin import Plugin


class EventListener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        def send_welcome_message(player_name: str, player_id: UUID) -> None:
            self.server.broadcast_message(ColorFormat.YELLOW + f"{player_name} joined the game.")
            self.server.dispatch_command(self.server.command_sender, f"say {player_name}, uuid: {player_id}")

        self.server.scheduler.run_task_later(
            self._plugin, partial(send_welcome_message, event.player.name, event.player.unique_id), delay=20
        )

        assert event.player in self.server.online_players
        assert self.server.get_player(event.player.name) is event.player
        # assert self.server.get_player(event.player.unique_id) is event.player # TODO: this will crash

    @property
    def server(self) -> Server:
        return self._plugin.server
