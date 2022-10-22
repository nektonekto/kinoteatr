import os
from flask import Blueprint
from flask import render_template, request, current_app
from db_model import work_with_db
from sql_provider import SQLProvider
from access import login_permission_required

requests_app = Blueprint('requests', __name__, template_folder='templates')
provider = SQLProvider('sql')


@requests_app.route('/select', methods=['GET', 'POST'])
@login_permission_required
def select():
    return render_template('select.html')




@requests_app.route('/zapros1', methods=['GET', 'POST'])
def zapros1():
    # if request.method == 'POST':
    task = f'{"Информация о проданных билетах"}'
    _SQL = provider.get('bought.sql')
    result = work_with_db(current_app.config['DB_CONFIG'], _SQL)
    print(result)
    schema = [a for a in result[0]]
    return render_template('result1.html', result=result, schema=schema, task=task)

@requests_app.route('/zapros2', methods=['GET', 'POST'])
def zapros2():
    if request.method == 'GET':
        return render_template('zapros2_usl.html')
    else:
        session = request.form.get('number')
        if session:
            task = f'{"Количество проданных билетов в сессии №"}{session}'
            _SQL = provider.get('count_bilet.sql', num_session=session)
            result = work_with_db(current_app.config['DB_CONFIG'], _SQL)
            print(result)
            schema = [a for a in result[0]]
            return render_template('result1.html',  result=result, schema=schema,task=task)
        else:
            return "Wrong input for session"