import os
from flask import Flask
from airsorted_address_book.models import db
import airsorted_address_book.views
from config import basedir

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

    app.add_url_rule('/api/v1/contacts/<int:id>', view_func=views.show, methods=['GET'])
    app.add_url_rule('/api/v1/contacts/<int:id>', view_func=views.delete, methods=['DELETE'])
    app.add_url_rule('/api/v1/contacts/<int:id>', view_func=views.update, methods=['PUT'])
    app.add_url_rule('/api/v1/contacts', view_func=views.index, methods=['GET'])
    app.add_url_rule('/api/v1/contacts', view_func=views.create, methods=['POST'])
    return app