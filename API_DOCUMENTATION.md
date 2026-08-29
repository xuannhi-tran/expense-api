# Expense API Documentation

## 1. Overview

This is an Expense Tracker API that allows authenticated users to manage their expenses.

The API supports creating, retrieving, updating, deleting, searching, filtering, ordering, and paginating expenses.

Each expense belongs to a specific user, and users can only access their own expenses.

---

## 2. Authentication

### Authentication Method

This API uses **TokenAuthentication**.

Clients must provide a valid authentication token when making requests to protected endpoints.

### Request Header

The token should be included in the request header as follows:

```text
Authorization: Token <your-token>
```

For example:

```text
Authorization: Token 29sf8fd...
```

If a client sends a request without valid authentication, the API returns:

```text
401 Unauthorized
```

---

## 3. Expense Endpoints

### 3.1 List Expenses

**Method:** `GET`

**Endpoint:** `/expenses/`

**Description:**

This endpoint allows an authenticated user to retrieve a paginated list of their expenses.

**Authentication:** Required

### Query Parameters

| Parameter  | Type    | Description                         |
| ---------- | ------- | ----------------------------------- |
| `category` | string  | Filter expenses by category         |
| `search`   | string  | Search expenses by name             |
| `ordering` | string  | Order expenses by a specified field |
| `page`     | integer | Retrieve a specific page of results |

### Example Request

```text
GET /expenses/
```

### Successful Response

**Status Code:** `200 OK`

