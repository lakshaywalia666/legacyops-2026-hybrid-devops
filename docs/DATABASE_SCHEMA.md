# Database Schema

## products

Stores sellable products and current inventory count.

| Column | Type | Notes |
|---|---|---|
| id | integer | primary key |
| sku | string | unique |
| name | string | required |
| category | string | optional |
| unit_price | numeric | required |
| stock_quantity | integer | current stock |
| is_active | boolean | active/inactive |
| created_at | timestamp | created timestamp |
| updated_at | timestamp | updated timestamp |

## customers

Stores customer records.

| Column | Type | Notes |
|---|---|---|
| id | integer | primary key |
| name | string | required |
| email | string | unique, optional |
| phone | string | optional |
| address | text | optional |
| created_at | timestamp | created timestamp |

## orders

Stores order header records.

| Column | Type | Notes |
|---|---|---|
| id | integer | primary key |
| customer_id | integer | foreign key |
| status | string | default `created` |
| total_amount | numeric | calculated |
| created_at | timestamp | created timestamp |

## order_items

Stores order line items.

| Column | Type | Notes |
|---|---|---|
| id | integer | primary key |
| order_id | integer | foreign key |
| product_id | integer | foreign key |
| quantity | integer | required |
| unit_price | numeric | captured at order time |
| line_total | numeric | calculated |

## inventory_events

Audit table for inventory changes.

| Column | Type | Notes |
|---|---|---|
| id | integer | primary key |
| product_id | integer | foreign key |
| event_type | string | `initial_stock`, `order_reserved`, etc. |
| quantity_delta | integer | positive or negative |
| reason | text | human-readable reason |
| created_at | timestamp | created timestamp |
