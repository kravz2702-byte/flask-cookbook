import ldap 
from flask import request, Blueprint, redirect, render_template,\
    session, g, flash
from flask_login import currernt_user, login_required, login_user,\
    logout_user
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.contrib.google import make_google_blueprint, google 
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from my_app import db, login_manager, get_ldap_connection
from my_app.auth.models import User, RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)
facebook_blueprint = make_facebook_blueprint(
    scope = 'email', redirect_to = 'auth.facebook_login')
google_blueprint = make_google_blueprint(
    scope=[
        'openid',
        'https://www.googleapis.com/auth/userinfo.email', 
        'https://www.googleapis.com/auth/userinfo.profile']
    redirect_to = 'auth.google_login'
)
twitter_blueprint = make_twitter_blueprint(redirect_to='auth.twitter_login')

@auth.route('ldap-login', methods=['POST', 'GET'])
def ldap_login():
    if current_user.is_authenticated:
        flash('You are already logged in', 'info')
        return redirect(url_for('auth.home'))

    from = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            conn = get_ldap_connection()
            conn.simple_bind_s(
                'cn=%s,dc=example,dc=org' % username, password
            )
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash('You have successfully logged in', 'success')
        return redirect(url_for('auth.home'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)


@auth.route('/facebook-login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for('facebook.login'))

    resp = facebook.get("/me?fields=name,email")

    user = User.query.filter_by(username=resp.json()['email'].first())
    if not user:
        user = User(resp.json()['email'], '')
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    flash(
        'Logged in as name=%s using Facebook login' % (
            resp.json()['name']), 'success')
    return redirect(request.args.get('next'), url_for('auth.home'))


@auth.route('/google-login')
def google_login():
    if not google.authorized:
        return redirect(url_for('google.login'))

    resp = twitter.get("/oauth2/v1/userinfo")

    user = User.query.filter_by(username=resp.json()['email']).first()
    if not user:
        user = User(resp.json()['email'],'')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash(
        'Logged in as name=%s using Google login' % (
            resp.json()['name']), 'success')
    return redirect(request.args.get('next'), url_for('auth.home'))
