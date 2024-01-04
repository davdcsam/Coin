# Standard Libraries
import pprint
from typing import Any, Literal

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules
from utils.fonts import Fonts
from utils.formater import Formater
from utils.switch_view import SwitchView
from utils.themes import Themes

from viewmodel.set_input_viewmodel import SetInputViewModel


class SetInputView:
    def __init__(self, parent_object, viewmodel: SetInputViewModel) -> None:
        self.viewmodel: SetInputViewModel = viewmodel

        # === Utils === #

        self.instance_fonts = Fonts()
        self.instance_switch_view: SwitchView = SwitchView.getInstance()
        self.instance_themes = Themes()

        # === Windows === #

        self.child_window: int | str = dpg.add_child_window(
            parent=parent_object, width=300, height=550
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

        # === Group Data Trade === #

        self.group_data_trade: int | str = dpg.add_group(
            width=180, parent=self.child_window
        )

        self.title_data_trade: int | str = dpg.add_text(
            default_value="Data Trade", parent=self.group_data_trade
        )

        self.input_lot_size: int | str = dpg.add_input_float(
            label="Lot Size", parent=self.group_data_trade
        )

        self.input_take_profit: int | str = dpg.add_input_float(
            label="Take Profit",
            parent=self.group_data_trade,
        )

        self.input_stop_loss: int | str = dpg.add_input_float(
            label="Stop Loss", parent=self.group_data_trade
        )

        self.input_magic_number: int | str = dpg.add_input_int(
            label="Magic Number",
            parent=self.group_data_trade,
        )

        self.input_deviation_trade: int | str = dpg.add_input_int(
            label="Deviation",
            parent=self.group_data_trade,
        )

        # === Group Section Time == #

        self.group_section_time: int | str = dpg.add_group(
            width=180, parent=self.child_window
        )

        self.title_section_time: int | str = dpg.add_text(
            default_value="Section Time", parent=self.group_section_time
        )

        self.input_time_start: int | str = dpg.add_time_picker(
            label="Start Time", hour24=True, parent=self.group_section_time
        )

        self.input_time_end: int | str = dpg.add_time_picker(
            label="End Time",
            hour24=True,
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
            label="Deplay Time",
            default_value=self.viewmodel.model_connection.delay_time,
            format="%.2f s",
            min_value=0.1,
            max_value=2,
            callback=self.delay_time_connection,
            parent=self.group_manager_bot,
        )

        self.button_deploy: int | str = dpg.add_button(
            label="Deploy",
            callback=self.deploy,
            show=False,
            parent=self.group_manager_bot,
        )

        self.button_undeploy: int | str = dpg.add_button(
            label="Undeploy",
            pos=(136, 494),
            callback=self.undeploy,
            show=False,
            parent=self.group_manager_bot,
        )

        self.button_checker: int | str = dpg.add_button(
            label="Checker",
            callback=self.checker,
            parent=self.group_manager_bot,
        )

        # dpg.add_button(label="Test", callback=lambda: print(dpg.get_item_pos(self.button_checker), dpg.get_item_pos(self.input_lot_size)), parent=self.group_manager_bot)

        self.instance_fonts.set_font_items(
            [
                self.title_bot_manager,
                self.title_data_trade,
                self.title_section_time,
            ]
        )

        self.viewmodel.bind_inputs(self)

    def update_item(self, item, value):
        if dpg.does_item_exist(item):
            dpg.set_value(item, value)

    def load_inputs(self, sender, app_data):
        inputs: dict[str, Any] | Literal[False] = self.viewmodel.load_inputs()

        pprint.pprint(inputs)
        if not inputs:
            return

        for k, v in inputs.items():
            self.update_item(self.__getattribute__(k), v)

    def load_last_inputs(self):
        inputs: dict[str, Any] | Literal[False] = self.viewmodel.load_last_input()
        if not inputs:
            return

        for k, v in inputs.items():
            self.update_item(self.__getattribute__(k), v)

        print("Load Last Inputs Successfully")

    def save_inputs(self, sender, app_data):
        self.viewmodel.save_inputs()

    def save_last_inputs(self):
        self.viewmodel.save_last_input()

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

        if (
            "symbol_info_digits" in change["name"]
            or "account_info_currency" in change["name"]
        ):
            for atr in [
                self.input_take_profit,
                self.input_stop_loss,
            ]:
                if dpg.does_item_exist(atr):
                    if "symbol_info_digits" in change["name"]:
                        dpg.configure_item(
                            atr,
                            format=Formater.change_decimals_from_format_num(
                                dpg.get_item_configuration(atr)["format"], change["new"]
                            ),
                        )
                    else:
                        dpg.configure_item(
                            atr,
                            format="{} {}".format(
                                dpg.get_item_configuration(atr)["format"], change["new"]
                            ),
                        )
            return

    def deploy(self, sender, app_data):
        dpg.show_item(self.button_undeploy)
        dpg.hide_item(self.button_deploy)
        self.viewmodel.change_bot_state(True)

    def undeploy(self, sender, app_data):
        dpg.show_item(self.button_checker)
        dpg.hide_item(self.button_undeploy)
        self.viewmodel.change_bot_state(False)

    def checker(self, sender, app_data):
        if self.viewmodel.checker_orders_positions():
            dpg.show_item(self.button_deploy)
            dpg.hide_item(self.button_undeploy)
            dpg.hide_item(self.button_checker)

    def delay_time_connection(self, sender, app_data):
        self.viewmodel.change_delay_time(app_data)
