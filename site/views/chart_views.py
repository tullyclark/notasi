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



template_dir = os.path.abspath('./templates/chart/')
blueprint = flask.Blueprint('chart', __name__, template_folder = template_dir)

@blueprint.before_request
@login_required
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
	chart = run_chart(id)

	return flask.render_template(
		'chart_run.html'
		, chart = chart["chart"]
		, values = chart["values"]
		, labels = chart["labels"]
		, type = chart["chart_type"]
		, color_palette = chart["color_palette"])

