from flask import Blueprint, request, render_template, current_app
from sql_provider import SQLProvider
from access import login_permission_required
from db_model import db_update, work_with_db

edit_app = Blueprint('edit', __name__, template_folder='templates')
provider = SQLProvider('sql')

@edit_app.route('/', methods=['GET', 'POST'])
@login_permission_required
def fun_edit():
    db_config = current_app.config['dbconfig']
    if request.method == 'POST':
        id_c = request.form.get('id_c', None)
        if id_c is not None:
            _SQL = provider.get('delete.sql', gen1=id_c)
            db_update(db_config, _SQL)
    _SQL = provider.get('list_for_edit.sql')
    result = work_with_db(current_app.config['dbconfig'], _SQL)
    return render_template('edit.html', items=result)

@edit_app.route('/insert', methods=['GET', 'POST'])
@login_permission_required
def fun_insert():
    if request.method == 'GET':
        return render_template('insert.html', forma=True)
    else:
        film_name = request.form.get('film_name', None)
        print(film_name)
        dtime = request.form.get('dtime', None)
        print(dtime)
        num_hall = request.form.get('num_hall', None)
        print(num_hall)
        num_place = request.form.get('num_place', None)
        print(num_place)
        price = request.form.get('price', None)
        print(price)
        if film_name is not None and dtime is not None and num_hall is not None and num_place is not None and price is not None:
            db_config = current_app.config['dbconfig']
            _SQL = provider.get('insert.sql', gen1=film_name,  gen2=dtime, gen3=num_hall, gen4=num_place, gen5=price)
            db_update(db_config, _SQL)
        return fun_edit()


