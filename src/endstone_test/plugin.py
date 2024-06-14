from endstone import __minecraft_version__
from endstone.plugin import Plugin

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

        self.logger.info("on_enable is called!")

        assert len(self.server.levels) == 1
        assert self.server.max_players == 10
        self.server.max_players = 100
        assert self.server.max_players == 100

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")
