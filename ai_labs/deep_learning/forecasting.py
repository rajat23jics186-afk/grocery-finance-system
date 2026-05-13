"""Lab 3: Deep Learning - LSTM Forecasting & Autoencoder Anomaly Detection."""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


class LSTMForecaster:
    """LSTM-based time series forecasting for demand (7-day and 30-day)."""
    
    def __init__(self, sequence_length: int = 7):
        """Initialize LSTM forecaster."""
        self.sequence_length = sequence_length
        self.is_fitted = False
        self.scaler = StandardScaler()
        
    def prepare_sequences(self, data: np.ndarray) -> tuple:
        """Prepare sequences for LSTM."""
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(data[i + self.sequence_length])
        return np.array(X), np.array(y)
    
    def forecast_7days(self, historical_data: np.ndarray) -> np.ndarray:
        """Forecast 7-day demand."""
        # Simulate LSTM forecast
        trend = np.mean(np.diff(historical_data[-7:]))
        forecast = []
        last_value = historical_data[-1]
        
        for i in range(7):
            forecast.append(last_value + trend * (i + 1))
        
        return np.array(forecast)
    
    def forecast_30days(self, historical_data: np.ndarray) -> np.ndarray:
        """Forecast 30-day demand."""
        # Simulate LSTM forecast
        trend = np.mean(np.diff(historical_data[-30:]))
        forecast = []
        last_value = historical_data[-1]
        
        for i in range(30):
            forecast.append(last_value + trend * (i + 1))
        
        return np.array(forecast)


class AutoencoderAnomalyDetector:
    """Autoencoder for fraud and anomaly detection."""
    
    def __init__(self, contamination: float = 0.1):
        """Initialize anomaly detector."""
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def prepare_transaction_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract transaction features for anomaly detection."""
        features = []
        
        for _, row in df.iterrows():
            transaction_features = [
                row.get('customer_id', 0),
                row.get('amount', 0),
                row.get('quantity', 0),
                row.get('unit_price', 0),
            ]
            features.append(transaction_features)
        
        return np.array(features)
    
    def fit(self, X: np.ndarray):
        """Fit anomaly detector."""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)
        self.is_fitted = True
        
    def detect_anomalies(self, X: np.ndarray) -> dict:
        """Detect anomalies in transactions."""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before detection")
        
        X_scaled = self.scaler.transform(X)
        anomaly_labels = self.model.predict(X_scaled)
        anomaly_scores = self.model.score_samples(X_scaled)
        
        anomalies = {
            'anomaly_indices': np.where(anomaly_labels == -1)[0],
            'anomaly_scores': anomaly_scores,
            'anomaly_count': (anomaly_labels == -1).sum(),
        }
        
        return anomalies


class FraudDetectionSystem:
    """Comprehensive fraud detection using multiple heuristics."""
    
    @staticmethod
    def check_transaction(transaction: dict) -> dict:
        """Check single transaction for fraud indicators."""
        fraud_score = 0
        indicators = []
        
        # Check for unusual amount
        if transaction.get('amount', 0) > 10000:
            fraud_score += 20
            indicators.append("Large transaction amount")
        
        # Check for unusual quantity
        if transaction.get('quantity', 0) > 100:
            fraud_score += 15
            indicators.append("Unusual quantity")
        
        # Check payment method
        if transaction.get('payment_method') == 'cash' and transaction.get('amount', 0) > 5000:
            fraud_score += 10
            indicators.append("Large cash transaction")
        
        return {
            'is_suspicious': fraud_score >= 30,
            'fraud_score': fraud_score,
            'indicators': indicators,
        }
