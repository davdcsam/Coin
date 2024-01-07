# Standard Libraries
import os
import threading
import time
from datetime import datetime
from typing import Any, Self

# Third Party Libraries
import pandas as pd
import dearpygui.dearpygui as dpg

# Owner
from utils.themes import Themes


class Logs:
    _instance = None
    _container = "BottomTabs.logs"

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance: Self = cls()
        return cls._instance

    def __init__(self) -> None:
        if self._instance is not None:
            raise Exception(
                """
                This is a Singleton Class. Use 'getInstance()'
                to get the single instance.
                """
            )
        else:
            # Initializing a DataFrame with columns for datetime, type, and message
            self.df = pd.DataFrame(columns=["datetime", "type", "message"])
            # Defining a dictionary to map format types to their respective string representations
            self.format_type: dict[str, str] = {
                "w": "[WARNING]",
                "e": "[ERROR]",
                "t": "[TRADE]",
                "n": "[NOTE]",
                "s": "[SYSTEM]",
            }
            # Constructing the file path for the output CSV file
            self.csv_file_path: str = os.getcwd() + "\\data\\logs\\logs-{}.csv".format(
                datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            )
            self.instance_themes = Themes()

            if not os.path.isdir(os.path.dirname(self.csv_file_path)):
                dirname_log = os.path.dirname(self.csv_file_path)
                if not os.path.isdir(os.path.dirname(dirname_log)):
                    os.mkdir(os.path.dirname(dirname_log))
                os.mkdir(dirname_log)

    def set_container(cls, container: int | str):
        cls._container: int | str = container

    # Defining a method to log a message with a specific format type
    def log(self, message: str, f_type: str = "s"):
        """
        Logs a message with a specific format type.

        Args:
            f_type (str): The format type of the message.
                'w': [WARNING]
                'e': [ERROR]
                't': [TRADE]
                'n': [NOTE]
                's': [SYSTEM]
            message (str): The message to log.
        """
        # Creating a new row with the current datetime, format type, and message
        new_row: dict[str, str] = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.format_type[f_type],
            "message": message,
        }

        # Adding the new row to the DataFrame
        insert_loc: Any = self.df.index.max()

        if pd.isna(insert_loc):
            self.df.loc[0] = new_row
        else:
            self.df.loc[insert_loc + 1] = new_row

        # Adding a new text widget for each message
        dpg.add_text(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {self.format_type[f_type]} {message}",
            parent=self._container,
            wrap=dpg.get_item_width(self._container),
        )

        # Print the message
        print(f"{self.format_type[f_type]} {message}")

    def save_csv_when_stop(self):
        # Saving the DataFrame to a CSV file
        self.df.to_csv(self.csv_file_path, mode="w")

    def notification(self, message: str, f_type: str = "s"):
        """
        Logs a message with a specific format type.

        Args:
            f_type (str): The format type of the message.
                'w': [WARNING]
                'e': [ERROR]
                't': [TRADE]
                'n': [NOTE]
                's': [SYSTEM]
            message (str): The message to log.
        """
        notification: int | str = dpg.add_window(
            width=300,
            height=100,
            no_move=False,
            no_title_bar=True,
            no_close=True,
            no_open_over_existing_popup=True,
        )

        dpg.add_text(
            default_value=message,
            parent=notification,
            wrap=dpg.get_item_width(notification) - 30,
            pos=(15, 15),
        )

        self.instance_themes.dark_window(notification)

        dpg.set_item_pos(
            notification,
            pos=(
                (dpg.get_viewport_width() - dpg.get_item_width(notification)) / 2,
                dpg.get_viewport_height() * 0.8,
            ),
        )

        self.log(message, f_type)

        threading.Thread(target=self.close_notification, args=(notification,)).start()

    def close_notification(self, notification):
        time.sleep(5)
        dpg.delete_item(notification)


def verify_singleton():
    temp: Logs = Logs.getInstance()

    temp1: Logs = Logs.getInstance()

    if temp is temp1:
        print(True)
    else:
        print(False)
