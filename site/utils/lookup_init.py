from data.source import LocationType, RequestMethod, Subtype, ChartType, GroupCategory, Group
import data.db_session as db_session

def init_rows():
	location_types = [
		{'name': 'SQL'}
		, {'name': 'Folder'}
		, {'name': 'HTTP'}
		, {'name': 'LDAP'}
		, {'name': 'Notasi Users'}
		, {'name': 'Notasi Groups'}]

	request_methods = [
		{'name': 'GET'}
		, {'name': 'POST'}
	]

	subtypes = [
		{'name': 'DB2','dialect': 'db2'}
		, {'name': 'PostgreSQL','dialect': 'postgresql'}
		, {'name': 'MySQL','dialect': 'mysql+mysqldb'}
		, {'name': 'Active Directory' ,'dialect': 'Active Directory'}
		, {'name': 'LDAP3','dialect': 'LDAP3'}]

	chart_types = [
		{'name':'Line', 'type':'line'}
		,{'name':'Bar', 'type':'bar'}
		,{'name':'Horizontal Bar', 'type':'horizontalBar'}
		,{'name':'Radar', 'type':'radar'}
		,{'name':'Pie', 'type':'pie'}
		,{'name':'Doughnut', 'type':'doughnut'}
		,{'name':'Polar Area', 'type':'polarArea'}]

	session = db_session.create_session()
	try:	
		for location_type in location_types:
			init_location_type(location_type.get("name"), session)	

		for request_method in request_methods:
			init_request_method(request_method.get("name"), session)

		for subtype in subtypes:
			init_subtype(subtype.get("name"), subtype.get("dialect"), session)

		for chart_type in chart_types:
			init_chart_type(chart_type.get("name"), chart_type.get("type"), session)

		group_category = session.query(GroupCategory).filter_by(name='Access Level Groups').first()
		
		if not group_category:
			group_category = GroupCategory()
			group_category.name = 'Access Level Groups'
			session.add(group_category)

		group = session.query(Group).filter_by(name='Administrators', group_category_id = group_category.id).first()
		
		if not group:
			group = Group()
			group.name = 'Administrators'
			group.group_category_id = group_category.id
			session.add(group)

	except Exception as error:
		print(str(error))
	finally:
		session.commit()
		session.close()


def init_location_type(name, session):
    if not session.query(LocationType).filter_by(name=name).first():
    	location_type = LocationType()
    	location_type.name = name
    	session.add(location_type)

def init_request_method(name, session):
    if not session.query(RequestMethod).filter_by(name=name).first():
    	request_method = RequestMethod()
    	request_method.name = name
    	session.add(request_method)

def init_subtype(name, dialect, session):
    if not session.query(Subtype).filter_by(name=name, dialect=dialect).first():
    	subtype = Subtype()
    	subtype.name = name
    	subtype.dialect = dialect
    	session.add(subtype)

def init_chart_type(name, type, session):
    if not session.query(ChartType).filter_by(name=name, chart_type=type).first():
    	chart_type = ChartType()
    	chart_type.name = name
    	chart_type.chart_type = type
    	session.add(chart_type)