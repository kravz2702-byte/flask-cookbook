from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api 

filepath = os.path.join(os.path.abspath(os.getcwd()),'database.db')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + filepath
db = SQLAlchemy(app)
api = Api(app)

app.secret_key = 'some_secret_key'


from myapp.catalog.views import catalog 
app.register_blueprint(ccatalog)

db.create_all() 