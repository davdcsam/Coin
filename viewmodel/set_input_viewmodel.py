# Standard Libraries
import os
from typing import Any, Literal

# Third Party Libraries
from connection.connection import Connection

# Owner Modules
from model.set_input_model import SetInputModel
from utils.info_widgets import InfoWidgets


class SetInputViewModel(InfoWidgets):
    def __init__(self, model, model_connection: Connection | Any) -> None:
        # ··· Models ··· #
        self.model: SetInputModel = model
        self.model_connection = model_connection

        # ··· Atr Class ··· #
        InfoWidgets.__init__(self)
        self.view = None

    def bind_inputs(self, view):
        self.view = view
        items_observed: list[str] = [
            "symbol_info_volume_min",
            "symbol_info_volume_max",
            "symbol_info_volume_step",
        ]
        for item_observed in items_observed:
            self.model_connection.observe(view.format_items, item_observed)
        
        self.model_connection.observe(view.hide_undeploy, "bot_status")

    def load_inputs(self) -> dict[str, Any] | Literal[False]:
        return self.model.load_inputs_file()

    def load_last_input(self):
        return self.model.load_inputs_last_file()

    def save_inputs(self):
        try:
            if self.model.save_inputs_file(
                self.get_inputs(self.view), os.path.basename(os.getcwd()) + "Input"
            ):
                print("Save Set Inputs Successfully")
        except Exception as e:
            print(e)
            pass

    def save_last_input(self):
        try:
            if self.model.save_inputs_last_file(self.get_inputs(self.view)):
                print("Save Last Set Inputs Successfully")
        except Exception as e:
            print(e)
            pass

    def change_bot_state(self, status: bool) -> None:
        self.model.change_bot_state(status, self.get_inputs(self.view))

    def checker(self) -> bool:
        return self.model.checker(self.get_inputs(self.view))

    def change_delay_time(self, new_delay: float) -> None:
        self.model.change_delay_time(new_delay)
