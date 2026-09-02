# Expense API

A RESTful API for managing personal expenses, built with Django REST Framework.

The API provides authenticated, user-scoped expense management with search, filtering, ordering, pagination, validation, timestamps, and automated testing.

It serves as the backend for the Expense Tracker frontend application.

## Live API

Base URL:

https://expense-api-1p6n.onrender.com

Admin:

https://expense-api-1p6n.onrender.com/admin/

> The service is hosted on Render and may take a short time to wake up after periods of inactivity.

## Frontend

Live application:

https://expense-frontend-tau-eight.vercel.app/

Frontend repository:

https://github.com/xuannhi-tran/expense-frontend

## Features

- Token-based authentication
- User registration
- Create, retrieve, update, and delete expenses
- User-specific data ownership
- Search expenses by name
- Filter expenses by category
- Ordering
- Pagination
- Created and updated timestamps
- Input validation
- Automated API tests
- PostgreSQL production database

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- SQLite for local development
- DRF Token Authentication
- Gunicorn
- Render
- Django Test Framework
- Django REST Framework `APIClient`

## Expense Model

Each expense contains:

```text
id
name
amount
category
user
created_at
updated_at
```

Expenses are ordered by newest creation time by default.

`created_at` records when an expense was originally created, while `updated_at` records the most recent modification.

## Project Structure

```text
expense_api/
├── expense_api/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── expenses/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── admin.py
│
├── API_DOCUMENTATION.md
├── build.sh
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/xuannhi-tran/expense-api.git
cd expense-api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

## Authentication

The API uses Django REST Framework Token Authentication.

Authenticated requests must include:

```text
Authorization: Token <your-token>
```

Users can only access and modify their own expense records.

## API Endpoints

| Method   | Endpoint           | Description                    | Authentication |
| -------- | ------------------ | ------------------------------ | -------------- |
| `POST`   | `/register/`       | Register a new user            | No             |
| `POST`   | `/api-token-auth/` | Obtain an authentication token | No             |
| `GET`    | `/expenses/`       | List user's expenses           | Required       |
| `POST`   | `/expenses/`       | Create an expense              | Required       |
| `GET`    | `/expenses/<id>/`  | Retrieve an expense            | Required       |
| `PATCH`  | `/expenses/<id>/`  | Partially update an expense    | Required       |
| `PUT`    | `/expenses/<id>/`  | Fully update an expense        | Required       |
| `DELETE` | `/expenses/<id>/`  | Delete an expense              | Required       |

## Query Parameters

### Search

```text
GET /expenses/?search=Pizza
```

### Category Filter

```text
GET /expenses/?category=Food
```

### Ordering

```text
GET /expenses/?ordering=amount
GET /expenses/?ordering=-amount
GET /expenses/?ordering=created_at
GET /expenses/?ordering=-created_at
```

### Pagination

The API returns 10 expenses per page.

```text
GET /expenses/?page=2
```

## Example Request

### Create an Expense

```http
POST /expenses/
Authorization: Token <your-token>
Content-Type: application/json
```

Request body:

```json
{
  "name": "Lunch",
  "amount": 15.0,
  "category": "Food"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Lunch",
  "amount": "15.00",
  "category": "Food",
  "created_at": "2026-09-03T00:21:15.123456Z",
  "updated_at": "2026-09-03T00:21:15.123456Z"
}
```

## Validation

The API validates expense data before creation or modification.

- Expense name cannot be empty
- Expense amount must be greater than `0`
- Expense category cannot be empty

Invalid input returns:

```text
400 Bad Request
```

## User Ownership

Each expense belongs to the authenticated user who created it.

Ownership is enforced at the query level, meaning users cannot retrieve, edit, or delete another user's expenses.

Attempts to access another user's record return:

```text
404 Not Found
```

## Pagination and Analytics

The expense list endpoint is paginated with 10 records per page.

The frontend separately retrieves the complete expense dataset when calculating dashboard-wide analytics, ensuring that metrics such as total spending and category breakdown are not limited to the current transaction page.

## Testing

Run the test suite with:

```bash
python manage.py test
```

Tests cover:

- Authentication
- User ownership
- Authorization
- Creating expenses
- Retrieving expenses
- Updating expenses
- Deleting expenses
- Validation
- Search
- Category filtering
- Ordering
- Pagination

## Deployment

The API is deployed on Render using:

- Gunicorn as the production WSGI server
- PostgreSQL as the production database
- Environment variables for sensitive configuration
- `build.sh` for dependency installation and database migrations

## API Documentation

For detailed endpoint information, request examples, query parameters, validation rules, and response formats, see:

**[API Documentation](API_DOCUMENTATION.md)**

## Future Improvements

Potential improvements include:

- Dedicated analytics and summary endpoints
- Date-range filtering
- Monthly and yearly aggregation endpoints
- Budget management
- JWT authentication
- Improved API documentation with OpenAPI / Swagger
- Increased automated test coverage

## License

This project is for educational and portfolio purposes.
