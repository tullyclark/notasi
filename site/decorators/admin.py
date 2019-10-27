from flask_login import current_user
from functools import wraps

def is_admin(fn):
    @wraps(fn)
    def wrap(*args, **kwargs):
        for user_group in current_user.user_groups:
            if user_groups.group.name =='Administrators' and user_groups.group.group_category.name == 'Access Level Groups': 
                return f(*args, **kwargs)
            abort(401)
    return wrap