# Standard Libraries
from typing import Self
import os

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules


class Fonts:
    """
    Singleton class for managing fonts.

    Attributes:
        _instance (Fonts): The singleton instance of the class.
        fonts (dict): Dictionary to store the created fonts.
    """

    _instance = None

    def __new__(cls):
        """
        Creates a new instance if it does not exist,
        otherwise returns the existing instance.
        """
        if cls._instance is None:
            cls._instance: Self = super(Fonts, cls).__new__(cls)
            cls._instance.fonts = {}  # Initialize the fonts dictionary
        return cls._instance

    def add_fonts(
        self,
        fonts: dict = {
            "opensans_regular_content": {
                "file": "{}".format(
                    os.path.join(
                        os.getcwd(),
                        "assets",
                        "OpenSans",
                        "static",
                        "OpenSans-Regular.ttf",
                    )
                ),
                "size": 20,
            },
            "opensans_semibold_subtitle": {
                "file": "{}".format(
                    os.path.join(
                        os.getcwd(),
                        "assets",
                        "OpenSans",
                        "static",
                        "OpenSans-SemiBold.ttf",
                    )
                ),
                "size": 24,
            },
            "opensans_semibold_title": {
                "file": "{}".format(
                    os.path.join(
                        os.getcwd(),
                        "assets",
                        "OpenSans",
                        "static",
                        "OpenSans-SemiBold.ttf",
                    )
                ),
                "size": 40,
            },
            "opensans_semibold_title_60": {
                "file": "{}".format(
                    os.path.join(
                        os.getcwd(),
                        "assets",
                        "OpenSans",
                        "static",
                        "OpenSans-SemiBold.ttf",
                    )
                ),
                "size": 60,
            },
        },
    ) -> None:
        """
        Creates the fonts and stores them in the fonts dictionary.
        """
        self.main_font_register: int | str = dpg.add_font_registry()

        for font, value in fonts.items():
            self.fonts[font] = dpg.add_font(
                value["file"], value["size"], parent=self.main_font_register
            )

    def set_font_content(self, font_name: str = None) -> None:
        """
        Sets the default font for the application.
        """
        self.add_fonts()
        if font_name is None:
            font_name = self.fonts["opensans_regular_content"]
        else:
            font_name = self.fonts[font_name]
        dpg.bind_font(font_name)

    def set_font_item(self, object_instance, font_name: str = None) -> None:
        """
        Sets the font for a specific item.
        """
        if font_name is None:
            font_name = self.fonts["opensans_semibold_title"]
        else:
            font_name = self.fonts[font_name]
        dpg.bind_item_font(object_instance, font_name)

    def set_font_items(self, object_instances: list, font_name: str = None) -> None:
        """
        Sets the font for multiple items.
        """
        if font_name is None:
            font_name = self.fonts["opensans_semibold_subtitle"]
        else:
            font_name = self.fonts[font_name]
        for object_instance in object_instances:
            dpg.bind_item_font(object_instance, font_name)
