# Standard Libraries
from typing import Any

# Third Party Libraries
from connection.connection import Connection

# Owner Modules


class WatchMarketViewModel:
    def __init__(self, model_connection: Connection | Any) -> None:
        self.model_connection: Connection | Any = model_connection

    def bind(self, view):
        items_observed: list[str] = [
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
            "symbol_info_trade_mode",
            "symbol_info_ask",
            "symbol_info_bid",
            "symbol_info_volume_min",
            "symbol_info_volume_max",
            "symbol_info_volume_step",
            "symbol_info_volume_limit",
        ]
        for item_observed in items_observed:
            self.model_connection.observe(view.update_items, item_observed)

        tables_observed: list[str] = [
            "terminal_info",
            "account_info",
            "symbol_info",
        ]
        for table_observed in tables_observed:
            self.model_connection.observe(view.update_tables, table_observed)
