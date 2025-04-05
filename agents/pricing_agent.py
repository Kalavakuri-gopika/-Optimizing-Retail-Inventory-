import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

class PricingAgent:
    def __init__(self, csv_path='data/pricing_optimization.csv'):
        self.data = pd.read_csv(csv_path)
        self.model = None

    def train_model(self):
        df = self.data.copy()
        required_columns = ['Store ID', 'Product ID', 'Competitor Prices', 'Discounts', 'Return Rate (%)', 'Price']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Missing column in data: {col}")

        features = df[['Store ID', 'Product ID', 'Competitor Prices', 'Discounts', 'Return Rate (%)']]
        target = df['Price']

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(features, target)

        # Save model
        with open('models/pricing_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)

    def predict_price(self, store_id, product_id, competitor_price, discount, return_rate):
        # Load the trained model
        with open('models/pricing_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        input_data = pd.DataFrame([[store_id, product_id, competitor_price, discount, return_rate]],
                                  columns=['Store ID', 'Product ID', 'Competitor Prices', 'Discounts', 'Return Rate (%)'])

        predicted_price = self.model.predict(input_data)[0]

        reason = (
            f"The price is optimized based on Store ID: {store_id}, Product ID: {product_id}, "
            f"Competitor Price: {competitor_price}, Discount: {discount}%, and Return Rate: {return_rate}%."
        )

        return round(predicted_price, 2), reason
