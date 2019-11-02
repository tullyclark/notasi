import flask
import os
import pandas
import json
import data.db_session as db_session
from flask_login import login_required
from data.source import Chart, ChartType
from services.select_services import get_objects, search_object
from services.save_services import save_object
from services.chart_services import run_chart
from decorators.admin import is_admin



template_dir = os.path.abspath('./templates/dashboard/')
blueprint = flask.Blueprint('chart', __name__, template_folder = template_dir)

@blueprint.before_request
@login_required
@is_admin
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

@blueprint.route('/')
def chart_index():

	session = db_session.create_session()
	try:
		charts = get_objects(Chart, session)
	except Exception as error:
		print(str(error))
	finally:
		session.close()

	return flask.render_template('chart_index.html', charts = charts)

@blueprint.route('/edit', methods=['GET', 'POST'])
def chart_edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":

		session = db_session.create_session()
		try:
			chart_types = get_objects(ChartType, session)
			data_obj = search_object(id, Chart, session)
		except Exception as error:
			print(str(error))
		finally:
			session.close()

		return flask.render_template(
			'chart_edit.html'
			, item_type = 'chart'
			, data_obj = data_obj
			, back_link = flask.request.referrer
			, chart_types = chart_types

			)

	if flask.request.method == "POST":
		data = flask.request.form
		session = db_session.create_session()
		try:
			save_object('chart', id, data, session)
			session.commit()
		except Exception as error:
			print(str(error))
		finally:
			session.close()
		return flask.redirect('/chart')



@blueprint.route('/run/<id>')
def run(id: int):
	charts = []
	pages = []
	session = db_session.create_session()
	try:
		for chart in run_chart(id, session):
				charts.append(chart)
				if  chart["page"] and chart["page"] not in pages:
					pages.append(chart["page"])

		temp = flask.render_template(
			'dashboard_run.html'
			, charts = charts
			, pages = pages)

	except Exception as error:
		message = str(type(error).__name__) +': ' +str(error)
		temp = flask.render_template(
		'./process/error.html',
		 error = message)

	finally:
		session.close()
		return temp

