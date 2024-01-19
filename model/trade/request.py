# Standard

# Third Party
from typing import Any
import MetaTrader5 as mt5

# Owner


class RequestModule:
    @staticmethod
    def build(
        symbol: str,
        volume: float,
        type_positions: mt5.ORDER_TYPE_BUY | mt5.ORDER_TYPE_SELL,
        take_profit: int,
        stop_loss: int,
        deviation_trade: int,
        price_ask: float,
        price_bid: float,
        point,
        time_mode: mt5.ORDER_TIME_GTC
        | mt5.ORDER_TIME_DAY
        | mt5.ORDER_TIME_SPECIFIED
        | mt5.ORDER_TIME_SPECIFIED_DAY = mt5.ORDER_TIME_GTC,
        filling_mode: mt5.ORDER_FILLING_FOK
        | mt5.ORDER_FILLING_IOC
        | mt5.ORDER_FILLING_RETURN
        | mt5.ORDER_FILLING_BOC = mt5.ORDER_FILLING_IOC,
    ) -> dict[str | Any]:
        trade_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": type_positions,
            "deviation": deviation_trade,
            "magic": 0,
            "reason": mt5.ORDER_REASON_CLIENT,
            "comment": "",
            "type_time": time_mode,
            "type_filling": filling_mode,
        }
        # If the order type is Buy, calculate the price, stop loss, and take profit
        if type_positions == mt5.ORDER_TYPE_BUY:
            price = price_ask
            sl = price - stop_loss * point
            tp = price + take_profit * point
        # If the order type is Sell, calculate the price, stop loss, and take profit
        elif type_positions == mt5.ORDER_TYPE_SELL:
            price = price_bid
            sl = price + stop_loss * point
            tp = price - take_profit * point
        # Update the trade request with the calculated price, stop loss, and take profit
        trade_request.update({"price": price, "sl": sl, "tp": tp})

        return trade_request
