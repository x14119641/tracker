import os
from pickle import TRUE
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'daniel.gil.romero24@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['daniel.gil.romero24@gmail.com', 'daniel.gil@zitrogames.com']
    MAIL_PORT=587
    MAIL_USE_TLS=True

    # FLASK_ENV='production'