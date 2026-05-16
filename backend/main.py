"""Main FastAPI application for Grocery Finance System."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from backend.config import APP_NAME, APP_VERSION
from backend.database import init_db

# IMPORTANT: Import all models BEFORE init_db() so SQLAlchemy
# metadata knows about every table and creates them correctly.
from backend.models import User, Product, Order, OrderItem, Payment, StockHistory, Anomaly  # noqa: F401

from backend.routes import (
    users_router, products_router, orders_router,
    payments_router, reports_router
)

# Initialize database (creates all tables registered above)
init_db()

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered Retail & Wholesale Order Management System"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
static_path = os.path.join(os.path.dirname(__file__), "../frontend/static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# Include routers
app.include_router(users_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(payments_router)
app.include_router(reports_router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Mount frontend templates at root
templates_path = os.path.join(os.path.dirname(__file__), "../frontend/templates")
if os.path.exists(templates_path):
    app.mount("/", StaticFiles(directory=templates_path, html=True), name="frontend")



if __name__ == "__main__":
    import uvicorn
    # Use string reference — reload=True requires a module path string, not an app object
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
