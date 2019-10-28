import sqlalchemy as sa
import datetime

from data.modelbase import SqlAlchemyBase
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from flask_login import UserMixin
import config


class Subtype(SqlAlchemyBase):

	__tablename__ = 'subtypes'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	dialect = sa.Column(sa.String)
	driver = sa.Column(sa.String)
	locations = sa.orm.relationship("Location")

class RequestMethod(SqlAlchemyBase):

	__tablename__ = 'request_methods'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	queries = sa.orm.relationship("Query")

class LocationType(SqlAlchemyBase):

	__tablename__ = 'location_types'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	locations = sa.orm.relationship("Location")

class Location(SqlAlchemyBase):

	__tablename__ = 'locations'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	location_type_id = sa.Column(sa.Integer, sa.ForeignKey('location_types.id'))
	location_type = sa.orm.relationship("LocationType")
	address = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	port = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	username = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	password = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	subtype_id = sa.Column(sa.Integer, sa.ForeignKey('subtypes.id'))
	subtype = sa.orm.relationship("Subtype")
	database = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	queries = sa.orm.relationship("Query")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class Query(SqlAlchemyBase):
	
	__tablename__ = 'queries'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	notasi_query = sa.Column(sa.String)
	endpoint = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	head = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	body = sa.Column(EncryptedType(sa.String,
                                       config.sqlalchemy_secret_key,
                                       AesEngine,
                                       'pkcs5'))
	request_method_id = sa.Column(sa.Integer, sa.ForeignKey('request_methods.id'))
	request_method = sa.orm.relationship("RequestMethod")
	location_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'), nullable=False)
	location = sa.orm.relationship("Location")
	views = sa.orm.relationship("DataView")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class DataView(SqlAlchemyBase):
	
	__tablename__ = 'data_views'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String, nullable=False)
	view_name = sa.Column(sa.String, nullable=False)
	business_keys = sa.Column(sa.String, nullable=False)
	information_columns = sa.Column(sa.String, nullable=False)
	query_id = sa.Column(sa.Integer, sa.ForeignKey('queries.id'), nullable=False)
	query = sa.orm.relationship("Query")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class ViewRun(SqlAlchemyBase):
	
	__tablename__ = 'view_runs'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)
	data_view_id = sa.Column(sa.Integer, sa.ForeignKey('data_views.id', ondelete='SET NULL'))
	data_view = sa.orm.relationship("DataView")

class UserData(SqlAlchemyBase):
	
	__tablename__ = 'user_data'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	data = sa.Column(postgresql.JSONB)
	view_run_id = sa.Column(sa.Integer, sa.ForeignKey('view_runs.id'))
	view_run = sa.orm.relationship("ViewRun")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class Schedule(SqlAlchemyBase):
	
	__tablename__ = 'schedules'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	schedule_steps = sa.orm.relationship("ScheduleStep")
	cron_schedule = sa.Column(sa.String)

class ScheduleStep(SqlAlchemyBase):
	
	__tablename__ = 'schedule_steps'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	schedule_id = sa.Column(sa.Integer, sa.ForeignKey('schedules.id'), nullable=False)
	schedule = sa.orm.relationship("Schedule")
	query_id = sa.Column(sa.Integer, sa.ForeignKey('queries.id'), nullable=False)
	query = sa.orm.relationship("Query")


class User(UserMixin, SqlAlchemyBase):
	__tablename__ = 'notasi_users'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	username = sa.Column(sa.String, unique=True)
	password = sa.Column(sa.String)
	name = sa.Column(sa.String)
	user_groups = sa.orm.relationship("UserGroup")

class Group(SqlAlchemyBase):

	__tablename__ = 'notasi_groups'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	group_category_id = sa.Column(sa.Integer, sa.ForeignKey('notasi_group_categories.id'), nullable=False)
	group_category = sa.orm.relationship("GroupCategory")
	user_groups = sa.orm.relationship("UserGroup")

class GroupCategory(SqlAlchemyBase):

	__tablename__ = 'notasi_group_categories'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	groups = sa.orm.relationship("Group")


class UserGroup(SqlAlchemyBase):

	__tablename__ = 'notasi_user_group'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	group_id = sa.Column(sa.Integer, sa.ForeignKey('notasi_groups.id'), nullable=False)
	group = sa.orm.relationship("Group")
	user_id = sa.Column(sa.Integer, sa.ForeignKey('notasi_users.id'), nullable=False)
	user = sa.orm.relationship("User")



class Endpoint(SqlAlchemyBase):
	
	__tablename__ = 'endpoints'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	category = sa.Column(sa.String)
	endpoint_location = sa.Column(sa.String)
	request_method_id = sa.Column(sa.Integer, sa.ForeignKey('request_methods.id'))
	request_method = sa.orm.relationship("RequestMethod")
	key = sa.Column(sa.String)
	notasi_query = sa.Column(sa.String)
	request_body = sa.Column(sa.String)
	response_body = sa.Column(sa.String)
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)


class Dashboard(SqlAlchemyBase):
	
	__tablename__ = 'dashboards'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	dashboard_charts = sa.orm.relationship("DashboardChart")


class DashboardChart(UserMixin, SqlAlchemyBase):

	__tablename__ = 'dashboard_charts'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	dashboard_id = sa.Column(sa.Integer, sa.ForeignKey('dashboards.id'), nullable=False)
	dashboard = sa.orm.relationship("Dashboard")
	chart_id = sa.Column(sa.Integer, sa.ForeignKey('charts.id'), nullable=False)
	chart = sa.orm.relationship("Chart")
	order = sa.Column(sa.Integer, nullable=False)


class Chart(SqlAlchemyBase):
	
	__tablename__ = 'charts'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	chart_type_id = sa.Column(sa.Integer, sa.ForeignKey('chart_types.id'))
	chart_type = sa.orm.relationship("ChartType")
	notasi_query = sa.Column(sa.String)
	x_categories = sa.Column(sa.String)
	dataset_legends = sa.Column(sa.String)
	value_columns = sa.Column(sa.String)
	color_columns = sa.Column(sa.String)
	options = sa.Column(sa.String)
	access_columns = sa.Column(sa.String)
	access_groups = sa.Column(sa.String)
	dashboard_charts = sa.orm.relationship("DashboardChart")
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)

class ChartType(SqlAlchemyBase):
	
	__tablename__ = 'chart_types'
	id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
	name = sa.Column(sa.String)
	chart_type = sa.Column(sa.String)
	created_date = sa.Column(sa.DateTime, default = datetime.datetime.now)
