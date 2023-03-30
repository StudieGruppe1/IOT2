import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('PH_DB.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    PH_SENSOR = conn.execute('SELECT * FROM PH_SENSOR').fetchall()
    conn.close()
    return render_template('index.html', PH_SENSOR = PH_SENSOR) 


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=80, debug=False)