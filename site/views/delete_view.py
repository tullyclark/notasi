import flask
from data.source import Location, Query, DataView, User, Endpoint, Schedule, ScheduleStep, Chart, Group, UserGroup, GroupCategory
from flask_login import login_required
from services.delete_services import delete_object


blueprint = flask.Blueprint('delete', __name__)


@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

    
@blueprint.route('/<item_type>/<id>', methods=['POST', 'GET'])
def delete(item_type: str, id: int):

	next = flask.request.args.get('next', default = None, type = str)
	if flask.request.method == "GET":
		if item_type == 'location':
			delete_object(id, Location)
		if item_type ==  'query':
			delete_object(id, Query)
		if item_type == 'view':
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
		return flask.redirect(next)