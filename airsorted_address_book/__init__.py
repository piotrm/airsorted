import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object('config')
    if config_name is None:
        app.config.from_envvar('ADDRESS_BOOK_CONFIG', silent=True)
    else:
        app.config.from_pyfile(basedir+'/config/'+config_name+'.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    db.create_all()
    return app
