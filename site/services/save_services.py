import sqlalchemy.orm
from sqlalchemy import sql
import re
from data.source import Location, Query, DataView, Subtype, LocationType, \
    UserData, User, Endpoint, Schedule, ScheduleStep, \
    ViewRun, Group, UserGroup, GroupCategory, \
    Dashboard, DashboardChart, Chart
from services.process_services import create_view
from services.delete_services import drop_view
from utils.split_strip import split_strip
from werkzeug.security import generate_password_hash
from services.crontab_services import write_cron_job, delete_cron_job
import json
import datetime


def save_object(item_type, id, data, session):
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
            username = data["username"],
            session = session)

    elif item_type == 'query':
        save_query(
            id = id,
            name = data["name"], 
            endpoint = data["endpoint"], 
            notasi_query = data["notasi_query"], 
            head = data["head"], 
            body = data["body"], 
            location_id = data["location_id"],
            request_method_id = data.get("request_method_id", default = None),
            session = session)

    elif item_type == 'view':
        save_data_view(
            id = id,
            name = data["name"],
            view_name = re.sub('\W+','', data["view_name"] ), 
            business_keys = data["business_keys"], 
            information_columns = data["information_columns"], 
            query_id = data["query_id"],
            session = session)

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
            response_body =  data["response_body"],
            session = session
            )

    elif item_type == 'schedule':
        save_schedule(
            id = id,
            name = data["name"],
            cron_schedule = data["cron_schedule"],
            session = session
            )

    elif item_type == 'schedule_step':
        save_schedule_step(
            id = id,
            query_id = data["query_id"],
            schedule_id = data["schedule_id"],
            session = session
            )

    elif item_type == 'dashboard':
        save_dashboard(
            id = id,
            name = data["name"],
            session = session
            )

    elif item_type == 'dashboard_chart':
        save_dashboard_chart(
            id = id,
            dashboard_id = data["dashboard_id"],
            order = data.get("order", default = None),
            chart_id = data["chart_id"],
            session = session
            )

    elif item_type == 'chart':
        save_chart(
            id = id,
            name = data["name"],
            chart_type_id = data.get("chart_type_id", default = None),
            notasi_query = data["notasi_query"],
            x_categories = data["x_categories"],
            value_columns = data["value_columns"],
            dataset_legends = data["dataset_legends"],
            color_columns = data["color_columns"],
            page_column = data["page_column"],
            access_columns = data["access_columns"],
            access_groups = data["access_groups"],
            options = data["options"],
            session = session
            )

    elif item_type == 'group_category':
        save_group_category(
            id = id,
            name = data["name"],
            session = session
            )


    elif item_type == 'group':
        save_group(
            id = id,
            name = data["name"],
            group_category_id = data.get("group_category_id", default = None),
            session = session
            )

    elif item_type == 'user_group':
        save_user_group(
            id = id,
            user_id = data["user_id"],
            group_id = data["group_id"],
            session = session
            )

    elif item_type == 'user':
        save_user(
            id = id,
            name = data.get("name"),
            username = data.get("username"),
            password = data.get("password"),
            session = session
            )

def save_location(id,
    location_type_id, 
    database, 
    name, 
    password, 
    port, 
    address, 
    subtype_id, 
    username,
    session
):

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
    return location


def save_query(id,
    name,
    endpoint,
    notasi_query,
    request_method_id,
    head, 
    body, 
    location_id,
    session
):

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
    return query


def save_data_view(id,
    name,
    view_name,
    business_keys, 
    information_columns, 
    query_id,
    session
):

    if id:
        drop_view(id, session)
        data_view = session.query(DataView).filter_by(id=id).first()
    else:
        data_view = DataView()
    session.add(data_view)

    data_view.name = name
    data_view.view_name = view_name
    data_view.business_keys = business_keys
    data_view.information_columns = information_columns
    data_view.query_id = query_id
    create_view(data_view, session)
    return data_view


def save_user(id,
    name,
    username,
    password,
    session
):

    if id:
        user = session.query(User).filter_by(id=id).first()
    else:
        user = User()
        session.add(user)
        
    user.name = name
    user.username = username
    if password !='': user.password = generate_password_hash(password, method='sha256')
    return user

