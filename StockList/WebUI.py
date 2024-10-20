from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
from StockList import StockList
import os
import bcrypt
from UserState import UserState

class WebUI:
    __all_stocks = None
    __all_stocklists = None
    __app = Flask(__name__)
    ALLOWED_PATHS = [
        "/login",
        "/do_login",
        "/static/stocklist.css"
    ]
    MENU = {
        "Print": {
            "print_stocklist?stocklist=Stock": "Print a list of all stocks.",
            "print_stocklists": "Print a list of all stocklists.",
            "show_stocklist_contents": "Select a stocklist and show the contents."
        },
        "Create": {
            "create_generic_stock": "Create a generic stock.",
            "create_bank_stock": "Create a bank stock.",
            "create_computer_stock": "Create a computer stock.",
            "create_stocklist": "Create a new stocklist.",
            "join_stocklists": "Join two stocklists together."
        },
        "Update": {
            "update_stock_price": "Update the stocks price.",
            "add_stock_to_stocklist": "Add a stock to a stocklist.",
            "remove_stock_from_stocklist": "Remove a stock from a stocklist.",
        },
        "Delete": {
            "delete_stock": "Delete a stock.",
            "delete_stocklist": "Delete a stocklist."
        }
    }

    @classmethod
    def get_app(cls):
        return cls.__app

    @classmethod
    def get_user(cls):
        if "user" in session:
            return session["user"]
        return None

    @classmethod
    def get_user_key(cls):
        user = cls.get_user()
        if user is None:
            return None
        return user.get_key()
    @classmethod
    def get_all_stocklists(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_all_stocklists()
        return None

    @classmethod
    def get_all_stocks(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_all_stocks()
        return None

    @classmethod
    def get_stock_map(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_stock_map()
        return None

    @classmethod
    def get_stocklist_map(cls):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.get_stocklist_map()
        return None

    @classmethod
    def login(cls, user):
        session["user"] = user
        UserState(user)

    @classmethod
    def logout(cls):
        UserState.logout(WebUI.get_user_key())

    @classmethod
    def lookup_stocklist(cls, key):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.lookup_stocklist(key)

    @classmethod
    def lookup_stock(cls, key):
        user_state = UserState.lookup(cls.get_user_key())
        if user_state is not None:
            return user_state.lookup_stock(key)

    @classmethod
    def init(cls):
        cls.__all_stocks, cls.__all_stocklists = StockList.read_data()

    @classmethod
    def validate_field(cls, object_name, field_name):
        print(request.form)
        if field_name not in request.form:
            return None, render_template(
                "error.html",
                message_header=f"{object_name} was not specified!",
                message_body=f"{object_name} was not specified. Please check the URL and try again."
            )
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template(
                "error.html",
                message_header=f"A {object_name} was not specified!",
                message_body=f"No {object_name} was not specified. Please check the URL and try again."
            )
        return field_value, None

    @staticmethod
    @__app.before_request
    def before_request():
        if "user" not in session:
            if request.path not in WebUI.ALLOWED_PATHS:
                return redirect(url_for("login"))
            return
        user_state = UserState.lookup(WebUI.get_user_key())
        if user_state is None:
            UserState(WebUI.get_user())

    @__app.route('/')

    @staticmethod
    def homepage():
        return render_template("homepage.html", options=WebUI.MENU)


    @classmethod
    def run(cls):
        from routes.PrintRoutes import PrintRoutes
        from routes.CreateRoutes import CreateRoutes
        from routes.UpdateRoutes import UpdateRoutes
        from routes.DeleteRoutes import DeleteRoutes
        from routes.UserRoutes import UserRoutes

        if "APPDATA" in os.environ:
            path = os.environ["APPDATA"]
        elif "HOME" in os.environ:
            path = os.environ["HOME"]
        else:
            raise Exception("Couldn't find config folder")

        cls.__app.secret_key = bcrypt.gensalt()
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        Session(cls.__app)

        cls.__app.run(host="0.0.0.0", port=8443, ssl_context=(path + "/stock_list/cert.pem", path + "/stock_list/key.pem"))

