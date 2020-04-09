import logging
from typing import Tuple

import MySQLdb
from MySQLdb.cursors import Cursor


class MySQLDbClient:
    """Attention: Singleton object, use by MySQLDbClient.get_instance().select_one_from_table()"""
    # Read documentation https://mysqlclient.readthedocs.io/user_guide.html
    __instance = None
    __db_cursor = None
    __connect = None
    __mysql_host = '127.0.0.1'

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            logging.debug("Creating MySQLDbClient instance")
            cls.__instance = MySQLDbClient()
        return cls.__instance

    def get_db_cursor(self, db: str = 'test') -> Cursor:
        if self.__db_cursor:
            return self.__db_cursor
        db = MySQLdb.connect(host=self.__mysql_host, db=db, user='root')
        self.__connect = db
        self.__db_cursor = db.cursor(MySQLdb.cursors.DictCursor)
        return self.__db_cursor

    def select_one_from_table(self, table: str, search_condition: str = None) -> Tuple:
        cursor = self.get_db_cursor()
        query_str = f"SELECT * FROM {table}"
        if search_condition:
            query_str = f"{query_str} WHERE {search_condition}"

        logging.info(f"MySQL query is '{query_str}'")
        cursor.execute(query_str)
        # Fetching one row. Use fetchall() in another methods if necessary
        result = cursor.fetchone()
        logging.info(f"Result from request is: '{result}'")
        return result

    def delete_from_table(self, table: str, delete_condition: str) -> Tuple:
        cursor = self.get_db_cursor()
        query_str = f"DELETE FROM {table} WHERE {delete_condition}"

        logging.info(f"MySQL DELETE query is '{query_str}'")
        cursor.execute(query_str)
        result = cursor.fetchall()
        logging.info(f"Result from DELETE request is: '{result}'")

        self.__connect.commit()
        return result

    def close(self):
        if self.__db_cursor:
            logging.info("Closing MySQL instance session")
            self.__db_cursor.close()
            self.__connect.close()
            self.__db_cursor = None
            self.__connect = None
