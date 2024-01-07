# Standard Libraries
from typing import Any, Literal

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules
from utils.fonts import Fonts
from utils.switch_view import SwitchView
from utils.themes import Themes

from viewmodel.sign_viewmodel import SignViewModel


class SignView:
    def __init__(
        self,
        viewmodel: SignViewModel,
    ) -> None:
        self.viewmodel: SignViewModel = viewmodel

        # === Utils === #

        self.instance_fonts = Fonts()
        self.instance_switch_view: SwitchView = SwitchView.getInstance()
        self.instance_themes = Themes()

        # === Sign In Window === #

        self.sign_in_window: int | str = dpg.add_window(
            no_title_bar=True,
            no_resize=True,
            width=300,
            height=430,
        )

        self.instance_themes.dark_window(self.sign_in_window)

        dpg.set_item_pos(
            self.sign_in_window,
            pos=(
                (
                    int(dpg.get_viewport_width())
                    - int(dpg.get_item_width(self.sign_in_window))
                )
                / 2,
                (
                    int(dpg.get_viewport_height())
                    - int(dpg.get_item_height(self.sign_in_window))
                )
                / 2,
            ),
        )

        # === Group Titles === #

        self.group_titles: int | str = dpg.add_group(parent=self.sign_in_window)

        self.title_coin: int | str = dpg.add_text(
            default_value="Coin",
            color=self.instance_themes.primary,
            parent=self.group_titles,
        )

        self.instance_fonts.set_font_items(
            [self.title_coin], "opensans_semibold_title_60"
        )

        self.description: int | str = dpg.add_text(
            default_value="Authorize access to your trade account",
            parent=self.group_titles,
        )

        # === Group Inputs === #

        self.group_inputs: int | str = dpg.add_group(parent=self.sign_in_window)

        self.input_alias_name: int | str = dpg.add_input_text(
            label="Alias", parent=self.group_inputs
        )

        self.input_user: int | str = dpg.add_input_text(
            label="User",
            no_spaces=True,
            parent=self.group_inputs,
        )

        self.input_password: int | str = dpg.add_input_text(
            label="Password",
            no_spaces=True,
            parent=self.group_inputs,
        )

        self.input_server: int | str = dpg.add_input_text(
            label="Server",
            no_spaces=True,
            parent=self.group_inputs,
        )

        self.input_path: int | str = dpg.add_combo(
            items=self.viewmodel.fill_input_path(),
            label="Terminal",
            parent=self.group_inputs,
        )

        self.input_symbol: int | str = dpg.add_input_text(
            label="Symbol",
            no_spaces=True,
            parent=self.group_inputs,
        )

        # === Group Buttons === #

        self.group_buttons: int | str = dpg.add_group(parent=self.sign_in_window)

        self.custom_terminal: int | str = dpg.add_button(
            label="Custom Terminal",
            callback=self.custom_terminal_update,
            parent=self.group_buttons,
        )

        self.sign_in: int | str = dpg.add_button(
            label="Sign in",
            callback=self.sign_in_connect,
            parent=self.group_buttons,
        )

        # === Group Load Save === #

        self.group_load_save: int | str = dpg.add_group(parent=self.sign_in_window)

        self.load: int | str = dpg.add_button(
            label="Load",
            callback=self.load_inputs,
            parent=self.group_load_save,
        )

        self.save: int | str = dpg.add_button(
            label="Save",
            callback=self.save_inputs,
            parent=self.group_load_save,
        )

        # === Sign Out Window === #

        self.sign_out_window: int | str = dpg.add_window(
            no_title_bar=True,
            no_resize=True,
            width=200,
            height=130,
        )

        self.instance_themes.dark_window(self.sign_out_window)

        dpg.set_item_pos(
            self.sign_out_window,
            pos=(
                (
                    int(dpg.get_viewport_width())
                    - int(dpg.get_item_width(self.sign_out_window))
                )
                / 2,
                (
                    int(dpg.get_viewport_height())
                    - int(dpg.get_item_height(self.sign_out_window))
                )
                / 2,
            ),
        )

        self.title_sign_out: int | str = dpg.add_text(
            default_value="Are you sure to sign out?",
            wrap=dpg.get_item_width(self.sign_out_window) - 40,
            pos=(20, 10),
            parent=self.sign_out_window,
        )

        self.instance_fonts.set_font_items([self.title_sign_out])

        self.accept_sign_out: int | str = dpg.add_button(
            label="Yes, I do",
            pos=(20, 80),
            callback=self._accept_sign_out,
            parent=self.sign_out_window,
        )

        self.cancel_sign_out: int | str = dpg.add_button(
            label="Cancel",
            pos=(130, 80),
            callback=self._cancel_sign_out,
            parent=self.sign_out_window,
        )

        # === Bind to ViewModel === #

        self.viewmodel.bind(self)

    def update_item(self, item, value):
        if dpg.does_item_exist(item):
            dpg.set_value(item, value)

    def custom_terminal_update(self, sender, app_data):
        self.update_item(self.input_path, self.viewmodel.custom_terminal_input_path())

    def sign_in_connect(self, sender, app_data):
        if self.viewmodel.open_connection():
            self.instance_switch_view.switch("loby")

    def load_inputs(self, sender, app_data):
        inputs: dict[str, Any] | Literal[False] = self.viewmodel.load_inputs()

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

    def _accept_sign_out(self, sender, app_data):
        self.viewmodel.close_connection()
        self.instance_switch_view.switch("sign_in")

    def _cancel_sign_out(self, sender, app_data):
        self.instance_switch_view.switch("loby")
