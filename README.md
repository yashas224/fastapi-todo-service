# Todo Service (FastAPI)

A simple Todo Management API built with **FastAPI**, **SQLAlchemy**, and **SQLite/PostgreSQL** support.  
It provides authentication, user-specific todo operations, and admin-level controls.

## Key Functionality

- User signup and login with JWT token
- Get current user profile
- Change password (current + new password validation)
- Create, read, update, and delete personal todos
- Admin can view all users’ todos and delete any todo

## Product Demo
[View Product Demo](/product-demo.md)



## FastAPI Components Used

- **`FastAPI` App**: Main application setup and startup lifecycle
- **`APIRouter`**: Modular route structure (`auth`, `todos`, `user`, `admin`)
- **Dependency Injection (`Depends`)**:
  - Database session injection
  - Authenticated user injection via JWT
  - Admin role guard for admin routes
- **Pydantic Models**: Request/response validation (`CreateUserRequest`, `TodoRequest`, etc.)
- **Security**:
  - `OAuth2PasswordBearer`
  - Token endpoint (`/auth/token`)
  - JWT encode/decode for authorization
- **HTTP Exceptions & Status Codes**: Consistent API error handling

## Route Overview

- **Auth**: `/auth/`, `/auth/token`
- **User**: `/user/`, `/user/update/password`
- **Todos**: `/todos`, `/todos/{id}`
- **Admin**: `/admin/todos`, `/admin/todos/{id}`


## Run Locally

```bash
pip install -r requirements.txt
Run with SQLite
DB_CONFIG=SQLite fastapi run main.py

Run with local PostgreSQL  server
DB_CONFIG=PostgreSQL DB_PASSWORD=test1234  fastapi run main.py

```

## Testing

The project includes API tests using **pytest** and **FastAPI TestClient**.

- **Unit-style API tests** for route behavior and status codes
- **Integration-style tests** with a test database and dependency overrides
- Covers authentication, user APIs, todo CRUD, and admin operations

Run tests:

```bash
pytest -vv