import pytest
from endstone.plugin import Plugin, PluginLoadOrder

from endstone_test.event_listener import EventListener
from endstone_test.test_helper import FixtureInjection


class EndstoneTest(Plugin):
    prefix = "EndstoneTest"
    api_version = "0.6"
    load = PluginLoadOrder.POSTWORLD

    commands = {
        "test": {
            "description": "Run the test command",
            "usages": [
                "/test form <message|action|modal>",
                "/test sender",
                "/test player <toast|title|kick|particle|boss|sound>",
                "/test block <block: block> [blockStates: block_states]",
                "/test broadcast",
                "/test inv <mainhand|offhand|meta>",
            ],
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

    def on_enable(self) -> None:
        self.logger.info("on_enable is called!")
        self.register_events(EventListener(self))
        self.run_tests("on_load")

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    def run_tests(self, name: str, **kwargs):
        return pytest.main(
            ["-s", "--pyargs", f"endstone_test.tests.{name}"],
            plugins=[FixtureInjection(server=self.server, plugin=self, **kwargs)],
        )
