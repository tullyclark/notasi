# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login
from data.source import User
from data import db_session
import requests
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from config import config_idp

auth = Blueprint('auth', __name__, template_folder = '../templates/auth')


metadata_url_for = {
    # For testing with http://saml.oktadev.com use the following:
    'test': 'https://kambala-login.cloudworkengine.net/saml2/idp/SSOService.php',
    # WARNING WARNING WARNING
    #   You MUST remove the testing IdP from a production system,
    #   as the testing IdP will allow ANYBODY to log in as ANY USER!
    # WARNING WARNING WARNING
    }


def saml_client_for(idp_name=None):
    '''
    Given the name of an IdP, return a configuation.
    The configuration is a hash for use by saml2.config.Config
    '''

    if idp_name not in metadata_url_for:
        raise Exception("Settings for IDP '{}' not found".format(idp_name))
    acs_url = url_for(
        "auth.idp_initiated",
        idp_name=idp_name,
        _external=True)
    https_acs_url = url_for(
        "auth.idp_initiated",
        idp_name=idp_name,
        _external=True,
        _scheme='https')

    #   SAML metadata changes very rarely. On a production system,
    #   this data should be cached as approprate for your production system.
    rv = requests.get(metadata_url_for[idp_name])

    settings = {
        'metadata': {
            'inline': [rv.text],
            },
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST),
                        (https_acs_url, BINDING_HTTP_REDIRECT),
                        (https_acs_url, BINDING_HTTP_POST)
                    ],
                },
                # Don't verify that the incoming requests originate from us via
                # the built-in cache for authn request ids in pysaml2
                'allow_unsolicited': True,
                # Don't sign authn requests, since signed requests only make
                # sense in a situation where you control both the SP and IdP
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': False,
            },
        },
        "xmlsec_binary" : "/usr/lib/x86_64-linux-gnu/libxmlsec1.so"
    }
    spConfig = Saml2Config()
    spConfig.load(settings)
    spConfig.allow_unknown_attributes = True
    saml_client = Saml2Client(config=spConfig)
    return saml_client


@auth.route("/")
def main_page():
    return render_template('main_page.html', idp_dict=metadata_url_for)


@auth.route("/saml/sso/<idp_name>", methods=['POST'])
def idp_initiated(idp_name):
    saml_client = saml_client_for(idp_name)
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        entity.BINDING_HTTP_POST)
    authn_response.get_identity()
    user_info = authn_response.get_subject()
    username = user_info.text

    user = User(username)
    session['saml_attributes'] = authn_response.ava
    login_user(user)
    url = url_for('user')
    # NOTE:
    #   On a production system, the RelayState MUST be checked
    #   to make sure it doesn't contain dangerous URLs!
    if 'RelayState' in request.form:
        url = request.form['RelayState']
    return redirect(url)


@auth.route("/saml/login/<idp_name>")
def sp_initiated(idp_name):
    saml_client = saml_client_for(idp_name)
    reqid, info = saml_client.prepare_for_authenticate()

    redirect_url = None
    # Select the IdP URL to send the AuthN request to
    for key, value in info['headers']:
        if key is 'Location':
            redirect_url = value
    response = redirect(redirect_url, code=302)
    # NOTE:
    #   I realize I _technically_ don't need to set Cache-Control or Pragma:
    #     http://stackoverflow.com/a/5494469
    #   However, Section 3.2.3.2 of the SAML spec suggests they are set:
    #     http://docs.oasis-open.org/security/saml/v2.0/saml-bindings-2.0-os.pdf
    #   We set those headers here as a "belt and suspenders" approach,
    #   since enterprise environments don't always conform to RFCs
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response







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