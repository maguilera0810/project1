import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))
# DATABASE_URL is an environment variable that indicates where the database lives
# create a 'scoped session' that ensures different users' interactions with the
db = scoped_session(sessionmaker(bind=engine))
# database are kept separate

if True:
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
        user_id INTEGER REFERENCES tuser NOT NULL, 
        book_id VARCHAR REFERENCES tbook NOT NULL, 
        rank INTEGER NOT NULL, 
        opinion VARCHAR
        )"""
    )
else:
    db.execute("DROP TABLE treview")
    db.execute("DROP TABLE tuser")
    db.execute("DROP TABLE tbook")
db.commit()
