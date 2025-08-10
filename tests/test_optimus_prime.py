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
                    order = Order(int(row['qty']), float(row['price']), symbol, row['side'])
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
            breakpoint()  # Debugger will stop here
            print(f"\nState for {symbol}:")
            print(f"Orders: {len(state.orders.orders)}")
            print(f"Buy appetites: {len(state.appetite.data['buy'])}")
            print(f"Sell appetites: {len(state.appetite.data['sell'])}")

    def test_optimus_prime_optimization(self):
        """Test the optimization logic for all symbols in test."""
        for symbol, state in self.states.items():
            optimus_prime = OptimusPrime(state=self.state)
            self.test_optimus_prime_optimization_for_symbol(optimus_prime)
        return True

    def test_optimus_prime_optimization_for_symbol(self, optimus_prime):
        """Test the optimization logic for a specific symbol."""
        res = optimus_prime.prime_optimization()
        return True

if __name__ == '__main__':
    unittest.main()
