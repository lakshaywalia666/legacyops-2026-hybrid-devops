# API Contract

Base URL:

```text
http://localhost:8000
```

## Platform endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | API root |
| GET | `/health` | Liveness endpoint |
| GET | `/ready` | Readiness endpoint with database and Redis checks |
| GET | `/metrics` | Prometheus metrics |
| POST | `/admin/seed` | Create demo data |

## Business endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/dashboard` | Business dashboard numbers |
| GET | `/products` | List products |
| POST | `/products` | Create product |
| GET | `/customers` | List customers |
| POST | `/customers` | Create customer |
| GET | `/orders` | List orders |
| POST | `/orders` | Create order |
| GET | `/inventory/events` | List inventory audit events |

## Example product payload

```json
{
  "sku": "SKU-1001",
  "name": "Wireless Mouse",
  "category": "Electronics",
  "unit_price": 699.00,
  "stock_quantity": 50
}
```

## Example customer payload

```json
{
  "name": "Aman Sharma",
  "email": "aman@example.com",
  "phone": "9999999999",
  "address": "Delhi, India"
}
```

## Example order payload

```json
{
  "customer_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```
