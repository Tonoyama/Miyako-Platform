from datetime import timedelta
from dateutil.relativedelta import relativedelta
import datetime, jpholiday
import app


#今日
today = datetime.date.today()
#print(today)

one_month_after = today + relativedelta(months=1)
#print(one_month_after)

date = datetime.date(2015, 1, 1) - datetime.timedelta(days=1)
#print(date)

#日を設定
endDate = datetime.date(2020, 5, 10)
#print(endDate)

#差分を計算
period = endDate - today
#print(period)

#差分を整数型に変換
period = int(period.days)

#差分を使って、現在から終日まで一日ずつ足していく
"""
for d in range(period):
    day = today + datetime.timedelta(days=d)
    print(day)  
"""

DATE = "20200209" # 日付は８桁文字列の形式

holiday_list = []

Date = (datetime.datetime.strptime(DATE, '%Y%m%d')).date()
if Date.weekday() <= 5 or jpholiday.is_holiday(Date):
    holiday_list.append(0)
else:
    holiday_list.append(1)

#print(holiday_list)