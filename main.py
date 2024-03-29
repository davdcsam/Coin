# Standard Libraries
import os

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules
from utils.fonts import Fonts
from utils.logs import Logs
from utils.switch_view import SwitchView
from utils.themes import Themes

from model.trade.trade_model import TradeModel

from model.sign_model import SignModel
from viewmodel.sign_viewmodel import SignViewModel
from view.sign_view import SignView

from model.set_input_model import SetInputModel
from viewmodel.set_input_viewmodel import SetInputViewModel
from view.set_input_view import SetInputView

from viewmodel.watch_market_viewmodel import WatchMarketViewModel
from view.watch_market_view import WatchMarketView

from view.tabs_view import TabsView


class NH0:
    def __init__(self, name: str, ico: str) -> None:
        self.name = name
        self.ico = ico

    def created_envioment(self):
        dpg.create_context()

        dpg.create_viewport(
            title=self.name,
            large_icon=self.ico,
            small_icon=self.ico,
            width=700,
            height=900,
            max_width=700,
            min_width=700,
            clear_color=(40, 40, 40, 240),
            always_on_top=False,
        )

    def launch(self):
        loby_window: int | str = dpg.add_window(no_scrollbar=False)

        # · Utils · #
        fonts = Fonts()
        fonts.set_font_content()
        logs: Logs = Logs.getInstance()
        switch_view: SwitchView = SwitchView.getInstance()
        themes = Themes()
        themes.dark()

        # · Trade · #

        trade_model: TradeModel = TradeModel.getInstance()

        # · Sign · #

        sign_model = SignModel()
        sign_viewmodel = SignViewModel(sign_model, trade_model)
        sign_view = SignView(sign_viewmodel)

        # · SetInput · #

        set_input_model = SetInputModel()
        set_input_model_view = SetInputViewModel(set_input_model, trade_model)
        set_input_view = SetInputView(loby_window, set_input_model_view)

        # · WatchMarket · #

        watch_market_model_view = WatchMarketViewModel(trade_model)
        watch_market_view = WatchMarketView(loby_window, watch_market_model_view)

        # · Tabs · #

        tabs_view = TabsView(loby_window)

        # Set View #

        switch_view.set_page(
            "loby",
            to_hide=[sign_view.sign_in_window, sign_view.sign_out_window],
            to_show=[loby_window],
            to_set_primary=loby_window,
        )

        switch_view.set_page(
            "sign_in",
            to_hide=[loby_window, sign_view.sign_out_window],
            to_show=[sign_view.sign_in_window],
            to_unset_primary=sign_view.sign_in_window,
        )

        switch_view.set_page(
            "sign_out",
            to_hide=[loby_window, sign_view.sign_in_window],
            to_show=[sign_view.sign_out_window],
            to_unset_primary=loby_window,
        )

        switch_view.switch("sign_in")

        logs.notification(f"Hello, Welcome to {self.name}")

        def start_callback():
            sign_view.load_last_inputs()
            set_input_view.load_last_inputs()

        def exit_callback():
            sign_view.save_last_inputs()
            set_input_view.save_last_inputs()
            logs.save_csv()

        dpg.set_start_callback(start_callback)

        dpg.set_exit_callback(exit_callback)

        dpg.setup_dearpygui()

        dpg.show_viewport()

        dpg.start_dearpygui()

        dpg.destroy_context()


if __name__ == "__main__":
    instance_nh0 = NH0(
        name="Coin",
        ico=os.path.join(os.getcwd(), "assets", "logo", "coin_standard.ico"),
    )

    instance_nh0.created_envioment()

    instance_nh0.launch()
