import click
from .db import get_session
from . import crud
from .models import User, Book

@click.group()
def cli():
    """📚 BookBuddy CLI - Manage users, books, and reviews."""
    pass

# --- USER COMMANDS ---

@cli.command()
@click.argument("name")
@click.argument("email")
def add_user(name, email):
    """Add a new user."""
    session = get_session()
    user = crud.create_user(session, name, email)
    click.echo(f"User '{user.name}' added with ID {user.id}")

@cli.command()
def list_users():
    """List all users."""
    session = get_session()
    users = crud.get_all_users(session)
    if not users:
        click.echo("No users found.")
        return
    for user in users:
        click.echo(f"{user.id}. {user.name} - {user.email}")

# --- BOOK COMMANDS ---

@cli.command()
@click.argument("title")
@click.argument("author")
def add_book(title, author):
    """Add a new book."""
    session = get_session()
    book = crud.create_book(session, title, author)
    click.echo(f"Book '{book.title}' by {book.author} added with ID {book.id}")

@cli.command()
def list_books():
    """List all books."""
    session = get_session()
    books = crud.get_all_books(session)
    if not books:
        click.echo("No books found.")
        return
    for book in books:
        borrower = f" (Borrowed by User {book.borrower_id})" if book.borrower_id else ""
        click.echo(f"{book.id}. {book.title} by {book.author}{borrower}")

# --- BORROWING COMMANDS ---

@cli.command()
@click.argument("book_id", type=int)
@click.argument("user_id", type=int)
def borrow_book(book_id, user_id):
    """Borrow a book for a user."""
    session = get_session()
    book = crud.borrow_book(session, book_id, user_id)
    if not book:
        click.echo(f"Book or user not found.")
        return
    click.echo(f"Book '{book.title}' borrowed by User {user_id}.")

@cli.command()
@click.argument("book_id", type=int)
def return_book(book_id):
    """Return a borrowed book."""
    session = get_session()
    success = crud.return_book(session, book_id)
    if not success:
        click.echo(f"Book with ID {book_id} not found.")
        return
    click.echo(f"Book ID {book_id} returned successfully.")

@cli.command()
@click.argument("user_id", type=int)
def list_borrowed(user_id):
    """List all books borrowed by a user."""
    session = get_session()
    books = crud.get_borrowed_books_by_user(session, user_id)
    if not books:
        click.echo(f"No borrowed books found for User {user_id}.")
        return
    for book in books:
        click.echo(f"{book.id}. {book.title} by {book.author}")

# --- REVIEW COMMANDS ---

@cli.command()
@click.argument("user_id", type=int)
@click.argument("book_id", type=int)
@click.argument("content")
@click.argument("rating", type=int)
def add_review(user_id, book_id, content, rating):
    """Add a review for a book."""
    if rating < 1 or rating > 5:
        click.echo("Rating must be between 1 and 5.")
        return

    session = get_session()
    user = session.query(User).get(user_id)
    book = session.query(Book).get(book_id)

    if not user:
        click.echo(f"User with ID {user_id} does not exist.")
        return

    if not book:
        click.echo(f"Book with ID {book_id} does not exist.")
        return

    review = crud.create_review(session, user_id, book_id, content, rating)
    click.echo(f"Review added by User {user_id} for Book {book_id} (Rating: {rating}/5)")

@cli.command()
@click.argument("book_id", type=int)
def list_reviews(book_id):
    """List all reviews for a book."""
    session = get_session()
    reviews = crud.get_reviews_for_book(session, book_id)
    if not reviews:
        click.echo("No reviews found for this book.")
        return
    for r in reviews:
        click.echo(f"{r.id}. {r.user.name} rated {r.rating}/5 - {r.content}")

if __name__ == "__main__":
    cli()
