import sqlalchemy.orm

import data.db_session as db_session
from data.source import Location, Query, DataView, SqlType, LocationType, User, Endpoint, Schedule, ScheduleStep

def delete_object(id, item_type):
    session = db_session.create_session()
    obj = session.query(item_type) \
        .filter_by(id=id) \
        .first()
    session.delete(obj)
    
    session.commit()
    session.close()

def drop_view(id):
    session = db_session.create_session()
    obj = session.query(DataView) \
        .filter_by(id=id) \
        .first()
    print(obj.name)

    sql_text = f"drop view {obj.view_name}"
    session.execute(sql_text)
    
    session.commit()
    session.close()