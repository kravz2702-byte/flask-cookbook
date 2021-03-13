from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from my_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pwdhash = db.Column(db.String())

    def __init__(self, name, password):
        self.name = name
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
        return True 

    @property
    def is_active(self):
        return True

    @property 
    def is_anonymus(self):
        return False

    @property 
    def get_id(self):
        return str(self.id)


class RegistrationForm(FlaskForm):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', \
        validators=[InputRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Confirm Password', [InputRequired()])

class LoginRequired(FlaskForm):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])