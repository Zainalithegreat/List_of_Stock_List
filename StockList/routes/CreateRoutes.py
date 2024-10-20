from WebUI import  WebUI
from flask import render_template, request
from StockList import StockList
from Stock import Stock
from Bank import Bank
from ComputerCompany import ComputerCompany

class CreateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/create_stocklist')
    def create_stocklist():
        return render_template("create/create_stocklist.html")

    @staticmethod
    @__app.route('/do_create_stocklist', methods=['GET', 'POST'])
    def do_create_stocklist():
        name, error = WebUI.validate_field("The Stocklist name","name")
        if name is None:
            return error
        key = name.lower()
        stocklist = WebUI.lookup_stocklist(key)

        if stocklist is not None:
            return render_template(
                "error.html",
                message_header="Stocklist already exists!",
                message_body=f"A stocklist named {name} already exists. Please choose another name and try again."
            )
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""
        stocklist = StockList(name, [], description, WebUI.get_user_key(), WebUI.get_stocklist_map(), save=True)
        WebUI.get_all_stocklists().append(stocklist)
        return render_template("create/confirm_stocklist_created.html", stocklist=stocklist)

    @staticmethod
    @__app.route('/create_generic_stock')
    def create_generic_stock():
        return render_template("create/create_generic_stock.html")


    @staticmethod
    @__app.route('/do_create_generic_stock', methods=['GET', 'POST'])
    #name, price, starting_price, date, time
    def do_create_generic_stock():
        name, error = WebUI.validate_field("The Generic Stock name", "name")
        if name is None:
            return error
        key = Stock.make_key(name).lower()
        stock = WebUI.lookup_stock(key)

        if stock is not None:
            return render_template(
                "error.html",
                message_header=f"stock already exists!",
                message_body=f"A stock named '{name}' already exists. Please choose another name and try again."
            )

        price, error = WebUI.validate_field("The Generic Stock price","price")
        if price is None:
            return error

        starting_price, error = WebUI.validate_field("The generic Stock starting price", "starting_price")
        if starting_price is None:
            return error

        date, error = WebUI.validate_field("The Generic Stock date", "date")
        if date is None:
            return error
        time, error = WebUI.validate_field("The Generic Stock time", "time")
        if time is None:
            return error

        stock = Stock(name, price, starting_price, date, time, WebUI.get_user_key(), WebUI.get_stock_map(), save=True)

        WebUI.get_all_stocks().append_stock(stock)
        return render_template("create/confirm_generic_stock_created.html", stock=stock)




    @staticmethod
    @__app.route('/create_bank_stock')
    def create_bank_stock():
        return render_template("create/create_bank_stock.html")


    @staticmethod
    @__app.route('/do_create_bank_stock', methods=['GET', 'POST'])
    #name, price, starting_price, date, time
    def do_create_bank_stock():
        name, error = WebUI.validate_field("The Bank Stock name", "name")
        if name is None:
            return error
        key = Bank.make_key(name).lower()
        stock = WebUI.lookup_stock(key)

        if stock is not None:
            return render_template(
                "error.html",
                message_header=f"stock already exists!",
                message_body=f"A stock named '{name}' already exists. Please choose another name and try again."
            )

        price, error = WebUI.validate_field("The Bank Stock price","price")
        if price is None:
            return error

        starting_price, error = WebUI.validate_field("The Bank Stock starting price", "starting_price")
        if starting_price is None:
            return error

        date, error = WebUI.validate_field("The Bank Stock date", "date")
        if date is None:
            return error
        time, error = WebUI.validate_field("The Bank Stock time", "time")
        if time is None:
            return error

        num_accounts, error = WebUI.validate_field("The Bank Stock accounts", "num_accounts")
        if num_accounts is None:
            return error

        stock = Bank(name, price, starting_price, date, time, WebUI.get_user_key(), WebUI.get_stock_map(), num_accounts, save=True)

        WebUI.get_all_stocks().append_stock(stock)
        return render_template("create/confirm_bank_stock_created.html", stock=stock)



    @staticmethod
    @__app.route('/create_computer_stock')
    def create_computer_stock():
        return render_template("create/create_computer_stock.html")

    @staticmethod
    @__app.route('/do_create_computer_stock', methods=['GET', 'POST'])
    # name, price, starting_price, date, time
    def do_create_computer_stock():
        name, error = WebUI.validate_field("The Computer Stock name", "name")
        if name is None:
            return error
        key = ComputerCompany.make_key(name).lower()
        stock = WebUI.lookup_stock(key)

        if stock is not None:
            return render_template(
                "error.html",
                message_header=f"stock already exists!",
                message_body=f"A stock named '{name}' already exists. Please choose another name and try again."
            )

        price, error = WebUI.validate_field("The Computer Stock price", "price")
        if price is None:
            return error

        starting_price, error = WebUI.validate_field("The Computer Stock starting price", "starting_price")
        if starting_price is None:
            return error

        date, error = WebUI.validate_field("The Computer Stock date", "date")
        if date is None:
            return error
        time, error = WebUI.validate_field("The Computer Stock time", "time")
        if time is None:
            return error

        best_gpu, error = WebUI.validate_field("The Computer Stock best product", "best_gpu")
        if best_gpu is None:
            return error

        stock = ComputerCompany(name, price, starting_price, date, time, WebUI.get_user_key(), WebUI.get_stock_map(), best_gpu, save=True)

        WebUI.get_all_stocks().append_stock(stock)
        return render_template("create/confirm_computer_stock_created.html", stock=stock)

    @staticmethod
    @__app.route("/join_stocklists")
    def join_stocklists():
        return render_template("create/join_stocklists.html", stocklists=WebUI.get_all_stocklists())


    @staticmethod
    @__app.route("/do_join_stocklists", methods=["GET", "POST"])
    def do_join_stocklists():
        first_key, error = WebUI.validate_field("The first stocklist name", "first_stocklist")
        if first_key is None:
            return error

        second_key, error = WebUI.validate_field("The second stocklist name", "second_stocklist")
        if second_key is None:
            return error

        first_stocklist = WebUI.lookup_stocklist(first_key.lower())
        if first_stocklist is None:
            return render_template(
                "error.html",
                message_header=f"The stocklist {first_key} was not found.",
                message_body=f"A stocklist with the name '{first_key}' was not found. Please choose another stocklist and try again."
            )

        second_stocklist = WebUI.lookup_stocklist(second_key.lower())
        if second_stocklist is None:
            return render_template(
                "error.html",
                message_header=f"The stocklist {second_key} was not found.",
                message_body=f"A stocklist with the name '{second_key}' was not found. Please choose another stocklist and try again."
            )
        new_key = f"{first_stocklist.get_name()}/{second_stocklist.get_name()}"
        new_stocklist = WebUI.lookup_stocklist(new_key.lower())
        if new_stocklist is not None:
            return render_template(
                "error.html",
                message_header=f"The stocklist {new_key} already exists.",
                message_body=f"A stocklist with the name '{new_key}' already exists. Please choose another stocklist and try again."
            )
        new_stocklist = first_stocklist + second_stocklist
        WebUI.get_all_stocklists().append(new_stocklist)

        return render_template("create/confirm_stocklists_joined.html", first_stocklist=first_stocklist, second_stocklist=second_stocklist, new_stocklist=new_stocklist)


