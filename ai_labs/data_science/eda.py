"""Lab 1: Data Science - EDA & Customer Segmentation."""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List


class CustomerSegmentation:
    """K-Means customer segmentation for retail vs wholesale behavior analysis."""
    
    def __init__(self, n_clusters: int = 3):
        """Initialize segmentation model."""
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare customer data for segmentation."""
        # Feature engineering
        customer_features = df.groupby('customer_id').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'order_status': lambda x: (x == 'delivered').sum(),
        }).reset_index()
        
        customer_features.columns = ['customer_id', 'total_spending', 'avg_order_value', 
                                     'order_frequency', 'successful_orders']
        
        customer_features['success_rate'] = (
            customer_features['successful_orders'] / customer_features['order_frequency']
        )
        
        self.feature_names = ['total_spending', 'avg_order_value', 'order_frequency', 'success_rate']
        return customer_features
    
    def fit(self, df: pd.DataFrame) -> np.ndarray:
        """Fit K-Means model."""
        features = self.prepare_data(df)
        X = features[self.feature_names].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Adjust clusters if we have fewer samples than requested clusters
        n_clusters = min(self.n_clusters, len(X))
        if n_clusters != self.n_clusters:
            self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        
        self.kmeans.fit(X_scaled)
        return features
    
    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Predict customer segments."""
        features = self.prepare_data(df)
        X = features[self.feature_names].fillna(0)
        X_scaled = self.scaler.transform(X)
        return self.kmeans.predict(X_scaled)
    
    def get_segment_profiles(self, df: pd.DataFrame) -> Dict:
        """Get profile of each segment."""
        features = self.prepare_data(df)
        X = features[self.feature_names].fillna(0)
        X_scaled = self.scaler.transform(X)
        segments = self.kmeans.predict(X_scaled)
        
        profiles = {}
        n_clusters = min(self.n_clusters, X.shape[0])
        for i in range(n_clusters):
            mask = segments == i
            segment_data = X[mask].values if hasattr(X[mask], 'values') else X[mask]
            profiles[f"Segment_{i}"] = {
                "count": mask.sum(),
                "avg_spending": segment_data[:, 0].mean() if mask.sum() > 0 else 0,
                "avg_order_value": segment_data[:, 1].mean() if mask.sum() > 0 else 0,
                "avg_frequency": segment_data[:, 2].mean() if mask.sum() > 0 else 0,
            }
        return profiles


class CorrelationAnalysis:
    """Correlation analysis for product relationships."""
    
    @staticmethod
    def analyze(df: pd.DataFrame) -> pd.DataFrame:
        """Generate correlation heatmap data."""
        # Group by product and get statistics
        product_stats = df.groupby('product_id').agg({
            'quantity': 'sum',
            'unit_price': 'mean',
            'subtotal': 'sum',
        }).reset_index()
        
        # Calculate correlations
        correlations = product_stats.corr()
        return correlations


class EDA:
    """Exploratory Data Analysis utilities."""
    
    @staticmethod
    def get_summary_stats(df: pd.DataFrame) -> Dict:
        """Get basic statistics."""
        return {
            "total_records": len(df),
            "total_revenue": float(df['subtotal'].sum() if 'subtotal' in df.columns else 0),
            "avg_transaction": float(df['subtotal'].mean() if 'subtotal' in df.columns else 0),
            "unique_customers": df['customer_id'].nunique() if 'customer_id' in df.columns else 0,
            "unique_products": df['product_id'].nunique() if 'product_id' in df.columns else 0,
        }


if __name__ == "__main__":
    import sys
    import os
    
    # Add parent directory to path for imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    
    from backend.database import SessionLocal
    from backend.models.order import Order
    from backend.models.product import Product
    
    print("\n" + "="*60)
    print("📊 GROCERY FINANCE SYSTEM - DATA SCIENCE LAB #1")
    print("   Customer Segmentation & EDA Analysis")
    print("="*60 + "\n")
    
    # Load data from database
    db = SessionLocal()
    try:
        orders = db.query(Order).all()
        
        # Convert to DataFrame
        data = []
        for order in orders:
            data.append({
                'customer_id': order.customer_id,
                'product_id': order.id,
                'total_amount': order.total_amount,
                'order_status': order.order_status,
                'quantity': len(order.items) if hasattr(order, 'items') else 1,
                'unit_price': order.total_amount,
                'subtotal': order.total_amount,
            })
        
        df = pd.DataFrame(data)
        
        if len(df) > 0:
            print("✓ Loaded", len(df), "orders from database\n")
            
            # 1. Summary Statistics
            print("📈 SUMMARY STATISTICS:")
            print("-" * 60)
            stats = EDA.get_summary_stats(df)
            print(f"  Total Orders: {stats['total_records']}")
            print(f"  Total Revenue: ${stats['total_revenue']:,.2f}")
            print(f"  Average Transaction: ${stats['avg_transaction']:,.2f}")
            print(f"  Unique Customers: {stats['unique_customers']}")
            print(f"  Unique Products: {stats['unique_products']}\n")
            
            # 2. Customer Segmentation
            print("👥 CUSTOMER SEGMENTATION (K-Means, K=3):")
            print("-" * 60)
            segmentation = CustomerSegmentation(n_clusters=3)
            features = segmentation.fit(df)
            profiles = segmentation.get_segment_profiles(df)
            
            for segment, profile in profiles.items():
                print(f"  {segment}:")
                print(f"    - Customers: {profile['count']}")
                print(f"    - Avg Spending: ${profile['avg_spending']:,.2f}")
                print(f"    - Avg Order Value: ${profile['avg_order_value']:,.2f}")
                print(f"    - Order Frequency: {profile['avg_frequency']:.1f}\n")
            
            # 3. Correlation Analysis
            print("🔗 PRODUCT CORRELATIONS:")
            print("-" * 60)
            correlations = CorrelationAnalysis.analyze(df)
            if not correlations.empty:
                print("  Correlation Matrix:")
                print(correlations.to_string())
            print()
            
            print("="*60)
            print("✅ Analysis Complete!")
            print("="*60 + "\n")
        else:
            print("⚠️  No data found in database\n")
    
    finally:
        db.close()
