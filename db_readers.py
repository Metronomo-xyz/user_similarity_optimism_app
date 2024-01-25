import pymongo
from abc import ABC, abstractmethod

class DBSimilarityReader(ABC):
    @abstractmethod
    def getSimilaritiesByWallet(self, wallet):
        pass


class MongoReader(DBSimilarityReader):
    def __init__(self, database, collection, host="127.0.0.1", port=27017, ):
        timeout = 5000
        self.client = pymongo.MongoClient(host=host, port=port, serverSelectionTimeoutMS=timeout)
        try:
            result = self.client.admin.command("ismaster")
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Server did not managed to set connection in " + (
                str(timeout / 1000)) + " seconde. Liekly that server is unavailable")
            raise ValueError("Can't establish connection. Wrong host or/and port : " + host + ":" + str(port))

        self.db = self.client[database]
        self.collection = self.db[collection]

    def getSimilaritiesByWallet(self, wallet):
        try:
            similarities = list(self.collection.find({"wallet_1" : wallet}, {"_id":0}))
        except StopIteration as e:
            return []

        return similarities

