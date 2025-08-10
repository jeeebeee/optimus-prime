from auction_orders import AuctionOrders
from auction_appetite import AuctionAppetite

class AuctionState:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.orders = AuctionOrders(symbol)
        self.appetite = AuctionAppetite(symbol)
        
    def __repr__(self):
        return f"AuctionState(symbol={self.symbol}, orders={self.orders}, appetite={self.appetite})"
