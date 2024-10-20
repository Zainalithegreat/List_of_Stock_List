from WebUI import WebUI
from flask import render_template, request
from StockList import StockList
from Stock import Stock


class DeleteRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/delete_stocklist")
    def delete_stocklist():
        return render_template("delete/delete_stocklist.html", stocklists=WebUI.get_all_stocklists())

    @staticmethod
    @__app.route("/do_delete_stocklist", methods=["GET", "POST"])
    def do_delete_stocklist():
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
        if stocklist.get_name() == StockList.ALL_STOCKS:
            return render_template(
                "error.html",
                message_header=f"Cannot delete stocklist.",
                message_body=f"You cannot delete the '{StockList.ALL_STOCKS}' stocklist."
            )
        WebUI.get_all_stocklists().remove(stocklist)
        stocklist.delete()
        return render_template("delete/confirm_stocklist_deleted.html", stocklist=stocklist)


    @staticmethod
    @__app.route("/delete_stock")
    def delete_stock():
        return render_template("delete/delete_stock.html", stocks=WebUI.get_all_stocks())


    @staticmethod
    @__app.route("/do_delete_stock", methods=["GET", "POST"])
    def do_delete_stock():
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
        for stocklist in WebUI.get_all_stocklists():
            if stock in stocklist:
                stocklist.remove(stock)
        stock.delete()

        return render_template("delete/confirm_stock_deleted.html", stock=stock)

