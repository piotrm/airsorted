from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    app.config.from_envvar('ADDRESS_BOOK_SETTINGS', silent=True)
    db.init_app(app)
    db.app = app
    db.create_all()
    return app
