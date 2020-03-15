import xlrd
import itertools as itr
import numpy as np


fname = '/Users/yudai/Desktop/三条シフト2019_12.xls' 

#エクセルファイルを読み込む(formatting_info=Trueを付けて読み込む)
book  = xlrd.open_workbook(fname, formatting_info=True)

work_list = []

#1,2の場合、１日しか計算していない
for sheet_num in range(1, 16):
    for index_num in range(22, 42):
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
            if color_map == "None" or color_map == "(255, 255, 255)":
                work_list.append(0)
            elif color_map == "(255, 102, 0)" or color_map == "(51, 51, 153)":
                work_list.append(1)
            else:
                work_list.append(0)  

#print(work_list)

#リストを一行(0:31)ずつ加算
sum_list = [sum(work_list[i:i+31]) for i in range(0,len(work_list),31)]
#print(sum_list)

#総労働時間
sum_work_list = sum(sum_list)
sum_work_list = sum_work_list / 2
#print(sum_work_list)

#加算しておらず、work_listを31毎に区切っている
one_work_list = [work_list[i:i + 31] for i in range(0,len(work_list), 31)]
#print(one_work_list)

#深夜労働時間
simple_night_work_list = [sum(x[29:31]) for x in one_work_list]
#print(night_work_list)

one_night_work_list = [simple_night_work_list[i:i + 20] for i in range(0,len(simple_night_work_list), 20)]
night_work_list = list(map(list, zip(*one_night_work_list)))

#総深夜労働時間
total_night_work_list = sum(map(sum, night_work_list))
total_night_work_list = total_night_work_list / 2
#print(total_night_work_list)

#深夜労働時間リスト
array_night_work_list = np.array(night_work_list)
array_night_work_list = np.sum(array_night_work_list, axis=1)
list_night_work_list = array_night_work_list.tolist()
list_night_work_list = [i / 2 for i in list_night_work_list]
#print(list_night_work_list)


#通常労働時間
simple_noon_work_list = [sum(x[1:29]) for x in one_work_list]
#print(simple_noon_work_list)

one_noon_work_list = [simple_noon_work_list[i:i + 20] for i in range(0,len(simple_noon_work_list), 20)]
noon_work_list = list(map(list, zip(*one_noon_work_list)))

#総通常労働時間
total_noon_work_list = sum(map(sum, noon_work_list))
total_noon_work_list = total_noon_work_list / 2
#print(total_noon_work_list)

#通常労働時間リスト
array_noon_work_list = np.array(noon_work_list)
array_noon_work_list = np.sum(array_noon_work_list, axis=1)
list_noon_work_list = array_noon_work_list.tolist()
list_noon_work_list = [i / 2 for i in list_noon_work_list]
#print(list_noon_work_list)


#深夜労働給与
night_hourly_wage_list = [i * 625 for i in simple_night_work_list]
#print(night_hourly_wage_list)


#通常労働給与
noon_hourly_wage_list = [i * 500 for i in simple_noon_work_list]
#print(noon_hourly_wage_list)

#合計給与
combined_hourly_wage_list = [x + y for (x, y) in zip(night_hourly_wage_list, noon_hourly_wage_list)]
#print(combined_hourly_wage_list)

#リストを１０個ずつの要素に分ける
one_work_list = [combined_hourly_wage_list[i:i + 20] for i in range(0,len(combined_hourly_wage_list), 20)]
#print(one_work_list)

#ユーザーの違う日の要素を多重配列にまとめる->各個人の１日ずつの給与
sum_wage_per_day = list(map(list, zip(*one_work_list)))
#print(sum_wage_per_day)

#ndarray変換、行同士を足し算->各個人の合計給与
array_sum_wage_per_day = np.array(sum_wage_per_day)
array_sum_wage_per_day = np.sum(array_sum_wage_per_day, axis=1)
array_sum_wage_per_day = array_sum_wage_per_day.tolist()
#print(array_sum_wage_per_day)

#listの全ての要素の足し算
total_cost = sum(map(sum, sum_wage_per_day))
#print(total_cost)
