"""Streamlit Dashboard for AI Model Exploration."""

import streamlit as st
import pandas as pd
import numpy as np
from ai_labs.data_science import CustomerSegmentation, EDA
from ai_labs.neural_network import StockAlertSystem
from ai_labs.deep_learning import LSTMForecaster

st.set_page_config(page_title="Grocery Finance AI Dashboard", layout="wide")

st.title("🤖 Grocery Finance System - AI Analytics Dashboard")

# Sidebar navigation
page = st.sidebar.radio("Select Analytics", [
    "Dashboard Summary",
    "Customer Segmentation",
    "Demand Forecasting",
    "Stock Alerts",
    "Data Exploration"
])

# Sample data generation
@st.cache_data
def load_sample_data():
    """Load sample data for demo."""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100)
    data = {
        'order_id': range(1, 101),
        'customer_id': np.random.randint(1, 21, 100),
        'product_id': np.random.randint(1, 11, 100),
        'total_amount': np.random.uniform(50, 5000, 100),
        'quantity': np.random.randint(1, 20, 100),
        'order_status': np.random.choice(['pending', 'delivered', 'cancelled'], 100),
    }
    return pd.DataFrame(data)

df = load_sample_data()

if page == "Dashboard Summary":
    st.header("📊 Dashboard Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(df))
    with col2:
        st.metric("Total Revenue", f"${df['total_amount'].sum():,.2f}")
    with col3:
        st.metric("Avg Order Value", f"${df['total_amount'].mean():,.2f}")
    with col4:
        st.metric("Unique Customers", df['customer_id'].nunique())
    
    st.subheader("Order Status Distribution")
    status_counts = df['order_status'].value_counts()
    st.bar_chart(status_counts)

elif page == "Customer Segmentation":
    st.header("👥 Customer Segmentation Analysis")
    
    st.write("K-Means Clustering for customer behavior segmentation")
    
    n_clusters = st.slider("Number of segments", 2, 5, 3)
    
    segmentation = CustomerSegmentation(n_clusters=n_clusters)
    features = segmentation.prepare_data(df)
    
    st.write(f"Segmented {len(features)} customers into {n_clusters} groups")
    st.dataframe(features.head())

elif page == "Demand Forecasting":
    st.header("📈 7-Day & 30-Day Demand Forecasting")
    
    # Sample historical data
    historical = np.random.uniform(100, 500, 30)
    
    forecaster = LSTMForecaster(sequence_length=7)
    
    forecast_7day = forecaster.forecast_7days(historical)
    forecast_30day = forecaster.forecast_30days(historical)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("7-Day Forecast")
        st.line_chart(forecast_7day)
        st.write(forecast_7day)
    
    with col2:
        st.subheader("30-Day Forecast")
        st.line_chart(forecast_30day)

elif page == "Stock Alerts":
    st.header("⚠️ Stock Reorder Alerts")
    
    # Sample products
    products_data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Milk', 'Bread', 'Eggs', 'Butter', 'Cheese'],
        'quantity_in_stock': [5, 2, 15, 8, 3],
        'reorder_level': [10, 10, 20, 10, 10],
    }
    products_df = pd.DataFrame(products_data)
    
    alert_system = StockAlertSystem()
    alerts = alert_system.check_reorder_alerts(products_df)
    
    if alerts:
        st.error(f"⚠️ {len(alerts)} products need reordering!")
        for alert in alerts:
            st.warning(f"{alert['product_name']}: {alert['current_stock']} units (Level: {alert['reorder_level']})")
    else:
        st.success("✅ All products have sufficient stock")

elif page == "Data Exploration":
    st.header("🔍 Exploratory Data Analysis")
    
    st.subheader("Dataset Overview")
    st.dataframe(df.head(10))
    
    st.subheader("Summary Statistics")
    st.write(df.describe())
    
    st.subheader("Product Distribution")
    product_counts = df['product_id'].value_counts()
    st.bar_chart(product_counts)

st.sidebar.markdown("---")
st.sidebar.write("**Grocery Finance System**  \nAI-Powered Order Management")
