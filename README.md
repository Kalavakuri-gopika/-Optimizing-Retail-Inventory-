# Multi-Agent Inventory Optimization System

A smart retail system using AI agents to optimize inventory, pricing, and supply chain collaboration.

## Features
- Demand forecasting using ML
- Real-time inventory checks
- Dynamic pricing suggestions
- Supplier interaction simulation
- Customer satisfaction tracking
- LLM integration using Ollama

## Run with:
```bash
streamlit run app/main.py
```

## Train the demand model before using it:
```bash
python -c "from agents.demand_agent import DemandAgent; DemandAgent().train_model()"
```