Example response:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Bus",
      "amount": "5.00",
      "category": "Transport"
    },
    {
      "id": 2,
      "name": "Pizza",
      "amount": "10.00",
      "category": "Food"
    }
  ]
}
```

---

### 3.2 Create Expense

**Method:** `POST`

**Endpoint:** `/expenses/`

**Description:**

This endpoint allows an authenticated user to create a new expense.

The user is automatically assigned to the expense based on the authenticated user. The client does not need to provide a `user` field.

**Authentication:** Required

### Request Body

```json
{
  "name": "Lunch",
  "amount": 15.0,
  "category": "Food"
}
```

### Successful Response

**Status Code:** `201 Created`

Example response:

```json
{
  "id": 3,
  "name": "Lunch",
  "amount": "15.00",
  "category": "Food"
}
```

---

### 3.3 Retrieve Expense

**Method:** `GET`

**Endpoint:** `/expenses/<id>/`

**Description:**

This endpoint allows an authenticated user to retrieve a specific expense.

The expense must belong to the authenticated user.

**Authentication:** Required

### Example Request

```text
GET /expenses/1/
```

### Successful Response

**Status Code:** `200 OK`

Example response:

```json
{
  "id": 1,
  "name": "Pizza",
  "amount": "10.00",
  "category": "Food"
}
```

If the expense does not exist or does not belong to the authenticated user, the API returns:

```text
404 Not Found
```

---

### 3.4 Partially Update Expense

**Method:** `PATCH`

**Endpoint:** `/expenses/<id>/`

**Description:**

This endpoint allows an authenticated user to partially update an existing expense.

Only the fields that need to be changed are required.

**Authentication:** Required

### Example Request

```text
PATCH /expenses/1/
```

### Request Body

```json
{
  "name": "Updated Pizza"
}
```

### Successful Response

**Status Code:** `200 OK`

Example response:

```json
{
  "id": 1,
  "name": "Updated Pizza",
  "amount": "10.00",
  "category": "Food"
}
```

---

### 3.5 Fully Update Expense

**Method:** `PUT`

**Endpoint:** `/expenses/<id>/`

**Description:**

This endpoint allows an authenticated user to fully update an existing expense.

All required fields should be provided.

**Authentication:** Required

### Example Request

```text
PUT /expenses/1/
```

### Request Body

```json
{
  "name": "Updated Pizza",
  "amount": 20.0,
  "category": "Food"
}
```

### Successful Response

**Status Code:** `200 OK`

Example response:

```json
{
  "id": 1,
  "name": "Updated Pizza",
  "amount": "20.00",
  "category": "Food"
}
```

---

### 3.6 Delete Expense

**Method:** `DELETE`

**Endpoint:** `/expenses/<id>/`

**Description:**

This endpoint allows an authenticated user to delete their own expense.

The expense must belong to the authenticated user.

**Authentication:** Required

### Example Request

```text
DELETE /expenses/1/
```

### Successful Response

**Status Code:** `204 No Content`

The API does not return a response body after a successful deletion.

If the expense does not exist or does not belong to the authenticated user, the API returns:

```text
404 Not Found
```

---

## 4. Query Parameters

### 4.1 Search

**Parameter:** `search`

The `search` parameter searches expenses by name using a case-insensitive partial match.

### Example

```text
GET /expenses/?search=Pizza
```

For example, this search may match:

```text
Pizza
Pizza Dinner
Chicken Pizza
```

---

### 4.2 Filter by Category

**Parameter:** `category`

The `category` parameter filters expenses by their category.

### Example

```text
GET /expenses/?category=Food
```

Only expenses with the `Food` category are returned.

---

### 4.3 Ordering

**Parameter:** `ordering`

The `ordering` parameter sorts expenses by a specified field.

#### Ascending Order

```text
GET /expenses/?ordering=amount
```

Example result:

```text
5.00
10.00
20.00
```

#### Descending Order

```text
GET /expenses/?ordering=-amount
```

Example result:

```text
20.00
10.00
5.00
```

---

### 4.4 Pagination

The API uses page-number pagination with a page size of **10 expenses per page**.

**Parameter:** `page`

### Example

```text
GET /expenses/?page=2
```

### Response Structure

```json
{
  "count": 13,
  "next": "/expenses/?page=2",
  "previous": null,
  "results": []
}
```

The pagination response contains the following fields:

| Field      | Description                                                       |
| ---------- | ----------------------------------------------------------------- |
| `count`    | Total number of expenses                                          |
| `next`     | URL for the next page, or `null` if there is no next page         |
| `previous` | URL for the previous page, or `null` if there is no previous page |
| `results`  | Expenses returned on the current page                             |

---

## 5. Validation

The API validates expense data before creating or updating an expense.

| Field      | Validation Rule        |
| ---------- | ---------------------- |
| `name`     | Cannot be empty        |
| `amount`   | Must be greater than 0 |
| `category` | Cannot be empty        |

### Example: Invalid Amount

**Request:**

```json
{
  "name": "Invalid",
  "amount": -10,
  "category": "Food"
}
```

**Response Status:**

```text
400 Bad Request
```

Example response:

```json
{
  "amount": ["Amount must be greater than 0."]
}
```

### Example: Empty Name

```json
{
  "name": "",
  "amount": 10,
  "category": "Food"
}
```

The API returns:

```text
400 Bad Request
```

### Example: Empty Category

```json
{
  "name": "Lunch",
  "amount": 10,
  "category": ""
}
```

The API returns:

```text
400 Bad Request
```

---

## 6. Authorization and Ownership

Each expense belongs to a specific user.

Users can only view, update, and delete their own expenses.

For example:

```text
User A
├── Pizza
└── Bus

User B
└── Dinner
```

User A can access:

- Pizza
- Bus

User A cannot access User B's Dinner expense.

If User A attempts to retrieve, update, or delete User B's expense, the API returns:

```text
404 Not Found
```

This ownership restriction is enforced by filtering expenses using the authenticated user.

---

## 7. HTTP Status Codes

| Status Code | Meaning      | Usage                                                               |
| ----------- | ------------ | ------------------------------------------------------------------- |
| `200`       | OK           | Successful GET, PATCH, or PUT request                               |
| `201`       | Created      | Expense successfully created                                        |
| `204`       | No Content   | Expense successfully deleted                                        |
| `400`       | Bad Request  | Invalid request data                                                |
| `401`       | Unauthorized | Authentication is required or invalid                               |
| `404`       | Not Found    | Expense does not exist or does not belong to the authenticated user |

---

## 8. Testing

The API is tested using Django's testing framework and Django REST Framework's `APIClient`.

### Test Command

```text
python manage.py test
```

### Test Coverage

The test suite covers:

- Authentication
- Expense ownership
- User authorization
- GET requests
- POST requests
- PATCH requests
- PUT requests
- DELETE requests
- Input validation
- Empty expense names
- Empty categories
- Search
- Category filtering
- Ascending ordering
- Descending ordering
- Pagination
- Access protection between different users

All implemented tests should pass before the API is considered ready for the next stage of development.
