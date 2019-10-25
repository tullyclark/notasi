import flask
import os
import pandas
import json
import data.db_session as db_session
from flask_login import login_required, current_user
from data.source import Chart, ChartType, UserGroup
from services.select_services import get_objects, search_object
from services.save_services import save_object
from utils.color_palette import generate_color_palette
from utils.split_strip import split_strip
import random


template_dir = os.path.abspath('./templates/dashboard/')
blueprint = flask.Blueprint('dashboard', __name__, template_folder = template_dir)


@login_required
@blueprint.route('/chart')
def chart_index():
    return flask.render_template('chart_index.html', charts = get_objects(Chart))

@login_required
@blueprint.route('/chart/edit', methods=['GET', 'POST'])
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
		return flask.redirect('/dashboard/chart')



@login_required
@blueprint.route('/chart/run/<id>')
def chart_raw(id: int):

	session = db_session.create_session()
	chart = session.query(Chart) \
		.filter_by(id=id)\
		.first()
	chart_type = chart.chart_type.chart_type


	user_groups = session.query(UserGroup) \
		.filter_by(user_id=current_user.id)\
		.all()

	groups = []
	for user_group in user_groups:
		groups.append(user_group.group.name)
	
	sql_cols = []
	
	if chart.access_groups.strip():
		cols = split_strip(chart.access_groups, ",")
		for col in cols:
			q = col + " in ('" + "','".join(groups) + "')"
			sql_cols.append(q)
	
	sql_cols_concat = " OR ".join(sql_cols)

	query = chart.notasi_query
	if  sql_cols_concat:
		query = "select * from (" + query + ") as tab1 where " + sql_cols_concat
	
	print(query)
	session.close()

	try:
		notasi_query = pandas.read_sql(query, db_session.notasi_engine()).to_dict('records')
	except Exception as error:
		return str(error)


	color_palette = generate_color_palette(len(notasi_query))
	random.shuffle(color_palette)

	return flask.render_template(
		'chart_run.html'
		, chart = chart
		, values = [d['value'] for d in notasi_query]
		, labels = [d['label'] for d in notasi_query]
		, type = chart_type
		, color_palette = color_palette)

