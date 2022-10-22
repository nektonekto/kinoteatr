from functools import wraps
from flask import session, request, current_app
from flask import render_template

def group_validation(ses: session) -> bool:
    group = session.get('group_name', None)
    if group is not None and group != '':
        return True
    return False


def group_permission_validation(config: dict, sess: session) -> bool:
    group = sess.get('group_name', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint
    print(target_app)
    print(group)
    if group in config and target_app in config[group]:
        return True
    return False

def login_required(f):
    # Декоратор
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_validation(session):
            return f(*args, **kwargs)
        return f"Permission denied"
    return wrapper


def login_permission_required(f):
    # Декоратор
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        # Возвращает страницу при отсутствии прав доступа
        return render_template('group_permission_denied.html')
    return wrapper

