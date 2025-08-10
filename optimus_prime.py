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
        side_appetite = self.state.appetite.get_appetites(side)
        """get opposite orders sorted by side"""
        opposite_orders = [o for o in self.state.orders if o.side != side]
        opposite_orders.sort(key=lambda x: x.price, reverse=(side == 'buy'))

        for price, appetite in appetite:
            total_adopted = 0
            for order in opposite_orders:
                if order.price == price:
                    1
                elif order.price < price:
                    1
                else:
                    1

        return True

    def __repr__(self):
        return f"OptimusPrime(auction_state={self.auction_state})"
