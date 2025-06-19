from endstone.event import (
    BlockBreakEvent,
    BlockPlaceEvent,
    event_handler,
)

from .event_listener import EventListener


class BlockEventListener(EventListener):
    @event_handler
    def on_block_break(self, event: BlockBreakEvent):
        self.plugin.on_event_triggered(
            event, f"{event.player.name} breaks a block {event.block}"
        )

    @event_handler
    def on_block_placed(self, event: BlockPlaceEvent):
        self.plugin.on_event_triggered(
            event,
            f"{event.player.name} places a {event.block_placed_state} against {event.block_against} (was {event.block})",
        )
