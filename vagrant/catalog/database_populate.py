from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

default_categories = ["Soccer",
                      "Basketball",
                      "Baseball",
                      "Frisbee",
                      "Snowboarding",
                      "Rock Climbing",
                      "Foosball",
                      "Skating",
                      "Hockey"]

# populate the database with categories

def populate_database():
    for cat in default_categories:
        newCategory = Category(name=cat)
        session.add(newCategory)
        print "adding category: ", cat
    session.commit()

populate_database()
