# 🚀 Quick Setup Guide

## Option 1: Docker Compose (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Clone and navigate to the project
git clone <your-repo>
cd ecommerce-backend

# Start all services (MySQL, Redis, API, phpMyAdmin)
docker-compose up -d

# View logs
docker-compose logs -f api
```

**Services will be available at:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- phpMyAdmin: http://localhost:8080
- MySQL: localhost:3306
- Redis: localhost:6379

## Option 2: Local Development

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Virtual environment

### Setup Steps

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up MySQL database:**
   ```sql
   CREATE DATABASE ecommerce_db;
   CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

## 📝 Testing the API

### 1. Register a new user
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login to get access token
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

### 3. Create admin user (directly in database)
```sql
UPDATE users SET is_admin = 1 WHERE email = 'test@example.com';
```

### 4. Create a category (as admin)
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics",
    "description": "Electronic devices and gadgets"
  }'
```

### 5. Create a product (as admin)
```bash
curl -X POST "http://localhost:8000/api/v1/products/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smartphone",
    "description": "Latest smartphone with great features",
    "price": 599.99,
    "stock_quantity": 100,
    "category_id": 1,
    "sku": "PHONE001"
  }'
```

### 6. Add product to cart
```bash
curl -X POST "http://localhost:8000/api/v1/cart/items" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

## 🔍 Explore the API

Visit http://localhost:8000/docs to explore all available endpoints using the interactive Swagger UI.

## 🛠️ Development

- **Database changes**: Modify models and use Alembic for migrations
- **New endpoints**: Add routes in `app/api/v1/endpoints/`
- **Business logic**: Extend models with new methods and properties
- **Testing**: Add tests in the `tests/` directory

## 📊 Database Access

- **phpMyAdmin**: http://localhost:8080 (user: ecommerce_user, password: ecommerce_password)
- **Direct MySQL**: `mysql -h localhost -u ecommerce_user -p ecommerce_db`

## 🔒 Security Notes

- Change default passwords in production
- Use strong SECRET_KEY for JWT tokens
- Enable HTTPS in production
- Regular security updates for dependencies