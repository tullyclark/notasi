
from data.source import Location, Query, DataView, SqlType, LocationType
from services.process_services import sql_select, file_select, http_select
from services.save_services import insert_user_data
from app import scheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
from services.select_services import search_object
import data.db_session as db_session
import sqlalchemy.orm

def schedule_query(id):
	session = db_session.create_session()
	query = session.query(Query).options(sqlalchemy.orm.joinedload('*')) \
		.filter_by(id=id) \
		.first()
	if query.cron_schedule:
		job = scheduler.add_job(select_into_user_data
			, CronTrigger.from_crontab(query.cron_schedule)
			, id=str(query.id)
			, replace_existing=True
			, kwargs=
			{ "query_id": id})
	session.close()

def select_into_user_data(query_id, action):
	print("start: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
	session = db_session.create_session()
	query = session.query(Query).options(sqlalchemy.orm.joinedload('*')) \
		.filter_by(id=query_id) \
		.first()

	location_type_name =  query.location.location_type.name
	views = query.views

	if location_type_name =='SQL':
		data_list = sql_select(query)

	if location_type_name =='Folder':
		data_list = file_select(query)

	if location_type_name =='HTTP':
		data_list = http_select(query)
	
	if action =="return":
		return(data_list)
	
	for d in data_list:
		for data_view in views:
			insert_user_data(d, data_view.id)
	print("stop: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
	session.close()