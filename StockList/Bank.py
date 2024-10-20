from Stock import Stock
from input_validation import input_string, input_int

class Bank(Stock):
    __num_accounts = 0

    def __init__(self, name, price, starting_price, date, time, user_key, stock_map, num_accounts, save=False):
        self.__num_accounts = num_accounts
        super().__init__(name, price, starting_price, date, time, user_key, stock_map, save=save)

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "Bank_Stock"
        dict["num_accounts"] = self.__num_accounts

        return dict

    def get_key(self):
        return f"{self.get_name()}".lower()

    def get_printable_key(self):
        return f"{self.get_name()}"

    def __str__(self):
        return f"{super().__str__()} (number of accounts: {self.__num_accounts})"

    def to_html(self):
        html = super().to_html()
        return html + " A Bank Stock"

    @staticmethod
    def make_key(name):
        return f"{name}".lower()
