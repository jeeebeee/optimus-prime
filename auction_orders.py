from order import Order

class AuctionOrders:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.orders = []

    def add_order(self, order: Order):
        self.orders.append(order)

    def get_orders_by_side(self, side):
        return [order for order in self.orders if getattr(order, 'side', None) == side]

    def __repr__(self):
        return f"AuctionOrders(orders={self.orders})"
