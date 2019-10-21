import flask
import os
from data.source import Location, Query, DataView, User
from services.select_services import get_locations
from services.save_services import save_user
from services.schedule_services import select_into_user_data
import datetime
import json
from flask_login import login_required


template_dir = os.path.abspath('../templates/process/')
blueprint = flask.Blueprint('process', __name__, template_folder = template_dir)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

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
		try:
			data = json.dumps(select_into_user_data(id, func), sort_keys=True, default=default, indent=40)
		except Exception as error:
			return flask.render_template('error.html', error = str(error))
		if func == 'return':
			return data
		else:
			return flask.redirect('/process')



