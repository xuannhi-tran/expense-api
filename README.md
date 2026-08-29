# Expense API

A RESTful API for managing personal expenses, built with Django REST Framework.

The API allows authenticated users to create, view, update, and delete their own expenses. It also supports searching, filtering, ordering, pagination, input validation, and automated testing.

## Features

- Token-based authentication
- Create expenses
- Retrieve expenses
- Update expenses with `PATCH` and `PUT`
- Delete expenses
- User-based expense ownership
- Search expenses by name
- Filter expenses by category
- Sort expenses by amount
- Pagination
- Input validation
- Automated API tests

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Token Authentication
- Django Test Framework
- Django REST Framework `APIClient`

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
├── manage.py
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd expense_api
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install django djangorestframework
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

The API uses Token Authentication.

Clients must include a valid token in the request header:

```text
Authorization: Token <your-token>
```

Example:

```text
Authorization: Token 29sf8fd...
```

Authenticated users can only access their own expenses.

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| `GET` | `/expenses/` | List user's expenses | Required |
| `POST` | `/expenses/` | Create an expense | Required |
| `GET` | `/expenses/<id>/` | Retrieve an expense | Required |
| `PATCH` | `/expenses/<id>/` | Partially update an expense | Required |
| `PUT` | `/expenses/<id>/` | Fully update an expense | Required |
| `DELETE` | `/expenses/<id>/` | Delete an expense | Required |

## Query Parameters

The expense list endpoint supports the following query parameters:

### Search

Search expenses by name:

```text
GET /expenses/?search=Pizza
```

### Filter

Filter expenses by category:

```text
GET /expenses/?category=Food
```

### Ordering

Sort expenses by amount:

```text
GET /expenses/?ordering=amount
```

For descending order:

```text
GET /expenses/?ordering=-amount
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
    "amount": 15.00,
    "category": "Food"
}
```

Example response:

```json
{
    "id": 1,
    "name": "Lunch",
    "amount": "15.00",
    "category": "Food"
}
```

## Validation

The API validates expense data before creating or updating an expense.

- Expense name cannot be empty.
- Expense amount must be greater than `0`.
- Expense category cannot be empty.

Invalid requests return:

```text
400 Bad Request
```

## User Ownership

Each expense is associated with a user.

Users can only access their own expenses.

For example:

```text
User A
├── Pizza
└── Bus

User B
└── Dinner
```

User A cannot retrieve, update, or delete User B's expenses.

If a user attempts to access another user's expense, the API returns:

```text
404 Not Found
```

## Testing

The project includes automated tests for the API.

Run the test suite with:

```bash
python manage.py test
```

The tests cover:

- Expense ownership
- Authentication
- Authorization
- Creating expenses
- Retrieving expenses
- Updating expenses
- Deleting expenses
- Input validation
- Search
- Category filtering
- Ascending ordering
- Descending ordering
- Pagination

## API Documentation

For detailed endpoint information, request examples, query parameters, validation rules, and response formats, see:

**[API Documentation](API_DOCUMENTATION.md)**

## Future Improvements

Possible future improvements include:

- User registration and login endpoints
- JWT authentication
- Expense statistics and summaries
- Date-based filtering
- Monthly spending reports
- Budget management
- Frontend interface
- Deployment to a cloud platform

## License

This project is for educational and portfolio purposes.