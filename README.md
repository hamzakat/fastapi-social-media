# fastapi-social-media
Basic Social Media, built and documented using FastAPI!
Implemeted in two versions in terms of database integration:
1. SQL queries
2. ORM

## Technologies
* Python
* FastAPI
* OpenAPI docuementation with SwaggerUI
* Pytest for integration tests
* Authentication using JWT
* PostgreSQL:
  * Psycopg2 (used in both SQL queries and ORM versions)
  * SQLAlchemy (used in ORM version)
* Alembic for managing database migrations
* Docker
* GitHub Actions for CI/CD pipeline

## Todo
* [x] CRUD operations
* [x] OpenAPI documentation
* [x] Integration with the database using Psycopg2
* [ ] Integration with the database using SQLAlchemy
* [ ] Setup integration tests
* [ ] App dockerization
* [ ] Setup the CI/CD pipeline
