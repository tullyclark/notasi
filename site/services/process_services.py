import sqlalchemy.orm
import sqlalchemy as sa
import ibm_db_sa
import datetime
import pandas
import json
import pathlib
import json
import time
import requests
from io import StringIO

import data.db_session as db_session
from data.source import Location, Query, DataView, Subtype, LocationType
from utils.json import flatten_json
from utils.split_strip import split_strip

from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, NTLM, SIMPLE


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def default(o):
	if isinstance(o, (datetime.date, datetime.datetime)):
		return o.isoformat()

def sql_select(
	query
):

	location = query.location
	connection_string = location.subtype.dialect + \
		"://" + location.username + \
		(":" + location.password if location.password else "") + \
		"@" + location.address + \
		":" + location.port + \
		("/" + location.database if location.database else "") + \
		("?driver=ODBC+DRIVER+17+for+SQL+Server" if location.subtype.dialect == 'mssql+pyodbc' else "")

	print(connection_string)

	location_engine = sa.create_engine(connection_string)
	location_connection = location_engine.connect()


	formatted_queries = []
	if query.notasi_query:
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')

		for row in notasi_query:
			key_list = list(row.keys())
			formatted_query = query.body

			for key in key_list:
				formatted_query = formatted_query.replace('{' + str(key) + '}', str(row[key]))

			formatted_queries.append(formatted_query)
	if not formatted_queries:
		formatted_queries.append(query.body)
	data = []
	for formatted_query in formatted_queries:

		df = pandas.read_sql_query(formatted_query, location_engine)
		data.append(df)

	data = json.loads(json.dumps(pandas.concat(data).to_dict('records'), default=default))
	return flatten_json(data)

def file_select(
	query
	):
	file = pathlib.Path(query.location.address) / query.endpoint
	if file.suffix =='.csv':
		df = pandas.read_csv(file)
		return flatten_json(df.to_dict('records'))
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
			try:
				data = json.loads(data_string)
			except ValueError as e:
				data = data_string
		else:
			data = []

		request_vars.append({'url':url_string, 'headers': headers,'data':data})

	if query.request_method.name == "GET":
		for request_var in request_vars:
			response = requests.get(url = request_var['url'], headers = request_var['headers'], data = request_var['data']).json()

			if type(response) == dict:
				responses.append(flatten_json(pandas.DataFrame(response, index=[0])))
			else:
				responses.append(flatten_json(pandas.DataFrame(response)))

	elif query.request_method.name == "POST":
		for request_var in request_vars:
			response = requests.post(url = request_var['url'], headers = request_var['headers'], data = request_var['data']).json()
			responses.append(pandas.DataFrame(response, index=[0]))

	result = [item for sublist in responses for item in sublist]
	return result

def selenium_select(
	query
	):
	script = query.body
	options = webdriver.ChromeOptions()
	options.addArguments("--window-size=1920,1080");
	options.addArguments("--disable-extensions");
	options.addArguments("--proxy-server='direct://'");
	options.addArguments("--proxy-bypass-list=*");
	options.addArguments("--start-maximized");
	options.addArguments("--headless");
	options.addArguments("--disable-gpu");
	options.addArguments("--disable-dev-shm-usage");
	options.addArguments("--no-sandbox");
	options.addArguments("--ignore-certificate-errors");
	driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
	loc = {"driver": driver, "options":options}
	exec(script, globals(), loc)
	return loc['output']

def ldap_select(query):

	location = query.location

	dc = 'dc=' + ',dc='.join(split_strip(location.database, "."))

	if location.subtype.name == 'Active Directory':
		auth = NTLM
	else:
		auth = SIMPLE



	server = Server(location.address, get_info=ALL)
	conn = Connection(
		server
		, 'cn=' + location.username + ',' + dc
		, location.password
		, auto_bind=True
		, authentication = auth
		)


	formatted_queries = []

	if query.notasi_query:
		notasi_query = pandas.read_sql(query.notasi_query, db_session.notasi_engine()).to_dict('records')

		for row in notasi_query:
			key_list = list(row.keys())
			formatted_query = query.body

			for key in key_list:
				formatted_query = formatted_query.replace('{' + str(key) + '}', str(row[key]))

			formatted_queries.append(formatted_query)

	if not formatted_queries:
		formatted_queries.append(query.body)

	data = []

	for formatted_query in formatted_queries:

		conn.search(dc
			, formatted_query
			, attributes=[ALL_ATTRIBUTES])

		for entry in conn.entries:
			dict1 = json.loads(entry.entry_to_json())["attributes"]
			dict1['dn'] = json.loads(entry.entry_to_json())["dn"]
			data.append(dict1)

	data = flatten_json(data)
	return(data)



def create_view(data_view, session):


	sql_text = f"create or replace view {data_view.view_name} as "

	business_keys = []
	information_columns = []

	for col in split_strip(data_view.business_keys, ","):
		business_keys.append({"json": "data ->> '" + col + "'", "name":col})

	for col in split_strip(data_view.information_columns, ","):
		information_columns.append({"json": "data ->> '" + col + "'", "name":col})

	business_keys_json_name = " , ".join([col["json"] + "as " + col["name"] for col in business_keys])
	information_columns_json_name = " , ".join([col["json"] + "as " + col["name"] for col in information_columns])

	business_keys_order = "row_number() over (partition by " + " , ".join(col["json"] for col in business_keys) + ' order by view_run_id desc) as rownum'

	all_cols = business_keys_json_name+ ', ' + information_columns_json_name + "," + business_keys_order

	col_names = " , ".join(col["name"] for col in business_keys + information_columns)

	sql_text = f'''
		create or replace view {data_view.view_name} as

			with q1 as
			(
				SELECT
					{all_cols}
					, user_data.view_run_id
				FROM
					user_data
					inner join view_runs on view_runs.id = user_data.view_run_id
				WHERE
					data_view_id = {data_view.id}
			)

			SELECT
				{col_names}
				, case
					when view_run_id = (select max(id) from view_runs where data_view_id = {data_view.id})
					then 1
					end as in_last_run
			FROM
				q1
			WHERE
				rownum = 1;


		'''

	session.execute(sql_text)
