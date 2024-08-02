import json

from endstone import ColorFormat, Player
from endstone import Translatable as tr
from endstone.command import Command, CommandExecutor, CommandSender, ConsoleCommandSender
from endstone.form import *


class TestCommandExecutor(CommandExecutor):
    __test__ = False

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
                                Dropdown(label="This is a dropdown", options=["Apple", "Orange", "Banana"]),
                                Label(text="This is a label"),
                                Slider(label="This is a slider", min=0, max=5, step=1, default_value=2),
                                StepSlider(label="This is a step slider", options=["Mild", "Hot", "Extra hot"]),
                                TextInput(
                                    label="This is a text input",
                                    placeholder="This is the placehoder",
                                    default_value="Delete me",
                                ),
                                Toggle(label="This is a toggle", default_value=True),
                            ],
                            submit_button="Let's GO",
                            icon="https://avatars.githubusercontent.com/u/142812342",
                            on_submit=lambda player, data: player.send_message(f"Response {json.loads(data)}"),
                            on_close=lambda player: player.send_message(
                                f"You just closed a {ColorFormat.GREEN}modal form"
                            ),
                        )
                    )
                else:
                    sender.send_error_message(f"Unknown form type: {type}")

            case ["sender"]:
                if isinstance(sender, Player):
                    sender.send_message("You are a player!")
                elif isinstance(sender, ConsoleCommandSender):
                    sender.send_message("You are the console!")
                else:
                    sender.send_error_message(f"Unknown sender: {sender.__class__}")

            case ["selector", target]:
                sender.send_message(f"The selector is {target}")

        return True
