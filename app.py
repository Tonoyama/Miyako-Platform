#!/usr/bin/env python3
from flask import Flask, request, Response, abort, render_template, url_for, redirect, flash, Blueprint
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict
import flask_excel as excel
import pyexcel_xls
import pandas as pd
import os
import sqlite3
from contextlib import closing


web_app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(web_app)
web_app.config['SECRET_KEY'] = os.urandom(24)
web_app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

UPLOAD_FOLDER = "./excel"

#Blueprint
from Payroll.payroll import bp_payroll

web_app.register_blueprint(bp_payroll)

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "yudaitonoyama@gmail.com", "srkn395%"),
    2: User(2, "user02", "Fusion360")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.email]["password"] = i.password
    user_check[i.email]["id"] = i.id


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@web_app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(web_app.root_path, 'static/images/favicon.ico'), 'favicon.ico', )

#ホーム画面
@web_app.route('/', methods=["GET","POST"])
def home():
    return render_template("home.html")

# ユーザー登録画面
@web_app.route('/create_acount/', methods=["GET", "POST"])
def create_acount():
    return render_template("create_acount.html")

# 選択画面
@web_app.route('/protected/', methods=["GET", "POST"])
@login_required
def protected():
    return render_template("select_work.html")

# ユーザー管理画面
@web_app.route('/user_manage/', methods=["GET", "POST"])
@login_required
def user_manage():
    return render_template("user_manage.html")

# 来客・売上予測画面
@web_app.route('/prediction/', methods=["GET", "POST"])
@login_required
def prediction():
    return render_template("prediction.html")

# ログインパス
@web_app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # ユーザーチェック
        if(request.form["email"] in user_check and request.form["password"] == user_check[request.form["email"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["email"]]["id"]))
            return render_template("login_success.html")
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@web_app.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template("logout.html")

@web_app.errorhandler(401)
def unauthorized_error(error):
    return render_template("unauthorized_error.html"), 401

if __name__ == '__main__':
    web_app.run(host="0.0.0.0",port=8080,debug=True)
