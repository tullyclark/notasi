import flask
import pandas
import data.db_session as db_session
from services.select_services import get_objects, search_object
from services.save_services import save_object
from data.source import Schedule, Query
from flask_login import login_required


blueprint = flask.Blueprint('schedule', __name__, template_folder = '../templates/schedule')
@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')

def index():

	return flask.render_template(
		'schedule_index.html'
		,schedules = get_objects(Schedule)
	)

@login_required
@blueprint.route('/edit', methods=['GET', 'POST'])
def edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'schedule_edit.html'
			, item_type = 'schedule'
			, data_obj = search_object(id, Schedule)
			, back_link = flask.request.referrer

			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('schedule', id, data)
		return flask.redirect('/schedule')

@blueprint.route('/schedule_step/edit', methods=['GET', 'POST'])
def schedule_edit():
	id = flask.request.args.get('id', default = None, type = int)
	schedule_id = flask.request.args.get('schedule_id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'schedule_step_edit.html'
			, item_type = 'schedule_step'
			, schedule = search_object(schedule_id, Schedule)
			, back_link = flask.request.referrer
			, queries = get_objects(Query)

			)

	if flask.request.method == "POST":
		data = flask.request.form
		print(data)
		save_object('schedule_step', id, data)
		return flask.redirect('/schedule/schedule_step/edit?schedule_id=' + str(schedule_id))
