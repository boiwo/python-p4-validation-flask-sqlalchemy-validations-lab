from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    phone_number = Column(String(10), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required.")
        return name

    @validates('phone_number')
    def validate_phone(self, key, phone):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Phone number must be exactly 10 digits and numeric.")
        return phone


class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(String(250), nullable=False)
    category = Column(Enum('Fiction', 'Non-Fiction', name='category_types'), nullable=False)

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be at most 250 characters long.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y and contain one of the phrases: 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title

