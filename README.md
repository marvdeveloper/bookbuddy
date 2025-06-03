# BookBuddy

BookBuddy is a project to manage and track books, authors, and user interactions.

## Features

- Add, update, and delete books and authors
- Track book details like title, genre, and publication date
- Manage relationships between books and authors
- Includes tests for models and core functionality


## Usage
## To reset the database:

python reset_db.py
## To run tests:
pytest -x
## Project Structure
bookbuddy/models.py — Database models for User, Book, and Review

bookbuddy/crud.py — CRUD operations for models

tests/test_crud.py — Tests for CRUD functionality