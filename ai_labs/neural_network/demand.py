"""Lab 2: Neural Network - Demand Prediction & Classification."""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor, MLPClassifier


class DemandPredictor:
    """MLP Neural Network for demand prediction."""
    
    def __init__(self, hidden_layer_size=(128, 64), max_iter=500):
        """Initialize MLP regressor."""
        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layer_size,
            max_iter=max_iter,
            random_state=42,
            learning_rate_init=0.001,
            activation='relu'
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features for demand prediction."""
        # Aggregate by product and date
        features_list = []
        
        for _, row in df.iterrows():
            features = [
                row.get('product_id', 0),
                row.get('quantity', 0),
                row.get('unit_price', 0),
            ]
            features_list.append(features)
        
        return np.array(features_list)
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit demand prediction model."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict demand."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


class ProductCategoryClassifier:
    """MLP Classifier for product category prediction."""
    
    def __init__(self, hidden_layer_size=(64, 32), max_iter=500):
        """Initialize MLP classifier."""
        self.model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_size,
            max_iter=max_iter,
            random_state=42,
            learning_rate_init=0.001,
        )
        self.scaler = StandardScaler()
        self.label_encoder = {}
        self.is_fitted = False
        
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit category classifier."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict product category."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


class StockAlertSystem:
    """Inventory management with automatic reorder alerts."""
    
    def __init__(self):
        """Initialize alert system."""
        self.reorder_threshold = 0.2  # 20% threshold
        
    def check_reorder_alerts(self, products: pd.DataFrame) -> list:
        """Check which products need reordering."""
        alerts = []
        
        for _, product in products.iterrows():
            if product['quantity_in_stock'] <= product['reorder_level']:
                alerts.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'current_stock': product['quantity_in_stock'],
                    'reorder_level': product['reorder_level'],
                    'severity': 'critical' if product['quantity_in_stock'] == 0 else 'warning',
                })
        
        return alerts
