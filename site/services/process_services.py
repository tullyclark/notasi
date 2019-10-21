import sqlalchemy.orm
import sqlalchemy as sa
import ibm_db_sa
import datetime
import pandas
import json
import pathlib
import json
import requests
from io import StringIO

import data.db_session as db_session
from data.source import Location, Query, DataView, SqlType, LocationType
from utils.json import flatten_json
from utils.split_strip import split_strip


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def get_locations():
	session = db_session.create_session()
	locations = session.query(Location).all()
	session.close()

	return locations


def sql_select(
	query
):
	location = query.location
	engine = sa.create_engine(location.sql_type.dialect + \
		"://" + location.username + \
		":" + location.password + \
		"@" + location.address + \
		":" + location.port + \
		"/" + location.database)

	df = pandas.read_sql_query(query.body, engine)
	return df.to_dict('records')

def file_select(
	query
	):
	file = pathlib.Path(query.location.address) / query.endpoint
	if file.suffix =='.csv':
		df = pandas.read_csv(file)
		return df.to_dict('records')
	elif file.suffix =='.json':
		json_obj = json.load(file.open())
		return flatten_json(json_obj)

def http_select(
	query
	):
	
	url_string = query.location.address + query.endpoint
	headers_string = query.head if query.head else ''
	data_string = query.body if query.body else ''
	request_vars = []
	responses = []


	if query.notasi_query:
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')

		for row in notasi_query:
			key_list = list(row.keys())
			url = url_string
			headers = headers_string
			data = data_string

			for key in key_list:
				if url:
					url = url.replace('{' + str(key) + '}', str(row[key]))
				if headers:
					headers = headers.replace('{' + str(key) + '}', str(row[key]))
				if data:
					data = data.replace('{' + str(key) + '}', str(row[key]))

			if headers:
				headers = json.loads(headers)
			if data:
				data = json.loads(data)
			request_vars.append({'url': url, 'headers': headers, 'data': data})

	else:
		if headers_string:
			headers = json.loads(headers_string)
		else:
			header = []

		if data_string:
			data = json.loads(data_string)
		else:
			data = []

		request_vars.append({'url':url_string, 'headers': headers,'data':data})

	if query.request_method.name == "GET":
		for request_var in request_vars:

			response = requests.get(url = request_var['url'], headers = request_var['headers'], data = request_var['data']).json()
			responses.append(pandas.DataFrame(response))
	
	elif query.request_method.name == "POST":
		for request_var in request_vars:
			response = requests.post(url = request_var['url'], headers = request_var['headers'], data = request_var['data']).json()
			responses.append(pandas.DataFrame(response, index=[0]))
	result = pandas.concat(responses)
	return flatten_json(result.to_dict())


def create_view(view_id):

	session = db_session.create_session()
	data_view = session.query(DataView) \
		.filter_by(id=view_id) \
		.first()

	sql_text = f"create or replace view {data_view.view_name} as "

	business_keys = []
	information_columns = []
	
	for col in split_strip(data_view.business_keys, ","):
		business_keys.append({"json": "data ->> '" + col + "'", "name":col})
	
	for col in split_strip(data_view.information_columns, ","):
		information_columns.append({"json": "data ->> '" + col + "'", "name":col})

	business_keys_json_name = " , ".join([col["json"] + "as " + col["name"] for col in business_keys])
	information_columns_json_name = " , ".join([col["json"] + "as " + col["name"] for col in information_columns])

	business_keys_order = "row_number() over (partition by " + " , ".join(col["json"] for col in business_keys) + ' order by created_date desc) as rownum'

	all_cols = business_keys_json_name+ ', ' + information_columns_json_name + "," + business_keys_order
	
	col_name = " , ".join(col["name"] for col in business_keys + information_columns)

	sql_text = sql_text \
		+ f"with q1 as (select {all_cols}" \
		+ f" from user_data where data_view_id = {data_view.id}) select {col_name} from q1 where rownum = 1;"

	session.execute(sql_text)
	session.commit()
	session.close()






