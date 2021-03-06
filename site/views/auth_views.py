# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session as flask_session
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from data.source import User, Group, UserGroup, GroupCategory
from data import db_session
from config import login_default
from decorators.admin import is_admin

auth = Blueprint('auth', __name__, template_folder = '../templates/auth')



@auth.route('/login', methods=['GET', 'POST'])
def login():
    next_dest = request.args.get('next', default = "/", type = str)
    if login_default == 'sso':
        return redirect(url_for('sso.index',  sso = 1, next = next_dest))
    elif login_default == 'local':
        return redirect(url_for('auth.local',  next = next_dest))

@auth.route('/local', methods=['GET', 'POST'])
def local():
    next_dest = request.args.get('next', default = "/", type = str)

    if request.method =='GET':
        next = request.args.get('next', default = "/", type = int)
        session = db_session.create_session()
        try:
            count = session.query(User).count()
        finally:
            session.close()

        if count == 0:
            return redirect(url_for('auth.signup'))
        return render_template('login.html', next_dest = next_dest)
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        session = db_session.create_session()
        try:
            user = session.query(User).filter_by(username=username).first()
        finally:
            session.close()
        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password): 
            return redirect(url_for('auth.local')) # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        flask_login.login_user(user, remember=remember)
        return redirect(next_dest)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    session = db_session.create_session()
    try:
        count = session.query(User).count()
    finally:
        session.close()

    if count > 0:
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':

        username = request.form.get('username')
        name = request.form.get('name')
        password = request.form.get('password')


        session = db_session.create_session()

        try:
            new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))
            session.add(new_user)
            session.commit()
            admin_group = session.query(Group) \
                .join(GroupCategory) \
                .filter(Group.name=='Administrators') \
                .filter(GroupCategory.name == 'Access Level Groups') \
                .first()
            user_group = UserGroup(user_id = new_user.id, group_id = admin_group.id)

            # add the new user to the database
            session.add(user_group)
            session.commit()
        finally:
            session.close()
        return redirect(url_for('auth.login'))


@auth.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    # if 'samlUserdata' in flask_session:
    #     return redirect('/sso/?slo')
    return redirect('/')
