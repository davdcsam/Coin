# Standard

# Third Party
import pandas as pd

# Owner


class NoPositionModule:
    def __init__(self) -> None:
        # Initialize the module
        pass

    def Init(self, inputs: dict, positions_symbol: pd.DataFrame):
        # Verify if there are no positions for the given inputs and symbol positions
        return self._verify_no_positions(inputs, positions_symbol)

    def Any(self, inputs: dict, positions_symbol: pd.DataFrame):
        # Verify if there are no positions for the given inputs and symbol positions
        return self._verify_no_positions(inputs, positions_symbol)

    def _verify_no_positions(
        self, inputs: dict, positions_symbol: pd.DataFrame
    ) -> bool:
        # If there are no positions for the symbol, return True
        if positions_symbol.empty:
            return True

        # Filter the positions where magic number is 0
        positions_symbol_magic = positions_symbol[positions_symbol["magic"] == 0]

        # If there are no positions with magic number 0, return True. Otherwise, return False
        if positions_symbol_magic.empty:
            return True
        else:
            return False
