import sqlalchemy.orm
from sqlalchemy import sql
import re
import data.db_session as db_session
from data.source import Location, Query, DataView, Subtype, LocationType, UserData, User, Endpoint, Schedule, ScheduleStep
from services.process_services import create_view
from services.delete_services import drop_view
from utils.split_strip import split_strip
from werkzeug.security import generate_password_hash
from services.crontab_services import write_cron_job, delete_cron_job
import json
import datetime


def save_object(item_type, id, data):
    if item_type == 'location':
        save_location(
            id = id,
            location_type_id = data["location_type_id"], 
            database = data["database"], 
            name = data["name"], 
            password = data["password"],
            address = data["address"],  
            port = data["port"], 
            subtype_id = data.get("subtype_id", default = None), 
            username = data["username"])

    elif item_type == 'query':
        save_query(
            id = id,
            name = data["name"], 
            endpoint = data["endpoint"], 
            notasi_query = data["notasi_query"], 
            head = data["head"], 
            body = data["body"], 
            location_id = data["location_id"],
            request_method_id = data.get("request_method_id", default = None))

    elif item_type == 'view':
        save_data_view(
            id = id,
            name = data["name"],
            view_name = re.sub('\W+','', data["view_name"] ), 
            business_keys = data["business_keys"], 
            information_columns = data["information_columns"], 
            query_id = data["query_id"])

    elif item_type == 'endpoint':
        save_endpoint(
            id = id,
            name = data["name"],
            endpoint_location = data["endpoint_location"],
            category = data["category"],
            request_method_id = data.get("request_method_id", default = None),
            key = data["key"],
            notasi_query = data["notasi_query"], 
            # request_body =  data["request_body"], 
            response_body =  data["response_body"]
            )

    elif item_type == 'schedule':
        save_schedule(
            id = id,
            name = data["name"],
            cron_schedule = data["cron_schedule"]
            )

    elif item_type == 'schedule_step':
        save_schedule_step(
            id = id,
            query_id = data["query_id"],
            schedule_id = data["schedule_id"]
            )

def save_location(id,
    location_type_id, 
    database, 
    name, 
    password, 
    port, 
    address, 
    subtype_id, 
    username 
):

    session = db_session.create_session()
    if id:
    	location = session.query(Location).filter_by(id=id).first()
    else:
        location = Location()
        session.add(location)

    location.location_type_id = location_type_id
    location.database = database
    location.name = name
    if password !='': location.password = password
    location.address = address
    location.port = port
    location.subtype_id = subtype_id
    location.username = username
    session.commit()
    session.close()
    return location


def save_query(id,
    name,
    endpoint,
    notasi_query,
    request_method_id,
    head, 
    body, 
    location_id
):
    session = db_session.create_session()

    if id:
    	query = session.query(Query).filter_by(id=id).first()
    else:
        query = Query()
        session.add(query)
    	
    query.name = name
    query.endpoint = endpoint
    query.request_method_id = request_method_id
    query.notasi_query = notasi_query
    query.head = head
    query.body = body
    query.location_id = location_id

    session.commit()
    session.close()
    return query


def save_data_view(id,
    name,
    view_name,
    business_keys, 
    information_columns, 
    query_id
):
    session = db_session.create_session()

    if id:
        drop_view(id)
        data_view = session.query(DataView).filter_by(id=id).first()
    else:
        data_view = DataView()
    session.add(data_view)

    data_view.name = name
    data_view.view_name = view_name
    data_view.business_keys = business_keys
    data_view.information_columns = information_columns
    data_view.query_id = query_id
    session.commit()
    create_view(data_view.id)
    session.close()
    return data_view


def save_user(id,
    name,
    username,
    password
):
    session = db_session.create_session()

    if id:
        user = session.query(User).filter_by(id=id).first()
    else:
        user = User()
        session.add(user)
        
    user.name = name
    user.username = username
    if password !='': user.password = generate_password_hash(password, method='sha256')

    session.commit()
    session.close()
    return user

def save_endpoint(id,
    name,
    endpoint_location,
    category,
    request_method_id,
    key,
    notasi_query, 
    # request_body, 
    response_body
):

    session = db_session.create_session()
    if id:
        endpoint = session.query(Endpoint).filter_by(id=id).first()
    else:
        endpoint = Endpoint()
        session.add(endpoint)
    endpoint.name = name
    endpoint.endpoint_location = endpoint_location
    endpoint.category = category
    endpoint.request_method_id = request_method_id
    if key !='': endpoint.key = generate_password_hash(key, method='sha256')
    endpoint.notasi_query = notasi_query
    # endpoint.request_body = request_body
    endpoint.response_body = response_body
    session.commit()
    session.close()
    return endpoint

def save_schedule(id,
    name,
    cron_schedule
):

    session = db_session.create_session()
    if id:
        schedule = session.query(Schedule).filter_by(id=id).first()
    else:
        schedule = Schedule()
        session.add(schedule)
    schedule.name = name
    schedule.cron_schedule = cron_schedule
    session.commit()
    session.close()
    return schedule

def save_schedule_step(id,
    query_id,
    schedule_id
):

    session = db_session.create_session()
    if id:
        schedule_step = session.query(ScheduleStep).filter_by(id=id).first()
    else:
        schedule_step = ScheduleStep()
        session.add(schedule_step)
    schedule_step.query_id = query_id
    schedule_step.schedule_id = schedule_id
    session.commit()
    session.close()
    delete_cron_job(schedule_id)
    write_cron_job(schedule_id)
    return schedule_step


def insert_user_data(new_data, data_view_id):
  
  session = db_session.create_session()
  data_view = session.query(DataView) \
    .filter_by(id=data_view_id) \
    .first()

  business_keys = split_strip(data_view.business_keys, ",")
  information_columns = split_strip(data_view.information_columns, ",")
  keys=[]
  for key in business_keys:
    sql_filter = f"data ->> '{key}' = '{new_data[key]}'"
    keys.append(sql_filter)

  where = ' AND '.join(keys)

  current_data = session.query(UserData) \
    .filter(sql.text(where)) \
    .order_by(UserData.created_date.desc()) \
    .first()

  cols = []
  if current_data:
    for col in information_columns:
      if current_data.data.get(col) != new_data.get(col):
        cols.append(col)

  write_date = {}

  for business_key in business_keys:
    write_date[business_key] = new_data[business_key]

  for information_column in information_columns:
    write_date[information_column] = new_data[information_column]

  if not current_data or cols:
    user_data = UserData()
    user_data.data = write_date
    user_data.data_view_id = data_view_id
    session.add(user_data)
    session.commit()
  
  session.close()