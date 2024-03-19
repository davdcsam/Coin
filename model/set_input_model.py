# Standard Libraries
import os
from typing import Any, Literal

# Third Party Libraries

# Owner Modules
from utils.logs import Logs
from utils.manager_files import ManagerFiles
from model.trade.trade_model import TradeModel


class SetInputModel:
    def __init__(self) -> None:
        # Initialize the TradeModel instance, logs, and manager files
        self.instance_trade: TradeModel = TradeModel.getInstance()
        self.instance_logs: Logs = Logs.getInstance()
        self.instance_manager_files = ManagerFiles()

        # Define the path for the last input file
        self.last_input_filename: str = os.path.join(
            os.getcwd(), "data", "inputs", "last_input.json"
        )

        # Create the directory for the last input file if it does not exist
        if not os.path.exists(os.path.dirname(self.last_input_filename)):
            os.makedirs(os.path.dirname(self.last_input_filename))

    def load_inputs_file(self) -> dict[str, Any] | Literal[False]:
        # Load the inputs file
        return self.instance_manager_files.load(
            os.path.join(os.getcwd(), "data", "inputs")
        )

    def load_inputs_last_file(self) -> dict[str, Any] | Literal[False]:
        # Load the last inputs file
        return self.instance_manager_files.load_last_file(self.last_input_filename)

    def save_inputs_file(self, inputs: dict, name: str) -> bool:
        # Save the inputs file
        return self.instance_manager_files.save(
            inputs, name, os.path.join(os.getcwd(), "data", "inputs")
        )

    def save_inputs_last_file(self, inputs: dict) -> bool:
        # Save the last inputs file
        return self.instance_manager_files.save_last_file(
            inputs, self.last_input_filename
        )

    def change_bot_state(self, status: bool, inputs: dict) -> None:
        # Change the bot state based on the status
        if status and not self.instance_trade.bot_status:
            self.instance_trade.formated_inputs = (
                self.instance_manager_files.get_data_formated(inputs)
            )

            self.instance_trade.init_flag = True
            self.instance_trade.bot_status = True

            self.instance_logs.log("Bot was Deployed", "t")
            self.instance_logs.log(f"Deplay Time at {self.instance_trade.delay_time}")

        elif not status and self.instance_trade.bot_status:
            self.instance_trade.bot_status = False
            self.instance_trade.deinit_flag = True

            self.instance_logs.log("Bot was Undeployed", "t")

    def checker(self, inputs: dict) -> Literal[True] | None:
        # Check the inputs
        if self.instance_trade.checker(inputs):
            return True

    def change_delay_time(self, deplay_time: float) -> None:
        # Change the delay time
        self.instance_trade.delay_time = deplay_time