def save_group_category(id,
    name,
    session
):

    if id:
        group_category = session.query(GroupCategory).filter_by(id=id).first()
    else:
        group_category = GroupCategory()
        session.add(group_category)
    group_category.name = name
    return group_category

def save_group(id,
    name,
    group_category_id,
    session
):

    if id:
        group = session.query(Group).filter_by(id=id).first()
    else:
        group = Group()
        session.add(group)
        
    group.name = name
    group.group_category_id = group_category_id
    return group

def save_user_group(id,
    user_id,
    group_id,
    session
):

    if id:
        user_group = session.query(UserGroup).filter_by(id=id).first()
    else:
        user_group = UserGroup()
        session.add(user_group)
    user_group.user_id = user_id
    user_group.group_id = group_id
    return user_group

def save_endpoint(id,
    name,
    endpoint_location,
    category,
    request_method_id,
    key,
    notasi_query, 
    # request_body, 
    response_body,
    session
):

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
    return endpoint

def save_schedule(id,
    name,
    cron_schedule,
    session
):

    if id:
        schedule = session.query(Schedule).filter_by(id=id).first()
    else:
        schedule = Schedule()
        session.add(schedule)
    schedule.name = name
    schedule.cron_schedule = cron_schedule
    return schedule

def save_schedule_step(id,
    query_id,
    schedule_id,
    session
):

    if id:
        schedule_step = session.query(ScheduleStep).filter_by(id=id).first()
    else:
        schedule_step = ScheduleStep()
        session.add(schedule_step)
    schedule_step.query_id = query_id
    schedule_step.schedule_id = schedule_id
    delete_cron_job(schedule_id)
    write_cron_job(schedule_id, session)
    return schedule_step

def save_dashboard(id,
    name,
    session
):

    if id:
        dashboard = session.query(Dashboard).filter_by(id=id).first()
    else:
        dashboard = Dashboard()
        session.add(dashboard)
    dashboard.name = name
    return dashboard

def save_dashboard_chart(id,
    dashboard_id,
    order,
    chart_id,
    session
):

    if id:
        dashboard_chart = session.query(DashboardChart).filter_by(id=id).first()
    else:
        dashboard_chart = DashboardChart()
        session.add(dashboard_chart)
    dashboard_chart.dashboard_id = dashboard_id
    dashboard_chart.order = order
    dashboard_chart.chart_id = chart_id
    return dashboard_chart

def save_chart(id,
    name,
    chart_type_id,
    notasi_query,
    x_categories,
    dataset_legends,
    value_columns,
    color_columns,
    page_column,
    options,
    access_columns,
    access_groups,
    session
    ):

    if id:
        chart = session.query(Chart).filter_by(id=id).first()
    else:
        chart = Chart()
        session.add(chart)
    chart.name = name
    chart.chart_type_id = chart_type_id
    chart.notasi_query = notasi_query
    chart.x_categories = x_categories
    chart.dataset_legends = dataset_legends
    chart.value_columns = value_columns
    chart.color_columns = color_columns
    chart.page_column = page_column
    chart.options = options
    chart.access_columns = access_columns
    chart.access_groups = access_groups
    return chart


def insert_user_data(new_data, view_run_id,
    session):

  view_run = session.query(ViewRun) \
    .filter_by(id=view_run_id) \
    .first()

  data_view = view_run.data_view

  business_keys = split_strip(data_view.business_keys, ",")
  information_columns = split_strip(data_view.information_columns, ",")
  keys=[]
  for key in business_keys + information_columns:

    sql_filter = f"coalesce(data ->> '{key}', '') = '{new_data.get(key)}'"
    keys.append(sql_filter)

  where = ' AND '.join(keys)

  current_data = session.query(UserData) \
    .filter(sql.text(where)) \
    .order_by(UserData.created_date.desc()) \
    .first()


  if not current_data:
    user_data = UserData()
    session.add(user_data)
    user_data.data = new_data
    user_data.view_run_id = view_run_id
  else:
    current_data.view_run_id = view_run_id


