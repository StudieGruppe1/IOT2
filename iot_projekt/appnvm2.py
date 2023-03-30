from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

conn=sqlite3.connect('PH_DB.db')
curs=conn.cursor()


@app.route("/")
def DBgraph():
    data = [conn]

    Time= [row[0] for row in data]
    Values = [row[1] for row in data]

    return render_template("templates/indexNY.html", Time = Time, Values = Values)