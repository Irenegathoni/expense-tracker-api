# Personal Expense Tracker API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A secure, production-ready REST API for personal financial management. Track expenses, set budgets, and gain insights into your spending habits.



---

## Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [Security](#-security)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## Overview

**Personal Expense Tracker API** is a backend solution designed to help individuals take control of their finances. Built with modern Python technologies, it provides a robust, secure, and scalable platform for tracking expenses, managing budgets, and analyzing spending patterns.

### The Problem

- **78%** of people don't know where their money goes
- Manual expense tracking is time-consuming and error-prone
- No warning system when approaching budget limits
- Financial data privacy concerns with third-party apps

### The Solution

A self-hosted API that puts YOU in control of your financial data with:

- Real-time expense tracking
- Automated budget monitoring
- Spending analytics (daily/weekly/monthly)
- Bank-grade security
- Complete data ownership

---

## Key Features

### Authentication & Security

- **JWT-based authentication** - Secure, stateless sessions
- **Password encryption** - Bcrypt hashing with salt
- **Token expiration** - Automatic session timeout (configurable)
- **User isolation** - Complete data privacy between users

### Expense Management

- **Full CRUD operations** - Create, read, update, delete expenses
- **Categorization** - Organize expenses by category
- **Date tracking** - Historical record of all transactions
- **Quick summaries** - Daily, weekly, and monthly totals
- **Search & filter** - Find expenses easily (coming soon)

### Budget Planning

- **Category budgets** - Set spending limits per category
- **Real-time tracking** - Monitor spending vs. budget
- **Over-budget alerts** - Automatic warning flags
- **Budget comparison** - See remaining allowance instantly

### Analytics (Coming Soon)

- Spending trends visualization
- Category breakdown charts
- Month-over-month comparisons
- Savings goals tracking

---

## Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | High-performance async API framework |
| **Database** | [PostgreSQL](https://www.postgresql.org/) | Reliable relational database |
| **Authentication** | [JWT](https://jwt.io/) + [Bcrypt](https://github.com/pyca/bcrypt/) | Secure user authentication |
| **Validation** | [Pydantic](https://docs.pydantic.dev/) | Data validation & serialization |
| **Containerization** | [Docker](https://www.docker.com/) | Easy deployment & scalability |
| **API Docs** | [Swagger UI](https://swagger.io/tools/swagger-ui/) | Interactive API documentation |

**Why these choices?**

- **FastAPI**: One of the fastest Python frameworks, auto-generates docs
- **PostgreSQL**: ACID compliance, handles relationships well
- **JWT**: Industry standard for stateless auth
- **Docker**: Deploy anywhere, consistent environments

---

## Quick Start

Get up and running in under 5 minutes with Docker:

```bash
# Clone the repository
git clone https://github.com/Irenegathoni/expense-tracker-api.git
cd expense-tracker-api

# Start with Docker Compose
docker-compose up -d

# API is now running at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

That's it! The database is automatically initialized with tables.

---

## Installation

### Prerequisites

- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 15+** ([Download](https://www.postgresql.org/download/))
- **Docker** (optional, recommended) ([Download](https://www.docker.com/get-started))

### Option 1: Docker Deployment (Recommended)

**1. Clone the repository:**

```bash
git clone https://github.com/Irenegathoni/expense-tracker-api.git
cd expense-tracker-api
```

**2. Configure environment (optional):**

```bash
# Edit docker-compose.yml to change passwords/secrets
nano docker-compose.yml
```

**3. Start the containers:**

```bash
docker-compose up --build -d
```

**4. Verify it's running:**

```bash
docker-compose ps
# Should show both 'api' and 'db' containers running

# Check logs
docker-compose logs -f api
```

**5. Access the API:**

- **API Base URL:**<http://localhost:8000>
- **Interactive Docs:** <http://localhost:8000/docs>
- **Alternative Docs:** <http://localhost:8000/redoc>

### Option 2: Manual Setup

**1. Clone and navigate:**

```bash
git clone https://github.com/Irenegathoni/expense-tracker-api.git
cd expense-tracker-api
```

**2. Create virtual environment:**

```bash

python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

**4. Set up database:**

```bash
# Create PostgreSQL database
createdb expense_tracker

# Run initialization script
psql -d expense_tracker -f init.sql
```

**5. Configure environment:**

```bash
# Create .env file
cp .env.example .env

# Edit with your values
nano .env
```

**6. Run the application:**

```bash
uvicorn main2:app --reload
```

**7. Access athttp://localhost:8000/docs**

---

## API Documentation

### Interactive Documentation

Once running, visit:

- **Swagger UI:**<http://localhost:8000/docs> (Try-it-now interface)
- **ReDoc:** <http://localhost:8000/redoc> (Clean documentation)

### Quick API Reference

#### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/auth/register` | Create new user account | wrong|
| `POST` | `/auth/login` | Login and receive JWT token | wrong |
| `GET` | `/auth/me` | Get current user info |right |

#### Expense Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/expenses` | Create new expense | |
| `GET` | `/expenses` | Get all user expenses |  |
| `GET` | `/expenses/{id}` | Get specific expense |  |
| `PUT` | `/expenses/{id}` | Update expense |  |
| `DELETE` | `/expenses/{id}` | Delete expense | |
| `GET` | `/expenses/total` | Get total expenses |  |
| `GET` | `/expenses/summary/today` | Today's total |  |
| `GET` | `/expenses/summary/weekly` | Last 7 days total | |
| `GET` | `/expenses/summary/monthly` | Current month total | |

#### Budget Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/budgets` | Create budget |  |
| `GET` | `/budgets` | Get all budgets |  |
| `GET` | `/budgets/status` | Budget vs. actual |  |
| `PUT` | `/budgets/{id}` | Update budget |  |
| `DELETE` | `/budgets/{id}` | Delete budget | |

---

## Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Njogu",
    "email": "njogu@gmail.com",
    "password": "Testing1!"
  }'
```

**Response:**

```json
{
  "message": "User registered successfully!",
  "user": {
    "id": 1,
    "name": "Njogu",
    "email": "njogu@gmail.com"
  }
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "njogu@gmail.com",
    "password": "Testing1!"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Njogu",
    "email": "njogu@gmail.com"
  }
}
```

### 3. Create an Expense

```bash
curl -X POST "http://localhost:8000/expenses" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Grocery Shopping",
    "amount": 85.50,
    "category": "Food",
    "date": "18-11-2025"
  }'
```

### 4. Set a Budget

```bash
curl -X POST "http://localhost:8000/budgets" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Food",
    "monthly_limit": 500.00
  }'
```

### 5. Check Budget Status

```bash
curl -X GET "http://localhost:8000/budgets/status" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Response:**

```json
[
  {
    "category": "Food",
    "limit": 500.00,
    "spent": 345.50,
    "remaining": 154.50,
    "over_budget": false
  }
]
```

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "name": "Njogu",
    "email": "njogu@gmail.com",
    "password": "Testing1!"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "njogu@gmail.com",
    "password": "Testing1!"
})
token = response.json()["access_token"]

# Create expense
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/expenses", headers=headers, json={
    "description": "Coffee",
    "amount": 4.50,
    "category": "Food",
    "date": "18-11-2025"
})
print(response.json())
```

---

## Architecture

### Project Structure

```bash
expense-tracker-api/
├── main2.py                    # Application entry point
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Python dependencies
├── init.sql                    # Database initialization
├── .env.example               # Environment variables template
├── .dockerignore              # Docker ignore file
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── LICENSE                    # MIT License
│
├── database/
│   ├── __init__.py
│   └── connection.py          # Database connection manager
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication endpoints
│   ├── expenses.py            # Expense CRUD operations
│   └── budgets.py             # Budget management
│
├── schemas/
│   ├── __init__.py
│   ├── user.py                # User validation models
│   ├── expense.py             # Expense validation models
│   └── budget.py              # Budget validation models
│
└── tests/                     # Unit and integration tests (coming soon)
    ├── __init__.py
    ├── test_auth.py
    ├── test_expenses.py
    └── test_budgets.py
