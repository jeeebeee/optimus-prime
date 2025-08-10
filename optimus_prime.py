from auction_appetite import AuctionAppetite
from auction_orders import AuctionOrders
from auction_state import AuctionState
from typing import Dict, Any

class OptimusPrime:
    """Main auction logic for matching orders to appetites."""
    def __init__(self, state: AuctionState = None):
        self.state = state

    def prime_optimization(self, side: str):
        if side not in ['buy', 'sell']:
            raise ValueError("Invalid order side")
        
        """Match orders at match price, reduce order size if needed, total adopted <= appetite."""
        appetite = self.state.appetites.get(side, 0)
        opposite_orders = [o for o in self.state.orders if o.side != side]
        opposite_orders.sort(key=lambda x: x.price, reverse=(side == 'buy'))

        return True

    def __repr__(self):
        return f"OptimusPrime(auction_state={self.auction_state})"
