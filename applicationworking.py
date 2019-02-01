import os
import base64
import requests

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///info.db")

@app.route("/")
def index():

    return render_template("cards.html")

@app.route("/suggestion", methods=["GET", "POST"])
def suggestion():

    if request.method =="POST":

        db.execute("INSERT INTO markers (what, why, lat, lng, history) VALUES(:what, :why, :lat, :lng, :history)",
                  what = request.form.get("what"), why = request.form.get("why"), lat = request.form.get("lat1"),
                  lng = request.form.get("lng1"), history = request.form.get("history"))
        return 'ok'
    else:
        return render_template("suggestion.html")

@app.route("/japan.html")
def japan():

    return render_template("japan.html")

@app.route("/norway.html")
def norway():
    return render_template("norway.html")

@app.route("/china.html")
def china():

    return render_template("china.html")


@app.route("/crazy.html")
def crazy():
    return render_template("crazy.html")
