import flask
import os
from data.source import Location, Query, DataView, User
from services.select_services import get_locations
from services.save_services import insert_user_data
from services.schedule_services import select_into_user_data
import data.db_session as db_session
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

		session = db_session.create_session()

		views = session.query(DataView) \
		.filter_by(query_id=id) \
		.all()

		session.close()

		try:
			data = select_user_data(id)
			data_string = json.dumps(data, sort_keys=True, default=default, indent=40)
		except Exception as error:
			return flask.render_template('error.html', error = str(error))
		if func == 'return':
			return data_string
		else:
			for d in data:
				for data_view in views:
					insert_user_data(d, data_view.id)
			return flask.redirect('/process')



