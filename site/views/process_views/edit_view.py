import flask
from data.source import Location, Query, DataView, Subtype, LocationType, RequestMethod
from services.select_services import get_locations, get_objects, search_object
from services.save_services import save_object
from flask_login import login_required
from decorators.admin import is_admin

blueprint = flask.Blueprint('process_edit', __name__, template_folder = '../../templates/process')

@blueprint.before_request
@login_required
@is_admin
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

type_variables = {
	"location_template": "edit_location.html"
	, "location_class": Location
	, "query_template": "edit_query.html"
	, "query_class": Query
	, "view_template": "edit_view.html"
	, "view_class": DataView

	}


@blueprint.route('/<item_type>', methods=['POST', 'GET'])
def edit(item_type: str):
	id = flask.request.args.get('id', default = None, type = int)
	print(id)
	if flask.request.method == "GET":
		return flask.render_template(

				type_variables[item_type+"_template"]
				, item_type = item_type
				, back_link = flask.request.referrer
				, locations = get_locations()
				, subtypes = get_objects(Subtype)
				, request_methods = get_objects(RequestMethod)
				, location_types = get_objects(LocationType)
				, data_obj = search_object(id, type_variables[item_type+"_class"])

			)


	if flask.request.method == "POST":
		data = flask.request.form
		save_object(item_type, id, data)
		return flask.redirect('/process')