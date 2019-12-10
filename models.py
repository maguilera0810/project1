import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))
# DATABASE_URL is an environment variable that indicates where the database lives
# create a 'scoped session' that ensures different users' interactions with the
db = scoped_session(sessionmaker(bind=engine))
# database are kept separate
db.execute(
    """CREATE TABLE tbook ( 
        isbn VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year INTEGER NOT NULL
        )"""
)
db.execute(
    """  CREATE TABLE tuser (
        id SERIAL PRIMARY KEY,
        fname VARCHAR NOT NULL,
        lname VARCHAR NOT NULL,
        email VARCHAR UNIQUE NOT NULL ,
        pwd VARCHAR NOT NULL
        )"""
)
db.execute(
    """CREATE TABLE treview ( 
        id SERIAL PRIMARY KEY, 
        user_id VARCHAR REFERENCES tuser NOT NULL, 
        book_id VARCHAR REFERENCES tbook NOT NULL, 
        rank INTEGER NOT NULL, 
        opinion VARCHAR
        )"""
)

db.commit()


""" class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    #review = db.relationship('reviews', backref='id_book', lazy=True)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    #review = db.relationship('reviews', backref='id_user', lazy=True)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_book = db.Column(db.String, db.ForeignKey('books.id'), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    opinion = db.Column(db.String, nullable=True)
    #role = db.relationship('Role', backref=db.backref('devices'))


    def search_by_title(self, search=""):
        res = self.query.filter(self.title.like("%search%")).all()
        print(res.id)
        return res
 """