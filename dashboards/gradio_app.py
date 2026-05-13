"""Gradio Dashboard for AI Model Interaction."""

import gradio as gr
import pandas as pd
import numpy as np
from ai_labs.data_science import CustomerSegmentation, EDA
from ai_labs.neural_network import DemandPredictor
from ai_labs.deep_learning import FraudDetectionSystem


def run_customer_segmentation(n_clusters: int = 3):
    """Run customer segmentation."""
    # Sample data
    np.random.seed(42)
    data = {
        'order_id': range(1, 101),
        'customer_id': np.random.randint(1, 21, 100),
        'total_amount': np.random.uniform(50, 5000, 100),
        'order_status': np.random.choice(['pending', 'delivered'], 100),
    }
    df = pd.DataFrame(data)
    
    segmentation = CustomerSegmentation(n_clusters=n_clusters)
    features = segmentation.prepare_data(df)
    
    return f"Segmented {len(features)} customers into {n_clusters} clusters", features.to_string()


def predict_demand(product_id: int = 1, days: int = 7):
    """Predict product demand."""
    # Simulate historical demand
    historical = np.random.uniform(100, 500, 30)
    
    predictor = DemandPredictor()
    X = np.array([[product_id, 1, 100]] * 10)
    y = np.random.uniform(100, 500, 10)
    
    try:
        predictor.fit(X, y)
        forecast = predictor.predict(np.array([[product_id, 1, 100]]))
        return f"Predicted demand for product {product_id}: {forecast[0]:.2f} units for {days} days"
    except:
        return "Error in prediction"


def check_fraud(customer_id: int = 1, amount: float = 100, quantity: int = 5, payment_method: str = "cash"):
    """Check transaction for fraud."""
    transaction = {
        'customer_id': customer_id,
        'amount': amount,
        'quantity': quantity,
        'payment_method': payment_method,
    }
    
    result = FraudDetectionSystem.check_transaction(transaction)
    status = "⚠️ SUSPICIOUS" if result['is_suspicious'] else "✅ NORMAL"
    
    return f"{status}\nFraud Score: {result['fraud_score']}/100\nIndicators: {', '.join(result['indicators']) if result['indicators'] else 'None'}"


# Create Gradio interface
with gr.Blocks(title="Grocery Finance AI Dashboard") as demo:
    gr.Markdown("# 🤖 Grocery Finance System - Gradio AI Dashboard")
    
    with gr.Tabs():
        with gr.TabItem("Customer Segmentation"):
            with gr.Row():
                n_clusters = gr.Slider(2, 5, value=3, step=1, label="Number of Clusters")
            with gr.Row():
                btn = gr.Button("Run Segmentation")
            with gr.Row():
                output1 = gr.Textbox(label="Result", lines=2)
                output2 = gr.Textbox(label="Customer Features", lines=10)
            
            btn.click(run_customer_segmentation, inputs=n_clusters, outputs=[output1, output2])
        
        with gr.TabItem("Demand Prediction"):
            with gr.Row():
                product_id = gr.Number(value=1, label="Product ID")
                days = gr.Slider(1, 30, value=7, step=1, label="Forecast Days")
            with gr.Row():
                btn = gr.Button("Predict Demand")
            with gr.Row():
                output = gr.Textbox(label="Prediction")
            
            btn.click(predict_demand, inputs=[product_id, days], outputs=output)
        
        with gr.TabItem("Fraud Detection"):
            with gr.Row():
                customer_id = gr.Number(value=1, label="Customer ID")
                amount = gr.Number(value=100, label="Transaction Amount")
            with gr.Row():
                quantity = gr.Slider(1, 100, value=5, step=1, label="Quantity")
                payment_method = gr.Dropdown(["cash", "credit_card", "debit_card", "upi"], value="cash", label="Payment Method")
            with gr.Row():
                btn = gr.Button("Check Fraud Risk")
            with gr.Row():
                output = gr.Textbox(label="Fraud Analysis")
            
            btn.click(check_fraud, inputs=[customer_id, amount, quantity, payment_method], outputs=output)


if __name__ == "__main__":
    demo.launch(share=True)
