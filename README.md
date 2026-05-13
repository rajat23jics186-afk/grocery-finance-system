# Grocery Finance System

Grocery Finance System is a full-stack retail and wholesale order management project with FastAPI, HTML/CSS/JavaScript frontend templates, and three AI lab modules for data science, neural networks, and deep learning.

This README is written to be self-contained so it can be shared online or uploaded into an AI assistant for project review.

## Project Overview

The application supports three roles:

- Owner or admin, who manages products, stock, orders, payments, and reports.
- Retail customers, who browse retail pricing and place smaller orders.
- Wholesale customers, who browse wholesale pricing and place bulk orders.

The backend exposes REST endpoints through FastAPI. The project also includes Streamlit and Gradio dashboards for AI model demos and experimentation.

## Main Features

- Retail and wholesale pricing support.
- Admin dashboard for products, orders, users, payments, and reports.
- JWT-based authentication with password hashing.
- Sales and operational analytics.
- AI modules for customer segmentation, demand prediction, forecasting, and anomaly detection.
- Sample database initialization with demo users, products, orders, and payments.
- Separate Streamlit and Gradio applications for AI demonstrations.

## Tech Stack

- Backend: Python, FastAPI, Uvicorn, Pydantic.
- Authentication: JWT, bcrypt, passlib.
- Database: SQLite for local development, MySQL via PyMySQL for production.
- Data and AI: Pandas, NumPy, scikit-learn, TensorFlow, Matplotlib, Seaborn, Plotly.
- Dashboards: Streamlit, Gradio.
- Frontend: HTML, CSS, JavaScript, Bootstrap-style static UI assets.

## Folder Structure

```text
Grocery Finance System/
├── README.md
├── requirements.txt
├── run.py
├── init_db.py
├── start_server.bat
├── QUICKSTART.md
├── WEB_INTERFACE_GUIDE.txt
├── WEB_INTERFACES_SUMMARY.txt
├── NEW_WEB_INTERFACES_GUIDE.txt
├── INTERFACE_PREVIEW.txt
├── RETAIL_CLIENT_USER_GUIDE.txt
├── GroceryFinanceSystem_ProjectDocs.pdf
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── schemas.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── schema.sql
│   ├── models/
│   │   ├── __init__.py
│   │   ├── anomaly.py
│   │   ├── order.py
│   │   ├── payment.py
│   │   ├── product.py
│   │   ├── stock.py
│   │   └── user.py
│   └── routes/
│       ├── __init__.py
│       ├── orders.py
│       ├── payments.py
│       ├── products.py
│       ├── reports.py
│       └── users.py
├── frontend/
│   ├── __init__.py
│   ├── static/
│   │   ├── css/
│   │   │   └── dashboard.css
│   │   └── js/
│   │       ├── dashboard.js
│   │       └── uploader.js
│   └── templates/
│       ├── analytics.html
│       ├── dashboard.html
│       ├── forecast.html
│       ├── index.html
│       ├── inventory.html
│       ├── login.html
│       ├── mobile.html
│       ├── place-order.html
│       └── reports.html
├── ai_labs/
│   ├── __init__.py
│   ├── data_science/
│   │   ├── __init__.py
│   │   └── eda.py
│   ├── neural_network/
│   │   ├── __init__.py
│   │   └── demand.py
│   └── deep_learning/
│       ├── __init__.py
│       └── forecasting.py
├── dashboards/
│   ├── __init__.py
│   ├── gradio_app.py
│   └── streamlit_app.py
├── data/
├── models/
│   └── scalers/
├── uploads/
├── env/
└── venv/
```

## Quick Start

### Windows

1. Double-click `start_server.bat` to install dependencies, initialize the database, and start the app.
2. Or run the project manually:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python run.py
```

### Linux or macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python run.py
```

## How To Run

### FastAPI Web App

Run the main server with:

```bash
python run.py
```

Useful URLs:

- Home or frontend: http://localhost:8000/
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

### Streamlit Dashboard

```bash
streamlit run dashboards/streamlit_app.py
```

### Gradio App

```bash
python dashboards/gradio_app.py
```

## Sample Credentials

After running `init_db.py`, the demo accounts are:

| Role | Username | Password |
| --- | --- | --- |
| Owner | admin | admin123 |
| Retail Customer | john_retail | password123 |
| Wholesale Buyer | bulk_buyer | password123 |

## Core Modules

### Backend

- `backend/main.py` creates the FastAPI app, mounts static files, loads routes, and exposes the health endpoint.
- `backend/config.py` stores database, security, upload, and model paths.
- `backend/auth/` contains authentication helpers and schemas.
- `backend/database/` contains the schema and database initialization logic.
- `backend/models/` contains ORM models for users, products, orders, payments, stock history, and anomalies.
- `backend/routes/` contains the API route modules for users, products, orders, payments, and reports.

### Frontend

- `frontend/templates/` contains the HTML pages used by the web UI.
- `frontend/static/css/dashboard.css` contains the main styling.
- `frontend/static/js/dashboard.js` and `frontend/static/js/uploader.js` contain the frontend behavior.

### AI Labs

- `ai_labs/data_science/eda.py` handles exploratory data analysis and customer segmentation work.
- `ai_labs/neural_network/demand.py` contains the neural network demand-related logic.
- `ai_labs/deep_learning/forecasting.py` contains forecasting and anomaly-related logic.

### Dashboards

- `dashboards/streamlit_app.py` runs the Streamlit interface.
- `dashboards/gradio_app.py` runs the Gradio interface.

## Configuration

The main configuration values live in `backend/config.py`.

Important defaults include:

- SQLite database in the `data/` folder.
- JWT secret key, algorithm, and token expiration settings.
- Upload folder in `uploads/`.
- Model and scaler storage under `models/` and `models/scalers/`.

## Database Initialization

Use `init_db.py` to create tables and seed sample users, products, orders, and payments.

```bash
python init_db.py
```

## Notes For Uploading Online

- Upload the source files, not the virtual environment folders.
- Keep `README.md`, `requirements.txt`, and the `backend/`, `frontend/`, `ai_labs/`, and `dashboards/` folders together.
- If you are sharing this with an AI assistant, include the README first so the project structure is understood before the code.

## Troubleshooting

- If port 8000 is busy, stop the other process or change the Uvicorn port in `run.py`.
- If the database looks empty, rerun `python init_db.py`.
- If a package is missing, reinstall dependencies with `pip install -r requirements.txt`.

## License

Educational project for learning and demonstration purposes.
