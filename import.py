import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))
# DATABASE_URL is an environment variable that indicates where the database lives
# create a 'scoped session' that ensures different users' interactions with the
db = scoped_session(sessionmaker(bind=engine))
# same import and setup statements as above
def insertar(name="books.csv"):
    db.execute(
        """CREATE TABLE tbook ( 
        isbn VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year VARCHAR NOT NULL
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
    db.commit()

    f = open(name)
    reader = csv.reader(f)
    columns = next(reader)
    #query = "INSERT INTO tbook (id,title,author,year) VALUES (:id,:title,:author,:year)"
    query = "INSERT INTO tbook ("+",".join(columns) + \
        ") VALUES (:"+",:".join(columns)+")"
    print(query)
    i = 1

    for isbn, title, author, year in reader:  # loop gives each column a name
        db.execute(
            query,
            {"isbn": isbn,
             "title": title,
             "author": author,
             "year": year}
        )  # substitute values from CSV line into SQL command, as per this dict
        print(
            f"{i} \t ISBN:{isbn}\tTITLE:{title}\n\tAUTHOR:{author}\t\tYEAR: {year}\n------------------------------------------------------")
        i += 1

    db.commit()  # transactions are assumed, so close the transaction finished


if __name__ == '__main__':
    insertar()
