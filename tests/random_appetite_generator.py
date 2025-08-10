import numpy as np
from auction_appetite import AuctionAppetite
from typing import Any

class RandomAppetiteGenerator:
    """Generates random appetites for a symbol."""
    def __init__(self, symbol: str, price_start: float, price_end: float, price_steps: int, base_appetite: int, appetite_step: int):
        self.symbol = symbol
        self.price_start = price_start
        self.price_end = price_end
        self.price_steps = price_steps
        self.base_appetite = base_appetite
        self.appetite_step = appetite_step

    def generate_appetite(self) -> Any:
        appetite = AuctionAppetite(self.symbol)
        prices = np.linspace(self.price_start, self.price_end, self.price_steps)
        # Quadratic monotonic curves
        # Buy appetite: highest at lowest price, decreases quadratically
        for i, price in enumerate(prices):
            t = i / (self.price_steps - 1) if self.price_steps > 1 else 0
            qty = max(1, int(round(self.base_appetite * (1 - t**2))))
            appetite.set_appetite(round(price, 2), qty, 'buy')
        # Sell appetite: lowest at lowest price, increases quadratically
        for i, price in enumerate(prices):
            t = i / (self.price_steps - 1) if self.price_steps > 1 else 0
            qty = max(1, int(round(self.base_appetite * (t**2))))
            appetite.set_appetite(round(price, 2), qty, 'sell')
        return appetite
