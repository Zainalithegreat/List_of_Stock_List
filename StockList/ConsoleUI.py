from Stock import Stock
from input_validation import select_item, input_string, y_or_n, input_float, input_int
from StockList import StockList
from ComputerCompany import ComputerCompany
from Bank import Bank



class ConsoleUI:
    CHOICES = ["ps", "pc", "cs", "dc", "sc", "ms", "ds", "ac", "rc", "us", "js", "x"]
    __all_stocks = None
    __all_category = []

    @classmethod
    def init(cls):
        cls.__all_stocks, cls.__all_category = StockList.read_data()

    @classmethod
    def select_stock(cls, stock=None):
        if stock is None:
            stock = cls.__all_stocks
        keys = []
        map = {}
        pos = 1
        for stk in stock:
            keys.append(stk.get_key())
            map[str(pos)] = stk.get_key()
            pos += 1
        keys.append("None")
        map[str(pos)] = "None"
        print("Please select a stock from the list below: ")
        pos = 1
        for key in keys:
            print(f"     {pos}: {key}")
            pos += 1
        key = select_item("Enter the stock or 'None' to exit: ", "Please type a stock", choices=keys, map=map)
        if key == "None":
            return None
        stk = Stock.lookup(key)
        return stk

    @classmethod
    def select_category(cls, include_all_stocks=False):
        names = []
        map = {}
        pos = 1

        for stk in cls.__all_category:
            if include_all_stocks or stk.get_name != "All Stocks":
                names.append(stk.get_name())
                map[str(pos)] = stk.get_name()
                pos += 1
        names.append("None")
        map[str(pos)] = "None"
        print("Please select a stock name from the list below: ")
        pos = 1

        for name in names:
            print(f"     {pos}: {name}")
            pos += 1

        name = select_item("Enter the name or 'None' to exit: ", "Please type a stock category name!", choices=names, map=map)

        if name == "None":
            return None

        stk = StockList.lookup(name)
        return stk

    @classmethod
    def list_stocks(cls):
        if cls.__all_stocks is None:
            print("No stocks available to list.")
            return
        for stock in cls.__all_stocks:
            print(stock.get_key(), ": ", stock, sep="")

    @classmethod
    def list_stocklist(cls):
        for stocklist in cls.__all_category:
            print(f"{stocklist.get_name()}: {stocklist.get_description()}")

    # Ask about map, ask about classmethod
    @classmethod
    def create_stockcategory(cls):
        name = input_string("Please enter the name for the stock or 'None' to exit: ")
        if name == "None":
            return
        stocklist = StockList.lookup(name)
        if stocklist is not None:
            print("Err! Stock already exists.")
            return

        description = input_string("Please enter a description: ")
        stocklist = StockList(name, [], description, save=True)
        cls.__all_category.append(stocklist)
        print("StockCategory created")

    @classmethod
    def delete_stockcategory(cls):
        stock_category = cls.select_category()
        if stock_category is None:
            return
        cls.__all_category.remove(stock_category)
        stock_category.delete()
        print("Stock category deleted.")


    @classmethod
    def show_stockcategory(cls):
        stock_category = cls.select_category(True)
        if stock_category is None:
            return
        print()
        print(f"Name: {stock_category.get_name()}")
        print(f"Description: {stock_category.get_description()}")
        for category in stock_category:
            print("    ", category)


    @classmethod
    def create_stock(cls):
        stock = None
        is_stock = input_string("Is the new stock a generic stock: ")

        name = input_string("Please enter the name for the stock: ")
        if Stock.lookup(f"{name}".lower()) is not None:
            print("The stock is already in the database please try again later")
            return
        price = input_float("Please enter the price for the stock: ")
        starting_price = input_float("Please enter the opening price for the stock: ")
        date = input_string("Please enter the date of the stocks price (Month/Day/Year): ")
        time = input_string("Please enter the time of the stocks price (00:00 for example 01:12): ")

        if is_stock.lower() == 'y':
            stock = Stock(name,  price, starting_price, date, time, save=True)
        elif is_stock.lower() == 'n':
            print("Option 1: Would you like to create an object of Computer Company.")
            print("Option 2: Would you like to create an object of the Bank Company.")
            num = input_int("Choose Option 1 or 2 [1/2]: ", ge=1, le=3)
            if num == 1:
                best_gpu = input_string("What is the best product this company sells: ")
                stock = ComputerCompany(name, price, starting_price, date, time, best_gpu, save=True)

            elif num == 2:
                accounts = input_int("How many accounts does this bank have: ")
                stock = Bank(name, price, starting_price, date, time, accounts, save=True)
        cls.__all_stocks.append_stock(stock)
        print("Stock Created.")

    @classmethod
    def delete_stock(cls):
        stk = cls.select_stock()
        if stk is None:
            return
        for stock in cls.__all_category:
            if stk in stock:
                stock.remove(stk)
        stk.delete()
        print("Stock deleted.")

    @classmethod
    def add_stock(cls):
        stock = cls.select_category()
        if stock is None:
            return

        stk = cls.select_stock()
        if stk is None:
            return

        if stk in stock:
            print("The stock is already in the category")
            return
        stock.append_stock(stk)
        print("Added stock to category")

    @classmethod
    def remove_listcategory(cls):
        stock = cls.select_category()
        if stock is None:
            return

        stk = cls.select_stock(stock)
        if stk is None:
            return

        if stk not in stock:
            print("The stock is not in the category")
            return
        stock.remove(stk)
        print("Removed stock from category")

    @classmethod
    def update_stock(cls):
        stock = cls.select_stock()
        if stock is None:
            print("Not found")
            return
        price = input_float("What is the new price for the stock: ")
        stock.update_price(price)
        print("Price Updated")

    @classmethod
    def join_stockcategory(cls):
        stock_1 = cls.select_category(include_all_stocks=True)
        if stock_1 is None:
            return
        stock_2 = cls.select_category(include_all_stocks=True)
        if stock_2 is None:
            return
        new_stock = stock_1 + stock_2
        cls.__all_category.append(new_stock)
        print("Joined Stock Categories.")



    @staticmethod
    def print_menu():
        print("Please select an option from the list below: ")
        print("      ps: Print all Stocks")
        print("      pc: Print category")
        print("      cs: Create stock category")
        print("      dc: Delete a category of stocks")
        print("      sc: Show category")
        print("      ms: Make stock")
        print("      ds: Delete stock")
        print("      ac: Add stock to category")
        print("      rc: Remove stock from category")
        print("      us: Update a stocks price")
        print("      js: Join two stock category")
        print("      x: Exit")

    @classmethod
    def run(cls):
        while True:
            cls.print_menu()
            choice = select_item("Please select an item: ", "Item must be a choice in the menu.", choices=cls.CHOICES)
            print()
            if choice == "x":
                break
            elif choice == "ps":
                cls.list_stocks()
            elif choice == "pc":
                cls.list_stocklist()
            elif choice == "cs":
                cls.create_stockcategory()
            elif choice == "dc":
                cls.delete_stockcategory()
            elif choice == "sc":
                cls.show_stockcategory()
            elif choice == "ms":
                cls.create_stock()
            elif choice == "ds":
                cls.delete_stock()
            elif choice == "ac":
                cls.add_stock()
            elif choice == "rc":
                cls.remove_listcategory()
            elif choice == "us":
                cls.update_stock()
            elif choice == "js":
                cls.join_stockcategory()
            print()
        print("Goodbye!")


if __name__ == "__main__":
    ConsoleUI.init()
    ConsoleUI.run()
