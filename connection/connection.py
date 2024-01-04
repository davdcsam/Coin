# Standard Libraries
import threading
import time
from datetime import datetime
from typing import Any, Self, Hashable

# Third Party Libraries
import MetaTrader5 as mt5
import pandas as pd
import requests
from traitlets import HasTraits, observe, Any

# Owner Modules
from utils.logs import Logs
from utils.switch_view import SwitchView


class Connection(HasTraits):
    """
    It handles the initialization, connection, and deinitialization,
    to provides real-time updates on the trading thread.
    """

    _instance = None

    login_info = Any()
    login_info_input_alias_name = Any()
    login_info_input_user = Any()
    login_info_input_password = Any()
    login_info_input_server = Any()
    login_info_input_path = Any()
    login_info_input_symbol = Any()

    terminal_info = Any()
    terminal_info_build = Any()
    terminal_info_codepage = Any()
    terminal_info_commondata_path = Any()
    terminal_info_community_account = Any()
    terminal_info_community_balance = Any()
    terminal_info_community_connection = Any()
    terminal_info_company = Any()
    terminal_info_connected = Any()
    terminal_info_data_path = Any()
    terminal_info_dlls_allowed = Any()
    terminal_info_email_enabled = Any()
    terminal_info_ftp_enabled = Any()
    terminal_info_language = Any()
    terminal_info_maxbars = Any()
    terminal_info_mqid = Any()
    terminal_info_name = Any()
    terminal_info_notifications_enabled = Any()
    terminal_info_path = Any()
    terminal_info_ping_last = Any()
    terminal_info_retransmission = Any()
    terminal_info_trade_allowed = Any()
    terminal_info_tradeapi_disabled = Any()

    account_info = Any()
    account_info_assets = Any()
    account_info_balance = Any()
    account_info_commission_blocked = Any()
    account_info_company = Any()
    account_info_credit = Any()
    account_info_currency = Any()
    account_info_currency_digits = Any()
    account_info_equity = Any()
    account_info_fifo_close = Any()
    account_info_leverage = Any()
    account_info_liabilities = Any()
    account_info_limit_orders = Any()
    account_info_login = Any()
    account_info_margin = Any()
    account_info_margin_free = Any()
    account_info_margin_initial = Any()
    account_info_margin_level = Any()
    account_info_margin_maintenance = Any()
    account_info_margin_mode = Any()
    account_info_margin_so_call = Any()
    account_info_margin_so_mode = Any()
    account_info_margin_so_so = Any()
    account_info_name = Any()
    account_info_profit = Any()
    account_info_server = Any()
    account_info_trade_allowed = Any()
    account_info_trade_expert = Any()
    account_info_trade_mode = Any()

    symbol_info = Any()
    symbol_info_ask = Any()
    symbol_info_askhigh = Any()
    symbol_info_asklow = Any()
    symbol_info_bank = Any()
    symbol_info_basis = Any()
    symbol_info_bid = Any()
    symbol_info_bidhigh = Any()
    symbol_info_bidlow = Any()
    symbol_info_category = Any()
    symbol_info_chart_mode = Any()
    symbol_info_currency_base = Any()
    symbol_info_currency_margin = Any()
    symbol_info_currency_profit = Any()
    symbol_info_custom = Any()
    symbol_info_description = Any()
    symbol_info_digits = Any()
    symbol_info_exchange = Any()
    symbol_info_expiration_mode = Any()
    symbol_info_expiration_time = Any()
    symbol_info_filling_mode = Any()
    symbol_info_filling_mode_real = None
    symbol_info_formula = Any()
    symbol_info_isin = Any()
    symbol_info_last = Any()
    symbol_info_lasthigh = Any()
    symbol_info_lastlow = Any()
    symbol_info_margin_hedged = Any()
    symbol_info_margin_hedged_use_leg = Any()
    symbol_info_margin_initial = Any()
    symbol_info_margin_maintenance = Any()
    symbol_info_name = Any()
    symbol_info_option_mode = Any()
    symbol_info_option_right = Any()
    symbol_info_option_strike = Any()
    symbol_info_order_gtc_mode = Any()
    symbol_info_order_mode = Any()
    symbol_info_page = Any()
    symbol_info_path = Any()
    symbol_info_point = Any()
    symbol_info_price_change = Any()
    symbol_info_price_greeks_delta = Any()
    symbol_info_price_greeks_gamma = Any()
    symbol_info_price_greeks_omega = Any()
    symbol_info_price_greeks_rho = Any()
    symbol_info_price_greeks_theta = Any()
    symbol_info_price_greeks_vega = Any()
    symbol_info_price_sensitivity = Any()
    symbol_info_price_theoretical = Any()
    symbol_info_price_volatility = Any()
    symbol_info_select = Any()
    symbol_info_session_aw = Any()
    symbol_info_session_buy_orders = Any()
    symbol_info_session_buy_orders_volume = Any()
    symbol_info_session_close = Any()
    symbol_info_session_deals = Any()
    symbol_info_session_interest = Any()
    symbol_info_session_open = Any()
    symbol_info_session_price_limit_max = Any()
    symbol_info_session_price_limit_min = Any()
    symbol_info_session_price_settlement = Any()
    symbol_info_session_sell_orders = Any()
    symbol_info_session_sell_orders_volume = Any()
    symbol_info_session_turnover = Any()
    symbol_info_session_volume = Any()
    symbol_info_spread = Any()
    symbol_info_spread_float = Any()
    symbol_info_start_time = Any()
    symbol_info_swap_long = Any()
    symbol_info_swap_mode = Any()
    symbol_info_swap_rollover3days = Any()
    symbol_info_swap_short = Any()
    symbol_info_ticks_bookdepth = Any()
    symbol_info_time = Any()
    symbol_info_trade_accrued_interest = Any()
    symbol_info_trade_calc_mode = Any()
    symbol_info_trade_contract_size = Any()
    symbol_info_trade_exemode = Any()
    symbol_info_trade_face_value = Any()
    symbol_info_trade_freeze_level = Any()
    symbol_info_trade_liquidity_rate = Any()
    symbol_info_trade_mode = Any()
    symbol_info_trade_stops_level = Any()
    symbol_info_trade_tick_size = Any()
    symbol_info_trade_tick_value = Any()
    symbol_info_trade_tick_value_loss = Any()
    symbol_info_trade_tick_value_profit = Any()
    symbol_info_visible = Any()
    symbol_info_volume = Any()
    symbol_info_volume_limit = Any()
    symbol_info_volume_max = Any()
    symbol_info_volume_min = Any()
    symbol_info_volume_real = Any()
    symbol_info_volume_step = Any()
    symbol_info_volumehigh = Any()
    symbol_info_volumehigh_real = Any()
    symbol_info_volumelow = Any()
    symbol_info_volumelow_real = Any()

    symbol_info_tick = Any()
    symbol_info_tick_ask = Any()
    symbol_info_tick_bid = Any()
    symbol_info_tick_flags = Any()
    symbol_info_tick_last = Any()
    symbol_info_tick_time = Any()
    symbol_info_tick_time_msc = Any()
    symbol_info_tick_volume = Any()
    symbol_info_tick_volume_real = Any()

    orders_total = Any()

    positions_total = Any()

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance: Self = cls()
        return cls._instance

    def __init__(self) -> None:
        if self._instance is not None:
            raise Exception(
                """
                This is a Singleton Class. Use 'getInstance()'
                to get the single instance.
                """
            )
        else:
            # === PrintLogs === #
            self.instance_logs: Logs = Logs.getInstance()

            # === SwitchView === #
            self.instance_switch_view: SwitchView = SwitchView.getInstance()

            self.thread = None
            self.running: bool = False
            self.delay_time = 0.5
            self.bot_status: bool = False
            self.order_types_dict: dict[str, int] = {
                "Buy": mt5.ORDER_TYPE_BUY,
                "Sell": mt5.ORDER_TYPE_SELL,
            }
            self.df_orders_total = pd.DataFrame(
                columns=[
                    "ticket",
                    "time_setup",
                    "time_setup_msc",
                    "time_expiration",
                    "type",
                    "type_time",
                    "type_filling",
                    "state",
                    "magic",
                    "volume_current",
                    "price_open",
                    "sl",
                    "tp",
                    "price_current",
                    "symbol",
                    "comment",
                    "external_id",
                ]
            )
            self.df_positions_total = pd.DataFrame(
                columns=[
                    "ticket",
                    "time",
                    "type",
                    "magic",
                    "identifier",
                    "reason",
                    "volume",
                    "price_open",
                    "sl",
                    "tp",
                    "price_current",
                    "swap",
                    "profit",
                    "symbol",
                    "comment",
                ]
            )

    def start(self, login_info: dict) -> bool:
        # Check if there's already a thread running
        if self.thread is not None:
            self.instance_logs.log("Already connected")
            return False

        if login_info is None:
            self.instance_logs.notification("Login Inputs are Nulls", "e")
            return False

        self.login_info: dict = login_info

        # Set the running value to True and start the trading thread
        self.running = True
        self.thread = threading.Thread(target=self._method)
        self.thread.start()
        time.sleep(4)
        if self.thread:
            return True

    def _method(self):
        # Verify Connection to Intenet
        try:
            requests.get("http://www.google.com", timeout=3)
        except (requests.ConnectionError, requests.Timeout):
            self.instance_logs.notification("No connection to internet.")
            self._restore_atributes()
            return

        # Try to initialize the MetaTrader 5 terminal
        if not mt5.initialize(
            path=self.login_info["input_path"]["value"],
            login=int(self.login_info["input_user"]["value"]),
            password=self.login_info["input_password"]["value"],
            server=self.login_info["input_server"]["value"],
            timeout=3000,
        ):
            self.instance_logs.notification(
                "Account {} in {} not logged. {}".format(
                    self.login_info["input_user"]["value"],
                    self.login_info["input_server"]["value"],
                    mt5.last_error(),
                ),
                "e",
            )
            self._restore_atributes()
            return

        # _    ____ ____ _ _  _    _  _ ___  ___  ____ ___ ____
        # |    |  | | __ | |\ |    |  | |__] |  \ |__|  |  |___
        # |___ |__| |__] | | \|    |__| |    |__/ |  |  |  |___

        for k, v in self.login_info.items():
            self.__setattr__(f"login_info_{k}", v)

        # ___ ____ ____ _  _ _ _  _ ____ _       _  _ ___  ___  ____ ___ ____
        #  |  |___ |__/ |\/| | |\ | |__| |       |  | |__] |  \ |__|  |  |___
        #  |  |___ |  \ |  | | | \| |  | |___    |__| |    |__/ |  |  |  |___

        terminal_info_temp = mt5.terminal_info()
        if not terminal_info_temp:
            self.instance_logs.notification(
                f"Failed to get to terminal information. {mt5.last_error()}", "e"
            )
            self._restore_atributes()
            return
        self.terminal_info: dict = terminal_info_temp._asdict()
        for k, v in self.terminal_info.items():
            self.__setattr__(f"terminal_info_{k}", v)

        # === Terminal Flags === #

        if not self.terminal_info["trade_allowed"]:
            self.instance_logs.notification(
                "Terminal has algo trading disable. Please, turn on.", "e"
            )
            self._restore_atributes()
            return

        if self.terminal_info["tradeapi_disabled"]:
            self.instance_logs.notification("Terminal blocked MetaTrader5 Api.", "e")
            self._restore_atributes()
            return

        # ____ ____ ____ ____ _  _ _  _ ___    _  _ ___  ___  ____ ___ ____
        # |__| |    |    |  | |  | |\ |  |     |  | |__] |  \ |__|  |  |___
        # |  | |___ |___ |__| |__| | \|  |     |__| |    |__/ |  |  |  |___

        account_info_temp = mt5.account_info()
        if not account_info_temp:
            self.instance_logs.notification(
                f"Failed to get to account information {mt5.last_error()}", "e"
            )
            self._restore_atributes()
            return
        self.account_info: dict = account_info_temp._asdict()
        for k, v in self.account_info.items():
            self.__setattr__(f"account_info_{k}", v)

        # === Account Flags === #

        if not self.account_info["trade_allowed"]:
            self.instance_logs.notification("Account has trade disable.", "e")
            self._restore_atributes()
            return

        if not self.account_info["trade_expert"]:
            self.instance_logs.notification("Account has expert advisors disable.", "e")
            self._restore_atributes()
            return

        # ____ _   _ _  _ ___  ____ _       _  _ ___  ___  ____ ___ ____
        # [__   \_/  |\/| |__] |  | |       |  | |__] |  \ |__|  |  |___
        # ___]   |   |  | |__] |__| |___    |__| |    |__/ |  |  |  |___

        symbol_info_temp = mt5.symbol_info(self.login_info["input_symbol"]["value"])
        if not symbol_info_temp:
            self.instance_logs.notification(
                "Symbol {} not allowed.".format(
                    self.login_info["input_symbol"]["value"]
                ),
                "e",
            )
            self._restore_atributes()
            return
        self.symbol_info: dict = symbol_info_temp._asdict()
        for k, v in self.symbol_info.items():
            self.__setattr__(f"symbol_info_{k}", v)

        # === Symbol Flags === #

        if not self.symbol_info["visible"]:
            self.instance_logs.notification(
                "Symbol {} not visible. Adding it.".format(self.symbol_info["name"])
            )
            if not mt5.symbol_select(self.symbol_info["name"], True):
                time.sleep(3)
                self.instance_logs.notification(
                    "Symbol {} can't be selected.".format(self.symbol_info["name"]), "e"
                )
                self._restore_atributes()
                return

        self.instance_logs.log("Login Flags Passed", "n")

        # Call Main Loop

        # Init
        self._update_data()

        self.instance_switch_view.switch("loby")

        print("Connected to {} Terminal".format(self.terminal_info["name"]))

        if self.bot_status:
            self.Init()
        time.sleep(int(self.delay_time))

        # Any
        while self.running:
            self._update_data()

            if self.bot_status:
                self.Any()
            time.sleep(int(self.delay_time))

        # DeInit
        self._update_data()

        if self.bot_status:
            self.DeInit()
        mt5.shutdown()

        # Restore Value
        self._restore_atributes()

    def _restore_atributes(self):
        # Restore atributes to initial values
        self.running = False

        if self.thread:
            self.thread = None

        for name_atr in (
            "login_info",
            "terminal_info",
            "account_info",
            "symbol_info",
            "symbol_info_tick",
        ):
            if hasattr(self, name_atr) and self.__getattribute__(name_atr):
                for k in self.__getattribute__(name_atr).keys():
                    if hasattr(self, f"{name_atr}_{k}"):
                        self.__setattr__(f"{name_atr}_{k}", None)
                self.__getattribute__(name_atr).clear()

        for dictatr in (
            self.orders_total,
            self.positions_total,
        ):
            if dictatr:
                dictatr.clear()

        for dfatr in (self.df_orders_total, self.df_positions_total):
            if not dfatr.empty:
                dfatr.iloc[0:0]

        self.instance_switch_view.switch("sign_in")
        self.instance_logs.log("All atributes restored", "n")

    def _update_data(self):
        # Verify Connection to Intenet
        try:
            requests.get("http://www.google.com", timeout=3)
        except (requests.ConnectionError, requests.Timeout):
            self.instance_logs.notification("Connection to internet lost.")
            time.sleep(self.delay_time)
            return

        # ____ ____ ____ ____ _  _ _  _ ___    _  _ ___  ___  ____ ___ ____
        # |__| |    |    |  | |  | |\ |  |     |  | |__] |  \ |__|  |  |___
        # |  | |___ |___ |__| |__| | \|  |     |__| |    |__/ |  |  |  |___

        account_info_temp = mt5.account_info()
        if not account_info_temp:
            self.instance_logs.notification(
                "Failed to get to account information. Method 'stop()' will execute.",
                "e",
            )
            self.stop()
            return

        self.account_info: dict = account_info_temp._asdict()
        for k, v in self.account_info.items():
            self.__setattr__(f"account_info_{k}", v)

        # ____ _   _ _  _ ___  ____ _       _  _ ___  ___  ____ ___ ____
        # [__   \_/  |\/| |__] |  | |       |  | |__] |  \ |__|  |  |___
        # ___]   |   |  | |__] |__| |___    |__| |    |__/ |  |  |  |___

        symbol_info_temp = mt5.symbol_info(self.login_info["input_symbol"]["value"])
        if not symbol_info_temp:
            self.instance_logs.notification(
                "Failed to get to account information. Method 'stop()' will execute.",
                "e",
            )
            self.stop()
            return
        self.symbol_info: dict = symbol_info_temp._asdict()
        for k, v in self.symbol_info.items():
            self.__setattr__(f"symbol_info_{k}", v)

        # ___ _ ____ _  _    _  _ ___  ___  ____ ___ ____
        #  |  | |    |_/     |  | |__] |  \ |__|  |  |___
        #  |  | |___ | \_    |__| |    |__/ |  |  |  |___

        symbol_info_tick_temp = mt5.symbol_info_tick(self.symbol_info["name"])
        if not symbol_info_tick_temp:
            self.instance_logs.notification(
                "Failed to get to symbol information. Method 'stop()' will execute.",
                "e",
            )
            self.stop()
            return
        self.symbol_info_tick: dict = symbol_info_tick_temp._asdict()
        for k, v in self.symbol_info.items():
            self.__setattr__(f"symbol_info_tick{k}", v)

        # ____ ___  ____ ____ ____     _  _ ___  ___  ____ ___ ____
        # |  | |  \ |___ |__/ [__      |  | |__] |  \ |__|  |  |___
        # |__| |__/ |___ |  \ ___]     |__| |    |__/ |  |  |  |___

        orders_total_temp = mt5.orders_get(symbol=self.symbol_info["name"])
        if orders_total_temp:
            self.df_orders_total = pd.DataFrame(
                list(orders_total_temp),
                columns=orders_total_temp[0]._asdict().keys(),
            )
        else:
            self.df_orders_total.iloc[0:0]
        self.orders_total: dict[Hashable, Any] = self.df_orders_total.to_dict()

        # ___  ____ ____ _ ___ _ ____ _  _ ____    _  _ ___  ___  ____ ___ ____
        # |__] |  | [__  |  |  | |  | |\ | [__     |  | |__] |  \ |__|  |  |___
        # |    |__| ___] |  |  | |__| | \| ___]    |__| |    |__/ |  |  |  |___

        positions_total_temp = mt5.positions_get(symbol=self.symbol_info["name"])
        if positions_total_temp:
            self.df_positions_total = pd.DataFrame(
                list(positions_total_temp),
                columns=positions_total_temp[0]._asdict().keys(),
            )
        else:
            self.df_positions_total.iloc[0:0]
        self.positions_total: dict[Hashable, Any] = self.df_positions_total.to_dict()

    def stop(self):
        """
        This method stops the trading thread if it is running.
        It sets the running value to False, joins the thread,
        and sets the thread to None.
        """
        # Check if there's a thread running
        if self.thread is None:
            self.instance_logs.log("No conection to stop", "e")
        else:
            # Stop the trading thread
            self.running = False
            self.thread = None
            self.instance_switch_view.switch("sign_in")

    def Init(self):
        """
        Called when the trading thread is initialized.
        Sets up the trading parameters and verifies the terminal information.
        """
        time_broker: str = datetime.fromtimestamp(
            self.symbol_info_tick["time_msc"] / 1000.0
        ).strftime("%H:%M:%S.%f")[:-3]

        print("InitIteration {}".format(time_broker))

    def Any(self):
        """
        Called during the trading thread.
        Checks the current time and verifies if a trade
        can be placed based onthe section time.
        """
        time_broker: str = datetime.fromtimestamp(
            self.symbol_info_tick["time_msc"] / 1000.0
        ).strftime("%H:%M:%S.%f")[:-3]

        print("AnyInteration: {}".format(time_broker))

    def DeInit(self):
        """
        This method is called when the trading thread is deinitialized.
        """
        time_broker: str = datetime.fromtimestamp(
            self.symbol_info_tick["time_msc"] / 1000.0
        ).strftime("%H:%M:%S.%f")[:-3]

        print("DeinitIteration {}".format(time_broker))
