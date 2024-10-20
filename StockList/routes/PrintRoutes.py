from WebUI import WebUI
from flask import render_template, request
from StockList import StockList


class PrintRoutes:
    __app = WebUI.get_app()

    @__app.route('/print_stocklists')
    @staticmethod
    def print_stocklists():
        return render_template("print/print_stocklists.html", stocklists=WebUI.get_all_stocklists())

    @__app.route('/print_stocklist')
    @staticmethod
    def print_stocklist():
        if "stocklist" not in request.args:
            return render_template(
                "error.html",
                message_header="Stocklist not specified!",
                message_body=f"No stocklist was specified. Please check the URL and try again."
            )
        name = request.args["stocklist"]
        key = StockList.make_key(name)
        stocklist = WebUI.lookup_stocklist(key)
        if stocklist is None:
            return render_template(
                "error.html",
                message_header="Stocklist not found!",
                message_body=f"No stocklist named '{key}' was not found. Please check the URL and try again."
            )
        return render_template('print/print_stocklist.html', stocklist=stocklist)

    @staticmethod
    @__app.route("/show_stocklist_contents")
    def show_stocklist_contents():
      return render_template("print/show_stocklist_contents.html", stocklists=WebUI.get_all_stocklists())



