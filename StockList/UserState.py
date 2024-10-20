class UserState:
    __user = None
    __all_stocks = None
    __all_stocklists = None
    __stock_map = None
    __stocklist_map = None
    __map = {}

    def __init__(self, user):
        from Database import Database
        self.__user = user
        self.__all_stocks, self.__all_stocklists, self.__stock_map, self.__stocklist_map = Database.read_data(
            user.get_key()
        )
        self.__class__.__map[self.get_key()] = self

    @classmethod
    def logout(cls, user_key):
        if user_key in cls.__map:
            del cls.__map[user_key]

    @classmethod
    def lookup(cls, key):
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def get_key(self):
        return self.__user.get_key()

    def get_all_stocklists(self):
        return self.__all_stocklists

    def get_all_stocks(self):
        return self.__all_stocks


    def get_stocklist_map(self):
        return self.__stocklist_map

    def get_stock_map(self):
        return self.__stock_map

    def lookup_stocklist(self, key):
        if key in self.__stocklist_map:
            return self.__stocklist_map[key]
        return None

    def lookup_stock(self, key):
        if key in self.__stock_map:
            return self.__stock_map[key]
        return None
