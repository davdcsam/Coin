# Standard Libraries
from datetime import datetime
from pprint import pprint


# Third Party Libraries
import MetaTrader5 as mt5
from traitlets import Any, Unicode

# Owner Modules
from connection.connection import Connection

from model.trade.section_time import SectionTimeModule
from model.trade.no_position import NoPositionModule

from utils.manager_files import ManagerFiles


class TradeModel(Connection):
    order_check = Any()
    order_check_retcode = Any()
    order_check_full_comment = Unicode()

    order_check_request = Any()
    order_check_request_volume = Any()
    order_check_request_price = Any()
    order_check_request_tp = Any()
    order_check_request_sl = Any()

    order_calc_profit = Any()
    order_calc_loss = Any()

    def __init__(self) -> None:
        super().__init__()
        self.instance_section_time = SectionTimeModule()
        self.instance_no_position = NoPositionModule()

    """
    ____ _  _ ____ ____ _  _ ____ ____
    |    |__| |___ |    |_/  |___ |__/
    |___ |  | |___ |___ | \_ |___ |  \
    """

    def checker(self, inputs: dict) -> bool:
        self.order_check = None
        self.order_check_retcode = None
        self.order_check_full_comment = ""

        self.order_check_request = None
        self.order_check_request_volume = None
        self.order_check_request_price = None
        self.order_check_request_tp = None
        self.order_check_request_sl = None

        self.order_calc_profit = None
        self.order_calc_loss = None

        formated_inputs: dict[str, Any] = ManagerFiles.get_data_formated(inputs)

        if not self._checker_inputs(formated_inputs):
            return False

        if not self._checker_positions(formated_inputs):
            return False

        return True

    def _checker_inputs(self, formated_inputs: dict) -> bool:
        start_time, end_time = self.instance_section_time.verify_existence_from_input(
            formated_inputs, self.symbol_info_tick_time
        )

        if start_time == end_time:
            self.order_check_full_comment += (
                "Start Time {} cannot equals to End Time {}.\n".format(
                    start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S")
                )
            )

            return False

        if (
            formated_inputs["input_stop_loss"] * 0.01
            > formated_inputs["input_deviation_trade"]
            or formated_inputs["input_take_profit"] * 0.01
            > formated_inputs["input_deviation_trade"]
        ):
            self.order_check_full_comment += "The deviation may not be sufficient. If there is too much volatility the order could not be placed.\n"

        return True

    def _checker_positions(self, formated_inputs: dict) -> bool:
        for request in self._checker_build_request(
            formated_inputs["input_lot_size"],
            self.order_types_dict[formated_inputs["input_order_type"]],
            formated_inputs["input_take_profit"],
            formated_inputs["input_stop_loss"],
            formated_inputs["input_deviation_trade"],
        ):
            order_check = mt5.order_check(request)

            if not order_check:
                self.instance_logs.notification(
                    "Error when indexing request format to check order. Contact to bot developer.",
                    "e",
                )
                return False

            if order_check.retcode != mt5.TRADE_RETCODE_INVALID_FILL:
                self.symbol_info_filling_mode_real = order_check.request.type_filling
                break

        self.order_check = order_check._asdict()
        order_check_comment_temp = self.order_check["comment"]
        if order_check_comment_temp == "Done":
            self.order_check_full_comment += "{} order can be placed.\n".format(
                formated_inputs["input_order_type"]
            )
        else:
            self.order_check_full_comment += "{}.\n".format(self.order_check["comment"])
        self.order_check_retcode = self.order_check["retcode"]

        self.order_check_request = self.order_check["request"]._asdict()
        for k, v in self.order_check_request.items():
            if not hasattr(self, f"order_check_request_{k}"):
                continue
            self.__setattr__(f"order_check_request_{k}", v)

        if order_check.retcode == 0:
            self.order_calc_profit = mt5.order_calc_profit(
                self.order_types_dict[formated_inputs["input_order_type"]],
                self.order_check_request["symbol"],
                self.order_check_request["volume"],
                self.order_check_request["price"],
                self.order_check_request["tp"],
            )
            self.order_calc_loss = mt5.order_calc_profit(
                self.order_types_dict[formated_inputs["input_order_type"]],
                self.order_check_request["symbol"],
                self.order_check_request["volume"],
                self.order_check_request["price"],
                self.order_check_request["sl"],
            )
            return True
        else:
            self.order_calc_profit = 0
            self.order_calc_loss = 0
            return False

    def _checker_build_request(
        self,
        volume: float,
        type_positions: mt5.ORDER_TYPE_BUY | mt5.ORDER_TYPE_SELL,
        take_profit: int,
        stop_loss: int,
        deviation_trade: int,
    ):
        """
        Prepare a trade request with the necessary parameters
        """
        request_list = []
        for filling_mode in [
            mt5.ORDER_FILLING_FOK,
            mt5.ORDER_FILLING_IOC,
            mt5.ORDER_FILLING_RETURN,
            mt5.ORDER_FILLING_BOC,
        ]:
            trade_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol_info_name,
                "volume": volume,
                "type": type_positions,
                "deviation": deviation_trade,
                "magic": 0,
                "comment": "",
                "type_time": self.symbol_info_order_gtc_mode,
                "type_filling": filling_mode,
            }
            # If the order type is Buy, calculate the price, stop loss, and take profit
            if type_positions == mt5.ORDER_TYPE_BUY:
                price = self.symbol_info_ask
                sl = price - stop_loss * self.symbol_info_point
                tp = price + take_profit * self.symbol_info_point
            # If the order type is Sell, calculate the price, stop loss, and take profit
            elif type_positions == mt5.ORDER_TYPE_SELL:
                price = self.symbol_info_bid
                sl = price + stop_loss * self.symbol_info_point
                tp = price - take_profit * self.symbol_info_point
            # Update the trade request with the calculated price, stop loss, and take profit
            trade_request.update({"price": price, "sl": sl, "tp": tp})

            request_list.append(trade_request)

        return request_list

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
            request = self._operation_build_request(
                self.formated_inputs["input_lot_size"],
                self.order_types_dict[self.formated_inputs["input_order_type"]],
                self.formated_inputs["input_take_profit"],
                self.formated_inputs["input_stop_loss"],
                self.formated_inputs["input_deviation_trade"],
            )

            order_check = mt5.order_check(request)

            if order_check.retcode == 0:
                self.instance_logs.notification(
                    "{} order can be placed".format(
                        self.formated_inputs["input_order_type"]
                    ),
                    "t",
                )
            else:
                self.instance_logs.notification(
                    "{} order cannot be placed. Error:{} {}.".format(
                        self.formated_inputs["input_order_type"],
                        order_check.retcode,
                        order_check.comment,
                    ),
                    "t",
                )

                self.instance_logs.notification("Bot'll will shutdown.")
                self.deinit_flag = True
                self.bot_status = False

            # Send the trade request
            order_result = mt5.order_send(request)

            # If the trade request was not successful, print an error message
            if order_result.retcode != mt5.TRADE_RETCODE_DONE:
                self.instance_logs.notification(
                    "{} order has [not] ben placed. Error: {} {}.".format(
                        self.formated_inputs["input_order_type"],
                        order_check.retcode,
                        order_check.comment,
                    )
                )
            else:
                # If the trade request was successful
                self.instance_logs.notification(
                    "{} order has been placed.".format(
                        self.formated_inputs["input_order_type"],
                    )
                )

            self.instance_logs.notification("Bot'll will shutdown.")
            self.deinit_flag = True
            self.bot_status = False

    def _operation_build_request(
        self,
        volume: float,
        type_positions: mt5.ORDER_TYPE_BUY | mt5.ORDER_TYPE_SELL,
        take_profit: int,
        stop_loss: int,
        deviation_trade: int,
    ):
        trade_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol_info_name,
            "volume": volume,
            "type": type_positions,
            "deviation": deviation_trade,
            "magic": 0,
            "comment": "",
            "type_time": self.symbol_info_order_gtc_mode,
            "type_filling": self.symbol_info_filling_mode_real,
        }
        # If the order type is Buy, calculate the price, stop loss, and take profit
        if type_positions == mt5.ORDER_TYPE_BUY:
            price = self.symbol_info_ask
            sl = price - stop_loss * self.symbol_info_point
            tp = price + take_profit * self.symbol_info_point
        # If the order type is Sell, calculate the price, stop loss, and take profit
        elif type_positions == mt5.ORDER_TYPE_SELL:
            price = self.symbol_info_bid
            sl = price + stop_loss * self.symbol_info_point
            tp = price - take_profit * self.symbol_info_point
        # Update the trade request with the calculated price, stop loss, and take profit
        trade_request.update({"price": price, "sl": sl, "tp": tp})

        return trade_request

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

        print(
            "InitIteration:{} - Section Time {} - No Positions {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3],
                self.instance_section_time.Any(self.symbol_info_tick_time),
                self.instance_no_position.Any(
                    self.formated_inputs, self.df_positions_total
                ),
            )
        )

    def Any(self):
        """
        Called during the trading thread.
        Checks the current time and verifies if a trade
        can be placed based onthe section time.
        """
        self._operation()

        print(
            "AnyInteration: {} - Section Time {} - No Positions {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3],
                self.instance_section_time.Any(self.symbol_info_tick_time),
                self.instance_no_position.Any(
                    self.formated_inputs, self.df_positions_total
                ),
            )
        )

    def DeInit(self):
        """
        This method is called when the trading thread is deinitialized.
        """

        print(
            "DeinitIteration {}".format(
                datetime.utcfromtimestamp(
                    self.symbol_info_tick_time_msc / 1000.0
                ).strftime("%H:%M:%S.%f")[:-3]
            )
        )
