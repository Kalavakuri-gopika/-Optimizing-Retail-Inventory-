class CoordinatorAgent:
    def __init__(self, demand_agent, inventory_agent, pricing_agent):
        self.demand_agent = demand_agent
        self.inventory_agent = inventory_agent
        self.pricing_agent = pricing_agent

    def evaluate_and_recommend(self, date, store_id, product_id, price, promotions,
                                seasonality, external_factors, trend, customer_segment):
        # Step 1: Predict demand
        predicted_demand, reason_demand = self.demand_agent.predict(
            date, store_id, product_id, price, promotions,
            seasonality, external_factors, trend, customer_segment
        )

        # Step 2: Check inventory
        inventory_message = self.inventory_agent.check_inventory(int(store_id), int(product_id))

        # Step 3: Suggest price
        suggested_price, _ = self.pricing_agent.predict_price(store_id, product_id, 0, 0, 0)

        # Step 4: Rule-based recommendation
        if "Out of stock" in inventory_message or "Low stock" in inventory_message:
            if predicted_demand > 50:
                recommendation = "📦 High demand expected but inventory is low. Recommend restocking."
            else:
                recommendation = "⚠️ Inventory is low. Monitor demand before restocking."
        elif "Overstocked" in inventory_message:
            if predicted_demand < 30:
                recommendation = "📉 Overstocked and low demand. Consider promotions."
            else:
                recommendation = "👍 Inventory high but demand looks okay. No urgent action."
        elif "No inventory data found" in inventory_message:
            recommendation = "❌ Inventory data missing. Please check the store/product ID."
        else:
            recommendation = "✅ Inventory and demand are balanced."

        return {
            "Predicted Demand": predicted_demand,
            "Demand Reason": reason_demand,
            "Inventory Status": inventory_message,
            "Suggested Price": round(suggested_price, 2),
            "Recommendation": recommendation
        }
