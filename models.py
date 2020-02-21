from flask_sqlalchemy import SQLAlchemy
import os

db_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=db_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Bootcamp(db.Model):
    __tablename__ = 'bootcamps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(500))
    website = db.Column(db.String(500))
    phone = db.Column(db.String(80))
    email = db.Column(db.String(80))
    address = db.Column(db.String(120))
    careers = db.Column(db.ARRAY(db.String(80)))
    job_assistance = db.Column(db.Boolean)
    upvotes = db.Column(db.Integer)
    img_url = db.Column(db.String(80))
    courses = db.relationship('Course', backref='bootcamp', lazy=True)

    def __init__(self, name, description, website,
                 phone, email, address, careers, job_assistance,
                 upvotes, img_url):
        self.name = name
        self.description = description
        self.website = website
        self.phone = phone
        self.email = email
        self.address = address
        self.careers = careers
        self.job_assistance = job_assistance
        self.upvotes = upvotes
        self.img_url = img_url

    def format_short(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "careers": self.careers,
            "upvotes": self.upvotes,
            "img_url": self.img_url
        }

    def format_long(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "website": self.website,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "careers": self.careers,
            "job_assistance": self.job_assistance,
            "upvotes": self.upvotes,
            "img_url": self.img_url
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            bootcamp = Bootcamp(name=name)
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            bootcamp.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            bootcamp = Bootcamp.query.filter(bootcamp.id=id).one_or_none()
            bootcamp.title = 'Juno'
            bootcamp.update()
    '''

    def update(self):
        db.session.commit()


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(500))
    duration = db.Column(db.Integer)
    tuition = db.Column(db.Integer)
    minimum_skill = db.Column(db.String(80))
    scholarships_available = db.Column(db.Boolean)
    upvotes = db.Column(db.Integer)
    bootcamp_id = db.Column(db.Integer, db.ForeignKey(
        'bootcamps.id'), nullable=False)

    def __init__(self, title, description, duration,
                 tuition, minimum_skill, scholarships_available,
                 upvotes, bootcamp_id):
        self.title = title
        self.description = description
        self.duration = duration
        self.tuition = tuition
        self.minimum_skill = minimum_skill
        self.scholarships_available = scholarships_available
        self.upvotes = upvotes
        self.bootcamp_id = bootcamp_id

    def format_short(self):
        return {
            "id": self.id,
            "title": self.title,
            "upvotes": self.upvotes,
            "bootcamp_id": self.bootcamp_id
        }

    def format_long(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "duration": self.duration,
            "tuition": self.tuition,
            "minimum_skill": self.minimum_skill,
            "scholarships_available": self.scholarships_available,
            "bootcamp_id": self.bootcamp_id,
            "upvotes": self.upvotes
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            course = Course(title=title)
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            course.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            course = Course.query.filter_by(id=id).one_or_none()
            course.title = 'Full Stack Web Development'
            course.update()
    '''

    def update(self):
        db.session.commit()
