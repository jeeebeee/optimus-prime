import unittest
import csv
import os
from auction_orders import AuctionOrders
from auction_appetite import AuctionAppetite
from auction_state import AuctionState
from optimus_prime import OptimusPrime
from symbol import Symbol
from order import Order

class TestOptimusPrime(unittest.TestCase):
    def setUp(self):
        """Initialize test data from CSVs and create AuctionState objects."""
        self.symbols = {}
        self.states = {}
        
        # Load symbols and create states
        symbols_csv = os.path.join(os.path.dirname(__file__), 'data', 'input_symbols.csv')
        with open(symbols_csv, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol']
                self.symbols[symbol] = Symbol(
                    symbol, 
                    float(row['refprx']), 
                    float(row['matchprx']),
                    float(row['mean']), 
                    float(row['stdev'])
                )
                self.states[symbol] = AuctionState(symbol)

        # Load orders into states
        orders_csv = os.path.join(os.path.dirname(__file__), 'data', 'input_orders.csv')
        with open(orders_csv, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol']
                if symbol in self.states:
                    order = Order(int(row['qty']), float(row['price']), symbol, row['side'], row['id'], row['pid'])
                    self.states[symbol].orders.add_order(order)

        # Load appetites into states
        appetites_csv = os.path.join(os.path.dirname(__file__), 'data', 'input_appetites.csv')
        with open(appetites_csv, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol']
                if symbol in self.states:
                    self.states[symbol].appetite.set_appetite(
                        float(row['price']), 
                        int(row['appetite']), 
                        row['side']
                    )

    def test_debug_setup_states(self):
        """Debug test to examine loaded states."""
        for symbol, state in self.states.items():
            print(f"\nState for {symbol}:")
            print(f"Orders: {len(state.orders.orders)}")
            print(f"Buy appetites: {len(state.appetite.data['buy'])}")
            print(f"Sell appetites: {len(state.appetite.data['sell'])}")
        return None

    def test_optimus_prime_optimization(self):
        """Test the optimization logic for all symbols in test."""
        for symbol, state in self.states.items():
            optimus_prime = OptimusPrime(symbol=self.symbols[symbol],state=state)
            optimus_prime = self._test_optimus_prime_optimization_for_symbol(optimus_prime)
        return None

    def _test_optimus_prime_optimization_for_symbol(self, optimus_prime):
        """Helper to test the optimization logic for a specific symbol."""
        optimus_prime = self._test_optimus_prime_optimization_for_symbol_side('buy',optimus_prime)
        optimus_prime = self._test_optimus_prime_optimization_for_symbol_side('sell',optimus_prime)
        return optimus_prime
    
    def _test_optimus_prime_optimization_for_symbol_side(self, side, optimus_prime):
        """Helper to test the optimization logic for a specific symbol and side."""
        print(f"\nTesting OptimusPrime for symbol: {optimus_prime.symbol.symbol}, side: {side}")
        optimus_prime = optimus_prime.prime_optimization(side)
        print(f"res: {optimus_prime}")
        match_prx = optimus_prime.symbol.matchprx
        print(f"Match Price: {match_prx}")

        parent_mkt_execute_qty = 0
        for order in optimus_prime.state.orders.get_orders_by_side('buy' if side=='sell' else 'sell'):
            if (side=='sell' and order.price >= match_prx) or (side=='buy' and order.price <= match_prx):
                parent_mkt_execute_qty += order.qty
        print(f"Parent should execute qty: {parent_mkt_execute_qty} at match price: {match_prx}")

        child_mkt_execute_qty = 0
        for order in optimus_prime.state.orders.get_orders_by_side('buy' if side=='sell' else 'sell'):
            for child in order.child_orders:
                if (side=='sell' and child.price >= match_prx) or (side=='buy' and child.price <= match_prx):
                    child_mkt_execute_qty += child.qty
        print(f"Child market executed qty: {child_mkt_execute_qty} at match price: {match_prx}")

        unfilled_parent_qty = parent_mkt_execute_qty - child_mkt_execute_qty
        print(f"Unfilled parent qty = {unfilled_parent_qty}")

        appetite_at_matchpx = optimus_prime.state.appetite.get_appetite(match_prx,side)
        print(f"Optimus appetite at match price: {appetite_at_matchpx}")

        assert appetite_at_matchpx == unfilled_parent_qty, "Optimus appetite at match price should be the unfilled parent qty"

        return optimus_prime

if __name__ == '__main__':
    unittest.main()
