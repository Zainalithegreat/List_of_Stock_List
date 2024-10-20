from Stock import Stock
from ComputerCompany import ComputerCompany
from Bank import Bank
from StockList import StockList
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from configparser import ConfigParser
import os
from User import User


class Database:
    __connection = None
    __database = None
    __stocks_collection = None
    __stocksLists_collections = None
    __users_collection = None
    APP_NAME = "stock_list"

    @classmethod
    def connect(cls):
        if cls.__connection is None:
            if "APPDATA" in os.environ:
                path = f"{os.environ["APPDATA"]}\\{cls.APP_NAME}\\{cls.APP_NAME}.ini"
            elif "HOME" in os.environ:
                path = f"{os.environ["HOME"]}/{cls.APP_NAME}/{cls.APP_NAME}.ini"
            else:
                raise Exception("Couldn't find config directory.")

            config_parser = ConfigParser()
            config_parser.read(path)
            username = config_parser["Database"]["username"]  # same thing but different syntax for below.
            password = config_parser.get("Database", "password")
            cluster = config_parser.get("Database", "cluster")

            uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.StockList
            cls.__stocks_collection = cls.__database.Stocks
            cls.__stocksLists_collections = cls.__database.StockLists
            cls.__users_collection = cls.__database.Users

            print("Client: ", cls.__connection)
            print("Database: ", cls.__database)
            print("Stocks: ", cls.__stocks_collection)
            print("StockLists: ", cls.__stocksLists_collections)

    @classmethod
    def rebuild_data(cls):
        cls.connect()
        cls.__stocks_collection.drop()
        cls.__stocks_collection = cls.__database.Stocks
        cls.__stocksLists_collections.drop()
        cls.__stocksLists_collections = cls.__database.StockLists
        cls.__users_collection.drop()
        cls.__users_collection = cls.__database.Users

        all_stocks, all_stocklists, all_users = cls.get_stock()

        user_dicts = [user.to_dict() for user in all_users]
        cls.__users_collection.insert_many(user_dicts)

        stock_dicts = [stock.to_dict() for stock in all_stocks]
        cls.__stocks_collection.insert_many(stock_dicts)

        stocklist_dicts = [stocklist.to_dict() for stocklist in all_stocklists]
        cls.__stocksLists_collections.insert_many(stocklist_dicts)

    @classmethod
    def read_data(cls, user_key):
        cls.connect()
        stock_map = {}
        stock_dicts = list(cls.__stocks_collection.find({"user_key": user_key}))
        stocks = [Stock.build(stock_dict, stock_map) for stock_dict in stock_dicts]

        stocklist_map = {}
        stocklist_dicts = list(cls.__stocksLists_collections.find({"user_key": user_key}))
        stocklist = [StockList.build(stocklist_dict, stocklist_map, stock_map) for stocklist_dict in stocklist_dicts]


        return stocklist_map[StockList.make_key(StockList.ALL_STOCKS)], stocklist, stock_map, stocklist_map

    @classmethod
    def read_user(cls, username):
        cls.connect()
        user_dict = cls.__users_collection.find_one({'_id': username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @staticmethod
    def get_stock():
        user1 = User("Zain", b'$2b$13$/htLKvHS3ho5NF5.qH78fu6T.F3Fc2gdEGzNg8iBgjAGeT//y.imu')
        user2 = User("Joe Biden", b'$2b$13$dvTyGZHjkkVcU.aM2KyYwOZcEECeO3dPyts19Gj2VJnAKwi241gba')

        stock_map = {}
        stocklist_map = {}

        NVDA = ComputerCompany(
            "NVIDIA",
            796.77,
            839.50,
            "4/24/2024",
            "10:19.00",
            user1.get_key(),
            stock_map,
            "RTX 4090"
        )

        JPM = Bank(
            "JPMorgan Chase & Co",
            193.08,
            190.53,
            "4/24/2024",
            "10:21.00",
            user2.get_key(),
            stock_map,
            100000000
        )

        AMD = ComputerCompany(
            "AMD",
            157.40,
            154.24,
            "4/28/2024",
            "11:53.00",
            user1.get_key(),
            stock_map,
            "RX 7900 XTX"
        )

        COFC = Bank(
            "Capital One Financial Corp",
            146.21,
            145.16,
            "4/28/2024",
            "11:54.00",
            user2.get_key(),
            stock_map,
            98000000
        )
        STK = Stock(
            "Apple INC",
            169.02,
            169.15,
            "4/24/2024",
            "10:24.00",
            user2.get_key(),
            stock_map
        )

        u1_all = StockList(
            "Stock",
            [NVDA, AMD],
            "This has all the stocks for Zain.",
            user1.get_key(),
            stocklist_map
        )

        u2_all = StockList(
            "Stock",
            [JPM, STK, COFC],
            "This has all the stocks for Joe Biden.",
            user2.get_key(),
            stocklist_map
        )

        bank_stocks = StockList(
            "Bank_Stock",
            [JPM, COFC],
            "This has all Bank related stocks.",
            user2.get_key(),
            stocklist_map
        )

        computer_hardware = StockList(
            "Computer_Stock",
            [AMD, NVDA],
            "This has all Computer Companies related Stocks.",
            user1.get_key(),
            stocklist_map
        )

        return [NVDA, JPM, STK, AMD, COFC], [computer_hardware, bank_stocks, u1_all, u2_all], [user1, user2]

    @classmethod
    def save_stocklist(cls, stocklist):
        cls.connect()
        stocklist_dict = stocklist.to_dict()
        cls.__stocksLists_collections.update_one({"_id": stocklist_dict["_id"]}, {"$set": stocklist_dict}, upsert=True)

    @classmethod
    def save_stock(cls, stock):
        cls.connect()
        stock_dict = stock.to_dict()
        cls.__stocks_collection.update_one({"_id": stock_dict["_id"]}, {"$set": stock_dict}, upsert=True)

    @classmethod
    def add_user(cls, user):
        cls.connect()
        user_dict = user.to_dict()
        cls.__users_collection.insert_one(user_dict)

    @classmethod
    def delete_stocklist(cls, stocklist):
        cls.connect()
        cls.__stocksLists_collections.delete_one({"_id": stocklist.get_id()})

    @classmethod
    def delete_stock(cls, stock):
        cls.connect()
        cls.__stocks_collection.delete_one({"_id": stock.get_id()})


if __name__ == "__main__":
    Database.connect()
