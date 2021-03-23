import ldap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


ALLOWED_EXTENSIONS = set(['set', 'jpg', 'gif', 'png', 'jpeg', 'pdf'])
filepath = os.path.join(os.path.abspath(os.getcwd()),'database.db')


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/my_app/static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + filepath
app.config['WTF_CSRF_SECRET_KEY'] = 'you_will_never_know'
app.config['FACEBOOK_OAUTH_CLIENT_ID'] = 'random_keys_of_social_networks'
app.config['FACEBOOK_OAUTH_CLIENT_SECRET'] = 'random_keys_of_social_networks'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = 'random_keys_of_social_networks'
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = 'random_keys_of_social_networks'
app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True
app.config["TWITTER_OAUTH_CLIENT_KEY"] = "twitter app api key"
app.config["TWITTER_OAUTH_CLIENT_SECRET"] = "twitter app secret key"
app.config['LDAP_PROVIDER_URL'] = 'ldap://localhost'
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

def get_ldap_connection():
    conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
    return conn

from myapp.auth.views import auth, flacebook_blueprint, google_blueprint, twitter_blueprint
app.register_blueprint(auth)    
app.register_blueprint(flacebook_blueprint)
app.register_blueprint(google_blueprint)
app.register_blueprint(twitter_blueprint)


db.create_all()