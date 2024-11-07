# python-clean-arch

This is a study project aimed at understanding how to apply Domain-Driven Design (DDD) and Clean Architecture principles in a Python project using FastAPI.

## Project Overview

The goal of this project is to explore and implement DDD concepts and the Clean Architecture pattern in a FastAPI application. The focus will be on organizing the code to promote scalability, maintainability, and ease of testing.

## Features

- FastAPI for building the web API
- Domain-Driven Design (DDD) concepts
- Clean Architecture for code structure
- Dependency injection
- Separation of concerns between different layers (domain, application, infrastructure, etc.)
- Unit tests for each layer

## Folder Structure

```plaintext
python-clean-arch/
├── docs/              # Ready API documentation to use with [Bruno]
├── src/               # Application code
│   ├── app/           # Presentation layer (e.g., HTTP routes, data transfer objects)
│   ├── domain/        # Domain business logic (domain and application layers)
│   ├── infra/         # Infrastructure layer (e.g., database, external services)
│   └── tests/         # Unit tests
│
├── requirements.txt   # Python dependencies
└── README.md          # Base project documentation
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vctrlima/python-clean-arch.git
cd python-clean-arch
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI application:

```bash
uvicorn src.__main__:api --reload
```

## Database Configuration

To run the application with SQLAlchemy, you need to configure a database connection. The application uses PostgreSQL, and the connection string is defined in the `.env` file under the `DATABASE_URL` variable. 

### Setting Up the `.env` File

Create a `.env` file in the root of your project with the following content:

```plaintext
DATABASE_URL=postgresql+asyncpg://<username>:<password>@<host>:<port>/<database_name>
```

Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your PostgreSQL credentials. Here is an example configuration:

```plaintext
DATABASE_URL=postgresql+asyncpg://postgres:admin@localhost:5432/python-clean-arch
```

In this example:
- `postgres` is the username.
- `admin` is the password.
- `localhost` is the host.
- `5432` is the port.
- `python-clean-arch` is the database name.

### Creating the database

Ensure that the PostgreSQL database specified in `DATABASE_URL` exists before running the application. You can create it manually with the following commands:

1. Open a PostgreSQL shell or a database client.
2. Run the following commands to create the database:

   ```sql
   CREATE DATABASE python-clean-arch;
   ```

Once the database is configured, you should be able to run the application as described in the installation steps.

## Learning Objectives

- Apply DDD principles such as value objects, aggregates, and repositories.
- Structure the project using Clean Architecture layers to separate concerns.
- Learn how to handle dependencies and integrate external services in a scalable way.
- Understand how to write unit and integration tests for each layer of the architecture.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Domain-Driven Design (DDD)](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
