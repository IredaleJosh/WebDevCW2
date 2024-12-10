from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Flask Admin
from flask_admin import Admin
from flask_babel import Babel
# Logging
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Define for Babel
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.secret_key = 'secreted-key'

migrate = Migrate(app, db)

# Admin
babel = Babel(app, locale_selector=get_locale)
admin = Admin(app,template_mode='bootstrap4')


from app import views, models

