import flask
import os
import pandas
import json
import data.db_session as db_session
from flask_login import login_required
from data.source import Chart, Dashboard
from services.select_services import get_objects, search_object
from services.save_services import save_object
from services.chart_services import run_chart
from decorators.admin import is_admin


template_dir = os.path.abspath('./templates/dashboard/')
blueprint = flask.Blueprint('dashboard', __name__, template_folder = template_dir)

@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

@blueprint.route('/')
@is_admin
def index():

	session = db_session.create_session()
	try:
		dashboards = get_objects(Dashboard, session)
	except Exception as error:
		print(str(error))
	finally:
		session.close()

	return flask.render_template('dashboard_index.html',dashboards = dashboards)



@blueprint.route('/edit', methods=['GET', 'POST'])
@is_admin
def edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			data_obj = search_object(id, Dashboard, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()


		return flask.render_template(
			'dashboard_edit.html'
			, item_type = 'dashboard'
			, back_link = flask.request.referrer
			, data_obj = data_obj
			)

	if flask.request.method == "POST":
		data = flask.request.form		
		session = db_session.create_session()
		try:
			save_object('dashboard', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/dashboard')





@blueprint.route('/dashboard_chart/edit', methods=['GET', 'POST'])
@is_admin
def dashboard_chart_edit():
	id = flask.request.args.get('id', default = None, type = int)
	dashboard_id = flask.request.args.get('dashboard_id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			charts = get_objects(Chart, session)
			dashboard = search_object(dashboard_id, Dashboard, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()

		return flask.render_template(
			'dashboard_chart_edit.html'
			, item_type = 'dashboard_chart'
			, dashboard = dashboard
			, back_link = flask.request.referrer
			, charts = charts

			)

	if flask.request.method == "POST":
		data = flask.request.form		
		session = db_session.create_session()
		try:
			save_object('dashboard_chart', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/dashboard/dashboard_chart/edit?dashboard_id=' + str(dashboard_id))



@blueprint.route('/run/<id>')
def run(id: int):

	session = db_session.create_session()
	try:
		dashboard =search_object(id, Dashboard, session)
		charts = []
		pages = []
		for dashboard_chart in dashboard.dashboard_charts:
			for chart in run_chart(dashboard_chart.chart_id, session):
				charts.append(chart)
				if chart["page"] and chart["page"] not in pages:
					pages.append(chart["page"])
		return flask.render_template(
			'dashboard_run.html'
			, charts = charts
			, pages = pages)

	except Exception as error:
		print(str(error))
	finally:
		session.close()
	



