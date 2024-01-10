# Standard

# Third Party
import pandas as pd

# Owner


class NoPositionModule:
    def __init__(self) -> None:
        pass

    def Init(self, inputs: dict, positions_symbol: pd.DataFrame):
        return self._verify_no_positions(inputs, positions_symbol)

    def Any(self, inputs: dict, positions_symbol: pd.DataFrame):
        return self._verify_no_positions(inputs, positions_symbol)

    def _verify_no_positions(
        self, inputs: dict, positions_symbol: pd.DataFrame
    ) -> bool:
        if positions_symbol.empty:
            return True

        positions_symbol_magic = positions_symbol[
            positions_symbol["magic"] == 0
        ]

        if positions_symbol_magic.empty:
            return True
        else:
            return False
