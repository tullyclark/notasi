# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from data.source import User
from data import db_session

auth = Blueprint('auth', __name__, template_folder = '../templates/auth')

@auth.route('/login')
def login():

    session = db_session.create_session()
    count = session.query(User).count()
    session.close()

    if count == 0:
        return redirect(url_for('auth.signup'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    session = db_session.create_session()
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = session.query(User).filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    flask_login.login_user(user, remember=remember)
    session.close()
    return redirect(url_for('home.index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    session = db_session.create_session()
    count = session.query(User).count()
    session.close()

    if count > 0:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        session = db_session.create_session()

        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')

        user = session.query(User).filter_by(username=username).first() # if this returns a user, then the username already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again  
            return redirect(url_for('auth.signup'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        session.add(new_user)
        session.commit()

        session.close()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect('/')