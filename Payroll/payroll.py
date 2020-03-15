from flask import render_template, request, Blueprint
from flask_login import login_required
from werkzeug.utils import secure_filename
import os


bp_payroll = Blueprint("bp_payroll", __name__, template_folder="templates",
                        static_folder="static",url_prefix="/payroll")

UPLOAD_FOLDER = "./excel"

@bp_payroll.route('/payroll/', methods=["GET"])
@login_required
def payroll_get():
    return render_template("Payroll/payroll_form.html")

@bp_payroll.route('/payroll/', methods=["POST"])
@login_required
def payroll_post():
    if request.method == "POST":
        file = request.files["excel"]
        print(file)
        filename = secure_filename(file.filename)
        print(filename)
        filepath = file.save(os.path.join(UPLOAD_FOLDER, filename))
        print(filepath)
    form_date = request.form["date"]
    #総労働時間
    all_work_time = excel_read_color.all_work_time
    #総深夜労働時間
    total_night_work_list = excel_read_color.total_night_work_list
    #深夜労働時間リスト
    list_night_work_list = excel_read_color.list_night_work_list
    #総通常労働時間
    total_noon_work_list = excel_read_color.total_noon_work_list
    #通常労働時間リスト
    list_noon_work_list = excel_read_color.list_noon_work_list
    payroll_user = ["岡田","上田","北村","矢巻","町口","吉田","今井","福本","高島","藤田","本松","関岡","田渕","山本","殿山","加差野","予備枠","近藤","小林"]
    all_total_cost = excel_read_color.all_total_cost
    sum_wage_per_day = excel_read_color.array_sum_wage_per_day
    shop = request.form.get("shop")
    date = request.form.get("date")
    print(date)
    return render_template("Payroll/payroll_post.html", filepath=filepath, all_work_time=all_work_time, total_night_work_list=total_night_work_list, \
        list_night_work_list=list_night_work_list, total_noon_work_list=total_noon_work_list, list_noon_work_list=list_noon_work_list, \
            all_total_cost=all_total_cost, payroll_user=payroll_user, sum_wage_per_day=sum_wage_per_day, shop=shop, date=date, payroll_round_up = zip(payroll_user, sum_wage_per_day, list_noon_work_list, list_night_work_list))

import excel_read_color
