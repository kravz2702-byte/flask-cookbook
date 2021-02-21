from flask import Flask
import os
from redis import Redis
from flask_mongoengine import MongoEngine 


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB' : 'my_catalog'}
app.debug = True 
db = MongoEngine(app)
redis = Redis()

from my_app.catalog.views import catalog
app.register_blueprint(catalog)
