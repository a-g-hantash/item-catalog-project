#!/usr/bin/env python3
"""The second project of the Udacity Full-Stack Engineer Nanodegree.

An item catalog that utilizes the Flask framework to create a web application
with authentication and authorization for users to read, add, update, and
delete items they have placed inside the application.
"""

# import needed modules
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# defining Base variable
Base = declarative_base()


# creating class User
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


# creating class Category
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns object data in easily serializeable format (JSON)."""
        return {
            'name': self.name,
            'id': self.id
        }


# creating class Items
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Returns object data in easily serializable format (JSON)."""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'category_id': self.category_id
        }


engine = create_engine('sqlite:///itemcatalog.db', pool_pre_ping=True)

Base.metadata.create_all(engine)
