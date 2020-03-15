import xlrd
from flask import Flask, send_from_directory
import itertools as itr
import numpy as np
import bottom_excel


fname = '/Users/yudai/Desktop/三条シフト2019_12.xls' 

#エクセルファイルを読み込む(formatting_info=Trueを付けて読み込む)
book  = xlrd.open_workbook(fname, formatting_info=True)

file_read_color = []

#1,2の場合、１日しか計算していない
for sheet_num in range(1, 17):
    for index_num in range(1, 21):
        for column_num in range(1, 32):
            #print(sheet_num, index_num, column_num)
            #print("index_num: " + str(index_num))
            #print("columns_num: " + str(column_num))
            #シートを選択する
            sheet = book.sheet_by_index(sheet_num)
            #セルを選択する
            cell = sheet.cell(index_num, column_num)
            #背景色を取得する
            xfx = cell.xf_index
            xf = book.xf_list[xfx]
            bgx = xf.background.pattern_colour_index
            color_map = book.colour_map[bgx]
            color_map = str(color_map)
            #”空白”か”白”はfile_read_color_lstに0を追加
            if color_map == "None" or color_map == "(255, 255, 255)":
                file_read_color.append(0)
            #オレンジか紺色の場合、file_read_color_lstに1を追加
            elif color_map == "(255, 102, 0)" or color_map == "(51, 51, 153)":
                file_read_color.append(1)
            #それ以外の場合、file_read_color_lstに0を追加
            else:
                file_read_color.append(0)   

#print(file_read_color)

#file_read_color_lstを一行(0:31)ずつ加算し、一行にまとめる
sum_index_lst = [sum(file_read_color[i:i+31]) for i in range(0,len(file_read_color),31)]
#print(sum_index_lst)

#総労働時間
all_work_time = sum(sum_index_lst)
all_work_time = all_work_time / 2
all_work_time = all_work_time + bottom_excel.sum_work_list
#print(all_work_time)

#加算しておらず、file_read_color_lstの要素を31毎に区切っている
user_color_lst = [file_read_color[i:i + 31] for i in range(0,len(file_read_color), 31)]
#print(user_color_lst)

#深夜労働時間
night_work_time = [sum(x[29:31]) for x in user_color_lst]
#print(night_work_list)

one_night_work_list = [night_work_time[i:i + 20] for i in range(0,len(night_work_time), 20)]
night_work_list = list(map(list, zip(*one_night_work_list)))

#総深夜労働時間
total_night_work_list = sum(map(sum, night_work_list))
total_night_work_list = total_night_work_list / 2
total_night_work_list = total_night_work_list + bottom_excel.total_night_work_list
#print(total_night_work_list)

#深夜労働時間リスト
array_night_work_list = np.array(night_work_list)
array_night_work_list = np.sum(array_night_work_list, axis=1)
list_night_work_list = array_night_work_list.tolist()
list_night_work_list = [i / 2 for i in list_night_work_list]
#print(list_night_work_list)


#通常労働時間
simple_noon_work_list = [sum(x[1:29]) for x in user_color_lst]
#print(simple_noon_work_list)

one_noon_work_list = [simple_noon_work_list[i:i + 20] for i in range(0,len(simple_noon_work_list), 20)]
noon_work_list = list(map(list, zip(*one_noon_work_list)))

#総通常労働時間
total_noon_work_list = sum(map(sum, noon_work_list))
total_noon_work_list = total_noon_work_list / 2
total_noon_work_list = total_noon_work_list + bottom_excel.total_noon_work_list
#print(total_noon_work_list)

#通常労働時間リスト
array_noon_work_list = np.array(noon_work_list)
array_noon_work_list = np.sum(array_noon_work_list, axis=1)
list_noon_work_list = array_noon_work_list.tolist()
list_noon_work_list = [i / 2 for i in list_noon_work_list]
#print(list_noon_work_list)

#深夜労働給与
night_hourly_wage_list = [i * 625 for i in night_work_time]
night_hourly_wage_list = night_hourly_wage_list + bottom_excel.night_hourly_wage_list
#print(night_hourly_wage_list)


#通常労働給与
noon_hourly_wage_list = [i * 500 for i in simple_noon_work_list]
noon_hourly_wage_list = noon_hourly_wage_list + bottom_excel.noon_hourly_wage_list
#print(noon_hourly_wage_list)

#合計給与
combined_hourly_wage_list = [x + y for (x, y) in zip(night_hourly_wage_list, noon_hourly_wage_list)]
#print(combined_hourly_wage_list)

#リストを１０個ずつの要素に分ける
user_color_lst = [combined_hourly_wage_list[i:i + 20] for i in range(0,len(combined_hourly_wage_list), 20)]
#print(user_color_lst)

#ユーザーの違う日の要素を多重配列にまとめる
sum_wage_per_day = list(map(list, zip(*user_color_lst)))
#print(sum_wage_per_day)

#ndarray変換、行同士を足し算
array_sum_wage_per_day = np.array(sum_wage_per_day)
array_sum_wage_per_day = np.sum(array_sum_wage_per_day, axis=1)
array_sum_wage_per_day = array_sum_wage_per_day.tolist()
#print(array_sum_wage_per_day)

#listの全ての要素の足し算
total_cost = sum(map(sum, sum_wage_per_day))
#print(total_cost)

#bottom_excelとの足し算->総人件費
all_total_cost = total_cost
#print(all_total_cost)
