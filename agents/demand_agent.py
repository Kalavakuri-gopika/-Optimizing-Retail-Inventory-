import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle

class DemandAgent:
    def __init__(self, csv_path='data/demand_forecasting.csv'):
        self.data = pd.read_csv(csv_path)
        self.model = None

    def train_model(self):
        df = self.data.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df['DayOfYear'] = df['Date'].dt.dayofyear

        # Handle categorical columns
        label_encoders = {}
        for col in ['Promotions', 'Seasonality Factors', 'External Factors', 'Demand Trend', 'Customer Segments']:
            if df[col].dtype == 'object':
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                label_encoders[col] = le

        features = df[['DayOfYear', 'Store ID', 'Product ID', 'Price', 
                       'Promotions', 'Seasonality Factors', 'External Factors',
                       'Demand Trend', 'Customer Segments']]
        target = df['Sales Quantity']

        self.model = RandomForestRegressor(n_estimators=100)
        self.model.fit(features, target)

        # Save model and encoders
        with open('models/demand_model.pkl', 'wb') as f:
            pickle.dump({'model': self.model, 'encoders': label_encoders}, f)

    def predict(self, date, store_id, product_id, price, promotions, seasonality, external_factors, trend, customer_segment):
        with open('models/demand_model.pkl', 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            encoders = data['encoders']

        date = pd.to_datetime(date)
        day_of_year = date.dayofyear

        # Encode inputs
        enc_promotions = encoders['Promotions'].transform([promotions])[0]
        enc_seasonality = encoders['Seasonality Factors'].transform([seasonality])[0]
        enc_external = encoders['External Factors'].transform([external_factors])[0]
        enc_trend = encoders['Demand Trend'].transform([trend])[0]
        enc_segment = encoders['Customer Segments'].transform([customer_segment])[0]

        input_data = pd.DataFrame([[
            day_of_year, store_id, product_id, price,
            enc_promotions, enc_seasonality, enc_external,
            enc_trend, enc_segment
        ]], columns=[
            'DayOfYear', 'Store ID', 'Product ID', 'Price',
            'Promotions', 'Seasonality Factors', 'External Factors',
            'Demand Trend', 'Customer Segments'
        ])

        prediction = self.model.predict(input_data)[0]

        # Human-readable reason
        reason = (
            f"Prediction based on: "
            f"Price = {price}, "
            f"Promotions = {promotions}, "
            f"Seasonality = {seasonality}, "
            f"External Factors = {external_factors}, "
            f"Trend = {trend}, "
            f"Customer Segment = {customer_segment}"
        )

        return prediction, reason
