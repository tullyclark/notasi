import flask
import sys
from sqlalchemy import exc
import data.source as source
from flask_login import login_required
from services.delete_services import delete_object, drop_view
from decorators.admin import is_admin
import data.db_session as db_session


blueprint = flask.Blueprint('delete', __name__)


@blueprint.before_request
@login_required
@is_admin
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

    
@blueprint.route('/<item_type>/<id>', methods=['GET'])
def delete(item_type: str, id: int):

	next = flask.request.args.get('next', default = None, type = str)
	if item_type == 'location':
		item =  source.Location
	if item_type ==  'query':
		item =  source.Query
	if item_type == 'view':
		item = source.DataView
	if item_type == 'user':
		item =  source.User
	if item_type == 'endpoint':
		item =  source.Endpoint
	if item_type == 'schedule':
		item =  source.Schedule
	if item_type == 'schedule_step':
		item =  source.ScheduleStep
	if item_type == 'chart':
		item =  source.Chart
	if item_type == 'group':
		item =  source.Group
	if item_type == 'user_group':
		item =  source.UserGroup
	if item_type == 'group_category':
		item =  source.GroupCategory
	if item_type == 'dashboard':
		item =  source.Dashboard
	if item_type == 'dashboard_chart':
		item =  source.DashboardChart

	session = db_session.create_session()
	try:
		if item ==  source.DataView:
			drop_view(id, session)

		delete_object(id, item, session)
		session.commit()
	except Exception as error:
		print(str(error))
	finally:
		session.close()
		return flask.redirect(next)