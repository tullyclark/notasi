
from data.source import Query
from services.process_services import sql_select, file_select, http_select, selenium_select, ldap_select
from services.user_group_services import update_users, update_groups, update_user_groups
import sqlalchemy.orm


def select_user_data(query_id, session):

	query = session.query(Query).options(sqlalchemy.orm.joinedload('*')) \
		.filter_by(id=query_id) \
		.first()

	location_type_name =  query.location.location_type.name

	try:
		if location_type_name =='SQL':
			data_list = sql_select(query)

		if location_type_name =='Folder':
			data_list = file_select(query)

		if location_type_name =='HTTP':
			data_list = http_select(query)

		if location_type_name =='Selenium':
			data_list = selenium_select(query)

		if location_type_name =='LDAP':
			data_list = ldap_select(query)

		if location_type_name =='Notasi Users':
			data_list = update_users(query, session)

		if location_type_name =='Notasi Groups':
			update_groups(query, session)
			update_user_groups(query, session)
			data_list = []


	except Exception as error:
		raise

	return(data_list)
