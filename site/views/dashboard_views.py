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


template_dir = os.path.abspath('./templates/dashboard/')
blueprint = flask.Blueprint('dashboard', __name__, template_folder = template_dir)


@login_required
@blueprint.route('/')
def index():
    return flask.render_template('dashboard_index.html',
    	dashboards = get_objects(Dashboard))

@login_required
@blueprint.route('/edit', methods=['GET', 'POST'])
def edit():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'dashboard_edit.html'
			, item_type = 'dashboard'
			, back_link = flask.request.referrer
			, data_obj = search_object(id, Dashboard)
			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('dashboard', id, data)
		return flask.redirect('/dashboard')


@blueprint.route('/dashboard_chart/edit', methods=['GET', 'POST'])
def dashboard_chart_edit():
	id = flask.request.args.get('id', default = None, type = int)
	dashboard_id = flask.request.args.get('dashboard_id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'dashboard_chart_edit.html'
			, item_type = 'dashboard_chart'
			, dashboard = search_object(dashboard_id, Dashboard)
			, back_link = flask.request.referrer
			, charts = get_objects(Chart)

			)

	if flask.request.method == "POST":
		data = flask.request.form
		save_object('dashboard_chart', id, data)
		return flask.redirect('/dashboard/dashboard_chart/edit?dashboard_id=' + str(dashboard_id))



@login_required
@blueprint.route('/run/<id>')
def run(id: int):
	mode = flask.request.args.get('mode', default = None, type = str)
	dashboard =search_object(id, Dashboard)
	charts = []
	for dashboard_chart in dashboard.dashboard_charts:
		charts.append(run_chart(dashboard_chart.chart_id))

	return flask.render_template(
		'dashboard_run.html'
		, charts = charts
		, mode=mode)

