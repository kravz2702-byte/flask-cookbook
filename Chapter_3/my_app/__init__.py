from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)
from my_app.catalog.views import catalog
app.register_blueprint(catalog)
db.create_all()