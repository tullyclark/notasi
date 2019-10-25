import flask
import pandas
import data.db_session as db_session
from flask_login import login_required
from data.source import Group
from services.select_services import get_objects, search_object, GroupCategory
from services.save_services import save_object
import os


template_dir = os.path.abspath('./templates/group')
blueprint = flask.Blueprint('groups', __name__, template_folder = template_dir)
@blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


@blueprint.route('/')
def index():

	return flask.render_template(
		'group_index.html'
		, groups = get_objects(Group)
	)

@blueprint.route('/edit', methods=['POST', 'GET'])
def reset():
	id = flask.request.args.get('id', default = None, type = int)

	if flask.request.method == "GET":
		return flask.render_template(
			'edit_group.html'
			, item_type = 'group'
			, data_obj = search_object(id=id, item_type=Group)
			, back_link = flask.request.referrer
			, group_categories = get_objects(GroupCategory)
		)


	if flask.request.method == "POST":
		data = flask.request.form
		print(data)
		save_object('group', id, data)
		return flask.redirect('/group')