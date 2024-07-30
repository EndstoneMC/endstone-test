from pathlib import Path

import pytest
from endstone.plugin import Plugin

from endstone_test.event_listener import EventListener


class FixtureInjection:
    def __init__(self, obj):
        self.obj = obj

    @pytest.fixture(scope='session')
    def plugin(self):
        return self.obj


class EndstoneTest(Plugin):
    prefix = "EndstoneTest"
    api_version = "0.5"

    commands = {
        "test": {
            "description": "Run the test command",
            "usages": ["/test (form)<test: EndstoneTests> (message|action|modal)<type: FormTypes>"],
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
        self.run_tests()

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")

    def run_tests(self) -> None:
        test_paths = Path(__file__).parent / "tests"
        ret_code = pytest.main(["-s", test_paths], plugins=[FixtureInjection(self)])
        self.logger.info(f"Testing finished with exit code {ret_code}")
