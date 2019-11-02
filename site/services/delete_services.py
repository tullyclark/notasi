import sqlalchemy.orm

import data.source as source
from services.crontab_services import write_cron_job, delete_cron_job

def delete_object(id, item_type, session):

    obj = session.query(item_type) \
        .filter_by(id=id) \
        .first()
    if item_type == source.ScheduleStep:   
        delete_cron_job(obj.schedule_id)
        session.commit()
        write_cron_job(obj.schedule_id, session)
    session.delete(obj)
    session.commit()

def drop_view(id, session):

    obj = session.query(source.DataView) \
        .filter_by(id=id) \
        .first()

    sql_text = f"drop view if exists {obj.view_name}"
    session.execute(sql_text)
    
    session.commit()

        