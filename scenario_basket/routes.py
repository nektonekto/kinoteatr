import os

from flask import Blueprint, request, render_template, current_app, session
from werkzeug.utils import redirect
from db_model import get_db_config, work_with_db, db_update
from sql_provider import SQLProvider
from scenario_basket.utils import add_to_basket, clear_basket
from access import login_permission_required

basket_app = Blueprint('basket', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['POST', 'GET'])
@login_permission_required
def basket():
    db_config = current_app.config['DB_CONFIG']
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        sql = provider.get('order_list.sql')
        result = work_with_db(current_app.config['DB_CONFIG'], sql)
        return render_template('basket_order_list.html', items=result, basket=current_basket)
    else:
        item_id = request.form.get('item_id', None)

        sql = provider.get('order_item.sql', id=item_id)
        items = work_with_db(current_app.config['DB_CONFIG'], sql)
        if not items:
            return ''

        add_to_basket(items[0])
        return redirect('/basket')


@basket_app.route('/clear', methods=['POST', 'GET'])
def clear_basket_handler():
    clear_basket()
    return redirect('/basket')


@basket_app.route('/buy')
def buy_items():
    """

    :return:
    """
    db_config = current_app.config['DB_CONFIG']
    basket = session.get('basket', [])

    for item in basket:
        sql = provider.get('insert_item.sql', **item)
        result = db_update(db_config, sql)
        if result:
            return "None"

        sql = provider.get('update.sql', **item)
        result = db_update(db_config, sql)

        clear_basket()
    return redirect('/basket')



