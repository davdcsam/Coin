# Standard Libraries
import json
import os
from tkinter import filedialog
from typing import Any, Literal

# Third Party Libraries

# Owner Modules
from utils.formater import Formater


class LoadFiles:
    def __init__(self) -> None:
        self.filedailog_filetypes: tuple[
            tuple[Literal["Set Files"], Literal["*.json"]],
            tuple[Literal["All files"], Literal["*.*"]],
        ] = (
            ("Set Files", "*.json"),
            ("All files", "*.*"),
        )  # File types for the file dialog

    def load(
        self, initialdir: str = os.path.join(os.getcwd(), "data", "inputs")
    ) -> dict[str] | Literal[False]:
        try:
            # Open a file dialog for the user to select a file to load from
            filename: str = filedialog.askopenfilename(
                title="Open",
                initialdir=initialdir,
                filetypes=self.filedailog_filetypes,
                defaultextension=".json",
            )
            if not filename:
                return False

            # Read the inputs from the selected file
            with open(filename, "r") as f:
                inputs: dict = json.load(f)

            return inputs

        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while writing to the file: {e}")

    def load_last_file(self, filename: str) -> dict[str] | Literal[False]:
        try:
            if not filename or not os.path.isfile(filename):
                return False

            # Read the inputs from the selected file
            with open(filename, "r") as f:
                inputs: dict = json.load(f)

            return inputs

        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while writing to the file: {e}")


class SaveFiles:
    # The constructor takes a trade_instance as a parameter
    def __init__(self) -> None:
        self.filedailog_filetypes: tuple[
            tuple[Literal["Set Files"], Literal["*.json"]],
            tuple[Literal["All files"], Literal["*.*"]],
        ] = (
            ("Set Files", "*.json"),
            ("All files", "*.*"),
        )  # File types for the file dialog

    def save(
        self,
        inputs: dict,
        name: str = os.path.basename(os.getcwd()),
        initialdir: str = os.path.join(os.getcwd(), "data", "inputs"),
    ) -> bool:
        """
        Saves input field values to a file selected by the user.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            # Open a file dialog for the user to select a file to save to
            filename = filedialog.asksaveasfilename(
                title="Save as",
                initialdir=initialdir,
                initialfile=name,
                filetypes=self.filedailog_filetypes,
                defaultextension=".json",
            )
            if not filename:
                return False

            # Created the inputs from the selected file
            with open(filename, "w") as f:
                json.dump(self.get_data_formated(inputs), f, indent=4)

            return True

        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        except Exception as e:
            # Print an error message if any other error occurred
            print(f"An error occurred while writing to the file: {e}")

    def save_last_file(
        self,
        inputs: dict,
        filename,
    ) -> bool:
        """
        Saves input field values to a file selected by the user.

        Args:
            sender: The widget that triggered the callback.
            app_data: Additional data from the widget.
        """
        try:
            if not filename:
                return False

            # Created the inputs from the selected file
            with open(filename, "w") as f:
                json.dump(self.get_data_formated(inputs), f, indent=4)

            return True

        except FileNotFoundError:
            # Print an error message if the file was not found
            print("The file was not found.")
        except PermissionError:
            # Print an error message if the user does not have permission to write to the file
            print("You do not have permission to write to the file.")
        # except Exception as e:
        #     # Print an error message if any other error occurred
        #     print(f"An error occurred while writing to the file: {e}")

    @staticmethod
    def get_data_formated(inputs: dict) -> dict[str, Any]:
        return {
            k: Formater.set_format_float(
                v["value"], Formater.get_format_from_incorrect_format(v["format"])
            )
            if "format" in v
            else v["value"]
            for k, v in inputs.items()
        }


class ManagerFiles(LoadFiles, SaveFiles):
    def __init__(self) -> None:
        LoadFiles.__init__(self)
        SaveFiles.__init__(self)
