__author__ = 'rwest'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
