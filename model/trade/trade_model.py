# Standard Libraries
from datetime import datetime
from pprint import pprint

# Third Party Libraries
import MetaTrader5 as mt5
from traitlets import Any, Unicode

# Owner Modules
from connection.connection import Connection

from model.trade.request import RequestModule
from model.trade.checker import CheckerModule
from model.trade.section_time import SectionTimeModule
from model.trade.no_position import NoPositionModule

from utils.manager_files import ManagerFiles
from utils.logs import Logs


class TradeModel(Connection, CheckerModule):
    order_result = Any()
    order_result_full_comment = Unicode()
    order_result_request = Any()
    order_result_request_volume = Any()
    order_result_request_price = Any()
    order_result_request_tp = Any()
    order_result_request_sl = Any()
    order_result_calc_profit = Any()
    order_result_calc_loss = Any()

    def __init__(self) -> None:
        Connection.__init__(self)
        CheckerModule.__init__(self)
        self.instance_section_time = SectionTimeModule()
        self.instance_no_position = NoPositionModule()
        self.instance_logs: Logs = Logs.getInstance()

    """
    ____ _  _ ____ ____ _  _ ____ ____
    |    |__| |___ |    |_/  |___ |__/
    |___ |  | |___ |___ | \_ |___ |  \
    """

    def checker(self, inputs: dict) -> bool:
        self.order_check_full_comment = ""

        formated_inputs: dict[str, Any] = ManagerFiles.get_data_formated(inputs)

        if not self._inputs(formated_inputs, self.symbol_info_tick_time):
            self.instance_logs.internal_log(
                f"Inputs didnt pass checker, {self.order_check_full_comment}", "c"
            )
            return False
        self.instance_logs.log("Inputs pass checker", "c")

        if not self._postitions_fill_mode(
            formated_inputs,
            self.symbol_info_name,
            self.symbol_info_tick_ask,
            self.symbol_info_tick_bid,
            self.symbol_info_point,
            self.symbol_info_order_gtc_mode,
        ):
            self.instance_logs.internal_log(
                f"Inputs didnt pass checker, {self.order_check_full_comment}", "c"
            )
            return False
        self.instance_logs.log("Positions pass checker", "c")

        self.instance_logs.internal_log(
            f"Inputs pass checker, {self.order_check_full_comment}", "c"
        )
        return True

    """
    ____ ___  ____ ____ ____ ___ _ ____ _  _
    |  | |__] |___ |__/ |__|  |  | |  | |\ |
    |__| |    |___ |  \ |  |  |  | |__| | \|
    """

    def _operation(self):
        if self.instance_section_time.Any(
            self.symbol_info_tick_time
        ) and self.instance_no_position.Any(
            self.formated_inputs, self.df_positions_total
        ):
            self.order_result_full_comment = ""

            # Send the trade request
            self.order_result = mt5.order_send(
                RequestModule.build(
                    self.symbol_info_name,
                    self.formated_inputs["input_lot_size"],
                    self.order_types_dict[self.formated_inputs["input_order_type"]],
                    self.formated_inputs["input_take_profit"],
                    self.formated_inputs["input_stop_loss"],
                    self.formated_inputs["input_deviation_trade"],
                    self.symbol_info_tick_ask,
                    self.symbol_info_tick_bid,
                    self.symbol_info_point,
                    self.symbol_info_order_gtc_mode,
                    self.symbol_info_filling_mode_real,
                )
            )._asdict()

            self.order_result_request = self.order_result["request"]._asdict()
            for k, v in self.order_result_request.items():
                if not hasattr(self, f"order_result_request_{k}"):
                    continue
                self.__setattr__(f"order_result_request_{k}", v)

            # If the trade request was not successful, show an error message
            if self.order_result["retcode"] == mt5.TRADE_RETCODE_DONE:
                self.order_result_full_comment += "{} order has been placed.".format(
                    self.formated_inputs["input_order_type"],
                )

                self.order_result_calc_profit = mt5.order_calc_profit(
                    self.order_types_dict[self.formated_inputs["input_order_type"]],
                    self.order_result_request["symbol"],
                    self.order_result_request["volume"],
                    self.order_result_request["price"],
                    self.order_result_request["tp"],
                )
                self.order_result_calc_loss = mt5.order_calc_profit(
                    self.order_types_dict[self.formated_inputs["input_order_type"]],
                    self.order_result_request["symbol"],
                    self.order_result_request["volume"],
                    self.order_result_request["price"],
                    self.order_result_request["sl"],
                )
            else:
                self.order_result_full_comment = (
                    "{} order has [not] ben placed. Error: {} {}.".format(
                        self.formated_inputs["input_order_type"],
                        self.order_result["retcode"],
                        self.order_result["comment"],
                    )
                )

            self.instance_logs.log(self.order_result_full_comment, "t")
            self.instance_logs.log(str(self.order_result), "t")
            self.instance_logs.notification("Bot has been shut down.")
            self.deinit_flag = True
            self.bot_status = False

    """
    _  _ ____ ___  _ ____ _ ____ ___     ___  ____ ____ ____ ____ ____ ____ ____ ____
    |\/| |  | |  \ | |___ | |___ |  \    |__] |__/ |  | |    |___ [__  [__  |___ [__ 
    |  | |__| |__/ | |    | |___ |__/    |    |  \ |__| |___ |___ ___] ___] |___ ___]
    """

    def Init(self):
        """
        Called when the trading thread is initialized.
        Sets up the trading parameters and verifies the terminal information.
        """
        self.instance_section_time.Init(
            self.formated_inputs, self.symbol_info_tick_time
        )

        self.instance_logs.internal_log(
            "InitIteration:{} - Section Time {} - No Positions {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3],
                self.instance_section_time.Any(self.symbol_info_tick_time),
                self.instance_no_position.Any(
                    self.formated_inputs, self.df_positions_total
                ),
            ),
            "t",
        )

    def Any(self):
        """
        Called during the trading thread.
        Checks the current time and verifies if a trade
        can be placed based onthe section time.
        """
        self._operation()

        self.instance_logs.internal_log(
            "AnyInteration: {} - Section Time {} - No Positions {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3],
                self.instance_section_time.Any(self.symbol_info_tick_time),
                self.instance_no_position.Any(
                    self.formated_inputs, self.df_positions_total
                ),
            ),
            "t",
        )

    def DeInit(self):
        """
        This method is called when the trading thread is deinitialized.
        """

        self.instance_logs.internal_log(
            "DeinitIteration {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3]
            ),
            "t",
        )
