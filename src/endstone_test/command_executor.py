from endstone import ColorFormat, Player
from endstone import Translatable as tr
from endstone.command import Command, CommandExecutor, CommandSender
from endstone.form import ActionForm, MessageForm, ModalForm, Toggle


class TestCommandExecutor(CommandExecutor):
    def on_close(self, player: Player):
        player.send_message("You just closed a form")

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        match args:
            case ["form", ("message" | "action" | "modal") as form_type]:
                if not isinstance(sender, Player):
                    sender.send_error_message("You must execute this command as a player")
                    return False

                if form_type == "message":
                    sender.send_form(
                        MessageForm(
                            title=tr("permissions.removeplayer"),
                            content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                            button1="Yes",
                            button2="No",
                            on_submit=lambda player, selection: player.send_message(f"You've selected #{selection}"),
                            on_close=lambda player: player.send_message(
                                f"You just closed a {ColorFormat.GREEN}message form"
                            ),
                        )
                    )
                elif form_type == "action":
                    sender.send_form(
                        ActionForm(
                            title=tr("permissions.removeplayer"),
                            content=tr("accessibility.list.or.two", ["Player 1", "Player 2"]),
                            buttons=[
                                ActionForm.Button("Endstone", icon="https://avatars.githubusercontent.com/u/142812342"),
                                ActionForm.Button("Instagram"),
                                ActionForm.Button("Twitter"),
                            ],
                            on_submit=lambda player, selection: player.send_message(f"You've selected #{selection}"),
                            on_close=lambda player: player.send_message(
                                f"You just closed an {ColorFormat.GREEN}action form"
                            ),
                        )
                    )
                elif form_type == "modal":
                    sender.send_form(
                        ModalForm(
                            title=tr("permissions.removeplayer"),
                            controls=[
                                Toggle("This is a toggle", True),
                                # Toggle(tr("accessibility.list.or.two", ["Player 1", "Player 2"]), True),
                            ],
                            submit_button="Let's GO",
                            icon="https://avatars.githubusercontent.com/u/142812342",
                            on_submit=lambda player, data: player.send_message(f"Response {data}"),
                            on_close=lambda player: player.send_message(
                                f"You just closed a {ColorFormat.GREEN}modal form"
                            ),
                        )
                    )
                else:
                    sender.send_error_message(f"Unknown form type: {type}")

        return True
