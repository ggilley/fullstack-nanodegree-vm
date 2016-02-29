from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database_setup import Base, Category, Item, User

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

default_categories = {"Soccer": ["Shinguards"],
                      "Basketball": ["Basketball"],
                      "Baseball": ["Bat", "Baseball"],
                      "Frisbee": ["Frisbee"],
                      "Snowboarding": ["Snowboard"],
                      "Rock Climbing": ["Shoes"],
                      "Foosball": ["Foosball Table"],
                      "Skating": ["Skates"],
                      "Hockey": ["Skates", "Puck", "Stick"]}

default_descriptions = {"Shinguards": "A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",  # noqa
                        "Basketball": "The Spalding NBA Official On-Court Game Ball is exactly what is used on court by the pros. It boasts an exclusive top grade full grain Horween leather cover and is designed for indoor play only. This ball is the official size and weight of the NBA.",  # noqa
                        "Bat": "Watch your young all-star knock those balls out of the park with this baseball bat. Its aircraft-grade aluminum design gives it a lightweight feel and fast swing speed, while the two-piece construction maximizes energy transfer to pack a serious wallop. With its large sweet spot and evenly balanced design, this bat delivers a smooth, solid hit every time.",  # noqa
                        "Baseball": "Full-grain leather cover. Made to the exact specifications of Major League Baseball, 5 ounces, 108 stitches.",  # noqa
                        "Shinguards": "A revolution in protection, G-Form is the world's first soft, flexible, sleeve-style guard to meet NOCSAE standards. This soft, flexible soccer shin guard hardens on impact. No hard shell for better comfort, performance, and compliance.",  # noqa
                        "Frisbee": "The Wham-O Ultimate Frisbee is specifically designed to balance distance - great for layout outs, speed and the ability to float based on your throws for all your Ultimate Frisbee plays.",  # noqa
                        "Snowboard": "With precise design and powerful drive, the pro-caliber Burton Custom X delivers high performance for snowboarding's most demanding riders.",  # noqa
                        "Shoes": "Aggressive shape for superior performance on the most technical routes. Dual-material upper uses a combination of Lorica (doesn't stretch) and leather (does stretch) in a specific bi-lateral stretch pattern for edging.",  # noqa
                        "Foosball Table": "Players that have tried these foosball tables are amazed on what they can do and the ball control they obtain. Play is far advanced to other tables. It's simply the best table ever made.",  # noqa
                        "Skates": "These skates are perennial favorites for easy comfort and support in a very attractive boot. Light support. Quilted lining cushions feet and the split tongue design provides stability on the ice. Maintenance free PVC sole unit keeps feet dry. Nickel plated blade gives a smooth edge.",  # noqa
                        "Puck": "Regulation ice hockey pucks are intended for ice hockey only. Due to their weight and shape, ice hockey pucks are not optimal for street hockey or inline hockey. Inline hockey pucks and inline hockey balls roll and slide better than ice hockey pucks on concrete, sport court and wood surfaces. Black colored, regulation ice hockey pucks are the best choice for on ice use because black pucks offer a sharp contrast to the color of the ice and vulcanized rubber slides very smoothly on the ice.",  # noqa
                        "Stick": "High modulus carbon fiber construction. Extra low kick point on shaft. High Torque power transfer design. Hand painted two tone blue and silver. Full 3K carbon fiber reinforced blade for added stiffness and control."}  # noqa


# populate the database with categories
def populate_database():
    newUser = User(name="ggilley", password="foo", email="ggilley@gerg.org",
                   picture="")
    session.add(newUser)
    session.commit()
    for cat in default_categories:
        newCategory = Category(name=cat)
        session.add(newCategory)
        session.commit()
        print "adding category: ", cat
        for item in default_categories[cat]:
            print "    adding item: ", item
            newItem = Item(name=item, user_id=newUser.id,
                           category_id=newCategory.id,
                           description=default_descriptions[item],
                           time=datetime.now())
            session.add(newItem)
            session.commit()

populate_database()
