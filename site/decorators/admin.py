from flask_login import current_user
from flask import abort
from functools import wraps

def is_admin(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        for user_group in current_user.user_groups:
            if user_group.group.name =='Administrators' and user_group.group.group_category.name == 'Access Level Groups': 
                return fn(*args, **kwargs)
        abort(401)

    return wrap