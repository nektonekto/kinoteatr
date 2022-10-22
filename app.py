# Стандартные библиотеки
import json
# Сторонние библиотеки
from flask import Flask,  render_template,  session

# Модули проекта
from scenario_requests.request import requests_app
from scenario_user.edit import edit_app
from scenario_auth.log_in import auth_app
from scenario_basket.routes import basket_app

from sql_provider import SQLProvider
# Определение главного приложение
app = Flask(__name__)

# Конфигурация прав доступа
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))

# Регистрация блюпринтов в главном приложении
app.register_blueprint(basket_app, url_prefix='/basket')
app.register_blueprint(edit_app, url_prefix='/edit')
app.register_blueprint(requests_app, url_prefix='/requests')
app.register_blueprint(auth_app, url_prefix='/auth')
provider=SQLProvider('sql')

# Конфигурация секретного ключа
app.config['SECRET_KEY'] = 'secretkey'

# Конфигурация доступа к БД
app.config['DB_CONFIG'] = json.load(open('configs/config.json'))


@app.route('/', methods=['GET', 'POST'])
def menu():
    # Начальная страница входа в приложением
    return render_template('menu.html')

@app.route('/goodbye', methods=['GET', 'POST'])
def goodbye():
    # Страница выхода из приложения
    return render_template('goodbye.html')

# @app.route('/menu', methods=['GET', 'Post'])
# def menu():
#     return render_template('menu.html')

# @app.route('/get-name')
# @login_required
# def select_version():
#     sql = provider.get('name.sql', name='')
#     result = work_with_db(app.congif['dbconfig'], sql)
#     return str(result)

# @app.route('/counter')
# def count_visits():
#     counter=session.get('count', None)
#     if counter is None:
#         session['count']=0
#     else:
#         session['count']=session['count']+1
#     return f"your count: {session['count']}"

@app.route('/session-clear')
def clear_session():
    # Полноая очистка сессии
    session.clear()
    # Страница с информированием о выходе из приложения
    return render_template('goodbye.html')

# @app.route('/get-name')
# @login_required
# def get_name():
#     sql=provider.get('name.sql', log='Vitaly')
#     result=work_with_db('DB_CONFIG', sql)
#     return str(result)



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5001, debug = True)