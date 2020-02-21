from models import db, Bootcamp, Course
import os

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def db_seed():
    bootcamp = Bootcamp("Devworks Bootcamp",
                        "Devworks is a full stack JavaScript Bootcamp " +
                        "located in the heart of Boston that focuses " +
                        "on the technologies you need to get a high " +
                        "paying job as a web developer",
                        "https://devworks.com",
                        "(111) 111-1111", "enroll@devworks.com",
                        "233 Bay State Rd Boston MA 02215",
                        ["Web Development", "UI/UX", "Business"],
                        False, 89, "/img-2.jpg")

    bootcamp.insert()

    course = Course("Full Stack Web Development",
                    "In this course you will learn full stack " +
                    "web development, first learning all about " +
                    "the frontend with HTML/CSS/JS/Vue and then " +
                    "the backend with Node.js/Express/MongoDB",
                    12, 10000, "intermediate", True, 93, 1)

    course.insert()


def drop_and_create_all():
    db.drop_all()
    db.create_all()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    drop_and_create_all()
    db_seed()
