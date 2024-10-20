from WebUI import  WebUI
from flask import render_template, request
from StockList import StockList
from Stock import Stock
from Bank import Bank
from ComputerCompany import ComputerCompany

class UpdateRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route('/update_stock_price')
    def update_stock_price():
        return render_template("update/update_stock_price.html", stocks=WebUI.get_all_stocks())

    @staticmethod
    @__app.route("/do_update_stock_price", methods=["GET", "POST"])
    def do_update_stock_price():
        key, error = WebUI.validate_field("The stock", "stock")
        if key is None:
            return error
        stock = WebUI.lookup_stock(key)

        if stock is None:
            return render_template(
                "error.html",
                message_header="Stock does not exist!",
                message_body=f"The stock {key} does not exist. Please choose another stock and try again."
            )
        if "price" in request.form:
            price = request.form["price"].strip()
        else:
            price = 0

        stock.update_price(price)
        return render_template("update/confirm_price_updated.html", stock=stock)

    @staticmethod
    @__app.route("/add_stock_to_stocklist")
    def add_stock_to_stocklist():
        return render_template("update/add_stock_to_stocklist.html", stocks=WebUI.get_all_stocks(), stocklists=WebUI.get_all_stocklists())

    @staticmethod
    @__app.route("/do_add_stock_to_stocklist", methods=["GET", "POST"])
    def do_add_stock_to_stocklist():
        stock_key, error = WebUI.validate_field("The stock", "stock")
        if stock_key is None:
            return error
        stock = WebUI.lookup_stock(stock_key)

        if stock is None:
            return render_template(
                "error.html",
                message_header="Stock does not exist!",
                message_body=f"The stock {stock_key} does not exist. Please choose another stock and try again."
            )
        stocklist_key, error = WebUI.validate_field("The stocklist name", "stocklist")
        if stocklist_key is None:
            return error

        stocklist = WebUI.lookup_stocklist(stocklist_key.lower())
        if stocklist is None:
            return render_template(
                "error.html",
                message_header=f"The stocklist {stocklist_key} was not found.",
                message_body=f"A stocklist with the name '{stocklist_key}' was not found. Please choose another stocklist and try again."
            )
        if stock in stocklist:
            return render_template(
                "error.html",
                message_header=f"The stock is already in the stocklist.",
                message_body=f"The stock '{stock.get_printable_key()}' is already in the stocklist '{stocklist.get_printable_key()}' with the name '{stocklist_key}'."
            )
        stocklist.append_stock(stock)
        return render_template("update/confirm_stock_added_to_stocklist.html", stock=stock, stocklist=stocklist)



    @staticmethod
    @__app.route("/remove_stock_from_stocklist")
    def remove_stock_from_stocklist():
        return render_template("update/remove_stock_from_stocklist.html", stocks=WebUI.get_all_stocks(),
                               stocklists=WebUI.get_all_stocklists())

    @staticmethod
    @__app.route("/do_remove_stock_from_stocklist", methods=["GET", "POST"])
    def do_remove_stock_from_stocklist():
        stock_key, error = WebUI.validate_field("The stock", "stock")
        if stock_key is None:
            return error
        stock = WebUI.lookup_stock(stock_key)

        if stock is None:
            return render_template(
                "error.html",
                message_header="Stock does not exist!",
                message_body=f"The stock {stock_key} does not exist. Please choose another stock and try again."
            )
        stocklist_key, error = WebUI.validate_field("The stocklist name", "stocklist")
        if stocklist_key is None:
            return error

        stocklist = WebUI.lookup_stocklist(stocklist_key.lower())
        if stocklist.get_name() == StockList.ALL_STOCKS:
            return render_template(
                "error.html",
                message_header=f"Cannot remove stock.",
                message_body=f"You cannot remove stocks from the '{StockList.ALL_STOCKS}' stocklist."
            )
        if stocklist is None:
            return render_template(
                "error.html",
                message_header=f"The stocklist {stocklist_key} was not found.",
                message_body=f"A stocklist with the name '{stocklist_key}' was not found. Please choose another stocklist and try again."
            )
        if stock not in stocklist:
            return render_template(
                "error.html",
                message_header=f"The stock is not in the stocklist.",
                message_body=f"The stock '{stock.get_printable_key()}' is not in the stocklist '{stocklist.get_printable_key()}' with the name '{stocklist_key}'."
            )

        stocklist.remove(stock)
        return render_template("update/confirm_stock_remove_from_stocklist.html", stock=stock, stocklist=stocklist)