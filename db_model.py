# Стандартные библиотеки
import json

# Модуль проекта
from dbcm import UseDatabase


def work_with_db(config, SQL):
    """
    Данная функция к базе данных по config и выполняет запрос по аргументу SQL
    :param config:
    :param SQL:
    :return: Возвращает значение, полученное в результате запроса
    """
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            col_names=[]
            res=[]
            cursor.execute(SQL)
            result=cursor.fetchall()
            for atr in cursor.description:
                col_names.append(atr[0])
            for col in result:
                res.append(dict(zip(col_names, col)))
            print(*res, sep="\n")

    return res;

def get_db_config() -> dict:
    """
    Функция получения конфигурации Базы Данных из файла config.json
    :return: Полученную конфигурацию
    """
    try:
        with open("configs/config.json", 'r') as config:
            db_config = json.load(config)
    except FileNotFoundError as err:
        if err.args[0] == 2:
            print('Такой файл не найден\n')
        print(err.args[1])
        exit(0)
    except json.decoder.JSONDecodeError as err:
        print('Не является файлом .json\n')
        exit(0)
    return db_config

def db_update(config, SQL):
    """
    Функция обновления Базы Данных
    :param config:
    :param SQL:
    :return:
    """
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор None')
        elif cursor:
            cursor.execute(SQL)


