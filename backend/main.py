from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import EmailStr
from typing import List, Optional
import uvicorn

# Import models
from models import Product, CartItem, ShippingAddress, OrderCreate, OrderResponse
from database import get_products, get_product_by_id, create_order_in_db

# ============ APP SETUP ============
app = FastAPI(
    title="NEVO Fashion API",
    description="Luxury Streetwear Backend API",
    version="1.0.0"
)

# ============ CORS CONFIG ============
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:3000",      # React dev server
        "https://nevo-final.vercel.app",  # Vercel production
        "https://nevo.store",         # Custom domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ HEALTH CHECK ============
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "NEVO Fashion API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# ============ PRODUCTS ============
@app.get("/api/products", response_model=List[Product])
async def list_products(category: Optional[str] = None):
    """Get all products, optionally filtered by category"""
    try:
        products = get_products()
        
        if category:
            products = [p for p in products if p.category.upper() == category.upper()]
        
        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch products: {str(e)}"
        )

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get single product by ID/slug"""
    try:
        product = get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product '{product_id}' not found"
            )
        
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch product: {str(e)}"
        )

@app.get("/api/categories")
async def list_categories():
    """Get available product categories"""
    try:
        products = get_products()
        categories = list(set(p.category.upper() for p in products))
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch categories: {str(e)}"
        )

# ============ ORDERS ============
@app.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create new order"""
    try:
        # Validate items have stock (basic check)
        products = get_products()
        for item in order.items:
            product = next((p for p in products if p.id == item.product_id), None)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product '{item.product_id}' not found"
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{product.name}'"
                )
        
        # Create order in database
        order_id = create_order_in_db(order)
        
        return OrderResponse(
            success=True,
            message="Order created successfully",
            order_id=order_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create order: {str(e)}"
        )

# ============ ERROR HANDLERS ============
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "success": False,
        "error": "Resource not found",
        "path": request.url.path
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "success": False,
        "error": "Internal server error",
        "path": request.url.path
    }

# ============ RUN SERVER ============
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload during development
    )