from Stock import Stock
from input_validation import input_string, input_int


class ComputerCompany(Stock):
    __best_gpu = ""

    def __init__(self, name, price, starting_price, date, time, user_key, stock_map, best_gpu, save=False):
        self.__best_gpu = best_gpu
        super().__init__(name, price, starting_price, date, time, user_key, stock_map, save=save)

    def to_dict(self):
        dict = super().to_dict()
        dict["type"] = "Computer_Stock"
        dict["best_gpu"] = self.__best_gpu

        return dict

    def get_key(self):
        return f"{self.get_name()}".lower()

    def get_printable_key(self):
        return f"{self.get_name()}"

    def __str__(self):
        return f"{super().__str__()} (Best Graphics Card: {self.__best_gpu})"

    def to_html(self):
        html = super().to_html()
        return html + " A Computer hardware Stock"

    @staticmethod
    def make_key(name):
        return f"{name}".lower()

