import os
import base64
import requests
import sqlite3
import csv

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions


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
conn = sqlite3.connect("info.db", check_same_thread=False)


@app.route("/")
def index():

    return render_template("cards.html")

@app.route("/suggestion", methods=["GET", "POST"])
def suggestion():

    if request.method =="POST":

        what = request.form.get("what")
        why = request.form.get("why")
        lat = request.form.get("lat1")
        lng = request.form.get("lng1")
        history = request.form.get("history")

        cur = conn.cursor()
        cur.execute("INSERT INTO markers (what, why, lat, lng, history) VALUES(?, ?, ?, ?, ?)",(what, why, lat, lng, history))
        conn.commit()
        cur.execute("SELECT what, why, lat, lng, history FROM markers")
        data = cur.fetchall()

        with open("data4.csv", "w", newline="") as f_handle:
            writer = csv.writer(f_handle)
            header = ["what, why, lat, lng, history"]
            writer.writerow(["what", "why", "lat", "lng", "history"])

            for row in data:
                writer.writerow(row)

        convxml()


        return render_template("marker.html")
    else:
        return render_template("marker.html")

@app.route("/japan")
def japan():

    return render_template("japan.html")

@app.route("/norway")
def norway():
    return render_template("norway.html")

@app.route("/china")
def china():

    return render_template("china.html")


@app.route("/crazy")
def crazy():
    return render_template("crazy.html")


def convxml():
    csvFile = 'data4.csv'
    xmlFile = 'static/myData2.xml'

    csvData = csv.reader(open(csvFile))
    xmlData = open(xmlFile, 'w')
    xmlData.write('<?xml version="1.0"?>' + "\n")
    # there must be only one top-level tag
    xmlData.write('<csv_data>' + "\n")

    rowNum = 0
    for row in csvData:
        if rowNum == 0:
            tags = row
            # replace spaces w/ underscores in tag names
            for i in range(len(tags)):
                tags[i] = tags[i].replace(' ', '_')
        else:
            xmlData.write('<marker')
            for i in range(len(tags)):
                xmlData.write(' ' + tags[i] + '=' + '"' + row[i] + '"')

            xmlData.write('/>'+ "\n")

        rowNum +=1

    xmlData.write('</csv_data>' + "\n")
    xmlData.close()
