from .models import User, Book, Review
from sqlalchemy.orm import Session

# ---- User CRUD ----

def create_user(session: Session, name: str, email: str) -> User:
    user = User(name=name, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_all_users(session: Session):
    return session.query(User).all()

def find_user_by_email(session: Session, email: str):
    return session.query(User).filter_by(email=email).first()

def delete_user(session: Session, user_id: int):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# ---- Book CRUD ----

def create_book(session: Session, title: str, author: str) -> Book:
    book = Book(title=title, author=author)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def get_all_books(session: Session):
    return session.query(Book).all()

def find_book_by_title(session: Session, title: str):
    return session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

# ---- Review CRUD ----

def create_review(session: Session, user_id: int, book_id: int, content: str, rating: int) -> Review:
    review = Review(user_id=user_id, book_id=book_id, content=content, rating=rating)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review

def get_reviews_by_user(session: Session, user_id: int):
    return session.query(Review).filter_by(user_id=user_id).all()

def get_reviews_for_book(session: Session, book_id: int):
    return session.query(Review).filter_by(book_id=book_id).all()
