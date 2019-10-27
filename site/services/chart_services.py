import pandas
import data.db_session as db_session
from data.source import Chart, UserGroup
from flask_login import current_user
from utils.color_palette import generate_color_palette
from utils.split_strip import split_strip
import random

def run_chart(id):
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

	session.close()

	notasi_query = pandas.read_sql(query, db_session.notasi_engine()).to_dict('records')
	
	color_palette = generate_color_palette(len(notasi_query))
	random.shuffle(color_palette)

	value_sets = []
	for col in split_strip(chart.value_columns, ","):
		value_sets.append([d[col] for d in notasi_query])


	return({"chart_type": chart_type, \
		"color_palette": color_palette, \
		"value_sets": value_sets, \
		"labels": [d[chart.label_column] for d in notasi_query], \
		"chart": chart, \
		"id": chart.id, \
		"name": chart.name})