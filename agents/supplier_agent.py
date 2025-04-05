class SupplierAgent:
    def __init__(self):
        pass

    def reorder(self, store_id, product_id, quantity):
        return f"Reordered {quantity} units of Product {product_id} for Store {store_id}"
