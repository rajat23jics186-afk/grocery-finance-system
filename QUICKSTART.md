#!/usr/bin/env python
"""QUICKSTART.md - Get started in 3 steps!"""

# 🚀 Quick Start Guide - Grocery Finance System

## ✅ Project Status: READY TO RUN!

The complete Grocery Finance System has been built and initialized with sample data.

---

## 🎯 Step 1: Start the FastAPI Server

### Windows (Easiest):
**Double-click:** `start_server.bat`

### Manual Start:
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run the server
python run.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The server will start at **http://localhost:8000**

---

## 📚 Step 2: Access the Application

### REST API Documentation
- **Swagger UI (Interactive):** http://localhost:8000/docs
- **ReDoc (Alternative):** http://localhost:8000/redoc

### Sample API Calls
```bash
# Get dashboard summary
curl http://localhost:8000/api/reports/dashboard-summary

# List products
curl http://localhost:8000/api/products/

# Login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

---

## 🔐 Step 3: Sample User Credentials

Use these to test the system:

| Role | Username | Password |
|------|----------|----------|
| **Admin/Owner** | admin | admin123 |
| **Retail Customer** | john_retail | password123 |
| **Wholesale Buyer** | bulk_buyer | password123 |

---

## 🤖 Step 4: Explore AI Dashboards (Optional)

### Streamlit Dashboard
```bash
streamlit run dashboards/streamlit_app.py
```
Opens at http://localhost:8501

Features:
- Customer Segmentation Visualization
- Demand Forecasting Charts
- Stock Alert Monitoring
- Data Exploration

### Gradio Interactive Interface
```bash
python dashboards/gradio_app.py
```

Features:
- Interactive customer segmentation
- Real-time demand prediction
- Fraud detection scoring

---

## 📊 Key API Endpoints

### Authentication
```
POST /api/users/register      - Register new user
POST /api/users/login         - User login (returns JWT token)
GET  /api/users/me            - Get current user
GET  /api/users/              - List all users
GET  /api/users/{id}          - Get user by ID
```

### Products
```
GET  /api/products/           - List all products
GET  /api/products/{id}       - Get product details
POST /api/products/           - Create new product
PUT  /api/products/{id}       - Update product
DELETE /api/products/{id}     - Delete product
```

### Orders
```
GET  /api/orders/             - List orders
GET  /api/orders/{id}         - Get order details
POST /api/orders/             - Create new order
PUT  /api/orders/{id}         - Update order status
```

### Payments
```
GET  /api/payments/           - List payments
GET  /api/payments/{id}       - Get payment details
POST /api/payments/           - Record payment
```

### Reports
```
GET  /api/reports/dashboard-summary        - Dashboard metrics
GET  /api/reports/sales-by-category        - Category breakdown
GET  /api/reports/payment-status           - Payment distribution
GET  /api/reports/retail-vs-wholesale      - Revenue comparison
```

---

## 🗄️ Database

**Location:** `data/grocery_finance.db` (SQLite)

**Tables:**
- `users` - Customers and owner
- `products` - Product catalog
- `orders` - Customer orders
- `order_items` - Order line items
- `payments` - Payment records
- `stock_history` - Inventory tracking
- `anomalies` - Fraud/anomaly detection

---

## 📁 Project Structure

```
├── backend/              # FastAPI server & database
│   ├── main.py          # App entry point
│   ├── models/          # ORM models
│   ├── routes/          # API endpoints
│   └── auth/            # Authentication
├── frontend/            # Web interface
│   ├── templates/       # HTML pages
│   └── static/          # CSS & JavaScript
├── ai_labs/             # ML modules
│   ├── data_science/    # Segmentation & EDA
│   ├── neural_network/  # Demand prediction
│   └── deep_learning/   # Forecasting & anomaly
├── dashboards/          # Streamlit & Gradio UIs
├── data/                # SQLite database
├── init_db.py           # Database initialization
├── run.py               # Server runner
└── requirements.txt     # Dependencies
```

---

## 🔧 Configuration

**File:** `backend/config.py`

Default settings use SQLite. For MySQL production:

```python
DATABASE_URL = "mysql+pymysql://user:password@localhost/grocery_db"
SECRET_KEY = "change-this-in-production"
```

---

## 📝 Sample Data

The database includes:
- **3 users** (1 owner + 1 retail + 1 wholesale)
- **10 products** (Dairy, Bakery, Produce, Meat, Pantry)
- **15 orders** with random statuses
- **10 payments** processed

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Reset database
del data\grocery_finance.db
python init_db.py

# Run server
python run.py

# Start Streamlit dashboard
streamlit run dashboards/streamlit_app.py

# Start Gradio interface
python dashboards/gradio_app.py
```

---

## 🎓 AI Lab Modules

### Lab 1: Data Science (EDA & Segmentation)
**File:** `ai_labs/data_science/eda.py`

- K-Means customer clustering
- Correlation analysis
- Summary statistics

### Lab 2: Neural Network (Demand Prediction)
**File:** `ai_labs/neural_network/demand.py`

- MLP demand forecaster
- Product category classifier
- Automatic stock alerts

### Lab 3: Deep Learning (Advanced Forecasting)
**File:** `ai_labs/deep_learning/forecasting.py`

- LSTM 7-day & 30-day forecasts
- Autoencoder anomaly detection
- Fraud detection system

---

## 🐛 Troubleshooting

**Port 8000 in use?**
```bash
python run.py --port 8001
```

**Database locked/corrupted?**
```bash
# Delete and reinitialize
del data\grocery_finance.db
python init_db.py
```

**Missing packages?**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📞 Need Help?

- Check `README.md` for full documentation
- Review API docs at `/docs`
- Check Django logs and terminal output

---

## ✨ You're All Set!

The Grocery Finance System is ready for:
✅ Learning fullstack web development
✅ Exploring machine learning workflows
✅ Building with FastAPI
✅ Database design with SQLAlchemy
✅ Authentication & security
✅ Interactive data visualization

**Happy Learning! 🚀**
