import uuid

class Order:
    """Represents a market order."""
    def __init__(self, qty: int, price: float, symbol: str, side: str, id=None, pid=None):
        self.qty = qty
        self.price = price
        self.symbol = symbol
        self.side = side
        self.id = id  # Unique order id
        self.pid = pid  # Parent order id, if root will be -1
        self.child_orders = []  # Child orders array of orders which have pid as id of this Order

    def __repr__(self) -> str:
        return f"Order(qty={self.qty}, price={self.price}, symbol='{self.symbol}', side='{self.side}', id={self.id}, pid={self.pid}, child_orders={self.child_orders})"

    def add_child_order(self, child_order):
        """Add a child order to the child_orders array."""
        self.child_orders.append(child_order)

    def create_child_order(self, qty, price=None, id=None):
        """Create a child order with pid set to this order's id and auto-generated unique id. Side is always same as parent."""
        child_price = price if price is not None else self.price
        # Auto-generate unique id for child order including pid
        suffix = uuid.uuid4().hex[:8]
        child_id = id if id is not None else f"{self.id}-child-{suffix}"
        child = Order(qty, child_price, self.symbol, self.side, id=child_id)
        child.pid = self.id
        return child

    def sum_child_order_qty(self):
        """Return the sum of qty for all child orders."""
        return sum(child.qty for child in self.child_orders)
    
    def balance_parent_qty(self):
        """Balance the parent order quantity with the sum of child orders."""
        balance_qty = self.qty
        balance_qty -= self.sum_child_order_qty()
        return balance_qty
