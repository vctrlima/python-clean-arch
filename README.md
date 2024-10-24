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
│
├── app/                 # Application code
│   ├── api/             # FastAPI routes
│   ├── core/            # Core business logic (domain and application layers)
│   ├── infrastructure/  # Infrastructure layer (e.g., database, external services)
│   └── tests/           # Unit and integration tests
│
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .env                 # Environment variables
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vctrlima/python-clean-arch.git
cd python-clean-arch
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the FastAPI application:

```bash
uvicorn app.api.main:app --reload
```

## Learning Objectives

- Apply DDD principles such as value objects, aggregates, and repositories.
- Structure the project using Clean Architecture layers to separate concerns.
- Learn how to handle dependencies and integrate external services in a scalable way.
- Understand how to write unit and integration tests for each layer of the architecture.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Domain-Driven Design (DDD)](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
