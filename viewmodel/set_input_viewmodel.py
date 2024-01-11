# Standard Libraries
import os
from typing import Any, Literal

# Third Party Libraries
from connection.connection import Connection

# Owner Modules
from model.set_input_model import SetInputModel
from utils.logs import Logs
from utils.info_widgets import InfoWidgets
from utils.switch_view import SwitchView


class SetInputViewModel(InfoWidgets):
    def __init__(self, model, model_connection: Connection | Any) -> None:
        # ··· Models ··· #
        self.model: SetInputModel = model
        self.model_connection = model_connection

        # ··· Atr Class ··· #
        InfoWidgets.__init__(self)
        self.instance_logs: Logs = Logs.getInstance()
        self.instance_switch_view: SwitchView = SwitchView.getInstance()
        self.view = None

    def bind_inputs(self, view):
        self.view = view

        # Items to view.format_items
        for item_observed in [
            "symbol_info_volume_min",
            "symbol_info_volume_max",
            "symbol_info_volume_step",
        ]:
            self.model_connection.observe(view.format_items, item_observed)

        # Items to view.update_checker_items
        for item_observed in [
            "order_check_full_comment",
            "order_check_retcode",
            "order_check_request_volume",
            "order_check_request_price",
            "order_check_request_tp",
            "order_check_request_sl",
            "order_check_calc_profit",
            "order_check_calc_loss",
        ]:
            self.model_connection.observe(view.update_checker_items, item_observed)

        # Items to view.update_result_items
        for item_observed in [
            "order_result_full_comment",
            "order_result_request_volume",
            "order_result_request_price",
            "order_result_request_tp",
            "order_result_request_sl",
            "order_result_calc_profit",
            "order_result_calc_loss",
        ]:
            self.model_connection.observe(view.update_result_items, item_observed)

        self.model_connection.observe(view.hide_undeploy, "bot_status")

        self.instance_switch_view.observe(view.callback_switch_view, "current_view")

    def load_inputs(self) -> dict[str, Any] | Literal[False]:
        return self.model.load_inputs_file()

    def load_last_input(self):
        return self.model.load_inputs_last_file()

    def save_inputs(self):
        try:
            if self.model.save_inputs_file(
                self.get_inputs(self.view), os.path.basename(os.getcwd()) + "Input"
            ):
                self.instance_logs.log("Save Set Inputs Successfully")
        except Exception as e:
            self.instance_logs.internal_log(e, "e")
            pass

    def save_last_input(self):
        try:
            if self.model.save_inputs_last_file(self.get_inputs(self.view)):
                self.instance_logs.log("Save Last Set Inputs Successfully")
        except Exception as e:
            self.instance_logs.internal_log(e, "e")
            pass

    def change_bot_state(self, status: bool) -> None:
        self.model.change_bot_state(status, self.get_inputs(self.view))

    def checker(self) -> bool:
        return self.model.checker(self.get_inputs(self.view))

    def change_delay_time(self, new_delay: float) -> None:
        self.model.change_delay_time(new_delay)
