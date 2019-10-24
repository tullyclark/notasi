import flask
import os
import pandas
from data.source import Endpoint, RequestMethod, DataView
from services.select_services import get_objects, search_object
from services.save_services import save_object
import data.db_session as db_session
import datetime
import json
from flask_login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text


template_dir = os.path.abspath('./templates/api/')
blueprint = flask.Blueprint('api', __name__, template_folder = template_dir)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()



@login_required
@blueprint.route('/')
def index():
    return flask.render_template('api_index.html', endpoints = get_objects(Endpoint))



@login_required
@blueprint.route('/edit', methods=['GET', 'POST'])
def edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'edit.html'
			, item_type = 'endpoint'
			, data_obj = search_object(id, Endpoint)
			, back_link = flask.request.referrer
			, request_methods = get_objects(RequestMethod)

			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('endpoint', id, data)
		return flask.redirect('/api')



@blueprint.route('/<category>/<endpoint_location>', methods=['GET'])
def run(category: str, endpoint_location: str):
	session = db_session.create_session()
	endpoint = session.query(Endpoint) \
		.filter_by(endpoint_location=endpoint_location, category=category)\
		.first()
	session.close()

	key = flask.request.headers.get('key')
	if not check_password_hash(endpoint.key, key):
		return "Unauthorised", 401


	
	data = flask.request.data.decode('utf-8')
	args = flask.request.args.to_dict()


	data_dict = dict()
	if data:
		data_dict = json.loads(data)
	else:
		for key in args:
			data_dict[key] = args[key]



	notasi_query_string = "select * from (" \
		+ endpoint.notasi_query \
		+") as tab1"

	where_list = []

	for key in data_dict:
		where_list.append("lower(" + key + ") = lower(:" + key +")")

	if where_list:
		notasi_query_string = notasi_query_string + " where " + " AND ".join(where_list)
	t = text(notasi_query_string)

	try:
		notasi_query = pandas.read_sql(t, db_session.notasi_engine(), params=data_dict).to_dict('records')
		return (json.dumps(notasi_query, default=default))
	except Exception as error:
		return str(error)


