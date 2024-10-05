from endstone.plugin import Plugin

from endstone_test import EndstoneTest
from endstone.command import CommandSenderWrapper


def test_instance(plugin: Plugin):
    assert plugin is not None
    assert isinstance(plugin, EndstoneTest)


def test_schedule_task(plugin: Plugin) -> None:
    # case study: https://github.com/EndstoneMC/endstone/issues/31
    server = plugin.server
    assert server.dispatch_command(server.command_sender, "save hold")

    # since /save hold takes time to save, we run /save query in a delayed task to avoid blocking the thread
    def save_query():
        messages = []
        sender = CommandSenderWrapper(server.command_sender,
                                      on_message=lambda msg: messages.extend([msg.translate, *msg.with_]))
        ready = server.dispatch_command(sender, "save query")
        if not ready:
            server.scheduler.run_task(plugin, save_query, delay=5)
            return

        assert 'commands.save-all.success' in messages
        assert server.dispatch_command(server.command_sender, "save resume")

    server.scheduler.run_task(plugin, save_query, delay=5)
