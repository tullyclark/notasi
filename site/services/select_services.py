import sqlalchemy.orm

import data.db_session as db_session
from data.source import Location, Query, DataView, Subtype, LocationType, RequestMethod, Schedule, GroupCategory

def get_objects(item_type, session):
    objects = session.query(item_type).options(sqlalchemy.orm.joinedload('*')) \
        .all()

    return objects

def search_object(id, item_type, session):
    obj = session.query(item_type) \
        .filter_by(id=id) \
        .options(sqlalchemy.orm.joinedload('*')) \
        .first()

    return obj



