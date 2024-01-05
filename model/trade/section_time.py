# Standard
from datetime import datetime
import time

# Third Party

# Owner
from utils.formater import Formater
from utils.logs import Logs


class SectionTimeModule:
    """
    This class represents a time section in the market.
    It has methods to initialize the section,
    check if a given time is within a time range.
    """

    def __init__(self) -> None:
        """
        Initializes the SectionTime object with default values.
        """
        self.instance_logs: Logs = Logs.getInstance()
        self.state = False
        self.time_start = None
        self.time_end = None

    @staticmethod
    def verify_existence_from_input(inputs: dict) -> tuple[datetime, datetime]:
        """
        This static method verifies the existence of
        'input_time_start' and 'input_time_end'
        keys in the input dictionary.

        It then converts the values of these keys from
        Dear PyGui time format to Python datetime objects.

        Args:
            inputs (dict): A dictionary that should contain the keys 'input_time_start' and 'input_time_end'.
                           The values corresponding to these keys should be in Dear PyGui time format.

        Returns:
            tuple[datetime, datetime]: A tuple containing two datetime objects corresponding to 'input_time_start' and 'input_time_end'.

        Raises:
            Exception: If either 'input_time_start' or 'input_time_end' do not exist in the input dictionary, an exception is raised.
        """
        if all(key in inputs for key in ["input_time_start", "input_time_end"]):
            time_start: datetime = Formater.time_dpg_to_datetime(
                inputs["input_time_start"]
            )
            time_end: datetime = Formater.time_dpg_to_datetime(inputs["input_time_end"])
            return time_start, time_end
        else:
            raise (
                """
                Keys 'input_time_start' and 'input_time_end' in arg inputs.
                """
            )

    def Init(self, inputs: dict):
        """
        Initializes the start and end times of the section from the input dictionary.
        If the end time is earlier than the start time, they are swapped.
        """
        # Extracting the start and end times from the input dictionary
        self.time_start, self.time_end = self.verify_existence_from_input(inputs)

        # Swapping the start and end times if the end time is earlier
        if self.time_start > self.time_end:
            time_temp: datetime = self.time_start
            self.time_start: datetime = self.time_end
            self.time_end: datetime = time_temp

    def Any(self, time_broker: datetime) -> None:
        """
        Checks if the given time falls within the start and end times of the section.
        Updates the section_time_state accordingly.
        """
        # Checking if the given time is after the start time
        if time_broker > self.time_start and time_broker < self.time_end:
            self.state = True
            print(self.state, self.time_start, time_broker, self.time_end)
        else:
            self.state = False
            print(self.state, self.time_start, time_broker, self.time_end)
