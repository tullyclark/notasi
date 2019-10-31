import flask
import sys
from sqlalchemy import exc
from data.source import Location, Query, DataView, User, Endpoint, Schedule, ScheduleStep, Chart, Group, UserGroup, GroupCategory, Dashboard, DashboardChart
from flask_login import login_required
from services.delete_services import delete_object, drop_view
from decorators.admin import is_admin


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
	try:
		if item_type == 'location':
			delete_object(id, Location)
		if item_type ==  'query':
			delete_object(id, Query)
		if item_type == 'view':
			drop_view(id)
			delete_object(id, DataView)
		if item_type == 'user':
			delete_object(id, User)
		if item_type == 'endpoint':
			delete_object(id, Endpoint)
		if item_type == 'schedule':
			delete_object(id, Schedule)
		if item_type == 'schedule_step':
			delete_object(id, ScheduleStep)
		if item_type == 'chart':
			delete_object(id, Chart)
		if item_type == 'group':
			delete_object(id, Group)
		if item_type == 'user_group':
			delete_object(id, UserGroup)
		if item_type == 'group_category':
			delete_object(id, GroupCategory)
		if item_type == 'dashboard':
			delete_object(id, Dashboard)
		if item_type == 'dashboard_chart':
			delete_object(id, DashboardChart)
		return flask.redirect(next)
	except exc.IntegrityError as error:
	    return flask.render_template(
		'./process/error.html',
		 error = "Integrity Error: Make sure you delete all child objects before deleting the parent")