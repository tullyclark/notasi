import flask
import os
from data.source import Location, Query, DataView, User
from services.select_services import get_locations
from services.save_services import save_user
from services.schedule_services import schedule_query, select_into_user_data
import json
from flask_login import login_required


template_dir = os.path.abspath('../templates/process/')
blueprint = flask.Blueprint('process', __name__, template_folder = template_dir)


@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')
def index():
    return flask.render_template('index.html', locations = get_locations())


@blueprint.route('/run/query/<id>/<func>', methods=['POST', 'GET'])
def run(id: int, func: str):
	if flask.request.method == "GET":
		data = select_into_user_data(id, func)
		if func == 'return':
			return json.dumps(data, sort_keys=True)
		else:
			return flask.redirect('/process')



