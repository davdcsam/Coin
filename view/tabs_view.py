# Standard Libraries

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules


class TabsView:
    def __init__(self, parent_object) -> None:
        self.child_window: int | str = dpg.add_child_window(
            parent=parent_object,
        )

        self.tab_bar: int | str = dpg.add_tab_bar(parent=self.child_window)

        self.logs: int | str = dpg.add_tab(
            tag="BottomTabs.logs", label="Logs", parent=self.tab_bar
        )
