from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
import os
from redis import Redis

redis = Redis()
app = Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"/database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
db = SQLAlchemy(app)
migrate = Migrate(app, db)
import my_app.catalog.views
from my_app.catalog.views import catalog
app.register_blueprint(catalog)
db.create_all()