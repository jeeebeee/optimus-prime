from auction_appetite import AuctionAppetite
from auction_orders import AuctionOrders
from auction_state import AuctionState
from typing import Dict, Any

from symbol import Symbol

class OptimusPrime:
    """Main auction logic for matching orders to appetites."""
    def __init__(self, symbol: Symbol, state: AuctionState = None):
        self.symbol = symbol
        self.state = state

    def prime_optimization(self, side: str):
        if side not in ['buy', 'sell']:
            raise ValueError("Invalid order side")
        
        """Match orders at match price, reduce order size if needed, total adopted <= appetite."""
        side_appetite = self.state.appetite.get_appetites(side)
        """get opposite orders sorted by side"""
        opposite_orders = [o for o in self.state.orders.orders if o.side != side]
        opposite_orders.sort(key=lambda x: x.price, reverse=(side == 'buy'))
        """side / appetite here is optimus side and opposite_orders is the input orders side"""
        """
        sell_appetite    buy_orders
                      |  B 2000 @ 110
                      |   B   1 @ 110
        105 1000      |   B 999 @ 105
        104 500       |   B 500 @ 104
        103 200       |   B 300 @ 103
        102 100       |   B 100 @ 102
        100 0         |
        """
        consumed_appetite = {}
        for price, appetite in side_appetite:
            for order in opposite_orders:
                if (side == 'buy' and order.price <= price) or (side == 'sell' and order.price >= price):
                    if(order.balance_parent_qty() == order.qty): #has no child order / not processed yet
                        stub0 = order.create_child_order(1)
                        order.add_child_order(stub0)
                    unsent_qty = order.balance_parent_qty()
                    if unsent_qty > 0:
                        remaining_appetite = max(0, appetite - consumed_appetite.get(price, 0))
                        qty_to_adopt = min(unsent_qty, remaining_appetite)
                        if qty_to_adopt > 0:
                            stubN = order.create_child_order(qty_to_adopt, price)
                            consumed_appetite[price] = consumed_appetite.get(price, 0) + qty_to_adopt
                            order.add_child_order(stubN)
                else:
                    stubF = order.create_child_order(order.qty)
                    order.add_child_order(stubF)

        return self

    def __repr__(self):
        return f"OptimusPrime(symbol={self.symbol}, state={self.state})"
