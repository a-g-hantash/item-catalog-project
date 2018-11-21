#!/usr/bin/env python3
"""The second project of the Udacity Full-Stack Engineer Nanodegree.

An item catalog that utilizes the Flask framework to create a web application
with authentication and authorization for users to read, add, update, and
delete items they have placed inside the application.
"""

# import needed modules
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from database_setup import *

engine = create_engine('sqlite:///itemcatalog.db', pool_pre_ping=True)

# Bind the engine to the metadata of the Base Class so
# the declarative can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Check and delete categories if exists
session.query(Category).delete()
# Check and delete items if exists
session.query(Items).delete()
# Check and delete Users if exists
session.query(User).delete()

# 1.Create fake Users

u1 = User(name="Aseel Abu Hantash",
          email="example@example.com")
session.add(u1)
session.commit()

u2 = User(name="Mohammad Alsheheri",
          email="example@example.com")
session.add(u2)
session.commit()

u3 = User(name="Talal Alsheheri",
          email="example@example.com")
session.add(u3)
session.commit()


# 2. Create fake categories

Category1 = Category(name="Books",
                     user_id=1)
session.add(Category1)
session.commit()

Category2 = Category(name="Music",
                     user_id=3)
session.add(Category2)
session.commit()

Category3 = Category(name="Movies",
                     user_id=2)
session.add(Category3)
session.commit()


Category4 = Category(name="Paintings",
                     user_id=1)
session.add(Category4)
session.commit()

# 3. Create fake items
# Populate category with data for testsing

item1 = Items(name="The Lightening Theif",
              description="""A book written by Rick Riordan and the first book
                              in the Percy Jackson and the Olympians Series.
                              Percy Jackson is a good kid, but he can't seem to
                              focus on his schoolwork or control his temper.
                              And lately, being away at boarding school is only
                              getting worse - Percy could have sworn his
                              pre-algebra teacher turned into a monster and
                              tried to kill him. He later finds out his father
                              is Poseidon, the God of the Sea, and sets out on
                              a quest to save his mother.""",
              category_id=1,
              user_id=1)
session.add(item1)
session.commit()

item2 = Items(name="The Sea of Monsters",
              description="""A book written by Rick Riordan and the second book
                              in the Percy Jackson and the Olympians Series.
                              Percy sets out to retreive the Golden Fleece
                              before his summer camp is destoryed, surpassing
                              the first book's drama, and setting the stage
                              for more thrill to come.""",
              category_id=1,
              user_id=1)
session.add(item2)
session.commit()

item3 = Items(name="The Titan's Curse",
              description="""A book written by Rick Riordan and the third book
                              in the Percy Jackson and the Olympians Series.
                              It's not every day you find yourself in combat
                              with a half-lion, half-human. Percy is the son
                              of a Greek God, so it happens. Another adventure,
                              another quest. But one of the heroes may
                              not survive this time.""",
              category_id=1,
              user_id=1)
session.add(item3)
session.commit()

print("Database has been populated successfully!")
