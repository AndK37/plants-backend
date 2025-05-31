from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import date


           
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    date_of_order = Column(DateTime, server_default=func.now(), nullable=False)

    user = relationship('User', backref='orders')
    plant = relationship('Plant', backref='orders')


class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    
    user = relationship('User', backref='carts')
    plant = relationship('Plant', backref='carts')


class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)

    user = relationship('User', backref='favorites')
    plant = relationship('Plant', backref='favorites')


class PlantRating(Base):
    __tablename__ = 'plants_ratings'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    rating = Column(Integer, nullable=False)

    user = relationship('User', backref='plants_rating')
    plant = relationship('Plant', backref='plants_rating')


class ReviewRating(Base):
    __tablename__ = 'reviews_ratings'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    review_id = Column(Integer, ForeignKey('reviews.id'), nullable=False)
    upvoted = Column(Boolean, nullable=False)

    user = relationship('User', backref='reviews_rating')
    review = relationship('Review', backref='reviews_rating')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plant_id = Column(Integer, ForeignKey('plants.id'), nullable=False)
    review = Column(String(4096), nullable=False)

    user = relationship('User', backref='reviews')
    plant = relationship('Plant', backref='reviews')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    surname = Column(String(32), nullable=False)
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    login = Column(String(32), nullable=False)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', backref='users')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(32), nullable=False)


class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(64), nullable=False)
    desc = Column(String(1024), nullable=True, default=None)
    price = Column(Float, nullable=False)
    packing = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image = Column(String(64), nullable=True, default=None)

    category = relationship('Category', backref='plants')
    seller = relationship('User', backref='users')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(32), nullable=False)