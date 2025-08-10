import numpy as np
from typing import List

class Symbol:
    """Represents a market symbol with price parameters."""
    def __init__(self, symbol: str, refprx: float, matchprx: float, mean: float, stdev: float):
        self.symbol = symbol
        self.refprx = refprx
        self.matchprx = matchprx
        self.mean = mean
        self.stdev = stdev

    def set_matchprx(self, matchprx: float) -> None:
        self.matchprx = matchprx

    def generate_random_prices(self, n: int) -> List[float]:
        prices = np.random.lognormal(self.mean, self.stdev, n)
        return [round(price, 2) for price in prices]

    def __repr__(self) -> str:
        return (f"Symbol(symbol='{self.symbol}', refprx={self.refprx}, mean={self.mean}, "
                f"stdev={self.stdev}, matchprx={self.matchprx})")
