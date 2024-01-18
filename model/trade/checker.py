# Standard Libraries
from datetime import datetime

# Third Party Libraries
import MetaTrader5 as mt5
from traitlets import HasTraits, Any, Unicode

# Owner Modules

from model.trade.section_time import SectionTimeModule

from utils.manager_files import ManagerFiles
from utils.logs import Logs


class CheckerModule(HasTraits):
    order_check = Any()
    order_check_retcode = Any()
    order_check_full_comment = Unicode()
    order_check_request = Any()
    order_check_request_volume = Any()
    order_check_request_price = Any()
    order_check_request_tp = Any()
    order_check_request_sl = Any()
    order_check_calc_profit = Any()
    order_check_calc_loss = Any()

    def __init__(self) -> None:
        self.instance_section_time = SectionTimeModule()
        self.instance_logs: Logs = Logs.getInstance()

    def _inputs(self, formated_inputs: dict, symbol_info_tick_time: int) -> bool:
        start_time, end_time = self.instance_section_time.verify_existence_from_input(
            formated_inputs, symbol_info_tick_time
        )

        if start_time == end_time:
            self.order_check_full_comment += (
                "Start Time {} cannot equals to End Time {}.\n".format(
                    start_time.strftime("%H:%M:%S"), end_time.strftime("%H:%M:%S")
                )
            )
            return False

        if datetime.utcfromtimestamp(symbol_info_tick_time) >= end_time:
            self.order_check_full_comment += "The broker's current time {} is after the set period {} to {}. The currency can send trades within the time section.\n".format(
                datetime.utcfromtimestamp(symbol_info_tick_time).strftime("%H:%M:%S"),
                start_time.strftime("%H:%M:%S"),
                end_time.strftime("%H:%M:%S"),
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

    def _postitions(self, formated_inputs: dict) -> bool:
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
        self.instance_logs.internal_log(str(self.order_check), "c")

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
            self.order_check_calc_profit = mt5.order_calc_profit(
                self.order_types_dict[formated_inputs["input_order_type"]],
                self.order_check_request["symbol"],
                self.order_check_request["volume"],
                self.order_check_request["price"],
                self.order_check_request["tp"],
            )
            self.order_check_calc_loss = mt5.order_calc_profit(
                self.order_types_dict[formated_inputs["input_order_type"]],
                self.order_check_request["symbol"],
                self.order_check_request["volume"],
                self.order_check_request["price"],
                self.order_check_request["sl"],
            )
            return True
        else:
            self.order_check_calc_profit = 0
            self.order_check_calc_loss = 0
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
