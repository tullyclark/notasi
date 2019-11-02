import pandas
from flask import abort
import data.db_session as db_session
from data.source import Chart, UserGroup
from flask_login import current_user
from utils.color_palette import generate_color_palette
from utils.split_strip import split_strip
import random
import collections

def run_chart(id, session):
	chart = session.query(Chart) \
		.filter_by(id=id)\
		.first()
	chart_type = chart.chart_type.chart_type

	user_groups = session.query(UserGroup) \
		.filter_by(user_id=current_user.id)\
		.all()


	####### COLUMN ACCESS ############

	groups = []
	for user_group in user_groups:
		groups.append(user_group.group.group_category.name + '.' + user_group.group.name)

	sql_cols = []
	
	if chart.access_columns.strip():
		cols = split_strip(chart.access_columns, ",")
		for col in cols:
			q = col + " in ('" + "','".join(groups) + "')"
			sql_cols.append(q)
	
	sql_cols_concat = " OR ".join(sql_cols)

	query = chart.notasi_query
	if  sql_cols_concat:
		query = "select * from (" + query + ") as tab1 where " + sql_cols_concat


	####### COLUMN GROUPS ############

	if chart.access_groups.strip():
		access_groups = split_strip(chart.access_groups, ",")
		match = set(groups) & set(access_groups)
		if not match and not sql_cols:
			abort(401)



	###########GET DATA ##############
	notasi_query = pandas.read_sql(query, db_session.notasi_engine()).to_dict('records')

	####### COLORS ############
	





	###########SPLIT CHART ON COL ##############

	charts = []
	result_list = []


	if chart.page_column:

		result = collections.defaultdict(list)

		for d in notasi_query:
		    result[d[chart.page_column]].append(d)

		result_list = list(result.values())

	else:
		result_list.append(notasi_query)


	for l in result_list:
		value_sets = []
		for col in split_strip(chart.value_columns, ","):
			value_sets.append([d[col] for d in l])


		color_palettes = []
		random_palette = generate_color_palette(len(l))
		random.shuffle(random_palette)

		if not chart.color_columns:
			for value_set in value_sets:
				color_palettes.append(random_palette)
		else:
			for col in split_strip(chart.color_columns, ","):
				if col.lower()=='random':
					color_palettes.append(random_palette)
				else:
					raw_palette = [d[col] for d in l]
					rgb_palette = []
					for color in raw_palette:
						if color.startswith("#"):
							rgb_palette.append(",".join([str(int(color.strip("#")[i:i+2], 16)) for i in (0, 2, 4)]))
						else:
							rgb_palette.append(color)
					color_palettes.append(rgb_palette)

		charts.append({"page": l[0].get(chart.page_column), \
		"chart_type": chart_type, \
		"color_palettes": color_palettes, \
		"value_sets": value_sets, \
		"x_categories": [d[chart.x_categories] for d in l], \
		"dataset_legends": split_strip(chart.dataset_legends, ","), \
		"chart": chart, \
		"options": chart.options, \
		"id": chart.id, \
		"name": chart.name})





	return(charts)