# Standard Libraries
from datetime import datetime

# Third Party Libraries

# Owner Modules
from connection.connection import Connection


class TradeModel(Connection):
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
