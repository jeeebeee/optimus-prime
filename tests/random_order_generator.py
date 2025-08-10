import numpy as np
from order import Order
from typing import List

class RandomOrderGenerator:
    """Generates random orders for a symbol."""
    def __init__(self, symbol: str, qty_mean: float, qty_std: float, price_mean: float, price_std: float):
        self.symbol = symbol
        self.qty_mean = qty_mean
        self.qty_std = qty_std
        self.price_mean = price_mean
        self.price_std = price_std
        self._order_id_counter = 0

    def generate_order(self, side: str) -> Order:
        qty = max(1, int(np.random.normal(self.qty_mean, self.qty_std)))
        price = round(np.random.normal(self.price_mean, self.price_std), 2)
        order_id = f"{self.symbol}-{side}-{self._order_id_counter}"
        self._order_id_counter += 1
        order = Order(qty, price, self.symbol, side)
        order.id = order_id  # Attach id attribute to the order
        order.pid = -1       # Set pid to -1
        return order

    def generate_orders(self, n: int, side: str) -> List[Order]:
        return [self.generate_order(side) for _ in range(n)]
