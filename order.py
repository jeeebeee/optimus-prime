class Order:
    """Represents a market order."""
    def __init__(self, qty: int, price: float, symbol: str, side: str, id=None, pid=None):
        self.qty = qty
        self.price = price
        self.symbol = symbol
        self.side = side
        self.id = id  # Unique order id
        self.pid = pid  # Parent order id, if root will be -1

    def __repr__(self) -> str:
        return f"Order(qty={self.qty}, price={self.price}, symbol='{self.symbol}', side='{self.side}', id={self.id})"
