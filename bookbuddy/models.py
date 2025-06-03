from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    borrowed_books = relationship("Book", back_populates="borrower", cascade="all")  # New relationship

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Foreign key for borrower (nullable if not borrowed)
    borrower = relationship("User", back_populates="borrowed_books")    # New backref

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"
