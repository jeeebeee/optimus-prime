import csv
import os
import numpy as np
from symbol import Symbol

def generate_sample_input_symbols(n: int):
    symbols = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'META'][:n]
    symbol_params = {}
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'input_symbols.csv')
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['symbol', 'refprx', 'matchprx', 'mean', 'stdev'])
        for symbol in symbols:
            mean = np.random.uniform(100, 120)
            stdev = np.random.uniform(1, 5)
            refprx = np.random.normal(mean, stdev)
            matchprx = np.random.normal(mean, stdev)
            writer.writerow([symbol, round(refprx,2), round(matchprx,2), round(mean,2), round(stdev,4)])
            symbol_params[symbol] = {
                'refprx': refprx,
                'matchprx': matchprx,
                'mean': mean,
                'stdev': stdev
            }
    return symbol_params

def generate_sample_input_orders(n: int, symbol_params):
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'input_orders.csv')
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pid', 'id', 'symbol', 'side', 'qty', 'price'])
        order_id_counter = 0
        for symbol, params in symbol_params.items():
            for _ in range(n):
                side = np.random.choice(['buy', 'sell'])
                qty = int(np.random.normal(100, 20))
                price = params['refprx'] * (1 + np.random.uniform(-0.02, 0.02))
                order_id = f"{symbol}-{side}-{order_id_counter}"
                pid = -1
                writer.writerow([pid, order_id, symbol, side, abs(qty), round(price,2)])
                order_id_counter += 1
    return True

def generate_sample_input_appetites(n: int, symbol_params):
    output_file = os.path.join(os.path.dirname(__file__), 'data', 'input_appetites.csv')
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['symbol', 'side', 'price', 'appetite'])
        for symbol, params in symbol_params.items():
            prices = np.linspace(params['refprx']*0.98, params['refprx']*1.02, n)
            for price in prices:
                for side in ['buy', 'sell']:
                    appetite = int(np.random.normal(500, 100))
                    writer.writerow([symbol, side, round(price,2), abs(appetite)])
    return True
