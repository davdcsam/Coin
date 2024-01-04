# Standard Libraries
from typing import Self

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Onwer Modules


class InfoWidgets:
    def __init__(self) -> None:
        self.view = None

    def get_all_atr(self, obj=None) -> dict:
        if obj is None:
            obj: Self = self
        return {
            attr_name: attr_value
            for attr_name, attr_value in vars(obj).items()
            if not attr_name.startswith("_")
            and (isinstance(attr_value, int) or isinstance(attr_name, str))
        }

    def get_inputs(self, obj=None) -> dict:
        inputs: dict = {}
        for k, v in self.get_all_atr(obj).items():
            if k.startswith("input"):
                temp_value: dict = dpg.get_item_configuration(v)
                temp_value.update(dpg.get_item_info(v))
                temp_value.update({"id": v, "value": dpg.get_value(v)})
                inputs[k] = temp_value
        return inputs