```

### Database Schema

```sql
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │──┐
│ name            │  │
│ email (UNIQUE)  │  │
│ hashed_password │  │
│ created_at      │  │
└─────────────────┘  │
                     │ One-to-Many
                     │
    ┌────────────────┴─────────────────┐
    │                                  │
┌───▼──────────┐              ┌───────▼────────┐
│   EXPENSES   │              │    BUDGETS     │
├──────────────┤              ├────────────────┤
│ id (PK)      │              │ id (PK)        │
│ user_id (FK) │              │ user_id (FK)   │
│ description  │              │ category       │
│ amount       │              │ monthly_limit  │
│ category     │              │ created_at     │
│ date         │              └────────────────┘
│ created_at   │
└──────────────┘
```

### Request Flow

```bash
Client Request
     │
     ▼
┌─────────────────┐
│   FastAPI App   │
│   (main2.py)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Router        │
│ (auth/expenses/ │
│   budgets)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │
│  (Pydantic)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Auth Check     │
│ (JWT Verify)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Database       │
│  (PostgreSQL)   │
└────────┬────────┘
         │
         ▼
    JSON Response
```

---

## Security

### Authentication Flow

1. **User Registration:**
   - Password hashed with Bcrypt + random salt
   - Stored in database (never plain text)

2. **User Login:**
   - Verify password against hash
   - Generate JWT token with user_id and expiration
   - Return token to client

3. **Protected Requests:**
   - Client sends: `Authorization: Bearer <token>`
   - Server verifies token signature
   - Extracts user_id from token
   - Proceeds with request

### Security Measure **Password Security**

- Bcrypt hashing with salt
- Minimum 6 characters required
- Must contain letters and numbers

  **Authentication**

- JWT tokens with HS256 algorithm
- 30-minute expiration (configurable)
- Stateless (no server-side session storage)

   **Authorization**

- User data isolation
- Ownership verification on updates/deletes
- Cannot access other users' data

  **Input Validation**

- Pydantic schemas validate all inputs
- SQL injection prevention (parameterized queries)
- Email format validation
- Positive amount validation

   **Error Handling**

- Generic error messages (no data leakage)
- Proper HTTP status codes
- Logging without sensitive data

### Environment Variables

**Never commit sensitive data!** Use environment variables:

```bash
# .env (add to .gitignore!)
PGHOST=localhost
PGDATABASE=expense_tracker
PGUSER=your_user
PGPASSWORD=your_password
SECRET_KEY=your-long-random-secret-key
```

---

## Testing

### Manual Testing with Swagger UI

1. Navigate to <http://localhost:8000/docs>
2. Click "Authorize" button ()
3. Register a user
4. Login to get token
5. Paste token in authorization dialog
6. Test all endpoints

### Automated Testing (Coming Soon)

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test file
pytest tests/test_auth.py -v
```

### Test Scenarios

- User registration with valid data
- User registration with duplicate email (should fail)
- Login with correct credentials
- Login with wrong password (should fail)
- Access protected route without token (should fail)
- Access protected route with expired token (should fail)
- Create expense with valid data
- Create expense with negative amount (should fail)
- User A cannot delete User B's expense
- Budget status calculations accuracy

---

## Deployment

### Deploy to Production

#### Option 1: Docker Compose (Recommended)

1. **Update environment variables in docker-compose.yml**
2. **Deploy:**

```bash
   docker-compose up -d --build
   ```

#### Option 2: Cloud Platforms

**Deploy to Heroku:**

