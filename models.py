from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date
from flask_sqlalchemy import SQLAlchemy
from config import *


db = SQLAlchemy()
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def insert_demo_data():
    """Insert some data for test"""

    actor1 = Actor(name='Matt Ryan')
    actor2 = Actor(name='Jerry O\'Connell')
    actor3 = Actor(name=' Jamie Foxx')
    actor4 = Actor(name='Vishwak Sen')

    movie1 = Movie(title='Justice League Dark', release_date='2020-7-19',
                   description='https://en.wikipedia.org/wiki/Justice_League_Dark:_Apokolips_War')
    movie2 = Movie(title='Soul', release_date='2020-9-1',
                   description='https://en.wikipedia.org/wiki/Soul_(2020_film)')
    movie3 = Movie(title='The Three', release_date='2020-02-28',
                   description='https://en.wikipedia.org/wiki/Vishwak_Sen')

    movie1.actors.append(actor1)
    movie1.actors.append(actor2)
    movie2.actors.append(actor3)
    movie3.actors.append(actor4)

    actor1.insert()
    actor2.insert()
    actor3.insert()
    actor4.insert()

    movie1.insert()
    movie2.insert()
    movie3.insert()


movie_actor = db.Table(
    'movies_actors',
    db.Column('movie_id', db.Integer,
              db.ForeignKey('movies.id'), primary_key=True),
    db.Column('actor.id', db.Integer,
              db.ForeignKey('actors.id'), primary_key=True)
)
'''
Movies
'''


class Movie(db.Model):
    ''' Define'''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    release_date = db.Column(Date)
    actors = db.relationship('Actor', secondary=movie_actor,
                             backref=db.backref('movies', lazy=True))
    description = Column(String(500))

    def __init__(self, title, release_date, description):
        self.title = title
        self.release_date = release_date
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'description': self.description
        }


'''
Actrors
'''


class Actor(db.Model):
    ''' Define'''
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)

    # movie = Column(String())

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }
