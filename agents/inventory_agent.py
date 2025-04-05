import pandas as pd

class InventoryAgent:
    def __init__(self, csv_path='data/inventory_monitoring.csv', low_threshold=10, high_threshold=100):
        self.data = pd.read_csv(csv_path)
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def check_inventory(self, store_id, product_id):
        # Filter the data for the specific store and product
        entry = self.data[
            (self.data['Store ID'] == store_id) & 
            (self.data['Product ID'] == product_id)
        ]

        if entry.empty:
            return "No inventory data found for the specified store and product."

        stock_level = entry.iloc[0]['Stock Levels']

        if stock_level == 0:
            return "Out of stock: No units left."
        elif stock_level < self.low_threshold:
            return f"Low stock: Only {stock_level} units left."
        elif stock_level > self.high_threshold:
            return f"Overstocked: {stock_level} units, which may lead to storage costs or wastage."
        else:
            return f"Stock level is normal: {stock_level} units available."
