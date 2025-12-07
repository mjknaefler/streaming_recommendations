# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Date, Text, Boolean, ForeignKey, DateTime, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


# content tables
class Title(Base):
    __tablename__ = 'title'
    
    show_id = Column(String(20), primary_key=True)
    title = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    date_added = Column(Date)
    release_year = Column(Integer)
    age_rating = Column(String(20))
    duration_value = Column(Integer)
    duration_unit = Column(String(20))
    description = Column(Text)
    
    # relationships
    genres = relationship('Genre', secondary='title_genre', back_populates='titles')
    countries = relationship('Country', secondary='title_country', back_populates='titles')
    people = relationship('TitlePeople', back_populates='title')
    user_swipes = relationship('UserSwipe', back_populates='title')


class Genre(Base):
    __tablename__ = 'genre'
    
    genre_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    
    titles = relationship('Title', secondary='title_genre', back_populates='genres')
    user_preferences = relationship('UserGenrePreference', back_populates='genre')


class TitleGenre(Base):
    __tablename__ = 'title_genre'
    
    show_id = Column(String(20), ForeignKey('title.show_id', ondelete='CASCADE'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id', ondelete='CASCADE'), primary_key=True)


class Country(Base):
    __tablename__ = 'country'
    
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    
    titles = relationship('Title', secondary='title_country', back_populates='countries')


class TitleCountry(Base):
    __tablename__ = 'title_country'
    
    show_id = Column(String(20), ForeignKey('title.show_id', ondelete='CASCADE'), primary_key=True)
    country_id = Column(Integer, ForeignKey('country.country_id', ondelete='CASCADE'), primary_key=True)


class People(Base):
    __tablename__ = 'people'
    
    person_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    
    titles = relationship('TitlePeople', back_populates='person')


class TitlePeople(Base):
    __tablename__ = 'title_people'
    
    show_id = Column(String(20), ForeignKey('title.show_id', ondelete='CASCADE'), primary_key=True)
    person_id = Column(Integer, ForeignKey('people.person_id', ondelete='CASCADE'), primary_key=True)
    role = Column(String(50), nullable=False, primary_key=True)
    credit_order = Column(Integer)
    
    title = relationship('Title', back_populates='people')
    person = relationship('People', back_populates='titles')


# user tables
class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    swipes = relationship('UserSwipe', back_populates='user', cascade='all, delete-orphan')
    genre_preferences = relationship('UserGenrePreference', back_populates='user', cascade='all, delete-orphan')


class UserSwipe(Base):
    __tablename__ = 'user_swipes'
    
    swipe_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    show_id = Column(String(20), ForeignKey('title.show_id', ondelete='CASCADE'), nullable=False)
    preference = Column(String(20), nullable=False)
    swiped_at = Column(DateTime, default=func.now())
    
    user = relationship('User', back_populates='swipes')
    title = relationship('Title', back_populates='user_swipes')


class UserGenrePreference(Base):
    __tablename__ = 'user_genre_preferences'
    
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genre.genre_id', ondelete='CASCADE'), primary_key=True)
    is_preferred = Column(Boolean, default=True)
    
    user = relationship('User', back_populates='genre_preferences')
    genre = relationship('Genre', back_populates='user_preferences')