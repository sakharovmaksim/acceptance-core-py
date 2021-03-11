import logging

from pymongo import MongoClient


class MongoDbClient:
    """Attention: Singleton object, use by MongodbClient.get_instance().get_collection()"""

    __instance = None
    __client = None
    __mongo_host = "127.0.0.1"
    __mongo_port = 27017

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            logging.debug("Creating MongoDbClient instance")
            cls.__instance = MongoDbClient()
        return cls.__instance

    def get_client(self) -> MongoClient:
        if self.__client:
            return self.__client

        self.__client = MongoClient(self.__mongo_host, self.__mongo_port)
        return self.__client

    def get_db(self, db: str) -> MongoClient:
        client = self.get_client()
        logging.info(f"Getting a Database '{db}' from MongoDB")
        return client[db]

    def get_collection(self, collection: str, db: str = "test") -> MongoClient:
        db = self.get_db(db)
        logging.info(f"Getting from a Database '{str(db)}' Collection '{collection}'")
        return db[collection]

    def close(self):
        if self.__client:
            logging.info("Closing MongoDb instance session")
            self.__client.close()
            self.__client = None
