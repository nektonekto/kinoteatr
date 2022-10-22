from flask import Blueprint, render_template,request,session, current_app
# Модуль проекта
from sql_provider import SQLProvider
from access import login_permission_required
from db_model import work_with_db
import os

# Путь к папке sql
provider = SQLProvider(os.path.join(os.path.dirname('app.py'),'sql'))

# Создание объекта Blueprint
auth_app = Blueprint('log_in', __name__, template_folder='templates')



@auth_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        loginn = request.form.get('login', None)
        password = request.form.get('password', None)
        print(loginn, password)
        if loginn is not None and password is not None:
            group=work_with_db(current_app.config['DB_CONFIG'], 'select group_name from kinoteatr.my_user \
             where login=\''+str(loginn)+'\''+' and password=\''+str(password)+'\'')
            print(group)
            if len(group) != 0:
                session['group_name'] = group[0]['group_name']
                return render_template('logged_in.html')
            else:
                return render_template('err_log.html')
        else:
            return render_template('err_log.html')