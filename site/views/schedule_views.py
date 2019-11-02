import flask
import pandas
import data.db_session as db_session
from services.select_services import get_objects, search_object
from services.save_services import save_object
from data.source import Schedule, Query
from flask_login import login_required
from decorators.admin import is_admin


blueprint = flask.Blueprint('schedule', __name__, template_folder = '../templates/schedule')
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
		schedules = get_objects(Schedule, session)
	except Exception as error:
		print(str(error))
	finally:
		session.close()


	return flask.render_template(
		'schedule_index.html'
		,schedules = schedules
	)


@blueprint.route('/edit', methods=['GET', 'POST'])
def edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			data_obj = search_object(id, Schedule, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()


		return flask.render_template(
			'schedule_edit.html'
			, item_type = 'schedule'
			, data_obj = data_obj
			, back_link = flask.request.referrer

			)

	if flask.request.method == "POST":
		data = flask.request.form
		session = db_session.create_session()
		try:
			save_object('schedule', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/schedule')


@blueprint.route('/schedule_step/edit', methods=['GET', 'POST'])
def schedule_edit():
	id = flask.request.args.get('id', default = None, type = int)
	schedule_id = flask.request.args.get('schedule_id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			schedule = search_object(schedule_id, Schedule, session)
			queries = get_objects(Query, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()


		return flask.render_template(
			'schedule_step_edit.html'
			, item_type = 'schedule_step'
			, schedule = schedule
			, back_link = flask.request.referrer
			, queries = queries

			)

	if flask.request.method == "POST":
		data = flask.request.form
		session = db_session.create_session()
		try:
			save_object('schedule_step', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/schedule/schedule_step/edit?schedule_id=' + str(schedule_id))
