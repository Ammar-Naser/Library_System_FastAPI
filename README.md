# 📚 Library System API

A simple and efficient **Library Management REST API** built with **FastAPI**, **SQLAlchemy**, **Pydantic**, and **SQLite**.

The project provides CRUD operations for **Authors** and **Books**, while maintaining a one-to-many relationship between them. It also includes automatic API documentation through FastAPI's built-in Swagger UI and ReDoc.

---

## Features

*  Manage books
*  Manage authors
*  One-to-Many relationship between Authors and Books
*  Create authors and books
*  Retrieve all authors and books
*  Retrieve a specific author or book by ID
*  Update author information
*  Delete authors and books
*  ISBN uniqueness validation
*  Proper HTTP error handling
*  Automatic API documentation with Swagger UI
*  SQLite database with SQLAlchemy ORM
*  Request and response validation using Pydantic

---

##  Technologies

| Technology     | Purpose                           |
| -------------- | --------------------------------- |
| **Python**     | Programming language              |
| **FastAPI**    | REST API framework                |
| **SQLAlchemy** | ORM and database interaction      |
| **Pydantic**   | Data validation and serialization |
| **SQLite**     | Database                          |
| **Uvicorn**    | ASGI server                       |

---

##  Project Structure

```text
Library_System_FastAPI/
│
├── main.py          # FastAPI application and API endpoints
├── database.py      # Database configuration and session management
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── library.db       # SQLite database
└── README.md        # Project documentation
```

---

##  Architecture

The project follows a simple layered structure:

```text
Client
   │
   ▼
FastAPI Application
   │
   ├── API Endpoints
   │
   ├── Pydantic Schemas
   │
   ▼
SQLAlchemy ORM
   │
   ▼
SQLite Database
```

### Database Relationship

An **Author** can have multiple **Books**, while each **Book** belongs to one **Author**.

```text
Author
  │
  │ 1
  │
  ├───────────────┐
  │               │
  ▼               ▼
Book            Book
  │
  ▼
...
```

The relationship is implemented using SQLAlchemy's `relationship()` and a foreign key from `books.author_id` to `authors.id`.

---

## 📊 Data Models

### Author

| Field   | Type              | Description                 |
| ------- | ----------------- | --------------------------- |
| `id`    | Integer           | Unique author ID            |
| `name`  | String            | Author name                 |
| `bio`   | String / Optional | Author biography            |
| `books` | List              | Books written by the author |

### Book

| Field              | Type    | Description             |
| ------------------ | ------- | ----------------------- |
| `id`               | Integer | Unique book ID          |
| `title`            | String  | Book title              |
| `isbn`             | String  | Unique ISBN             |
| `publication_year` | Integer | Year of publication     |
| `author_id`        | Integer | ID of the book's author |

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Ammar-Naser/Library_System_FastAPI.git
```

Then move into the project directory:

```bash
cd Library_System_FastAPI
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

##  API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to:

* Explore all available endpoints
* View request and response schemas
* Send requests directly from the browser
* Test CRUD operations

### ReDoc

You can also access the ReDoc documentation at:

```text
http://127.0.0.1:8000/redoc
```

---

#  API Endpoints

##  Authors

### Create an Author

```http
POST /authors/
```

Example request:

```json
{
  "name": "J. K. Rowling",
  "bio": "British author best known for the Harry Potter series."
}
```

Returns:

```json
{
  "id": 1,
  "name": "J. K. Rowling",
  "bio": "British author best known for the Harry Potter series.",
  "books": []
}
```

---

### Get All Authors

```http
GET /authors/
```

Optional pagination parameters:

```text
?skip=0&limit=100
```

Example:

```http
GET /authors/?skip=0&limit=10
```

---

### Get an Author by ID

```http
GET /authors/{author_id}
```

Example:

```http
GET /authors/1
```

---

### Update an Author

```http
PUT /authors/{author_id}
```

Example:

```json
{
  "name": "J. K. Rowling",
  "bio": "Updated biography."
}
```

Both `name` and `bio` are optional during an update.

---

### Delete an Author

```http
DELETE /authors/{author_id}
```

Example:

```http
DELETE /authors/1
```

Returns:

```text
204 No Content
```

---

# 📖 Books

### Create a Book for an Author

```http
POST /authors/{author_id}/books/
```

Example:

```http
POST /authors/1/books/
```

Request body:

```json
{
  "title": "Harry Potter and the Philosopher's Stone",
  "isbn": "9780747532699",
  "publication_year": 1997
}
```

The API verifies that the specified author exists before creating the book.

---

### Get All Books

```http
GET /books/
```

Optional pagination:

```text
?skip=0&limit=100
```

---

### Get a Book by ID

```http
GET /books/{book_id}
```

Example:

```http
GET /books/1
```

---

### Delete a Book

```http
DELETE /books/{book_id}
```

Example:

```http
DELETE /books/1
```

Returns:

```text
204 No Content
```

---

##  Validation & Error Handling

The API includes validation and appropriate HTTP status codes.

For example:

### Author Not Found

```http
404 Not Found
```

```json
{
  "detail": "Author not found"
}
```

### Book Not Found

```http
404 Not Found
```

```json
{
  "detail": "Book not found"
}
```

### Duplicate ISBN

Every book must have a unique ISBN.

If a book with the same ISBN already exists:

```http
400 Bad Request
```

```json
{
  "detail": "Book with this ISBN already exists"
}
```

---

## 🗄️ Database

The application uses **SQLite** as its database.

The database configuration is defined in `database.py`:

```text
sqlite:///./library.db
```

SQLAlchemy is responsible for:

* Database connection
* Session management
* ORM mapping
* Querying
* Creating database tables

The database tables are automatically created when the application starts.

---

##  Pydantic Schemas

The project separates database models from API schemas.

### Book Schemas

* `BookBase`
* `BookCreate`
* `BookResponse`

### Author Schemas

* `AuthorBase`
* `AuthorCreate`
* `AuthorUpdate`
* `AuthorResponse`

This separation helps control the data accepted by the API and the data returned to clients.

---

##  Example Workflow

A typical workflow can be:

### 1. Create an author

```http
POST /authors/
```

### 2. Create a book for that author

```http
POST /authors/1/books/
```

### 3. Retrieve the author

```http
GET /authors/1
```

The response includes the author's books:

```json
{
  "id": 1,
  "name": "J. K. Rowling",
  "bio": "British author.",
  "books": [
    {
      "id": 1,
      "title": "Harry Potter and the Philosopher's Stone",
      "isbn": "9780747532699",
      "publication_year": 1997,
      "author_id": 1
    }
  ]
}
```

---

##  Learning Objectives

This project demonstrates the fundamentals of building a backend REST API using FastAPI, including:

* FastAPI application development
* RESTful API design
* CRUD operations
* SQLAlchemy ORM
* SQLite database integration
* One-to-Many database relationships
* Pydantic data validation
* Dependency Injection with `Depends`
* HTTP status codes
* Exception handling
* Automatic OpenAPI documentation
* Basic pagination using `skip` and `limit`
