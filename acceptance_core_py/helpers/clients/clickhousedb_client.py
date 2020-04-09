from clickhouse_driver import Client
from typing import List, Tuple

import clickhouse_driver
import logging


class ClickHouseDbClient:
    """Attention: Singleton object, use by ClickHouseDbClient.get_instance().select_from_table()"""
    # Read documentation https://clickhouse-driver.readthedocs.io/en/latest/index.html
    # Notice: When DB API 2.0 will be correctly working with our ClickHouse, use it instead of using Client
    __instance = None
    __db_client = None
    __clickhouse_host = '127.0.0.1'
    __clickhouse_port = 9007

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            logging.debug("Creating ClickHouseDbClient instance")
            cls.__instance = ClickHouseDbClient()
        return cls.__instance

    def get_db_client(self, db: str = 'test') -> Client:
        if self.__db_client:
            return self.__db_client
        self.__db_client = clickhouse_driver.Client(host=self.__clickhouse_host, port=self.__clickhouse_port, database=db)
        return self.__db_client

    def select_from_table(self, table: str, search_condition: str = None, limit: int = 30) -> List:
        client = self.get_db_client()
        query_str = f"SELECT * FROM {table}"
        if search_condition:
            query_str = f"{query_str} WHERE {search_condition}"
        if limit:
            query_str = f"{query_str} LIMIT {str(limit)}"

        logging.info(f"ClickHouse query is '{query_str}'")
        result = client.execute(query_str)
        logging.info(f"Result from request is: '{result}' with len {len(result)}")
        return result

    def select_first_from_table(self, table: str, search_condition: str = None) -> Tuple:
        result = self.select_from_table(table=table, search_condition=search_condition, limit=1)
        if len(result) == 0:
            return tuple()
        return_result = result[0]
        logging.info(f"Returning first tuple from list-result. Tuple is: '{return_result}'")
        return return_result

    def close(self):
        if self.__db_client:
            logging.info("Closing ClickHouseDbClient instance")
            self.__db_client.disconnect()
            self.__db_client = None
