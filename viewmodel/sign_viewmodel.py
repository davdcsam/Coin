# Standard Libraries
import os
from typing import Any, Literal

# Third Party Libraries

# Owner Modules
from model.trade.trade_model import TradeModel

from model.sign_model import SignModel

from utils.info_widgets import InfoWidgets
from utils.logs import Logs
from utils.switch_view import SwitchView

class SignViewModel(InfoWidgets):
    def __init__(self, model, model_connection) -> None:
        InfoWidgets.__init__(self)
        self.model_connection: TradeModel = model_connection
        self.model: SignModel = model
        self.instance_switch_view: SwitchView = SwitchView.getInstance()
        self.instance_logs: Logs = Logs.getInstance()
        self.view = None

    def bind(self, view):
        self.view = view

        self.instance_switch_view.observe(self.view.notification_post_sing_out, "current_view")

    def fill_input_path(self) -> list:
        return self.model.get_fill_input_custom_terminal()

    def custom_terminal_input_path(self):
        return self.model.custom_terminal()

    def open_connection(self) -> bool:
        return self.model.open_connection(self.get_inputs(self.view))

    def close_connection(self) -> None:
        self.model.close_connection()

    def load_inputs(self) -> dict[str, Any] | Literal[False]:
        return self.model.load_inputs_file()

    def load_last_input(self):
        return self.model.load_inputs_last_file()

    def save_inputs(self) -> None:
        try:
            if self.model.save_inputs_file(
                self.get_inputs(self.view), os.path.basename(os.getcwd())
            ):
                self.instance_logs.log("Save Inputs Successfully")
        except Exception as e:
            self.instance_logs.internal_log(e, "e")
            pass

    def save_last_input(self):
        try:
            if self.model.save_inputs_last_file(self.get_inputs(self.view)):
                self.instance_logs.log("Save Last Inputs Successfully")
        except Exception as e:
            self.instance_logs.internal_log(e, "e")
            pass
