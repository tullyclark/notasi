import flask
import pandas
from data.source import Location, Query, DataView, User
from services.select_services import get_locations
import json
from flask_login import login_required
from services.query_services import run_query
from decorators.admin import is_admin

blueprint = flask.Blueprint('process', __name__)


@blueprint.before_request
@login_required
@is_admin

def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')
def index():
    return flask.render_template('process/index.html', locations = get_locations())


@blueprint.route('/run/query/<id>/<func>', methods=['POST', 'GET'])
def run(id: int, func: str):
	if flask.request.method == "GET":

		data = run_query(id, func)
		if data:
			return flask.render_template('shared/test_response.html', table = pandas.DataFrame(data).to_html())
		return flask.redirect('/process')