```bash
heroku create expense-tracker-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

**Deploy to AWS ECS:**

```bash
# Build and push Docker image
docker build -t expense-tracker-api .
docker tag expense-tracker-api:latest YOUR_ECR_REPO
docker push YOUR_ECR_REPO

# Deploy with ECS
# (Follow AWS ECS deployment guide)
```

**Deploy to DigitalOcean App Platform:**

1. Connect GitHub repository
2. Select Dockerfile deployment
3. Add environment variables
4. Deploy

### Production Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Use production database (not SQLite)
- [ ] Enable HTTPS/SSL
- [ ] Set up database backups
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring/logging
- [ ] Use environment-specific configs
- [ ] Add health check endpoint
- [ ] Set appropriate token expiration

---

## Roadmap

### Version 1.0 (Current)

- [] User authentication (register/login)
- [] JWT token-based auth
- [] Expense CRUD operations
- [] Budget management
- [] Daily/weekly/monthly summaries
- [] Budget vs. actual comparison
- [] Docker deployment
- [] API documentation

### Version 1.1 (In Progress)

- [ ] Unit and integration tests
- [ ] Income tracking
- [ ] Expense categories API
- [ ] Date range filtering
- [ ] Pagination for expense list
- [ ] User profile updates
- [ ] Password reset functionality

### Version 2.0 (Planned)

- [ ] Recurring expenses/income
- [ ] Savings goals tracking
- [ ] Multi-currency support
- [ ] Export to CSV/PDF
- [ ] Budget notifications via email
- [ ] Analytics dashboard API
- [ ] Receipt image uploads
- [ ] Shared budgets (family accounts)

### Version 3.0 (Future)

- [ ] React/Vue frontend
- [ ] Mobile app (React Native)
- [ ] Data visualization charts
- [ ] AI-powered spending insights
- [ ] Bank account integration
- [ ] Financial advice recommendations

---

## Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

**Fork the repository**
**Create a feature branch:**

```bash
   git checkout -b feature/amazing-feature
   ```

**Make your changes**
**Commit with clear messages:**

```bash
   git commit -m "Add: Income tracking feature"
   ```

**Push to your fork:**

```bash
   git push origin feature/amazing-feature
   ```

1. **Open a Pull Request**

### Contribution Guidelines

- Follow existing code style (PEP 8 for Python)
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described
- Be respectful in discussions

### Development Setup

```bash
# Clone your fork
git clone https://github.com/Irenegathoni/expense-tracker-api.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
uvicorn main2:app --reload
```

### Reporting Issues

Found a bug? Have a feature request?

1. Check [existing issues](../../issues)
2. If none exist, [create a new issue](../../issues/new)
3. Provide:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Environment details (OS, Python version, etc.)

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```bash
MIT License

Copyright (c) 2025 [Gathoni Njogu]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## Contact

## Gathoni Njogu

- LinkedIn: [linkedin.com/in/Irene Njogu](https://www.linkedin.com/in/irene-njogu-661a4b298/)
- GitHub: [@Irenegathoni](https://github.com/Irenegathoni)
- Email: <irenegnjogu003@gmail.com>

**Project Link:** [https://github.com/Irenegathoni/expense-tracker-api](https://github.com/Irenegathoni/expense-tracker-api)

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Amazing framework by Sebastián Ramírez
- [PostgreSQL](https://www.postgresql.org/) - Powerful open-source database
- [Pydantic](https://docs.pydantic.dev/) - Data validation made easy
- [Docker](https://www.docker.com/) - Containerization platform
- Inspiration from personal financial struggles

---

## Project Stats

![GitHub stars](https://img.shields.io/github/stars/Irenegathoni/expense-tracker-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/Irenegathoni/expense-tracker-api?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Irenegathoni/expense-tracker-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/Irenegathoni/expense-tracker-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Irenegathoni/expense-tracker-api)

---
