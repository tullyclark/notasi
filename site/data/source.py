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
