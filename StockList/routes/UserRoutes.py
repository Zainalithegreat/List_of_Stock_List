from WebUI import  WebUI
from flask import render_template, request, session, redirect, url_for
from StockList import StockList
from Stock import Stock
from Bank import Bank
from ComputerCompany import ComputerCompany
from User import User

class UserRoutes:
    __app = WebUI.get_app()

    @staticmethod
    @__app.route("/get_user")
    def get_user():
        if "username" in session:
            return session["username"]
        return "None"

    @staticmethod
    @__app.route("/set_user")
    def set_user():
        if "username" in request.args:
            session["username"] = request.args["username"]
            return "User set"
        if "username" in session:
            del session["username"]
        return "User cleared"

    @staticmethod
    @__app.route("/login")
    def login():
        return render_template("user/login.html")

    @staticmethod
    @__app.route("/do_login", methods=["GET", "POST"])
    def do_login():
        username, error = WebUI.validate_field("Username", "username")
        if error is not None:
            return error
        password, error = WebUI.validate_field("Password", "password")
        if error is not None:
            return error
        type, error = WebUI.validate_field("Type", "type")
        if error is not None:
            return error
        user = User.read_user(username)
        if type == "login":
            if user is None:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt failed. Please check your account information and try again"
                )
            logged_in = user.verify_password(password)
            if not logged_in:
                return render_template(
                    "error.html",
                    message_header="Login Failed",
                    message_body="The login attempt failed. Please check your account information and try again"
                )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        elif type == "register":
            if user is not None:
                return render_template(
                    "error.html",
                    message_header="Registration Failed",
                    message_body="The registration attempt failed. Please check your account information and try again"
                )
            user = User(username, User.hash_password(password))
            # name, category, description, user_key, stocklist_map, save=False
            user.add()
            StockList(
                StockList.ALL_STOCKS,
                [],
                f"All Stocks for {username}",
                user.get_key(),
                {},
                save=True
            )
            WebUI.login(user)
            return redirect(url_for("homepage"))
        else:
            return render_template(
                "error.html",
                message_header="Unknown Login Type",
                message_body="Login type must be login or register. Please check your account information and try again"
            )


    @staticmethod
    @__app.route("/logout")
    def logout():
        if "user" in session:
            del session["user"]
        return redirect(url_for("login"))