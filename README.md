# Project 1

Web Programming with Python and JavaScript

Welcome to project 1: Books

It is organized as follows:
9 HTML files:
    - 404.html: Contains an error message which shows up when 
    the website's /api/<isbn> route does not exist. Where <isbn>
    is an ISBN number.
    -books.html: The information of a given book appears on this page
    -fails.html: It appears when there exist a login or sign up error
    -form.html: The page used to sign up a new user    
    -index.html: The login page
    -review.html: It is the page where the user can write its first review
    or update an old one.
    -reviewschange.html: It appears when a new review has been created or updated
    -search.html: It is the page where the user can search for books,
    by typing the ISBN number, title or the author of a book
    -success.html: When a new user has been registered succesfully

books.csv: contains information of 5000 books.

The heroku database url is the following:
    postgres://tvviudmrjxggzt:0e1dcfbbf5d37a6031e5f0d4fda56d42289c591c67a7aa4d459eb0b36ab9c5fc@ec2-54-225-205-79.compute-1.amazonaws.com:5432/dats98s4nmt92g


application.py file contains all the logic on the server side, the different functions defined on each one of the routes, and the corresponding global variables established  through Flask. There is also a set of Raw SQL queries to retrieve information from the database,
3 tables were created: users, reviews & books. 


