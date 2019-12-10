import os
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# database engine object from SQLAlchemy that manages connections to the database
engine = create_engine(os.getenv("DATABASE_URL"))

# DATABASE_URL is an environment variable that indicates where the database lives
# create a 'scoped session' that ensures different users' interactions with the
db = scoped_session(sessionmaker(bind=engine))


# --------------------------------------------



def avrg(reviews):
    rating = 0
    if len(reviews) > 0:
        for review in reviews:
            rating += review.rank
        rating = rating / len(reviews)
    return rating
# --------------------------------------------

# -------------------------------------------------------------

# -------------------------------------------------------------


@app.route("/")
def index():
    if not "active" in session or ("active" in session and session["active"] == []):
        session["active"] = []
        return render_template("index.html")
    else:

        return redirect(url_for("search"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/sign", methods=["POST"])
def sign():

    email = request.form.get("email")
    password = request.form.get("pwd")
    user = db.execute(
        "SELECT * FROM tuser WHERE email = :email", {"email": email}).fetchall()
    if len(user) > 0:
        if password == user[0].pwd:
            session["active"].append(user[0].id)
            session["active"].append(user[0].fname)
            session["active"].append(user[0].lname)
            session["active"].append(user[0].pwd)
            print(session, "-------------\n-----------------------")
            return redirect(url_for("search"))
        else:
            message = "wrong password"
    else:
        message = "wrong user"
    return render_template(
        'error.html',
        message=message,
        head="Error 404",
        dir="",
        dir_placeholder="Login"
    ), 200


@app.route("/register", methods=["POST"])
def register():
    """Register new user"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("pwd")

    f = db.execute("SELECT * FROM tuser WHERE email = :email",
                   {"email": email})
    print(f)

    if f.rowcount > 0:

        return render_template(
            'error.html',
            message="User exists already",
            head="Error",
            dir="",
            dir_placeholder="Login"
        ), 404
    db.execute("INSERT INTO tuser (fname,lname,email,pwd) VALUES (:fname,:lname,:email,:pwd)",
               {"fname": fname, "lname": lname, "email": email, "pwd": password})
    db.commit()

    return render_template(
        'error.html',
        message="Registered",
        head="Success",
        dir="",
        dir_placeholder="Login"
    ), 200


@app.route("/search", methods=["GET"])
def search():
    print(session)
    if not "active" in session or ("active" in session and session["active"] == []):
        session["active"] = []
        return redirect(url_for("index"))
    return render_template("busquedad.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    res = []
    if request.method == "POST":
        query = "SELECT * FROM tbook"
        l = []
        isbn = request.form.get("isbn")
        if isbn:
            l.append(f"isbn LIKE '%{isbn}%'")
        title = request.form.get("title")

        if title:
            l.append(f"title LIKE '%{title}%'")
        author = request.form.get("author")
        if author:
            l.append(f"author LIKE '%{author}%'")
        year = request.form.get("year")
        if year:
            l.append(f"year LIKE '%{year}%';")
        if len(l) > 0:
            query += " WHERE "+" AND ".join(l)
        print(query)
        res = db.execute(query).fetchall()
        if len(res) > 0:
            return render_template("resultado.html", books=enumerate(res))
        else:
            # return render_template("error.html", message="There no exist the book", head="Error 404")
            return render_template(
                'error.html',
                message="There no exist the book",
                head="Error 404",
                dir="search",
                dir_placeholder="Search",
                sidebar="logout",
                sidebar_placeholder="Logout"
            ), 200
    else:
        print(session)
        if not "active" in session or ("active" in session and session["active"] == []):
            session["active"] = []
            return redirect(url_for("index"))
        else:
            return redirect(url_for("search"))


@app.route("/result/<string:isbn>", methods=["GET"])
def search_book(isbn):
    id = session["active"][0]
    message = "Add review"
    book = db.execute(
        f"SELECT * FROM tbook WHERE isbn = '{isbn}';"
    ).fetchall()
    if len(book) == 0:
        # return render_template('error.html', message="There no exist the book", head="Error 404")
        return render_template(
            'error.html',
            message="There no exist the book",
            head="Error 404",
            dir="search",
            dir_placeholder="Search",
            sidebar="logout",
            sidebar_placeholder="Logout"
        ), 200

    reviews = db.execute(
        f"SELECT * FROM treview WHERE book_id = '{isbn}';"
    ).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "ajIDHorLujYoRl0OIglQOQ", "isbns": isbn})
    print(res.json())
    if db.execute(f"SELECT * FROM treview WHERE book_id = '{isbn}' AND user_id = {id};").rowcount > 0:
        message = "Update review"
    return render_template("books.html", book=book[0], reviews=reviews, res=res.json()['books'][0], message=message)


@app.route("/addreview/<string:ISBN>", methods=["POST"])
def reviews(ISBN):
    """Register new user"""

    # Get form information.
    id = session["active"][0]
    isbn = ISBN

    rank = request.form.get("rank")
    opinion = request.form.get("opinion")

    # Make sure flight exists.
    if db.execute(f"SELECT * FROM treview WHERE book_id = '{isbn}' AND user_id = {id};").rowcount == 0:
        db.execute("INSERT INTO treview (user_id,book_id, rank, opinion) VALUES (:user_id, :book_id, :rank, :opinion)",
                   {"user_id": id, "book_id": isbn, "rank": rank, "opinion": opinion})
        db.commit()
        return render_template(
            'error.html',
            message="Your review has been created",
            head="Success",
            dir="search",
            dir_placeholder="Search",
            sidebar="logout",
            sidebar_placeholder="Logout"
        ), 200
    else:
        db.execute(
            "UPDATE treview SET rank = :rank, opinion = :opinion WHERE user_id = :user_id AND book_id = :book_id",
            {"user_id": id, "book_id": isbn, "rank": rank, "opinion": opinion}
        )
        db.commit()
        return render_template(
            'error.html',
            message="Your review has been updated",
            head="Success",
            dir="search",
            dir_placeholder="Search",
            sidebar="logout",
            sidebar_placeholder="Logout"
        ), 200


""" @app.route("/api/<string:id>",methods=["GET"])
def api(id):
    try:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "ajIDHorLujYoRl0OIglQOQ", "isbns": id}).json()
    except:
        res = "The ISBN code does not exist."
    return res """


@app.route("/api/<string:id>", methods=["GET"])
def api(id):

    book = db.execute(f"SELECT * FROM tbook WHERE isbn = '{id}'").fetchall()
    reviews = db.execute(
        f"SELECT * FROM treview WHERE book_id = '{id}'").fetchall()

    if len(book) == 0:
        json_res = {
            "error":404
        }
        return json_res, 200
    else:
        book = book[0]
        json_res = {
            "title": book.title,
            "author": book.author,
            "year": int(book.year),
            "isbn": book.isbn,
            "review_count": len(reviews),
            "average_score": avrg(reviews)
        }
        return json_res, 200
