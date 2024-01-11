# Standard Libraries
import json
import os
from tkinter import filedialog
from typing import Any, Literal

# Third Party Libraries

# Owner Modules
from utils.formater import Formater
from utils.logs import Logs


class LoadFiles:
    """
    A class to load inputs from JSON files using a file dialog.
    """

    def __init__(self) -> None:
        """
        Initialize a LoadFiles object with an instance of Logs and a filetypes tuple.
        """
        self.instance_logs: Logs = Logs.getInstance()

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
        """
        Load inputs from a JSON file selected by the user using a file dialog.

        Args:
            initialdir: The initial directory to open the file dialog. Default is the data/inputs folder.

        Returns:
            A dictionary of inputs from the JSON file, or False if the user cancels the file dialog or the file is invalid.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the user does not have permission to read the file.
            Exception: If any other error occurs while reading the file.
        """
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
            self.instance_logs("The file was not found.", "e")
        except PermissionError:
            self.instance_logs("You do not have permission to write to the file.", "e")
        except Exception as e:
            self.instance_logs(f"An error occurred while writing to the file: {e}", "e")

    def load_last_file(self, filename: str) -> dict[str] | Literal[False]:
        """
        Load inputs from a JSON file specified by the filename.

        Args:
            filename: The name of the JSON file to load from.

        Returns:
            A dictionary of inputs from the JSON file, or False if the filename is empty or the file is invalid.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the user does not have permission to read the file.
            Exception: If any other error occurs while reading the file.
        """
        try:
            if not filename or not os.path.isfile(filename):
                return False

            # Read the inputs from the selected file
            with open(filename, "r") as f:
                inputs: dict = json.load(f)

            return inputs

        except FileNotFoundError:
            self.instance_logs("The file was not found.", "e")
        except PermissionError:
            self.instance_logs("You do not have permission to write to the file.", "e")
        except Exception as e:
            self.instance_logs(f"An error occurred while writing to the file: {e}", "e")


class SaveFiles:
    """
    This class is responsible for saving files in a specified format.

    Attributes:
        instance_logs (Logs): An instance of the Logs class.
        filedialog_filetypes (tuple): A tuple specifying the file types for the file dialog.
    """
    def __init__(self) -> None:
        """
        Initialize a SaveFiles object with an instance of Logs and a filetypes tuple.
        """
        self.instance_logs: Logs = Logs.getInstance()

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
        Saves the given inputs to a file.

        Args:
            inputs (dict): The inputs to be saved.
            name (str): The name of the file.
            initialdir (str): The initial directory where the file will be saved.

        Returns:
            bool: True if the file was saved successfully, False otherwise.
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
            self.instance_logs("The file was not found.", "e")
        except PermissionError:
            self.instance_logs("You do not have permission to write to the file.", "e")
        except Exception as e:
            self.instance_logs(f"An error occurred while writing to the file: {e}", "e")

    def save_last_file(
        self,
        inputs: dict,
        filename,
    ) -> bool:
        """
        Saves the given inputs to the last file.

        Args:
            inputs (dict): The inputs to be saved.
            filename (str): The name of the file.

        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        try:
            if not filename:
                return False

            # Created the inputs from the selected file
            with open(filename, "w") as f:
                json.dump(self.get_data_formated(inputs), f, indent=4)

            return True

        except FileNotFoundError:
            self.instance_logs("The file was not found.", "e")
        except PermissionError:
            self.instance_logs("You do not have permission to write to the file.", "e")
        except Exception as e:
            self.instance_logs(f"An error occurred while writing to the file: {e}", "e")

    @staticmethod
    def get_data_formated(inputs: dict) -> dict[str, Any]:
        """
        Formats the given inputs.

        Args:
            inputs (dict): The inputs to be formatted.

        Returns:
            dict[str, Any]: The formatted inputs.
        """
        return {
            k: Formater.set_format_float(
                v["value"], Formater.get_format_from_incorrect_format(v["format"])
            )
            if "format" in v
            else v["value"]
            for k, v in inputs.items()
        }


class ManagerFiles(LoadFiles, SaveFiles):
    """
    This class manages the loading and saving of files.

    It inherits from the LoadFiles and SaveFiles classes.
    """
    def __init__(self) -> None:
        LoadFiles.__init__(self)
        SaveFiles.__init__(self)
