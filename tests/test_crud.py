import pytest
import time
from bookbuddy.db import get_session, init_db
from bookbuddy import crud
from bookbuddy.models import User, Book, Review

@pytest.fixture(scope="module")
def session():
    init_db()
    session_gen = get_session()
    session = next(session_gen)  # Get the session from generator
    yield session
    session.close()
    try:
        next(session_gen)
    except StopIteration:
        pass

def unique_email(base="testuser"):
    # Generate a unique email using current time
    return f"{base}_{int(time.time() * 1000)}@example.com"

def test_create_and_get_user(session):
    email = unique_email()
    user = crud.create_user(session, "Test User", email)
    session.commit()
    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == email

    fetched_user = crud.find_user_by_email(session, email)
    assert fetched_user is not None
    assert fetched_user.id == user.id

    session.delete(user)
    session.commit()

def test_create_and_get_book(session):
    book = crud.create_book(session, "Test Book", "Test Author")
    session.commit()
    assert book.id is not None
    assert book.title == "Test Book"
    assert book.author == "Test Author"

    fetched_books = crud.find_book_by_title(session, "Test Book")
    assert len(fetched_books) > 0
    assert fetched_books[0].id == book.id

    session.delete(book)
    session.commit()

def test_create_and_get_review(session):
    user_email = unique_email("reviewuser")
    user = crud.create_user(session, "Review User", user_email)
    book = crud.create_book(session, "Review Book", "Review Author")
    session.commit()

    review = crud.create_review(session, user.id, book.id, "Great book!", 5)
    session.commit()
    assert review.id is not None
    assert review.content == "Great book!"
    assert review.rating == 5

    user_reviews = crud.get_reviews_by_user(session, user.id)
    assert any(r.id == review.id for r in user_reviews)

    book_reviews = crud.get_reviews_for_book(session, book.id)
    assert any(r.id == review.id for r in book_reviews)

    # Cleanup
    session.delete(review)
    session.delete(book)
    session.delete(user)
    session.commit()
