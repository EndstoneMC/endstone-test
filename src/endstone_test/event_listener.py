from endstone import ColorFormat, Server
from endstone.event import *
from endstone.plugin import Plugin

from endstone_test.test_helper import run_tests


class EventListener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @event_handler
    def on_player_login(self, event: PlayerLoginEvent) -> None:
        self.server.broadcast_message(
            ColorFormat.YELLOW + f"{event.player.name} logged in."
        )

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        event.join_message = ColorFormat.BOLD + event.join_message

        self._plugin.logger.info("===========================")
        self._plugin.logger.info(f"Name: {event.player.name}")
        self._plugin.logger.info(f"UUID: {event.player.unique_id}")
        self._plugin.logger.info(f"XUID: {event.player.xuid}")
        self._plugin.logger.info(f"Entity Id: {event.player.runtime_id}")
        self._plugin.logger.info(f"Address: {event.player.address}")
        self._plugin.logger.info(f"Game mode: {event.player.game_mode}")
        self._plugin.logger.info(f"Location: {event.player.location}")
        self._plugin.logger.info(f"Velocity: {event.player.velocity}")
        self._plugin.logger.info(f"Op status: {event.player.is_op}")
        self._plugin.logger.info(f"Ping: {event.player.ping}ms")
        self._plugin.logger.info(f"Locale: {event.player.locale}")
        self._plugin.logger.info(
            f"Device: {event.player.device_os} {event.player.device_id}"
        )
        self._plugin.logger.info("===========================")

        run_tests("on_player_join", player=event.player, plugin=self._plugin)

    @event_handler
    def on_player_interact(self, event: PlayerInteractEvent):
        self._plugin.logger.info(
            f"{event.player.name} interacts with {event.block} (face={event.block_face}) using {event.item} item"
        )

    @event_handler
    def on_player_interact_actor(self, event: PlayerInteractActorEvent):
        self._plugin.logger.info(
            f"{event.player.name} interacts with actor {event.actor.name}"
        )

    @event_handler
    def on_player_kick(self, event: PlayerKickEvent) -> None:
        self._plugin.logger.info(
            f"{event.player.name} has been kicked due to {event.reason}"
        )
        event.reason = ColorFormat.BOLD + event.reason

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        event.quit_message = ColorFormat.BOLD + event.quit_message

    @event_handler
    def on_player_teleport(self, event: PlayerTeleportEvent):
        self._plugin.logger.info(
            f"{event.player.name} teleported from {event.from_location} to {event.to_location}"
        )

    @event_handler
    def on_player_death(self, event: PlayerDeathEvent):
        event.death_message = ColorFormat.RED + event.death_message

    @event_handler
    def on_actor_death(self, event: ActorDeathEvent):
        self._plugin.logger.info(f"{event.actor.name} ({event.actor.type}) died.")

    @event_handler
    def on_actor_knockback(self, event: ActorKnockbackEvent):
        self._plugin.logger.info(f"{event.actor.name} ({event.actor.type}) is knocked by {event.knockback}")

    @event_handler
    def on_actor_removed(self, event: ActorRemoveEvent):
        self._plugin.logger.info(f"{event.actor.name} ({event.actor.type}) is removed from the world.")

    @event_handler
    def on_actor_spawned(self, event: ActorSpawnEvent):
        self._plugin.logger.info(f"{event.actor.name} ({event.actor.type}) just spawned.")

    @event_handler
    def on_actor_teleport(self, event: ActorTeleportEvent):
        self._plugin.logger.info(
            f"{event.actor.name} ({event.actor.type}) teleported from {event.from_location} to {event.to_location}"
        )

    @event_handler
    def on_block_break(self, event: BlockBreakEvent):
        self._plugin.logger.info(f"{event.player.name} breaks a block {event.block}")

    @event_handler
    def on_block_placed(self, event: BlockPlaceEvent):
        self._plugin.logger.info(
            f"{event.player.name} places a {event.block_placed_state} against {event.block_against} (was {event.block})"
        )

    @event_handler
    def on_thunder_change(self, event: ThunderChangeEvent):
        self._plugin.logger.info(f"Thunder state changed to {event.to_thunder_state}")

    @event_handler
    def on_weather_change(self, event: WeatherChangeEvent):
        self._plugin.logger.info(f"Weather state changed to {event.to_weather_state}")

    @event_handler
    def on_server_command(self, event: ServerCommandEvent):
        self._plugin.logger.info(
            f"{event.sender.name} executed command: {event.command}"
        )

    @event_handler
    def on_server_list_ping(self, event: ServerListPingEvent):
        event.motd = ColorFormat.BOLD + event.motd
        event.level_name = ColorFormat.GREEN + "Endstone Test" + ColorFormat.RESET

    @event_handler
    def on_script_message(self, event: ScriptMessageEvent):
        self._plugin.logger.info(
            f"Script message received from {event.sender}: message_id={event.message_id}, message={event.message}"
        )

    @property
    def server(self) -> Server:
        return self._plugin.server
