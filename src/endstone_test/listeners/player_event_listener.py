from endstone import ColorFormat
from endstone.event import (
    PlayerChatEvent,
    PlayerDeathEvent,
    PlayerDropItemEvent,
    PlayerEmoteEvent,
    PlayerGameModeChangeEvent,
    PlayerInteractActorEvent,
    PlayerInteractEvent,
    PlayerItemConsumeEvent,
    PlayerJoinEvent,
    PlayerJumpEvent,
    PlayerKickEvent,
    PlayerLoginEvent,
    PlayerMoveEvent,
    PlayerPickupItemEvent,
    PlayerQuitEvent,
    PlayerRespawnEvent,
    PlayerTeleportEvent,
    event_handler,
)

from .event_listener import EventListener


class PlayerEventListener(EventListener):
    @event_handler
    def on_player_login(self, event: PlayerLoginEvent) -> None:
        self.plugin.on_event_triggered(
            event, ColorFormat.YELLOW + f"{event.player.name} logged in."
        )

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent) -> None:
        self.plugin.on_event_triggered(event, event.join_message)
        event.join_message = ColorFormat.BOLD + event.join_message

        self.plugin.logger.info("===========================")
        self.plugin.logger.info(f"Name: {event.player.name}")
        self.plugin.logger.info(f"UUID: {event.player.unique_id}")
        self.plugin.logger.info(f"XUID: {event.player.xuid}")
        self.plugin.logger.info(f"Entity Id: {event.player.runtime_id}")
        self.plugin.logger.info(f"Address: {event.player.address}")
        self.plugin.logger.info(f"Game mode: {event.player.game_mode}")
        self.plugin.logger.info(f"Location: {event.player.location}")
        self.plugin.logger.info(f"Velocity: {event.player.velocity}")
        self.plugin.logger.info(f"Op status: {event.player.is_op}")
        self.plugin.logger.info(f"Ping: {event.player.ping}ms")
        self.plugin.logger.info(f"Locale: {event.player.locale}")
        self.plugin.logger.info(
            f"Device: {event.player.device_os} {event.player.device_id}"
        )
        self.plugin.logger.info("===========================")

        self.plugin.run_tests("on_player_join", player=event.player)
        self.plugin.bossbar.add_player(event.player)

    @event_handler
    def on_player_emote(self, event: PlayerEmoteEvent) -> None:
        self.plugin.on_event_triggered(
            event, f"{event.player.name} sends an emote: {event.emote_id}"
        )

    @event_handler
    def on_player_interact(self, event: PlayerInteractEvent):
        self.plugin.on_event_triggered(
            event,
            f"{event.player.name} interacts with {event.block} (face={event.block_face}) using {event.item} item",
        )

    @event_handler
    def on_player_interact_actor(self, event: PlayerInteractActorEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} interacts with actor {event.actor.name}"
        )

    @event_handler
    def on_player_kick(self, event: PlayerKickEvent) -> None:
        self.plugin.on_event_triggered(
            event, f"{event.player.name} has been kicked due to {event.reason}"
        )
        event.reason = ColorFormat.BOLD + event.reason

    @event_handler
    def on_player_quit(self, event: PlayerQuitEvent) -> None:
        self.plugin.on_event_triggered(event, event.quit_message)
        event.quit_message = ColorFormat.BOLD + event.quit_message

    @event_handler
    def on_player_chat(self, event: PlayerChatEvent) -> None:
        self.plugin.on_event_triggered(
            event, f"{event.player.name} says: {event.message}"
        )

    @event_handler
    def on_player_game_mode_changed(self, event: PlayerGameModeChangeEvent) -> None:
        self.plugin.on_event_triggered(
            event, f"{event.player.name} changed game mode to {event.new_game_mode}"
        )

    @event_handler
    def on_player_jump(self, event: PlayerJumpEvent):
        self.plugin.on_event_triggered(
            event,
            f"{event.player.name} {ColorFormat.YELLOW}jumps{ColorFormat.RESET} from {event.from_location} to {event.to_location}",
        )

    @event_handler
    def on_player_move(self, event: PlayerMoveEvent):
        self.plugin.on_event_triggered(
            event,
            f"{event.player.name} {ColorFormat.GREEN}moves{ColorFormat.RESET} from {event.from_location} to {event.to_location}",
        )

    @event_handler
    def on_player_teleport(self, event: PlayerTeleportEvent):
        self.plugin.on_event_triggered(
            event,
            f"{event.player.name} teleported from {event.from_location} to {event.to_location}",
        )

    @event_handler
    def on_player_death(self, event: PlayerDeathEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} died (source: {event.damage_source})."
        )
        event.death_message = ColorFormat.RED + event.death_message

    @event_handler
    def on_player_respawn(self, event: PlayerRespawnEvent):
        self.plugin.on_event_triggered(event, f"{event.player.name} respawned.")

    @event_handler
    def on_player_item_consume(self, event: PlayerItemConsumeEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} consumes {event.item}."
        )

    @event_handler
    def on_player_drop_item(self, event: PlayerDropItemEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} drops {event.item}."
        )
        if event.item.type == "minecraft:apple":
            event.player.send_message("Please do not throw away the apple :)")
            event.cancel()

    @event_handler
    def on_player_pick_up_item(self, event: PlayerPickupItemEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} picks up {event.item}."
        )
        if event.item.type == "minecraft:golden_apple":
            event.cancel()
