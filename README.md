# Project 1

Web Programming with Python and JavaScript

Welcome to project 1: Books

It is organized as follows:

6 HTML files:
    -books.html: The information of a given book appears 
    on this page.

    -busquedad.html: IN this part you put the information 
    about the book that you want to search

    - error.html: Contains a message which shows up when 
    the i want to show something, for instance error 404 
    or another mesaage. In adition a specific hiperlink 
    to move.

    -index.html: The login and registration page.

    -layout.html: Is the layout of most of files. It imports 
    boostrap and the stylesheet files.

    -resultado.html: Show the result of searching books, as a list 
    with all parameters(isbn, name, author, year)

    
books.csv: contains information of 5000 books.

The heroku database url is the following:
    postgres://qgjpvuzowqhzds:08cbf929285a7e71e70b984acb9a1399b7d72a56ce683c9979270d0006e3a4df@ec2-174-129-253-28.compute-1.amazonaws.com:5432/d8kcvshuksu1qv

import.py: this file contains the sql queries to create our tables, and
    a code to write all books on books.csv into the tbook table

application.py: file contains all the logic part on the server side, 
    the different functions defined on each route, and the corresponding 
    global variables established through Flask. There is also a set of 
    sql queries to retrieve information from the database,

3 tables were created: tusers, treview & tbook.  This part you can see 
    on models.py file



