# Standard Libraries
from typing import Self

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Onwer Modules


class InfoWidgets:
    def __init__(self) -> None:
        """Initialize an InfoWidgets object with a view attribute."""
        self.view = None

    def get_all_atr(self, obj=None) -> dict:
        """Return a dictionary of all the attributes and values of an object.

        Args:
            obj: The object to get the attributes from. If None, use self.

        Returns:
            A dictionary with the attribute names as keys and the attribute values as values.
            Only include attributes that do not start with an underscore and are either integers or strings.
        """
        if obj is None:
            obj: Self = self
        return {
            attr_name: attr_value
            for attr_name, attr_value in vars(obj).items()
            if not attr_name.startswith("_")
            and (isinstance(attr_value, int) or isinstance(attr_name, str))
        }

    def get_inputs(self, obj=None) -> dict:
        """Return a dictionary of all the input widgets and their configurations of an object.

        Args:
            obj: The object to get the input widgets from. If None, use self.

        Returns:
            A dictionary with the input widget names as keys and the input widget configurations as values.
            Only include input widgets that start with "input".
            The configuration is a dictionary that contains the id, value, and other information of the input widget.
        """
        inputs: dict = {}
        for k, v in self.get_all_atr(obj).items():
            if k.startswith("input"):
                temp_value: dict = dpg.get_item_configuration(v)
                temp_value.update(dpg.get_item_info(v))
                temp_value.update({"id": v, "value": dpg.get_value(v)})
                inputs[k] = temp_value
        return inputs
