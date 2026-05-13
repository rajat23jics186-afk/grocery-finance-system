"""Routes module."""

from backend.routes.users import router as users_router
from backend.routes.products import router as products_router
from backend.routes.orders import router as orders_router
from backend.routes.payments import router as payments_router
from backend.routes.reports import router as reports_router

__all__ = [
    "users_router",
    "products_router", 
    "orders_router",
    "payments_router",
    "reports_router"
]
