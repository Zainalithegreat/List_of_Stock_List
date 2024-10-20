class StockList:
    __name = ""
    __category = []
    __description = ""
    __user_key = ""
    ALL_STOCKS = "Stock"

    def __init__(self, name, category, description, user_key, stocklist_map, save=False):
        self.__name = name
        self.__category = category
        self.__description = description
        self.__user_key = user_key
        stocklist_map[self.get_key()] = self

        if save:
            self.save()

    @classmethod
    def build(cls, stocklist_dict, stocklist_map, stock_map):
        from Stock import Stock
        return StockList(
            stocklist_dict["name"],
            [stock_map[key] for key in stocklist_dict["Stocks"]],
            stocklist_dict["description"],
            stocklist_dict["user_key"],
            stocklist_map
        )


    def to_dict(self):
        return{
            "_id": self.get_id(),
            "name": self.__name,
            "description": self.__description,
            "user_key": self.__user_key,
            "Stocks": [stock.get_key() for stock in self.__category]
        }

    def get_id(self):
        return f"{self.get_key()}|{self.__user_key}"

    def get_key(self):
        return self.__name.lower()

    def get_printable_key(self):
        return self.__name

    @staticmethod
    def make_key(name):
        return name.lower()

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_category(self):
        return self.__category

    def append_stock(self, stock, save=True):
        from Database import Database

        self.__category.append(stock)
        if save:
            Database.save_stocklist(self)

    def remove(self, stock):
        from Database import Database
        self.__category.remove(stock)

        Database.save_stocklist(self)

    def delete(self):
        from Database import Database
        from UserState import UserState

        stocklist_key = self.get_key()
        user_state = UserState.lookup(self.__user_key)
        stocklist_map = user_state.get_stocklist_map()
        if stocklist_key in stocklist_map:
            del stocklist_map[stocklist_key]
        Database.delete_stocklist(self)

    @staticmethod
    def get_stocklists():
        from Database import Database
        return Database.get_stock()

    def __add__(self, other):
        from UserState import UserState

        name = f"{self.get_name()}/{other.get_name()}"
        description = self.get_description() + " " + other.get_description()
        user_key = self.__user_key
        user_state = UserState.lookup(user_key)
        new_stock = StockList(name, [], description, user_key, user_state.get_stocklist_map())
        for stock in self:
            if stock not in new_stock:
                new_stock.append_stock(stock, save=False)
        for stock in other:
            if stock not in new_stock:
                new_stock.append_stock(stock, save=False)
        new_stock.save()
        return new_stock

    @staticmethod
    def rebuild_data():
        from Database import Database

        return Database.rebuild_data()

    @staticmethod
    def read_data():
        from Database import Database

        return Database.read_data()

    def __iter__(self):
        return self.__category.__iter__()

    def __str__(self):
        s = f"{self.__name}: {self.__description}: "
        s += "Lists of Stocks: ("
        for stock in self.__category:
            s += str(stock)

        s += ")"

        return s

    def save(self):
        from Database import Database

        Database.save_stocklist(self)

