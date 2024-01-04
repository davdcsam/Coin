#  Standard Libraries
import re
import datetime


class Formater:
    @staticmethod
    def get_format_num(num: int | str) -> str:
        """
        Gets the format of a given number.

        This function takes a number (as an integer or string) and returns a string representing the format of that number.
        If the number has decimal places, the format returned will have the same number of decimal places.
        If the number has no decimal places, the format returned will be '%.0f'.

        Parameters:
        num (int | str): The number for which the format will be obtained.

        Returns:
        str: A string representing the format of the number.

        Example:
        >>> get_format_num(123,456)
        '%.3f'
        >>> get_format_num(123)
        '%.0f'
        """
        parts: list[str] = str(num).split(".")
        if len(parts) > 1:
            return "%." + str(len(parts[1])) + "f"
        else:
            return "%.0f"

    @staticmethod
    def set_format_float(float_num: float, format_str: str) -> float:
        """
        Formats a number according to the provided format.

        Parameters:
        float_numnum (float): the number to be formatted.
        format_str (str): A format string specifying how the number is to be formatted.

        Returns:
        flat: The number formatted.

        Example:
        >>> set_format_float(4.130000591278076, "%.3f")
        4.130
        """
        return float(format_str % float_num)

    @staticmethod
    def get_format_from_incorrect_format(format_str: str) -> str:
        """
        Gets a valid format from an incorrect format string.

        Parameters:
        format_str (str): an incorrect format string.

        Returns:
        str: The valid format found in the incorrect format string.

        Example:
        >>> get_format_from_incorrect_format("%d USD").
        '%d'
        """
        new_format: re.Match[str] | None = re.search(r"%.\w*", format_str)
        if new_format:
            return new_format.group()

    @staticmethod
    def change_decimals_from_format_num(format_str: str, decimals: int) -> str:
        """
        Changes the number of decimal places in a format string.

        Parameters:
        string (str): The format string to be changed.
        decimals (int): The new number of decimal places.

        Returns:
        str: The format string with the new number of decimal places.

        Example:
        >>> change_decimals_from_format_num("%.2f USD", 3)
        "%.3f USD"
        """
        parts = format_str.split(".")
        format_changed = parts[0] + "." + str(decimals) + parts[1][1:]
        return format_changed

    @staticmethod
    def time_dpg_to_datetime(input_time: dict) -> datetime.datetime:
        """
        Converts a time in DPG format to datetime time.

        Parameters:
        input_time (dict): a dictionary containing time information in DPG format. The dictionary keys are "year", "month", "month_day", "hour", "min", "sec".

        Returns:
        int: The time in datetime format.

        Example:
        >>> time_dpg_to_datetime({"year": 123, "month": 11, "month_day": 30, "hour": 15, "min": 30, "sec": 45})
        4120753945
        """
        dt = datetime.datetime(
            input_time["year"] + 1900,
            input_time["month"] + 1,
            input_time["month_day"],
            input_time["hour"],
            input_time["min"],
            input_time["sec"],
        )
        return dt
