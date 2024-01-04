# Standard Libraries
import os
from tkinter import filedialog
from typing import Any, Literal

# Third Party Libraries
import dearpygui.dearpygui as dpg


# Owner Modules
from model.trade.trade_model import TradeModel

from utils.manager_files import ManagerFiles
from utils.logs import Logs


class SignModel:
    def __init__(self) -> None:
        self.instance_trade: TradeModel = TradeModel.getInstance()
        self.instance_manager_files = ManagerFiles()
        self.instance_logs: Logs = Logs.getInstance()

        self.initialdir: str = "C:/Program Files"
        self.file_name = "terminal64.exe"
        self.last_input_filename: str = os.path.join(
            os.getcwd(), "data", "terminals", "last_input.json"
        )

        self.full_fields_input_custom_terminal: list[str] = [
            os.path.join(self.initialdir, name, self.file_name)
            for name in os.listdir(self.initialdir)
            if os.path.isdir(os.path.join(self.initialdir, name))
            and os.path.isfile(os.path.join(self.initialdir, name, self.file_name))
        ]

        if not os.path.exists(os.path.dirname(self.last_input_filename)):
            os.makedirs(os.path.dirname(self.last_input_filename))

    def get_fill_input_custom_terminal(self) -> list[str]:
        return [
            os.path.basename(os.path.dirname(full_field))
            for full_field in self.full_fields_input_custom_terminal
        ]

    def custom_terminal(self) -> str | Literal[False]:
        terminal_path: str = filedialog.askdirectory(
            title="Select your custom terminal",
            initialdir="C:/Program Files",
        )

        terminal_name: str = os.path.basename(terminal_path)

        terminal_file: str = terminal_path + "/terminal64.exe"

        if not terminal_path:
            return False
        elif not os.path.isfile(terminal_file):
            return False
        else:
            return terminal_name

    def open_connection(self, inputs: dict) -> bool:
        if isinstance(self.check_empty_fiel(inputs), dict):
            self.instance_logs.notification("There are a Login Fields Empty", "e")
            return False

        inputs["input_path"].update(
            {
                "value": os.path.join(
                    self.initialdir,
                    inputs["input_path"]["value"],
                    self.file_name,
                )
            }
        )

        if not os.path.isfile(inputs["input_path"]["value"]):
            self.instance_logs.notification(
                "Terminal no found in {}.".format(
                    os.path.dirname(inputs["input_path"]["value"])
                ),
                "e",
            )
            return False

        if not self.instance_trade.start(inputs):
            return False
        return True

    def check_empty_fiel(self, inputs: dict) -> dict | Literal[True]:
        empty_inputs: dict = {
            k: v for k, v in inputs.items() if not dpg.get_value(v["id"])
        }

        if empty_inputs:
            return empty_inputs

        return True

    def close_connection(self):
        self.instance_trade.stop()

    def load_inputs_file(self) -> dict[str, Any] | Literal[False]:
        return self.instance_manager_files.load(
            os.path.join(os.getcwd(), "data", "terminals")
        )

    def load_inputs_last_file(self) -> dict[str, Any] | Literal[False]:
        return self.instance_manager_files.load_last_file(self.last_input_filename)

    def save_inputs_file(self, inputs: dict, name: str) -> bool:
        return self.instance_manager_files.save(
            inputs, name, os.path.join(os.getcwd(), "data", "terminals")
        )

    def save_inputs_last_file(self, inputs: dict) -> bool:
        return self.instance_manager_files.save_last_file(
            inputs, self.last_input_filename
        )
