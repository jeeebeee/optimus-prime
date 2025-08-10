import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from tests.input_generators import generate_sample_input_symbols, generate_sample_input_orders, generate_sample_input_appetites

def main():
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate inputs with error handling
        symbol_params = generate_sample_input_symbols(n=5)
        if not symbol_params:
            raise ValueError("Failed to generate symbol parameters")
            
        if not generate_sample_input_orders(n=10, symbol_params=symbol_params):
            raise ValueError("Failed to generate orders")
            
        if not generate_sample_input_appetites(n=10, symbol_params=symbol_params):
            raise ValueError("Failed to generate appetites")
            
        print("Successfully generated input files in tests/data/")
        
    except Exception as e:
        print(f"Error generating inputs: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
