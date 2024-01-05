# Standard Libraries

# Third Party Libraries
import dearpygui.dearpygui as dpg

# Owner Modules


class ColorTheme:
    def __init__(self) -> None:
        self.white: list[int] = [255, 255, 255, 255]
        # Text
        self.silver: list[int] = [151, 151, 151, 255]
        # TextDisabled
        self.dark_slate: list[int] = [40, 40, 40, 240]
        # WindowBg
        self.charcoal_gray: list[int] = [32, 32, 32, 255]
        # ChildBg, TitleBg
        self.transparent_black: list[int] = [0, 0, 0, 0]
        # Border, FrameBgHovered, FrameBgActive, ScrollbarBg
        self.pure_black: list[int] = [0, 0, 0, 255]
        # BorderShadow
        self.dark_slate: list[int] = [40, 40, 40, 255]
        # FrameBg, Button, Header, Tab
        self.soft_black: list[int] = [21, 21, 21, 240]
        # TitleBgActive
        self.dim_gray: list[int] = [21, 21, 21, 123]
        # ButtonHovered, HeaderHovered, TabHovered
        self.eclipse: list[int] = [37, 37, 37, 255]
        # TitleBgCollapsed, ResizeGrip
        self.outer_space: list[int] = [51, 51, 55, 255]
        # MenuBarBg, ResizeGripHovered, ResizeGripActive, TabUnfocused
        self.gray_chateau: list[int] = [107, 107, 114, 200]
        # ScrollbarGrab
        self.gray_suit: list[int] = [90, 90, 95, 100]
        # ScrollbarGrabHovered
        self.bright_gray_suit: list[int] = [90, 90, 95, 255]
        # ScrollbarGrabActive
        self.primary: list[int] = [250, 237, 0]
        # CheckMark, SliderGrab, SliderGrabActive, ButtonActive, TabActive
        self.eerie_black: list[int] = [20, 20, 20, 153]
        # HeaderActive
        self.dove_gray: list[int] = [78, 78, 78, 255]
        # Separator, SeparatorHovered, SeparatorActive


class Themes(ColorTheme):
    def __init__(self) -> None:
        self.global_dark_theme: int | str = dpg.add_theme()
        self.global_light_theme: int | str = dpg.add_theme()
        ColorTheme.__init__(self)

    def set_global_light_theme(self) -> None:
        self._set_global_style(self.global_light_theme)

        self._set_global_light_palette(self.global_light_theme)

        dpg.bind_theme(self.global_light_theme)

    def set_global_dark_theme(self) -> None:
        self._set_global_style(self.global_dark_theme)

        self._set_global_dark_palette(self.global_dark_theme)

        dpg.bind_theme(self.global_dark_theme)

    def set_dark_theme_window(self, window: int | str) -> None:
        local_theme: int | str = dpg.add_theme()

        self.dark_theme_window: int | str = dpg.add_theme_component(
            dpg.mvAll, parent=local_theme
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg,
            self.charcoal_gray,
            parent=self.dark_theme_window,
        )

        dpg.bind_item_theme(window, local_theme)

    def _set_global_style(self, theme_parent: int | str):
        self.component_style_all: int | str = dpg.add_theme_component(
            dpg.mvAll, parent=theme_parent
        )

        # Main
        dpg.add_theme_style(
            dpg.mvStyleVar_WindowPadding, 8, 8, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_FramePadding, 4, 3, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_CellPadding, 0, 0, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ItemSpacing, 0, 5, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ItemInnerSpacing, 4, 4, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_IndentSpacing, 21, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ScrollbarSize, 14, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_GrabMinSize, 2, parent=self.component_style_all
        )

        # Borders
        dpg.add_theme_style(
            dpg.mvStyleVar_WindowBorderSize, 1, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ChildBorderSize, 1, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_PopupBorderSize, 1, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_FrameBorderSize, 0, parent=self.component_style_all
        )

        # Rounding
        dpg.add_theme_style(
            dpg.mvStyleVar_WindowRounding, 12, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ChildRounding, 12, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_FrameRounding, 6, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_PopupRounding, 0, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ScrollbarRounding, 12, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_GrabRounding, 0, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_TabRounding, 4, parent=self.component_style_all
        )

        # Alignment
        dpg.add_theme_style(
            dpg.mvStyleVar_WindowTitleAlign, 0.50, 0.50, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_ButtonTextAlign, 0.50, 0.50, parent=self.component_style_all
        )

        dpg.add_theme_style(
            dpg.mvStyleVar_SelectableTextAlign, 0, 0, parent=self.component_style_all
        )

    def _set_global_dark_palette(self, theme_parent: int | str):
        self.component_dark_palette_all: int | str = dpg.add_theme_component(
            dpg.mvAll, parent=theme_parent
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Text,
            self.white,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TextDisabled,
            self.silver,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_WindowBg,
            (self.dark_slate),
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ChildBg,
            self.charcoal_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Border,
            self.transparent_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_BorderShadow,
            self.pure_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBg,
            self.dark_slate,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBgHovered,
            self.transparent_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_FrameBgActive,
            self.transparent_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBg,
            self.charcoal_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBgActive,
            self.soft_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TitleBgCollapsed,
            self.eclipse,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_MenuBarBg,
            self.outer_space,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ScrollbarBg,
            self.transparent_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ScrollbarGrab,
            self.gray_chateau,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ScrollbarGrabHovered,
            self.gray_suit,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ScrollbarGrabActive,
            self.bright_gray_suit,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_CheckMark,
            self.primary,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_SliderGrab,
            self.primary,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_SliderGrabActive,
            self.primary,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Button,
            self.dark_slate,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonHovered,
            self.dim_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ButtonActive,
            self.primary,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Header,
            self.dark_slate,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_HeaderHovered,
            self.dim_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_HeaderActive,
            self.eerie_black,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Separator,
            self.dove_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_SeparatorHovered,
            self.dove_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_SeparatorActive,
            self.dove_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ResizeGrip,
            self.eclipse,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ResizeGripHovered,
            self.outer_space,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_ResizeGripActive,
            self.outer_space,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_Tab,
            self.dark_slate,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TabHovered,
            self.dim_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TabActive,
            self.dim_gray,
            parent=self.component_dark_palette_all,
        )

        dpg.add_theme_color(
            dpg.mvThemeCol_TabUnfocused,
            self.outer_space,
            parent=self.component_dark_palette_all,
        )

    def _set_global_light_palette(self, them_parent: int | str):
        pass
