import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from agents.demand_agent import DemandAgent
from agents.inventory_agent import InventoryAgent
from agents.pricing_agent import PricingAgent
from agents.coordinator_agent import CoordinatorAgent

st.set_page_config(page_title="Multi-Agent Inventory System")
st.title("Retail Inventory Optimization System")


# Initialize agents
demand_agent = DemandAgent()
inventory_agent = InventoryAgent()
pricing_agent = PricingAgent()
coordinator_agent = CoordinatorAgent(demand_agent, inventory_agent, pricing_agent)

# Load inventory data for trend visualization
try:
    inventory_df = pd.read_csv("data/inventory_monitoring.csv", parse_dates=["Expiry Date"])
except Exception as e:
    st.warning(f"Could not load inventory data: {e}")
    inventory_df = pd.DataFrame()

tab1, tab2, tab3, tab4 = st.tabs(["Demand Forecast", "Inventory Check", "Pricing Optimization", "📊 Coordinator Dashboard"])

with tab1:
    st.subheader("Train and Predict Demand")
    date_input = st.date_input("Select Date", key="demand_tab_date")
    store_id = st.number_input("Store ID", min_value=1)
    product_id = st.number_input("Product ID", min_value=1)
    price = st.number_input("Product Price", min_value=0.0, step=0.1)

    promotions = st.selectbox("Promotions", ["Yes", "No"])
    seasonality = st.selectbox("Seasonality Factors", ["Festival", "Holiday", "None"])
    external_factors = st.selectbox("External Factors", ["Competitor Pricing", "Weather", "Economic", "None"])
    trend = st.selectbox("Demand Trend", ["Increasing", "Stable", "Decreasing"])
    customer_segment = st.selectbox("Customer Segments", ["Regular", "Premium", "Budget"])

    if st.button("Train Demand Model"):
        demand_agent.train_model()
        st.success("Model trained successfully")

    if st.button("Predict Demand"):
        predicted_demand, reason = demand_agent.predict(
            str(date_input),  # convert date to string
            store_id,
            product_id,
            price,
            promotions,
            seasonality,
            external_factors,
            trend,
            customer_segment
        )
        st.success(f"Predicted Demand: {predicted_demand:.2f}")
        st.info(f"Reason: {reason}")

with tab2:
    st.subheader("Check Inventory")
    store_id_inv = st.number_input("Store ID", min_value=1, key="store_inv")
    product_id_inv = st.number_input("Product ID", min_value=1, key="product_inv")

    if st.button("Check Inventory"):
        message = inventory_agent.check_inventory(store_id_inv, product_id_inv)
        st.info(message)

with tab3:
    st.header("💲 Optimize Pricing")

    store_id_p = st.text_input("Enter Store ID", key="price_store")
    product_id_p = st.text_input("Enter Product ID", key="price_product")
    competitor_price = st.number_input("Enter Competitor Price", min_value=0.0, key="competitor_price")
    discount = st.number_input("Enter Discount (%)", min_value=0.0, max_value=100.0, key="discount")
    return_rate = st.number_input("Enter Return Rate (%)", min_value=0.0, max_value=100.0, key="return_rate")

    if st.button("Suggest Price"):
        price, reason = pricing_agent.predict_price(store_id_p, product_id_p, competitor_price, discount, return_rate)
        st.success(f"**Suggested Price:** ₹{price:.2f}")
        st.info(reason)

with tab4:
    st.header("📊 Coordinator Agent: Decision Support System")

    date_input = st.date_input("Select Date", key="coord_date")
    store_id_c = st.text_input("Enter Store ID", key="coord_store")
    product_id_c = st.text_input("Enter Product ID", key="coord_product")
    price = st.number_input("Enter Current Price", min_value=0.0, key="coord_price")
    promotions = st.selectbox("Are Promotions Active?", ["Yes", "No"], key="coord_promo")
    seasonality = st.selectbox("Seasonality Factor", ["Festival", "Holiday", "None"], key="coord_season")
    external_factors = st.selectbox("External Factors", ["Competitor Pricing", "Weather", "Economic", "None"], key="coord_ext")
    trend = st.selectbox("Demand Trend", ["Increasing", "Stable", "Decreasing"], key="coord_trend")
    customer_segment = st.selectbox("Customer Segment", ["Regular", "Premium", "Budget"], key="coord_segment")

    if st.button("Evaluate and Recommend"):
        result = coordinator_agent.evaluate_and_recommend(
            str(date_input), store_id_c, product_id_c, price,
            promotions, seasonality, external_factors, trend, customer_segment
        )

        st.write(f"🔮 **Predicted Demand:** {result['Predicted Demand']:.2f}")
        st.write(f"📌 **Reason:** {result['Demand Reason']}")
        st.write(f"📦 **Inventory Status:** {result['Inventory Status']}")
        st.write(f"💰 **Suggested Price:** ₹{result['Suggested Price']}")



    st.markdown("---")
    st.subheader("📦 Standalone Inventory Status Check")

    inv_store_id = st.text_input("Inventory Check: Store ID", key="coord_inv_store")
    inv_product_id = st.text_input("Inventory Check: Product ID", key="coord_inv_product")

    if st.button("Check Inventory Status"):
        try:
            trend_data = inventory_df[
                (inventory_df["Store ID"].astype(str) == inv_store_id) &
                (inventory_df["Product ID"].astype(str) == inv_product_id)
            ]
            if trend_data.empty:
                st.warning("❌ No inventory data found for this store and product.")
            else:
                    latest = trend_data.sort_values("Expiry Date", ascending=False).iloc[0]
                    stock = latest["Stock Levels"]

                    if stock == 0:
                        st.error("🔴 Out of stock")
                        st.markdown("**Reason:** Inventory is depleted. Replenishment required immediately to avoid lost sales.")
                    elif stock < 20:
                        st.warning("🟠 Low stock")
                        st.markdown("**Reason:** Current stock is below 20 units. Potential stockout risk if demand spikes.")
                    elif stock > 100:
                        st.info("🔵 Overstocked")
                        st.markdown("**Reason:** Inventory exceeds 100 units. Possible over-ordering or drop in demand.")
                    else:
                        st.success("🟢 Inventory is sufficient")
                        st.markdown("**Reason:** Stock level is within optimal range.")

                    st.subheader("📈 Inventory Trend")
                    trend_data = trend_data.sort_values("Expiry Date")
                    st.line_chart(trend_data.set_index("Expiry Date")["Stock Levels"])
        except Exception as e:
            st.error(f"Error checking inventory: {e}")
