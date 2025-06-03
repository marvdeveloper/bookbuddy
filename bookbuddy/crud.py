from .models import User, Book, Review
from sqlalchemy.orm import Session
from typing import List, Optional

# ---- User CRUD ----

def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    session.flush()  # flush so user.id is available without committing
    return user

def get_all_users(session: Session) -> List[User]:
    return session.query(User).all()

def find_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter_by(email=email).first()

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def update_user(session: Session, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
    user = get_user_by_id(session, user_id)
    if not user:
        return None
    if name:
        user.name = name
    if email:
        user.email = email
    session.flush()
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = get_user_by_id(session, user_id)
    if user:
        session.delete(user)
        session.flush()
        return True
    return False

# ---- Book CRUD ----

def create_book(session: Session, title: str, author: str) -> Book:
    book = Book(title=title, author=author)
    session.add(book)
    session.flush()
    return book

def get_all_books(session: Session) -> List[Book]:
    return session.query(Book).all()

def find_book_by_title(session: Session, title: str) -> List[Book]:
    return session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

def get_book_by_id(session: Session, book_id: int) -> Optional[Book]:
    return session.get(Book, book_id)

def update_book(session: Session, book_id: int, title: Optional[str] = None, author: Optional[str] = None) -> Optional[Book]:
    book = get_book_by_id(session, book_id)
    if not book:
        return None
    if title:
        book.title = title
    if author:
        book.author = author
    session.flush()
    return book

def delete_book(session: Session, book_id: int) -> bool:
    book = get_book_by_id(session, book_id)
    if book:
        session.delete(book)
        session.flush()
        return True
    return False

# ---- Review CRUD ----

def create_review(session: Session, user_id: int, book_id: int, content: str, rating: int) -> Review:
    review = Review(user_id=user_id, book_id=book_id, content=content, rating=rating)
    session.add(review)
    session.flush()
    return review

def get_reviews_by_user(session: Session, user_id: int) -> List[Review]:
    return session.query(Review).filter_by(user_id=user_id).all()

def get_reviews_for_book(session: Session, book_id: int) -> List[Review]:
    return session.query(Review).filter_by(book_id=book_id).all()

def get_review_by_id(session: Session, review_id: int) -> Optional[Review]:
    return session.get(Review, review_id)

def update_review(session: Session, review_id: int, content: Optional[str] = None, rating: Optional[int] = None) -> Optional[Review]:
    review = get_review_by_id(session, review_id)
    if not review:
        return None
    if content:
        review.content = content
    if rating is not None:
        review.rating = rating
    session.flush()
    return review

def delete_review(session: Session, review_id: int) -> bool:
    review = get_review_by_id(session, review_id)
    if review:
        session.delete(review)
        session.flush()
        return True
    return False
