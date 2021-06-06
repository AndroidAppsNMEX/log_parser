from flask import render_template, request, redirect, url_for
from app import app_object
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, func
import json
import sys

db = SQLAlchemy(app_object)


## Prepare model based on database table
class Logs(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    unix_timestamp = db.Column(db.Integer)
    log_datetime = db.Column(db.Date)
    from_host = db.Column(db.String(100))
    to_host = db.Column(db.String(100))
    loaddate = db.Column(db.Date)

    def __init__(self, unix_timestamp, log_datetime, from_host, to_host):
        self.unix_timestamp = unix_timestamp
        self.log_datetime = log_datetime
        self.from_host = from_host
        self.to_host = to_host


@app_object.route('/search')
def search():
    return render_template('search.html')


@app_object.route('/', methods=['GET', 'POST'])
def show_all():
   return render_template('show_all.html', logs=Logs.query.all())


@app_object.route('/handle_data', methods=['GET', 'POST'])
def handle_data():
    if request.method == "POST":
        host = request.form['from_host']
        init_datetime = request.form['init_datetime']
        end_datetime = request.form['end_datetime']

        print(f"{host}, {init_datetime}, {end_datetime}", file=sys.stderr)
        return render_template('query.html', logs=Logs.query.filter(and_(Logs.log_datetime.between(init_datetime, end_datetime), Logs.from_host == host)).all())
    else:
        return render_template('search.html')
