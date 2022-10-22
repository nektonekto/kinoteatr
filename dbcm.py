from pymysql import connect
from pymysql.err import *

class UseDatabase:
    """
    Class to connect to DataBase
    """
    def __init__(self, config: dict):
        self.config = config
        """
                Constructs all necessary attributes for class object

                :param config: Configuration dictionary for connecting to DataBase:
                {host:'host name', user:'user name', password:, database:'database name'}

                :type config: dict

                """
    def __enter__(self):
        """
                Trying to connect to DataBase

                :returns:
                    :return: Cursor, connected to databse
                    :rtype: Class Cursor. --
                    :return: Name of the error that caused the connection to the DataBase to fail
                    :rtype: str

        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0]==1049:
                print('wrong database name')
            if err.args[0]==2003:
                print('wrong host id')
            if err.args[0]==1045:
                print('wrong user name')
            return None
        #except RuntimeError as err:
         #   if err.argc[0]==1045:
          #      print('wrong user name')
           # return None

         #   print('wrong password')
    def __exit__(self, exc_type, exc_value, exc_trail):
        """
               Closing cursor and exiting from connection to DataBase

               :param exc_type: Type of Error
               :param exc_val: Number corresponding to the error
               :type exc_type: type
               :type exc_val: int
               :returns:
                   :return: True. If no fails in connecting to DataBase or exiting from Connection
                   :rtype: bool
                   :return String describing the error in the exit
                   :rtype: str

        """
        if exc_value is None:
            self.conn.commit()
            self.conn.close()
            self.cursor.close()
            return True
        else:
            if exc_value.args[0] == 'Курсор не создан':
                print('Курсор не был создан')
            if exc_value.args[0] == 1064:
               print('Синтаксическая ошибка в запросе')
            elif exc_value.args[0] == 1146:
                print('Такой таблицы не существует')
            elif exc_value.args[0] == 1054:
                print(exc_value, exc_type)
            return True