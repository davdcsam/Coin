# Standard Libraries
import pprint
from time import sleep
import time
from typing import Any, Literal

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules
from utils.fonts import Fonts
from utils.formater import Formater
from utils.logs import Logs
from utils.switch_view import SwitchView
from utils.themes import Themes

from viewmodel.set_input_viewmodel import SetInputViewModel


class SetInputView:
    def __init__(self, parent_object, viewmodel: SetInputViewModel) -> None:
        self.viewmodel: SetInputViewModel = viewmodel

        # === Utils === #

        self.instance_fonts = Fonts()
        self.instance_logs: Logs = Logs.getInstance()
        self.instance_switch_view: SwitchView = SwitchView.getInstance()
        self.instance_themes = Themes()

        # === Windows === #

        self.child_window: int | str = dpg.add_child_window(
            parent=parent_object, width=300, height=560
        )

        # === Group Titles === #

        self.group_titles: int | str = dpg.add_group(parent=self.child_window)

        self.title_coin: int | str = dpg.add_text(
            default_value="Coin",
            color=self.instance_themes.primary,
            parent=self.group_titles,
        )

        self.instance_fonts.set_font_items(
            [self.title_coin], "opensans_semibold_title_60"
        )

        self.sign_out_button: int | str = dpg.add_button(
            callback=lambda: self.instance_switch_view.switch("sign_out"),
            width=100,
            height=50,
            pos=(8, 18),
            parent=self.group_titles,
        )

        self.instance_themes.invisible_button(self.sign_out_button)

        # === Group Data Trade === #

        self.group_data_trade: int | str = dpg.add_group(
            width=180, parent=self.child_window
        )

        self.title_data_trade: int | str = dpg.add_text(
            default_value="Data Trade", parent=self.group_data_trade
        )

        self.input_order_type: int | str = dpg.add_combo(
            label="Order Type",
            items=list(self.viewmodel.model_connection.order_types_dict.keys()),
            default_value=list(self.viewmodel.model_connection.order_types_dict.keys())[
                0
            ],
            callback=self.show_checker,
            parent=self.group_data_trade,
        )

        self.input_lot_size: int | str = dpg.add_input_float(
            label="Lot Size",
            callback=self.show_checker,
            parent=self.group_data_trade,
        )

        self.input_take_profit: int | str = dpg.add_input_int(
            parent=self.group_data_trade
        )
        dpg.configure_item(
            self.input_take_profit,
            label="TP in Points",
            min_value=0,
            step=1,
            step_fast=3,
            callback=self.show_checker,
        )

        self.input_stop_loss: int | str = dpg.add_input_int(
            parent=self.group_data_trade,
        )
        dpg.configure_item(
            self.input_stop_loss,
            label="SL in Points",
            min_value=0,
            step=1,
            step_fast=3,
            callback=self.show_checker,
        )

        self.input_deviation_trade: int | str = dpg.add_input_int(
            parent=self.group_data_trade,
        )
        dpg.configure_item(
            self.input_deviation_trade,
            label="Deviation",
            min_value=0,
            step=1,
            step_fast=2,
            callback=self.show_checker,
        )

        # === Group Section Time == #

        self.group_section_time: int | str = dpg.add_group(
            width=200, parent=self.child_window
        )

        self.title_section_time: int | str = dpg.add_text(
            default_value="Section Time",
            parent=self.group_section_time,
        )

        self.input_time_start: int | str = dpg.add_time_picker(
            label="Start Time",
            callback=self.show_checker,
            hour24=True,
            parent=self.group_section_time,
        )

        self.input_time_end: int | str = dpg.add_time_picker(
            label="End Time",
            hour24=True,
            callback=self.show_checker,
            parent=self.group_section_time,
        )

        # ===  Group Load Save === #

        self.group_load_save: int | str = dpg.add_group(
            width=120, parent=self.child_window
        )

        self.button_load: int | str = dpg.add_button(
            label="Load",
            callback=self.load_inputs,
            parent=self.group_load_save,
        )

        self.button_save: int | str = dpg.add_button(
            label="Save",
            callback=self.save_inputs,
            parent=self.group_load_save,
        )

        # === Group Bot Manager === #

        self.group_manager_bot: int | str = dpg.add_group(
            width=120, parent=self.child_window
        )

        self.title_bot_manager: int | str = dpg.add_text(
            default_value="Bot Manager", parent=self.group_manager_bot
        )

        self.input_delay_time_connection: int | str = dpg.add_slider_double(
            label="Delay Time",
            default_value=self.viewmodel.model_connection.delay_time,
            format="%.2f s",
            min_value=0.1,
            max_value=2,
            callback=self.delay_time_connection,
            parent=self.group_manager_bot,
        )

        self.button_checker: int | str = dpg.add_button(
            label="Checker",
            callback=self.checker,
            parent=self.group_manager_bot,
        )

        self.button_deploy: int | str = dpg.add_button(
            label="Deploy",
            pos=(8, 525),
            callback=self.deploy,
            show=False,
            parent=self.group_manager_bot,
        )

        self.button_undeploy: int | str = dpg.add_button(
            label="Undeploy",
            pos=(136, 525),
            callback=self.undeploy,
            show=False,
            parent=self.group_manager_bot,
        )

        self.instance_fonts.set_font_items(
            [
                self.title_bot_manager,
                self.title_data_trade,
                self.title_section_time,
            ]
        )

        # === Build Checker View === #

        self.checker_result_window: int | str = dpg.add_window(
            label="Checker Result",
            width=400,
            height=300,
            no_collapse=True,
            no_resize=True,
            no_saved_settings=True,
            show=False,
        )

        dpg.set_item_pos(
            self.checker_result_window,
            pos=(
                (
                    int(dpg.get_viewport_width())
                    - int(dpg.get_item_width(self.checker_result_window))
                )
                / 2,
                (
                    int(dpg.get_viewport_height())
                    - int(dpg.get_item_height(self.checker_result_window))
                )
                / 2,
            ),
        )

        self.group_checker_result: int | str = dpg.add_group(
            width=200, parent=self.checker_result_window
        )

        self.order_check_full_comment: int | str = dpg.add_text(
            label="Comment",
            show_label=True,
            wrap=dpg.get_item_width(self.checker_result_window) * 1 / 2,
            parent=self.group_checker_result,
        )

        self.order_check_retcode: int | str = dpg.add_text(
            label="Retcode",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_calc_profit: int | str = dpg.add_text(
            label="Simulated Profit",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_calc_loss: int | str = dpg.add_text(
            label="Simulated Loss",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_request_volume: int | str = dpg.add_text(
            label="Simulated Volume",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_request_price: int | str = dpg.add_text(
            label="Simulated Price",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_request_tp: int | str = dpg.add_text(
            label="Simulated Take Profit",
            show_label=True,
            parent=self.group_checker_result,
        )

        self.order_check_request_sl: int | str = dpg.add_text(
            label="Simulated Stop Loss",
            show_label=True,
            parent=self.group_checker_result,
        )

        # === Build Trade Result Window === #

        self.trade_result_window: int | str = dpg.add_window(
            label="Trade Result",
            width=400,
            height=300,
            no_collapse=True,
            no_resize=True,
            no_saved_settings=True,
            show=False,
        )

        dpg.set_item_pos(
            self.trade_result_window,
            pos=(
                (
                    int(dpg.get_viewport_width())
                    - int(dpg.get_item_width(self.trade_result_window))
                )
                / 2,
                (
                    int(dpg.get_viewport_height())
                    - int(dpg.get_item_height(self.trade_result_window))
                )
                / 2,
            ),
        )

        self.group_trade_result: int | str = dpg.add_group(
            width=200, parent=self.trade_result_window
        )

        self.order_result_full_comment: int | str = dpg.add_text(
            label="Comment",
            show_label=True,
            wrap=dpg.get_item_width(self.trade_result_window) * 1 / 2,
            parent=self.group_trade_result,
        )

        self.order_result_calc_profit: int | str = dpg.add_text(
            label="Expected Profit",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.order_result_calc_loss: int | str = dpg.add_text(
            label="Expected Loss",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.order_result_request_volume: int | str = dpg.add_text(
            label="Volume",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.order_result_request_price: int | str = dpg.add_text(
            label="Open Price",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.order_result_request_tp: int | str = dpg.add_text(
            label="Take Profit",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.order_result_request_sl: int | str = dpg.add_text(
            label="Stop Loss",
            show_label=True,
            parent=self.group_trade_result,
        )

        self.viewmodel.bind_inputs(self)

    def update_item(self, item, value):
        if dpg.does_item_exist(item):
            dpg.set_value(item, value)

    def callback_switch_view(self, change):
        if change["new"] == "sign_out":
            dpg.hide_item(self.checker_result_window)
            dpg.hide_item(self.trade_result_window)
        if change["new"] == "sign_in":
            dpg.show_item(self.button_checker)
            dpg.hide_item(self.button_deploy)
            dpg.hide_item(self.button_undeploy)
            dpg.hide_item(self.checker_result_window)
            dpg.hide_item(self.trade_result_window)
        if change["old"] == "sign_out" and change["new"] == "loby":
            button_deploy_confi: dict = dpg.get_item_configuration(self.button_deploy)
            if button_deploy_confi["show"] is True:
                dpg.show_item(self.checker_result_window)

    def show_checker(self, sender, app_data):
        dpg.hide_item(self.button_deploy)
        dpg.show_item(self.button_checker)

    def load_inputs(self, sender, app_data):
        inputs: dict[str, Any] | Literal[False] = self.viewmodel.load_inputs()
        if self.set_inputs(inputs):
            self.instance_logs.log("Load Inputs Successfully")
        else:
            self.instance_logs.log("Inputs File is Empty")

    def load_last_inputs(self):
        inputs: dict[str, Any] | Literal[False] = self.viewmodel.load_last_input()
        if self.set_inputs(inputs):
            self.instance_logs.log("Load Last Inputs Successfully")
        else:
            self.instance_logs.log("Inputs File is Empty")

    def set_inputs(self, inputs: dict[str, Any]) -> bool:
        if not inputs:
            return False

        for k, v in inputs.items():
            if not hasattr(self, k):
                continue

            self.update_item(self.__getattribute__(k), v)
        return True

    def save_inputs(self, sender, app_data):
        self.viewmodel.save_inputs()

    def save_last_inputs(self):
        self.viewmodel.save_last_input()

    def update_checker_items(self, change):
        items: list[str] = [
            "order_check_full_comment",
            "order_check_retcode",
            "order_check_request_volume",
            "order_check_request_price",
            "order_check_request_tp",
            "order_check_request_sl",
            "order_check_calc_profit",
            "order_check_calc_loss",
        ]
        for item in items:
            if (
                item in change["name"]
                and hasattr(self, change["name"])
                and dpg.does_item_exist(self.__getattribute__(change["name"]))
            ):
                if item in [
                    "order_check_request_price",
                    "order_check_request_tp",
                    "order_check_request_sl",
                ]:
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        str(
                            "{:,."
                            + str(self.viewmodel.model_connection.symbol_info_digits)
                            + "f}"
                        ).format(
                            float(change["new"]),
                        ),
                    )
                    continue

                if item in ["order_check_calc_profit", "order_check_calc_loss"]:
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        "{} {:,.2f}".format(
                            self.viewmodel.model_connection.account_info["currency"],
                            float(change["new"]),
                        ),
                    )
                    continue

                dpg.set_value(
                    self.__getattribute__(item),
                    change["new"],
                )

    def update_result_items(self, change):
        items: list[str] = [
            "order_result_full_comment",
            "order_result_request_volume",
            "order_result_request_price",
            "order_result_request_tp",
            "order_result_request_sl",
            "order_result_calc_profit",
            "order_result_calc_loss",
        ]
        for item in items:
            if (
                item in change["name"]
                and hasattr(self, change["name"])
                and dpg.does_item_exist(self.__getattribute__(change["name"]))
            ):
                if item in [
                    "order_result_request_price",
                    "order_result_request_tp",
                    "order_result_request_sl",
                ]:
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        str(
                            "{:,."
                            + str(self.viewmodel.model_connection.symbol_info_digits)
                            + "f}"
                        ).format(
                            float(change["new"]),
                        ),
                    )
                    continue

                if item in ["order_result_calc_profit", "order_result_calc_loss"]:
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        "{} {:,.2f}".format(
                            self.viewmodel.model_connection.account_info["currency"],
                            float(change["new"]),
                        ),
                    )
                    continue

                dpg.set_value(
                    self.__getattribute__(item),
                    change["new"],
                )

    def format_items(self, change):
        if change["new"] is None:
            return

        if dpg.does_item_exist(self.input_lot_size):
            config_dict = {
                "symbol_info_volume_min": {
                    "min_value": change["new"],
                    "format": Formater.get_format_num(num=change["new"]),
                },
                "symbol_info_volume_max": {"max_value": change["new"]},
                "symbol_info_volume_step": {
                    "step": change["new"],
                    "step_fast": change["new"],
                },
            }
            if change["name"] in config_dict:
                dpg.configure_item(self.input_lot_size, **config_dict[change["name"]])
                return

    def deploy(self, sender, app_data):
        dpg.show_item(self.button_undeploy)
        dpg.hide_item(self.checker_result_window)
        dpg.hide_item(self.button_deploy)
        self.viewmodel.change_bot_state(True)

    def undeploy(self, sender, app_data):
        dpg.show_item(self.button_checker)
        dpg.hide_item(self.button_undeploy)
        self.viewmodel.change_bot_state(False)
        dpg.hide_item(self.trade_result_window)

    def hide_undeploy(self, change):
        if change["new"] is False:
            if self.instance_switch_view.current_view == "loby":
                dpg.show_item(self.trade_result_window)
            dpg.show_item(self.button_checker)
            dpg.hide_item(self.button_undeploy)

    def checker(self, sender, app_data):
        if self.viewmodel.checker():
            dpg.show_item(self.button_deploy)
            dpg.hide_item(self.button_checker)
            dpg.hide_item(self.button_undeploy)
            self.viewmodel.change_bot_state(False)
            self.save_last_inputs()

        dpg.show_item(self.checker_result_window)
        dpg.hide_item(self.trade_result_window)

    def delay_time_connection(self, sender, app_data):
        self.viewmodel.change_delay_time(app_data)
