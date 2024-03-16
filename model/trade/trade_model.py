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
    # Define class variables for order results and requests
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
        # Initialize parent classes
        Connection.__init__(self)
        CheckerModule.__init__(self)
        # Initialize instance variables for time section, no position, and logs
        self.instance_section_time = SectionTimeModule()
        self.instance_no_position = NoPositionModule()
        self.instance_logs: Logs = Logs.getInstance()

    """
    ____ _  _ ____ ____ _  _ ____ ____
    |    |__| |___ |    |_/  |___ |__/
    |___ |  | |___ |___ | \_ |___ |  \
    """

    def checker(self, inputs: dict) -> bool:
        # Initialize order check full comment
        self.order_check_full_comment = ""

        # Format inputs
        formated_inputs: dict[str, Any] = ManagerFiles.get_data_formated(inputs)

        # Check if inputs pass the checker
        if not self._inputs(formated_inputs, self.symbol_info_tick_time):
            # Log if inputs didn't pass the checker
            self.instance_logs.internal_log(
                f"Inputs didnt pass checker, {self.order_check_full_comment}", "c"
            )
            return False
        # Log if inputs pass the checker
        self.instance_logs.log("Inputs pass checker", "c")

        # Check if positions fill mode pass the checker
        if not self._postitions_fill_mode(
            formated_inputs,
            self.symbol_info_name,
            self.symbol_info_tick_ask,
            self.symbol_info_tick_bid,
            self.symbol_info_point,
            self.symbol_info_order_gtc_mode,
        ):
            # Log if positions didn't pass the checker
            self.instance_logs.internal_log(
                f"Inputs didnt pass checker, {self.order_check_full_comment}", "c"
            )
            return False
        # Log if positions pass the checker
        self.instance_logs.log("Positions pass checker", "c")

        # Log if inputs pass the checker
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
        # Check if the current time is within a specified section and if there are no positions
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

            # Store the request details in order_result_request
            self.order_result_request = self.order_result["request"]._asdict()
            for k, v in self.order_result_request.items():
                if not hasattr(self, f"order_result_request_{k}"):
                    continue
                self.__setattr__(f"order_result_request_{k}", v)

            # If the trade request was successful, calculate the potential profit and loss
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
                # If the trade request was not successful, log an error message
                self.order_result_full_comment = (
                    "{} order has [not] ben placed. Error: {} {}.".format(
                        self.formated_inputs["input_order_type"],
                        self.order_result["retcode"],
                        self.order_result["comment"],
                    )
                )

            # Log the full comment and the order result
            self.instance_logs.log(self.order_result_full_comment, "t")
            self.instance_logs.log(str(self.order_result), "t")
            # Send a notification that the bot has been shut down
            self.instance_logs.notification("Bot has been shut down.")
            # Set the deinit_flag and bot_status to indicate that the bot has been shut down
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
        # Initialize the section time with the formatted inputs and tick time
        self.instance_section_time.Init(
            self.formated_inputs, self.symbol_info_tick_time
        )

        # Log the initialization iteration, section time, and no positions status
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
        can be placed based on the section time.
        """
        # Perform the operation
        self._operation()

        # Log the iteration, section time, and no positions status
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
        # Log the deinitialization iteration
        self.instance_logs.internal_log(
            "DeinitIteration {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3]
            ),
            "t",
        )
