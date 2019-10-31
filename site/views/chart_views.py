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
    return flask.render_template('chart_index.html', charts = get_objects(Chart))

@blueprint.route('/edit', methods=['GET', 'POST'])
def chart_edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'chart_edit.html'
			, item_type = 'chart'
			, data_obj = search_object(id, Chart)
			, back_link = flask.request.referrer
			, chart_types = get_objects(ChartType)

			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('chart', id, data)
		return flask.redirect('/chart')



@blueprint.route('/run/<id>')
def run(id: int):
	charts = []
	pages = []
	try:
		for chart in run_chart(id):
				charts.append(chart)
				if  chart["page"] and chart["page"] not in pages:
					pages.append(chart["page"])
	except Exception as error:
		message = str(type(error).__name__) +': ' +str(error)
		return flask.render_template(
		'./process/error.html',
		 error = message)

	return flask.render_template(
		'dashboard_run.html'
		, charts = charts
		, pages = pages)

