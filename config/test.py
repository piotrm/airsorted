import os
basedir = os.getcwd()

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_db.sqlite')
TESTING	= True
DEBUG = True
