import json
import time
from decimal import Decimal
from typing import List

import redis
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import Base, engine, get_db
from app import models, schemas

settings = get_settings()

REQUEST_COUNT = Counter(
    "legacyops_http_requests_total",
    "Total HTTP requests processed by LegacyOps backend",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "legacyops_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
)

ORDER_CREATED = Counter(
    "legacyops_orders_created_total",
    "Total orders created through the API",
)

QUEUE_FAILURES = Counter(
    "legacyops_queue_failures_total",
    "Total Redis queue publish failures",
)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Developer-provided workload for the LegacyOps 2026 DevOps modernization project.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    endpoint = request.url.path
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        http_status=response.status_code,
    ).inc()
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint,
    ).observe(duration)

    return response


def redis_client():
    return redis.Redis.from_url(settings.redis_url, decode_responses=True)


def enqueue_job(job_type: str, payload: dict) -> None:
    job = {
        "type": job_type,
        "payload": payload,
        "created_at": int(time.time()),
    }
    try:
        client = redis_client()
        client.lpush("legacyops:jobs", json.dumps(job))
    except Exception:
        QUEUE_FAILURES.inc()


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    dependencies = {
        "database": "unknown",
        "redis": "unknown",
    }

    try:
        db.execute(text("SELECT 1"))
        dependencies["database"] = "ok"
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "dependency": "database",
                "error": str(exc),
            },
        )

    try:
        redis_client().ping()
        dependencies["redis"] = "ok"
    except Exception as exc:
        dependencies["redis"] = f"degraded: {exc}"
        if settings.redis_required:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "status": "not_ready",
                    "dependency": "redis",
                    "error": str(exc),
                },
            )

    return {
        "status": "ready",
        "dependencies": dependencies,
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/dashboard", response_model=schemas.DashboardSummary)
def dashboard(db: Session = Depends(get_db)):
    total_revenue = db.query(func.coalesce(func.sum(models.Order.total_amount), 0)).scalar()
    return {
        "products": db.query(models.Product).count(),
        "customers": db.query(models.Customer).count(),
        "orders": db.query(models.Order).count(),
        "low_stock_products": db.query(models.Product).filter(models.Product.stock_quantity <= 5).count(),
        "total_revenue": float(total_revenue or 0),
        "pending_orders": db.query(models.Order).filter(models.Order.status == "created").count(),
    }


@app.post("/products", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = models.Product(
        sku=payload.sku,
        name=payload.name,
        category=payload.category,
        unit_price=Decimal(str(payload.unit_price)),
        stock_quantity=payload.stock_quantity,
    )
    db.add(product)
    try:
        db.flush()
        if payload.stock_quantity > 0:
            db.add(
                models.InventoryEvent(
                    product_id=product.id,
                    event_type="initial_stock",
                    quantity_delta=payload.stock_quantity,
                    reason="Initial product stock",
                )
            )
        db.commit()
        db.refresh(product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Product SKU already exists")

    return product


@app.get("/products", response_model=List[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id.desc()).all()


@app.post("/customers", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: schemas.CustomerCreate, db: Session = Depends(get_db)):
    customer = models.Customer(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        address=payload.address,
    )
    db.add(customer)
    try:
        db.commit()
        db.refresh(customer)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Customer email already exists")

    return customer


@app.get("/customers", response_model=List[schemas.CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    return db.query(models.Customer).order_by(models.Customer.id.desc()).all()


@app.post("/orders", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    product_ids = [item.product_id for item in payload.items]
    products = db.query(models.Product).filter(models.Product.id.in_(product_ids)).all()
    product_by_id = {product.id: product for product in products}

    total = Decimal("0.00")
    order_items = []

    for item in payload.items:
        product = product_by_id.get(item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if not product.is_active:
            raise HTTPException(status_code=400, detail=f"Product {product.sku} is inactive")
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.sku}. Available: {product.stock_quantity}",
            )

        unit_price = Decimal(str(product.unit_price))
        line_total = unit_price * item.quantity
        total += line_total

        order_items.append(
            {
                "product": product,
                "quantity": item.quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    order = models.Order(
        customer_id=payload.customer_id,
        status="created",
        total_amount=total,
    )
    db.add(order)
    db.flush()

    for item in order_items:
        product = item["product"]
        product.stock_quantity -= item["quantity"]

        db.add(
            models.OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                line_total=item["line_total"],
            )
        )
        db.add(
            models.InventoryEvent(
                product_id=product.id,
                event_type="order_reserved",
                quantity_delta=-item["quantity"],
                reason=f"Reserved for order #{order.id}",
            )
        )

    db.commit()
    db.refresh(order)

    ORDER_CREATED.inc()
    enqueue_job("order_created", {"order_id": order.id, "customer_id": order.customer_id})

    return order


@app.get("/orders", response_model=List[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).order_by(models.Order.id.desc()).all()


@app.get("/inventory/events", response_model=List[schemas.InventoryEventRead])
def list_inventory_events(db: Session = Depends(get_db)):
    return db.query(models.InventoryEvent).order_by(models.InventoryEvent.id.desc()).limit(100).all()


@app.post("/admin/seed")
def seed_demo_data(db: Session = Depends(get_db)):
    existing_products = db.query(models.Product).count()
    existing_customers = db.query(models.Customer).count()

    if existing_products == 0:
        demo_products = [
            models.Product(sku="SKU-1001", name="Wireless Mouse", category="Electronics", unit_price=699, stock_quantity=50),
            models.Product(sku="SKU-1002", name="Mechanical Keyboard", category="Electronics", unit_price=2499, stock_quantity=25),
            models.Product(sku="SKU-1003", name="USB-C Cable", category="Accessories", unit_price=299, stock_quantity=100),
            models.Product(sku="SKU-1004", name="Notebook Pack", category="Stationery", unit_price=199, stock_quantity=70),
        ]
        db.add_all(demo_products)
        db.flush()

        for product in demo_products:
            db.add(
                models.InventoryEvent(
                    product_id=product.id,
                    event_type="initial_stock",
                    quantity_delta=product.stock_quantity,
                    reason="Demo seed stock",
                )
            )

    if existing_customers == 0:
        db.add_all(
            [
                models.Customer(name="Aman Sharma", email="aman@example.com", phone="9999999991", address="Delhi, India"),
                models.Customer(name="Priya Verma", email="priya@example.com", phone="9999999992", address="Noida, India"),
                models.Customer(name="Rahul Mehta", email="rahul@example.com", phone="9999999993", address="Gurugram, India"),
            ]
        )

    db.commit()

    return {
        "status": "seed_complete",
        "products": db.query(models.Product).count(),
        "customers": db.query(models.Customer).count(),
    }
