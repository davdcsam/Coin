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

    def Init(self, inputs: dict) -> bool:
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

        print(self.time_start)
        print(self.time_end)
        return True

    def Any(self, time_broker: datetime) -> None:
        """
        Checks if the given time falls within the start and end times of the section.
        Updates the section_time_state accordingly.
        """
        print(time_broker)
        # # Checking if the given time is after the start time
        # if time_broker > self.time_start and time_broker < self.time_end:
        #     self.state = True
        # else:
        #     self.state = False
