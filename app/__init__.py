from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import SMTPHandler,RotatingFileHandler
from flask_mail import Mail, Message
import logging,os, smtplib
from threading import Thread


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models, errors


class ThreadedSMTPHandler(SMTPHandler):
    """
    Mimic SMTPHandler from logging module but seperate the actual emission (.emit)
    in another thread to avoid blocking the main process
    """
    def emit(self, record):
        #I am not sure of the best way to write the following line
        thread = Thread(target=super().emit, args=(record,)) #for Python2 : either modify super either : thread = Thread(target=logging.handlers.SMTPHandler.emit, args=(self, record))
        thread.start()

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()

        mail_handler = ThreadedSMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            # fromaddr=app.config['MAIL_USERNAME'],
            toaddrs=app.config['ADMINS'], subject='Tracker Failure',
            credentials=auth, secure=secure
            )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/tracker.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info(f'{app.__repr__} - startup')