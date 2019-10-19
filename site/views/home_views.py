import flask
from flask_login import login_required

blueprint = flask.Blueprint('home', __name__, template_folder = 'templates')


@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 
    
@blueprint.route('/')
def index():
    return flask.render_template('home/index.html')