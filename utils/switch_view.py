# Standard Libraries
from typing import Self

# Third Party Libraries
import dearpygui.dearpygui as dpg
from traitlets import HasTraits, observe, Any

# Onwer Modules
from utils.logs import Logs


class SwitchView(HasTraits):
    _instance = None
    current_view = Any()

    class AutoDict(dict):
        """
        Dictionary subclass that returns a default value for missing keys.
        """

        def __missing__(self, key):
            return self.setdefault(key, None)

        def __getstate__(self):
            return self.__dict__

        def __setstate__(self, state):
            self.__dict__.update(state)

    @staticmethod
    def getInstance():
        if SwitchView._instance is None:
            SwitchView()
        return SwitchView._instance

    def __init__(self):
        if SwitchView._instance is not None:
            raise Exception(
                """
                This is a Singleton Class. Use 'getInstance()'
                to get the single instance.
                """
            )
        else:
            SwitchView._instance: Self = self
            self.instance_logs: Logs = Logs.getInstance()

    def set_page(
        self,
        name,
        to_hide: tuple[int | str] | list[int | str],
        to_show: tuple[int | str] | list[int | str],
        to_unset_primary: int | str = None,
        to_set_primary: int | str = None,
    ):
        self.__dict__[name] = self.AutoDict(
            {
                "to_hide": to_hide,
                "to_show": to_show,
                "to_unset_primary": to_unset_primary,
                "to_set_primary": to_set_primary,
            }
        )

    def switch(self, name: str):
        if not hasattr(self, name):
            raise Exception(
                f"""
                The argument '{name}' you have provided does not exist.
                Use 'get_pages()' to watch pages created.
                """
            )

        if self.current_view == name:
            print(f"You are already watching '{name}'")
            return

        for hide in self.__dict__[name]["to_hide"]:
            if dpg.does_item_exist(hide):
                dpg.hide_item(hide)

        for show in self.__dict__[name]["to_show"]:
            if dpg.does_item_exist(show):
                dpg.show_item(show)

        if dpg.does_item_exist(self.__dict__[name]["to_unset_primary"]):
            dpg.set_primary_window(self.__dict__[name]["to_unset_primary"], False)

        if dpg.does_item_exist(self.__dict__[name]["to_set_primary"]):
            dpg.set_primary_window(self.__dict__[name]["to_set_primary"], True)

        self.current_view = name

        self.instance_logs.log(f"Switched to {self.current_view}")

    def get_pages(self):
        pages: dict = {}
        for attr_name, attr_value in vars(self).items():
            if attr_name.startswith("_"):
                continue
            if isinstance(attr_value, dict):
                pages[attr_name] = attr_value
        return pages


def verify_singleton():
    instance1: SwitchView = SwitchView.getInstance()

    instance2: SwitchView = SwitchView.getInstance()

    if instance1 is instance2:
        print(True)
    else:
        print(False)

    instance1.set_page("TestPage", [1], [1], 1, 1)

    instance2.set_page("TestPage", [2], [1], 2, 1)

    print(instance1.TestPage)

    print(instance2.TestPage)
