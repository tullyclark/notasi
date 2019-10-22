
from data.source import Location, Query, DataView, SqlType, LocationType
from services.process_services import sql_select, file_select, http_select
# from uwsgi import scheduler
# from apscheduler.triggers.cron import CronTrigger
import datetime
from services.select_services import search_object
import data.db_session as db_session
import sqlalchemy.orm


def select_user_data(query_id):
	print("start: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
	session = db_session.create_session()
	query = session.query(Query).options(sqlalchemy.orm.joinedload('*')) \
		.filter_by(id=query_id) \
		.first()

	location_type_name =  query.location.location_type.name

	if location_type_name =='SQL':
		data_list = sql_select(query)

	if location_type_name =='Folder':
		data_list = file_select(query)

	if location_type_name =='HTTP':
		data_list = http_select(query)

	print("stop: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
	return(data_list)
	
	session.close()