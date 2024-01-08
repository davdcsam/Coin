# Standard Libraries
import datetime
from typing import LiteralString

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules
from utils.fonts import Fonts
from utils.switch_view import SwitchView


class WatchMarketView:
    def __init__(self, parent_object, viewmodel) -> None:
        # === Utils === #

        self.instance_fonts = Fonts()

        self.instance_switch_view: SwitchView = SwitchView.getInstance()

        # ··· Atr ··· #

        self.viewmodel = viewmodel

        # === Windows === #

        self.child_window: int | str = dpg.add_child_window(
            parent=parent_object, no_scrollbar=True, width=360, height=560, pos=(312, 8)
        )

        # === Group Titles === #

        self.group_titles: int | str = dpg.add_group(parent=self.child_window)

        self.title: int | str = dpg.add_text(
            default_value="Watch Market", parent=self.group_titles
        )

        self.instance_fonts.set_font_item(self.title)

        # === Group Full Info === #

        self.group_full_info: int | str = dpg.add_group(
            parent=self.child_window,
        )

        self.watch_market_full: int | str = dpg.add_button(
            label="More Information",
            callback=lambda: dpg.show_item(self.full_view_window),
            parent=self.group_full_info,
        )

        # === Group Login Info === #

        self.group_login_info: int | str = dpg.add_group(parent=self.child_window)

        self.login_info_input_alias_name: int | str = dpg.add_text(
            default_value="",
            label="Alias Name",
            show_label=True,
            parent=self.group_login_info,
        )

        self.login_info_input_user: int | str = dpg.add_text(
            default_value="",
            label="User",
            show_label=True,
            parent=self.group_login_info,
        )

        self.login_info_input_server: int | str = dpg.add_text(
            default_value="",
            label="Server",
            show_label=True,
            parent=self.group_login_info,
        )

        self.account_info_company: int | str = dpg.add_text(
            default_value="",
            label="Company",
            show_label=True,
            parent=self.group_login_info,
        )

        # === Group Account Info === #

        self.group_account_info: int | str = dpg.add_group(parent=self.child_window)

        self.account_info_balance: int | str = dpg.add_text(
            default_value="",
            label="Balance",
            show_label=True,
            parent=self.group_account_info,
        )

        self.account_info_equity: int | str = dpg.add_text(
            default_value="",
            label="Equity",
            show_label=True,
            parent=self.group_account_info,
        )

        self.account_info_profit: int | str = dpg.add_text(
            default_value="",
            label="Profit",
            show_label=True,
            parent=self.group_account_info,
        )

        # === Group Symbol Info === #

        self.group_symbol_info: int | str = dpg.add_group(parent=self.child_window)

        self.symbol_info_name: int | str = dpg.add_text(
            default_value="",
            label="Symbol",
            show_label=True,
            parent=self.group_symbol_info,
        )

        self.symbol_info_description: int | str = dpg.add_text(
            default_value="",
            label="Description",
            show_label=True,
            parent=self.group_symbol_info,
        )

        self.symbol_info_time: int | str = dpg.add_text(
            default_value="",
            label="Symbol Time",
            show_label=True,
            parent=self.group_symbol_info,
        )

        self.symbol_info_ask: int | str = dpg.add_text(
            default_value="",
            label="Ask",
            show_label=True,
            parent=self.group_symbol_info,
        )

        self.symbol_info_bid: int | str = dpg.add_text(
            default_value="",
            label="Bid",
            show_label=True,
            parent=self.group_symbol_info,
        )

        # === Group Full View === #

        self.full_view_window: int | str = dpg.add_window(
            label="Full View WatchMarket",
            width=500,
            height=400,
            no_collapse=True,
            show=False,
        )

        dpg.set_item_pos(
            self.full_view_window,
            pos=(
                (
                    int(dpg.get_viewport_width())
                    - int(dpg.get_item_width(self.full_view_window))
                )
                / 2,
                (
                    int(dpg.get_viewport_height())
                    - int(dpg.get_item_height(self.full_view_window))
                )
                / 2,
            ),
        )

        self.full_view_tab_bar: int | str = dpg.add_tab_bar(
            parent=self.full_view_window
        )

        # === Build Terminal Full View === #

        self.terminal_full_view_tab: int | str = dpg.add_tab(
            label="Terminal",
            parent=self.full_view_tab_bar,
        )

        self.terminal_info_table: int | str = dpg.add_table(
            header_row=True,
            parent=self.terminal_full_view_tab,
        )

        self.terminal_info_table_column_name: int | str = dpg.add_table_column(
            parent=self.terminal_info_table,
            label="Name",
        )

        self.terminal_info_table_column_value: int | str = dpg.add_table_column(
            parent=self.terminal_info_table,
            label="Value",
        )

        # === Build Account Full View === #

        self.account_full_view_tab: int | str = dpg.add_tab(
            label="Account",
            parent=self.full_view_tab_bar,
        )

        self.account_info_table: int | str = dpg.add_table(
            header_row=True,
            parent=self.account_full_view_tab,
        )

        self.account_info_table_column_name: int | str = dpg.add_table_column(
            parent=self.account_info_table,
            label="Name",
        )

        self.account_info_table_column_value: int | str = dpg.add_table_column(
            parent=self.account_info_table,
            label="Value",
        )

        # === Build Symbol Full View === #

        self.symbol_full_view_tab: int | str = dpg.add_tab(
            label="Symbol",
            parent=self.full_view_tab_bar,
        )

        self.symbol_info_table: int | str = dpg.add_table(
            header_row=True,
            parent=self.symbol_full_view_tab,
        )

        self.symbol_info_table_column_name: int | str = dpg.add_table_column(
            parent=self.symbol_info_table,
            label="Name",
        )

        self.symbol_info_table_column_value: int | str = dpg.add_table_column(
            parent=self.symbol_info_table,
            label="Value",
        )

        self.viewmodel.bind(self)

    def callback_switch_view(self, change):
        if change["new"] == "sign_out":
            dpg.hide_item(self.full_view_window)

    def update_items(self, change):
        if change["new"] is None:
            return

        items: list[str] = [
            "login_info_input_alias_name",
            "login_info_input_user",
            "login_info_input_server",
            "account_info_company",
            "account_info_balance",
            "account_info_equity",
            "account_info_profit",
            "symbol_info_name",
            "symbol_info_description",
            "symbol_info_time",
            "symbol_info_ask",
            "symbol_info_bid",
        ]
        for item in items:
            if (
                item in change["name"]
                and hasattr(self, change["name"])
                and dpg.does_item_exist(self.__getattribute__(change["name"]))
            ):
                if item in [
                    "account_info_balance",
                    "account_info_equity",
                    "account_info_profit",
                ]:
                    formated_value: str = "{} {:,.2f}".format(
                        self.viewmodel.model_connection.account_info["currency"],
                        float(change["new"]),
                    )
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        formated_value,
                    )
                    continue

                if item in "symbol_info_time":
                    formated_value: str = datetime.datetime.utcfromtimestamp(
                        change["new"]
                    )
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        formated_value,
                    )
                    continue

                if isinstance(change["new"], dict):
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        change["new"]["value"],
                    )
                else:
                    dpg.set_value(
                        self.__getattribute__(change["name"]),
                        change["new"],
                    )

    def update_tables(self, change):
        if change["new"] is None:
            return
        tables: dict[str, int | str] = {
            "terminal_info": self.terminal_info_table,
            "account_info": self.account_info_table,
            "symbol_info": self.symbol_info_table,
        }
        for name, table in tables.items():
            if name in change["name"] and dpg.does_item_exist(table):
                self._fill_table(change["new"], table)

    def _fill_table(self, info: dict, parent_table: int | str):
        children: list = dpg.get_item_children(parent_table)[1]
        for child in children:
            dpg.delete_item(child)

        for key, value in info.items():
            formatted_key: LiteralString = " ".join(
                word.capitalize() for word in key.split("_")
            )

            row: int | str = dpg.add_table_row(parent=parent_table)
            dpg.add_text(
                formatted_key,
                wrap=dpg.get_item_width(dpg.get_item_children(parent_table, 0)[0]),
                parent=row,
            )
            dpg.add_text(
                value,
                wrap=dpg.get_item_width(dpg.get_item_children(parent_table, 0)[1]),
                parent=row,
            )
