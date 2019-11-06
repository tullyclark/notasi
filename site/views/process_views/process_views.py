import flask
import pandas
from data.source import Location, Query, DataView, User
from services.select_services import get_objects
import json
from flask_login import login_required
from services.query_services import run_query
from decorators.admin import is_admin
import data.db_session as db_session

blueprint = flask.Blueprint('process', __name__)


@blueprint.before_request
@login_required
@is_admin

def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')
def index():

	session = db_session.create_session()
	try:
		locations = get_objects(Location, session)
	except Exception as error:
		print(str(error))
	finally:
		session.close()

	return flask.render_template('process/index.html', locations = locations)


@blueprint.route('/run/query/<id>/<func>', methods=['POST', 'GET'])
def run(id: int, func: str):
	if flask.request.method == "GET":
		try:
			data = run_query(id, func)
		except Exception as error:
			message = str(type(error).__name__) +': ' +str(error)
			temp = flask.render_template(
				'process/error.html',
				error = message)
		temp = flask.render_template('shared/test_response.html', table = pandas.DataFrame(data).to_html())

		return temp



