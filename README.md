# SwasthiQ Pharmacy Management API

A FastAPI-based REST API for managing pharmacy inventory and dashboard analytics.

## Features

### Dashboard
- Get today's sales summary (total sales, items sold, transactions)
- Get total items sold (all time)
- View low stock items
- Get purchase order summary (pending, delivered)

### Inventory Management
- List medicines with pagination
- Add new medicine to inventory
- Update medicine details
- Mark medicines as expired
- Mark medicines as out of stock
- Search medicines by name, description, or manufacturer
- Filter medicines by category
- Record sales transactions
- View inventory statistics
- Get list of medicine categories

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 10 or higher

## Installation

### 1. Clone/Extract the project

```bash
cd backend
```

### 2. Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root with your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/swasthiq_db
DEBUG=True
```

**Note:** Update the `username`, `password`, and database name according to your PostgreSQL setup.

### 5. Create PostgreSQL Database

```bash
# Using psql
createdb swasthiq_db
```

Or using PostgreSQL GUI tools like pgAdmin.

### 6. Seed Database with Dummy Data

```bash
python seed_data.py
```

This will populate the database with:
- 10 sample medicines
- Sample sales records for today
- Sample purchase orders

## Running the API

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py script
python app/main.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py        # SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py        # Pydantic schemas
│   ├── routes/
│   │   ├── dashboard.py       # Dashboard endpoints
│   │   ├── inventory.py       # Inventory endpoints
│   │   └── __init__.py
│   ├── main.py                # FastAPI application
│   └── __init__.py
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Example environment variables
├── requirements.txt           # Project dependencies
└── seed_data.py              # Script to seed dummy data
```

## API Endpoints

### Dashboard Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/sales-summary` | Get today's sales summary |
| GET | `/api/dashboard/total-items-sold` | Get total items sold |
| GET | `/api/dashboard/low-stock-items` | Get low stock items |
| GET | `/api/dashboard/purchase-order-summary` | Get purchase order summary |

### Inventory Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/inventory/medicines` | List all medicines (with pagination) |
| GET | `/api/inventory/medicines/{medicine_id}` | Get medicine details |
| POST | `/api/inventory/medicines` | Add new medicine |
| PUT | `/api/inventory/medicines/{medicine_id}` | Update medicine |
| PATCH | `/api/inventory/medicines/{medicine_id}/mark-expired` | Mark as expired |
| PATCH | `/api/inventory/medicines/{medicine_id}/mark-out-of-stock` | Mark as out of stock |
| GET | `/api/inventory/medicines/by/category/{category}` | Get medicines by category |
| GET | `/api/inventory/medicines/search/{search_term}` | Search medicines |
| POST | `/api/inventory/sales` | Record a sale |
| GET | `/api/inventory/categories` | Get all categories |
| GET | `/api/inventory/stats` | Get inventory statistics |

## Dummy Data

After seeding, the database contains:

### Medicines (10 items)
1. Paracetamol 500mg - Pain Relief
2. Ibuprofen 200mg - Pain Relief (Low stock)
3. Amoxicillin 500mg - Antibiotics
4. Metformin 500mg - Diabetes
5. Lisinopril 10mg - Cardiovascular
6. Atorvastatin 20mg - Cardiovascular (Low stock)
7. Vitamin D3 1000IU - Supplements
8. Levothyroxine 50mcg - Endocrine
9. Cetirizine 10mg - Allergy (Low stock)
10. Omeprazole 20mg - Gastro

### Sample Data
- 5 sales transactions for today
- 4 purchase orders (2 pending, 2 delivered)

## Database Schema

### Medicine Table
- `id` - Primary Key
- `name` - Medicine name
- `description` - Medicine description
- `price` - Price per unit
- `stock_quantity` - Current stock
- `reorder_level` - Low stock threshold
- `category` - Medicine category
- `manufacturer` - Manufacturer name
- `expiry_date` - Expiry date
- `is_active` - Active status (1=active, 0=inactive)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Sales Table
- `id` - Primary Key
- `medicine_id` - Foreign Key to Medicine
- `quantity_sold` - Quantity sold
- `sale_price` - Sale price per unit
- `sale_date` - Date of sale
- `created_at` - Creation timestamp

### PurchaseOrder Table
- `id` - Primary Key
- `medicine_id` - Foreign Key to Medicine
- `quantity_ordered` - Quantity ordered
- `order_date` - Order date
- `expected_delivery_date` - Expected delivery date
- `status` - Order status (pending/delivered/cancelled)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## Example API Calls

### Get Today's Sales Summary
```bash
curl http://localhost:8000/api/dashboard/sales-summary
```

### List All Medicines
```bash
curl "http://localhost:8000/api/inventory/medicines?skip=0&limit=10"
```

### Search Medicines
```bash
curl "http://localhost:8000/api/inventory/medicines/search/paracetamol"
```

### Add a New Medicine
```bash
curl -X POST http://localhost:8000/api/inventory/medicines \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin 100mg",
    "description": "Blood thinner",
    "price": 4.99,
    "stock_quantity": 500,
    "reorder_level": 100,
    "category": "Cardiovascular",
    "manufacturer": "PharmaCorp",
    "expiry_date": "2026-03-09T00:00:00"
  }'
```

### Record a Sale
```bash
curl -X POST http://localhost:8000/api/inventory/sales \
  -H "Content-Type: application/json" \
  -d '{
    "medicine_id": 1,
    "quantity_sold": 5,
    "sale_price": 5.99
  }'
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## Future Enhancements

- User authentication and authorization
- Advanced reporting and analytics
- Prescription management
- Customer management
- Inventory alerts and notifications
- Batch operations
- Export to CSV/Excel
- API rate limiting

## License

MIT License

## Support

For issues or questions, please contact the development team.
