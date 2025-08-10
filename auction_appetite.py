from typing import Dict, Any, Optional

class AuctionAppetite:
    """Represents appetite data for buy/sell sides per symbol and price."""
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.data: Dict[str, Dict[float, int]] = {'buy': {}, 'sell': {}}

    def set_appetite(self, price: float, appetite: int, side: str) -> None:
        self.data[side][price] = appetite

    def get_appetite(self, price: float, side: str) -> Optional[int]:
        side_data = self.data.get(side, {})
        if price in side_data:
            return side_data[price]
        if not side_data:
            return None
        prices = sorted(side_data.keys())
        lower = None
        upper = None
        for p in prices:
            if p < price:
                lower = p
            elif p > price and upper is None:
                upper = p
                break
        if lower is not None and upper is not None:
            appetite_lower = side_data[lower]
            appetite_upper = side_data[upper]
            interpolated = appetite_lower + (appetite_upper - appetite_lower) * ((price - lower) / (upper - lower))
            return int(round(interpolated))
        closest_price = min(prices, key=lambda p: abs(p - price))
        return side_data[closest_price]

    def get_appetites(self):
        appetites = []
        for side in ['buy', 'sell']:
            for price, qty in self.data[side].items():
                appetites.append((self.symbol, price, qty, side))
        return appetites

    def __repr__(self) -> str:
        return f"AuctionAppetite(symbol={self.symbol}, data={self.data})"
