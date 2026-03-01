from typing import List, Optional
from models import Product, CartItem, ShippingAddress, OrderCreate
import uuid
from datetime import datetime

# ============ DUMMY DATA (For Development) ============
DUMMY_PRODUCTS: List[Product] = [
    Product(
        id="oversized-shell-tee-black",
        name="Oversized Shell Tee",
        description="Premium heavyweight cotton tee with structured shell detailing. Designed for the modern minimalist.",
        price=2499.00,
        images=[
            "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&q=80",
            "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&q=80"
        ],
        category="APPAREL",
        sizes=["S", "M", "L", "XL"],
        stock=50,
        material="100% Organic Cotton",
        limited_edition=False
    ),
    Product(
        id="cargo-pants-olive",
        name="Utility Cargo Pants",
        description="Multi-pocket cargo design with adjustable straps. Built for function, styled for fashion.",
        price=4999.00,
        images=[
            "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&q=80",
            "https://images.unsplash.com/photo-1496217590453-aa65df56fb67?w=800&q=80"
        ],
        category="APPAREL",
        sizes=["28", "30", "32", "34"],
        stock=30,
        material="Cotton-Poly Blend",
        limited_edition=True
    ),
    Product(
        id="bomber-jacket-black",
        name="Technical Bomber Jacket",
        description="Water-resistant shell with premium insulation. Urban protection meets luxury aesthetics.",
        price=8999.00,
        images=[
            "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&q=80",
            "https://images.unsplash.com/photo-1551488852-7a3049f0c8e8?w=800&q=80"
        ],
        category="OUTERWEAR",
        sizes=["S", "M", "L", "XL"],
        stock=15,
        material="Nylon Shell, Down Fill",
        limited_edition=True
    ),
]

# ============ PRODUCT FUNCTIONS ============
def get_products() -> List[Product]:
    """Get all products"""
    return DUMMY_PRODUCTS

def get_product_by_id(product_id: str) -> Optional[Product]:
    """Get single product by ID"""
    for product in DUMMY_PRODUCTS:
        if product.id == product_id:
            return product
    return None

def get_products_by_category(category: str) -> List[Product]:
    """Filter products by category"""
    return [p for p in DUMMY_PRODUCTS if p.category.upper() == category.upper()]

# ============ ORDER FUNCTIONS ============
ORDERS_DB = []

def create_order_in_db(order: OrderCreate) -> str:
    """Create order and return order ID"""
    order_id = f"NV-{uuid.uuid4().hex[:8].upper()}"
    
    order_data = {
        "order_id": order_id,
        "items": [item.dict() for item in order.items],
        "customer_email": order.customer_email,
        "shipping_address": order.shipping_address.dict(),
        "origin_url": order.origin_url,
        "created_at": datetime.now().isoformat(),
        "status": "confirmed"
    }
    
    ORDERS_DB.append(order_data)
    print(f"✓ Order created: {order_id}")
    return order_id

def get_order_by_id(order_id: str) -> Optional[dict]:
    """Get order by ID"""
    for order in ORDERS_DB:
        if order["order_id"] == order_id:
            return order
    return None