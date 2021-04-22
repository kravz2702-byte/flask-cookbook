from functools import wraps
from flask import request, render_template, flash, redirect, url_for,\
    session, Blueprint, g, abort
from flask_login import login_required, login_user, logout_user,\
    current_user
from wtforms import PasswordField
from my_app import db, login_manager
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules
from flask_admin.actions import ActionsMixin
from my_app.auth.models import User, RegistrationForm, LoginForm,\
    AdminUserCreateForm, AdminUserUpdateFrom, generate_password_hash,\
    CKTextAreaField

auth = Blueprint('auth', __name__)


def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)
    return decorated_view


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('')
@auth.route('/home')
def home():
    return render_template('home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('auth.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash(
                'This username has been already taken. Try another one.'
            )
            return render_template('register.html', form=form)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('auth.login'))