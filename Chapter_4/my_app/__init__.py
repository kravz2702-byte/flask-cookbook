from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

filepath = os.path.join(os.path.abspath(os.getcwd()), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+filepath
db = SQLAlchemy(app)

from my_app.catalog.views import catalog
app.register_blueprint(catalog)