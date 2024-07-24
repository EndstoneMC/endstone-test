from endstone import Player
from endstone import Translatable as tr
from endstone.command import Command, CommandExecutor, CommandSender, ConsoleCommandSender
from endstone.form import ActionForm, MessageForm, Button


class TestCommandExecutor(CommandExecutor):
    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if isinstance(sender, ConsoleCommandSender):
            sender.send_message("You are the console!")
        elif isinstance(sender, Player):
            sender.send_message("You are the player!")
            sender.send_form(
                MessageForm(
                    title=tr("permissions.removeplayer"),
                    content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                    button1="Yes",
                    button2="No",
                )
            )

            sender.send_form(
                ActionForm(
                    title=tr("permissions.removeplayer"),
                    content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                    buttons=[
                        Button("Endstone", icon="https://avatars.githubusercontent.com/u/142812342"),
                        Button("Instagram"),
                        Button("Twitter"),
                    ],
                )
            )
        else:
            assert False, f"Unknown command sender: {sender.__class__}"

        return True
