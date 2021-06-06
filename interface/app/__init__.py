from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app_object = Flask(__name__)
app_object.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:pepe@db/logs'

from app import routes