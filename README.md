# # E-Commerce Backend API

A comprehensive e-commerce backend built with FastAPI, MySQL, and modern Python practices.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, authentication, profile management
- **Product Catalog**: CRUD operations, search, filtering, categories
- **Shopping Cart**: Add/remove items, quantity management
- **Order Processing**: Order creation, status tracking, history
- **Payment Processing**: Integration ready for Stripe/PayPal
- **Product Reviews**: Customer reviews and ratings system
- **Address Management**: Multiple shipping/billing addresses

### Technical Features
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy**: Powerful ORM with database migrations
- **JWT Authentication**: Secure token-based authentication
- **MySQL Database**: Reliable relational database with full ACID compliance
- **Pydantic Validation**: Request/response validation and serialization
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Admin Panel Ready**: Admin-only endpoints for management operations

## 📋 Requirements

- Python 3.8+
- MySQL 8.0+
- Redis (optional, for caching)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ecommerce-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Database
Create a MySQL database:
```sql
CREATE DATABASE ecommerce_db;
CREATE USER 'ecommerce_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'ecommerce_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Environment Configuration
Copy the example environment file and update with your settings:
```bash
cp .env.example .env
```

Edit `.env` with your database and other configuration:
```env
DATABASE_URL=mysql+pymysql://ecommerce_user:your_password@localhost:3306/ecommerce_db
SECRET_KEY=your-secret-key-generate-a-secure-one
STRIPE_SECRET_KEY=sk_test_your_stripe_key
# ... other settings
```

### 6. Run the Application
```bash
python run.py
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔐 Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register a new user: `POST /api/v1/auth/register`
2. Login to get access token: `POST /api/v1/auth/login`
3. Include the token in the Authorization header: `Authorization: Bearer <your-token>`

## 📊 Database Schema

The application implements a comprehensive e-commerce database schema with the following entities:

- **Users**: Customer accounts and authentication
- **Categories**: Hierarchical product categories
- **Products**: Product catalog with inventory management
- **Cart/CartItems**: Shopping cart functionality
- **Orders/OrderItems**: Order processing and history
- **Addresses**: Customer shipping and billing addresses
- **Payments**: Payment processing and tracking
- **Reviews**: Product reviews and ratings

## 🛣️ API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/test-token` - Validate token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile

### Products
- `GET /api/v1/products/` - List products (with filtering)
- `GET /api/v1/products/{id}` - Get product details
- `POST /api/v1/products/` - Create product (Admin)
- `PUT /api/v1/products/{id}` - Update product (Admin)
- `DELETE /api/v1/products/{id}` - Delete product (Admin)

### Categories
- `GET /api/v1/categories/` - List categories
- `POST /api/v1/categories/` - Create category (Admin)

### Shopping Cart
- `GET /api/v1/cart/` - Get user's cart
- `POST /api/v1/cart/items` - Add item to cart
- `PUT /api/v1/cart/items/{id}` - Update cart item
- `DELETE /api/v1/cart/items/{id}` - Remove cart item
- `DELETE /api/v1/cart/clear` - Clear cart

### Orders
- `GET /api/v1/orders/` - Get user's orders
- `POST /api/v1/orders/` - Create new order

### Addresses
- `GET /api/v1/addresses/` - Get user's addresses
- `POST /api/v1/addresses/` - Create new address

### Reviews
- `GET /api/v1/reviews/product/{id}` - Get product reviews
- `POST /api/v1/reviews/` - Create review

### Payments
- `POST /api/v1/payments/process` - Process payment

## 🏗️ Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py
│       │   ├── products.py
│       │   ├── cart.py
│       │   └── ...
│       └── api.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── models/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── ...
├── schemas/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── ...
└── main.py
```

## 🔧 Configuration

Key configuration options in `.env`:

- **Database**: Connection URL and credentials
- **Security**: JWT secret key and token expiration
- **Payment**: Stripe/PayPal API keys
- **Email**: SMTP settings for notifications
- **Storage**: AWS S3 configuration for file uploads

## 🚀 Deployment

### Docker
```bash
docker build -t ecommerce-api .
docker run -p 8000:8000 ecommerce-api
```

### Production Considerations
- Use a production ASGI server like Gunicorn with Uvicorn workers
- Set up SSL/TLS certificates
- Configure proper database backups
- Set up monitoring and logging
- Use environment-specific configuration

## 🧪 Testing

Run tests with pytest:
```bash
pytest
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the database schema in the ER diagram

---

**Built with ❤️ using FastAPI, SQLAlchemy, and MySQL**