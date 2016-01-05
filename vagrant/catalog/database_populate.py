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

default_categories = { "Soccer" : ["Shinguards"],
		       "Basketball" : ["Basketball"],
		       "Baseball" : ["Bat", "Baseball"],
		       "Frisbee" : ["Frisbee"],
		       "Snowboarding" : ["Snowboard"],
		       "Rock Climbing" : ["Shoes"],
		       "Foosball" : ["Foosball"],
		       "Skating" : ["Skates"],
		       "Hockey" : ["Skates", "Puck", "Stick"]}

# populate the database with categories

def populate_database():
    for cat in default_categories:
        newCategory = Category(name=cat)
        session.add(newCategory)
        session.commit()
        print "adding category: ", cat
        for item in default_categories[cat]:
            print "adding item: ", item
            newItem = Item(name=item, category_id=newCategory.id)
            session.add(newItem)
            session.commit()

populate_database()
