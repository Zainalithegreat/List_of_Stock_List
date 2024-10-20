class Stock:
    __name = ""
    __price = 0
    __starting_price = 0
    __date = ""
    __time = ""
    __user_key = ""

    def __init__(self, name, price, starting_price, date, time, user_key, stock_map, save=False):
        self.__name = name
        self.__price = price
        self.__starting_price = starting_price
        self.__date = date
        self.__time = time
        self.__user_key = user_key
        stock_map[self.get_key()] = self

        if save:
            self.save()

    @classmethod
    def build(cls, stock_dict, stock_map):
        from ComputerCompany import ComputerCompany
        from Bank import Bank
        if stock_dict["type"] == "Stock":
            return Stock(
                stock_dict["name"],
                stock_dict["price"],
                stock_dict["starting_price"],
                stock_dict["date"],
                stock_dict["time"],
                stock_dict["user_key"],
                stock_map
            )
        elif stock_dict["type"] == "Computer_Stock":
            return ComputerCompany(
                stock_dict["name"],
                stock_dict["price"],
                stock_dict["starting_price"],
                stock_dict["date"],
                stock_dict["time"],
                stock_dict["user_key"],
                stock_map,
                stock_dict["best_gpu"]
            )
        elif stock_dict["type"] == "Bank_Stock":
            return Bank(
                stock_dict["name"],
                stock_dict["price"],
                stock_dict["starting_price"],
                stock_dict["date"],
                stock_dict["time"],
                stock_dict["user_key"],
                stock_map,
                stock_dict["num_accounts"]
            )

    def to_dict(self):
        return {
            "_id": self.get_id(),
            "type": "Stock",
            "name": self.__name,
            "price": self.__price,
            "starting_price": self.__starting_price,
            "date": self.__date,
            "time": self.__time,
            "user_key": self.__user_key
        }

    def get_id(self):
        return f"{self.get_key()}|{self.__user_key}"

    def get_key(self):
        return f"{self.__name}".lower()

    def get_printable_key(self):
        return f"{self.__name}"

    @staticmethod
    def make_key(name):
        return f"{name}".lower()

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def update_price(self, price):
        self.__price = price
        self.save()

    def __str__(self):
        return f"{self.get_name()}: ${self.get_price()} (Opening Price: ${self.__starting_price}, Date: {self.__date}, Time: {self.__time})"

    def __repr__(self):
        return f"{self.get_name()}: ${self.get_price()} (Opening Price: ${self.__starting_price}, Date: {self.__date}, Time: {self.__time})"

    def to_html(self):
        return f"{self.get_name()}: ${self.get_price()} (Opening Price: ${self.__starting_price}, Date: {self.__date}, Time: {self.__time})"



    def delete(self):
        from Database import Database
        from UserState import UserState

        stock_key = self.get_key()
        user_state = UserState.lookup(self.__user_key)
        stock_map = user_state.get_stock_map()
        if stock_key in stock_map:
            del stock_map[stock_key]
        Database.delete_stock(self)


    def save(self):
        from Database import Database

        Database.save_stock(self)
