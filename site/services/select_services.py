import sqlalchemy.orm

import data.db_session as db_session
from data.source import Location, Query, DataView, SqlType, LocationType, RequestMethod


def get_locations():
    session = db_session.create_session()
    locations = session.query(Location).options(sqlalchemy.orm.joinedload('*')) \
        .all()
    session.close()
    return locations

def get_objects(item_type):
    session = db_session.create_session()
    objects = session.query(item_type).options(sqlalchemy.orm.joinedload('*')) \
        .all()

    session.close()

    return objects

def search_object(id, item_type):
    session = db_session.create_session()
    obj = session.query(item_type) \
        .filter_by(id=id) \
        .options(sqlalchemy.orm.joinedload('*')) \
        .first()

    session.close()

    return obj



