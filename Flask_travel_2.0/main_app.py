from flask import Flask, render_template, request, url_for, jsonify
from datetime import datetime
from pathlib import Path
import uuid
import pandas as pd
import time as t_module

import function.best_route as best_route
import function.get_sql_result as fgs
import function.check_city as fcc
import function.other_tool as fot
import function.get_recommend_weight as fgrw

from params import params_route_input
import sqlite3 as sql
import numpy as np

from datetime import datetime, timedelta, time as dt_time


#  add
import plotly
import plotly.graph_objs as go
import plotly.express as px
import json
from model.modeltest import ratemodel

#  end add
app = Flask(__name__)
print("----------------------正常運作 合併前端版本")

# @app.route('/test')
# def testtableau():
#     return render_template('tableau.html',
#                            page_header="page_header")


# @app.route('/Index.html')
# def index2():
#     return render_template('index2.html',
#                            page_header="page_header")

# ============================ 員工介紹 start =========================


@app.route('/about')
def about():
    return render_template('About.html',
                           page_header="page_header")
# xxxxxxxxxxxxxxxxxxxxxxxxxxxx 員工介紹 end xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================ 星等評分模型 start ========================


@app.route('/model')
def model():
    return render_template('model.html',
                           page_header="page_header")


@app.route("/commentresult", methods=['POST'])
def commentresult():
    data = request.form.to_dict()
    comment = data.get("comment")
    if len(comment) <= 0:
        return "沒評論我怎麼評分!"
    elif 0 < len(comment) <= 135:
        comment_dict = ratemodel(comment)
        star = comment_dict[0].get("label")
        return star
    else:
        return "評論過長，我會很累(請小於135字)"
# xxxxxxxxxxxxxxxxxxxxxxxxxxxx 星等評分模型 END xxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================ 數據圖表 start ============================


@app.route('/datachart')
def datachart():
    return render_template('datachart.html',
                           page_header="page_header")



# ====================================================================
# ============================ 旅遊系統 start ============================
# ====================================================================

@app.route('/')
def home_page():
    return render_template('index0.html',
                           page_header="Form")


@app.route('/choose')
def first_page():
    return render_template('index.html',
                           page_header="Form")
# 接收並處理表單提交


@app.route('/submit', methods=['POST'])
def submit_form():
    # 獲得回傳資料並轉為dict
    data = request.form.to_dict()
    # print(data)s
    # 將類別轉成list
    selected_options = [value for key,
                        value in data.items() if key.startswith('option')]

    # 辨識星期幾 獲得星期幾的數字（0-6，0 表示星期一，6 表示星期日）
    weekday = fot.get_week_day(data['date'])

    # 查詢sql
    df_result = fgs.get_view_overview_result(data['region'], selected_options)

    df_result_2 = fgs.get_view_overview_result_2(
        data['region'], selected_options)
    # df_combined = pd.concat([df_result, df_result_2], ignore_index=True)
    # print(df_combined)

    # 產生新欄位用來放入該景點被選到權重
    df_result['recommend_weight'] = None
    opentime_checker = fot.OpentimeCheck()

    # here-------------------------------------------------------------------------------------------------------------------------------
    df_result['distance'] = None
    for index, row in df_result.iterrows():  # 權重包含GOOGLE顆星、評論數目、營業時間、模型輸出顆星
        df_result.at[index, 'recommend_weight'] = fgrw.get_recommend_weight(avgstart=row['rating'],
                                                                            avgstartcount=row['rating_count'],
                                                                            opentimecheck=opentime_checker.opentime_check(
                                                                                weekday, data['time'], df_result, index),
                                                                            real_start=row['new_star_label'])
        if opentime_checker.opentime_check(weekday, data['time'], df_result, index) == 0:
            df_result.at[index, 'recommend_weight'] = 0
            df_result.at[index, 'distance'] = 0
        else:
            df_result.at[index, 'recommend_weight'] = fgrw.get_recommend_weight(avgstart=row['rating'],
                                                                                avgstartcount=row['rating_count'],
                                                                                opentimecheck=opentime_checker.opentime_check(
                                                                                weekday, data['time'], df_result, index),
                                                                                real_start=row['new_star_label'])
            df_result.at[index, 'distance'] = fgrw.get_distince(city=row['rw_city'],
                                                                view_latitude=row['latitude'],
                                                                view_longitude=row['longitude'])
    max_distance = df_result['distance'].max()
    df_result['recommend_weight'] = df_result['recommend_weight'] * \
        (1+(1-df_result['distance']/max_distance))
    # here-------------------------------------------------------------------------------------------------------------------------------

    # 根據權重隨機選擇
    try:
        Total_random = df_result['recommend_weight'].sum()
        weights = df_result['recommend_weight'] / Total_random
        df_result_byweight = df_result.sample(
            n=len(weights[weights > 0]), weights=weights).reset_index(drop=True)
    except:
        # 查無資料
        df_result_byweight = pd.DataFrame(columns=df_result.columns)
    # print(len(df_result))

    # 後15筆資料
    df_result_2['recommend_weight'] = None
    opentime_checker = fot.OpentimeCheck()

    # here-------------------------------------------------------------------------------------------------------------------------------
    df_result_2['distance'] = None
    for index, row in df_result_2.iterrows():  # 權重包含GOOGLE顆星、評論數目、營業時間、模型輸出顆星
        df_result_2.at[index, 'recommend_weigsht'] = fgrw.get_recommend_weight(avgstart=row['rating'],
                                                                            avgstartcount=row['rating_count'],
                                                                            opentimecheck=opentime_checker.opentime_check(
                                                                                weekday, data['time'], df_result_2, index),
                                                                            real_start=row['new_star_label'])
        if opentime_checker.opentime_check(weekday, data['time'], df_result_2, index) == 0:
            df_result_2.at[index, 'recommend_weight'] = 0
            df_result_2.at[index, 'distance'] = 0
        else:
            df_result_2.at[index, 'recommend_weight'] = fgrw.get_recommend_weight(avgstart=row['rating'],
                                                                                avgstartcount=row['rating_count'],
                                                                                opentimecheck=opentime_checker.opentime_check(
                                                                                weekday, data['time'], df_result_2, index),
                                                                                real_start=row['new_star_label'])
            df_result_2.at[index, 'distance'] = fgrw.get_distince(city=row['rw_city'],
                                                                view_latitude=row['latitude'],
                                                                view_longitude=row['longitude'])
    max_distance = df_result_2['distance'].max()
    df_result_2['recommend_weight'] = df_result_2['recommend_weight'] * \
        (1+(1-df_result_2['distance']/max_distance))
    # here-------------------------------------------------------------------------------------------------------------------------------

    # print(df_result_2['recommend_weight'])
    try:
        Total_random = df_result_2['recommend_weight'].sum()
        # print("-------", Total_random)
        weights = df_result_2['recommend_weight'] / Total_random
        # print(weights.head(20))
        df_result_byweight_2 = df_result_2.sample(
            n=len(weights[weights > 0]), weights=weights).reset_index(drop=True)
        # print(df_result_byweight_2)
    except:
        # 查無資料
        df_result_byweight_2 = pd.DataFrame(columns=df_result_2.columns)

    # 將空白字串替換為數字 60
    df_result_byweight['stay_time_min'] = df_result_byweight['stay_time_min'].replace(
        '', '60')
    df_result_byweight_2['stay_time_min'] = df_result_byweight_2['stay_time_min'].replace(
        '', '60')

    # 將欄位的資料型別轉換為整數
    df_result_byweight['stay_time_min'] = df_result_byweight['stay_time_min'].astype(
        int)
    df_result_byweight_2['stay_time_min'] = df_result_byweight_2['stay_time_min'].astype(
        int)

    # print(df_result_byweight.head(5))
    # print(df_result_byweight_2['stay_time_min'])

    # print("---------", len(df_result_byweight))
    df_result_byweight_count = len(df_result_byweight)
    if df_result_byweight_count < 35:
        df_combined = pd.concat([df_result_byweight[:df_result_byweight_count],
                                df_result_byweight_2[:50-len(df_result_byweight)]], ignore_index=True)
        df_combined_shuffled = df_combined.sample(
            frac=1).reset_index(drop=True)
    else:
        df_combined = pd.concat(
            [df_result_byweight[:35], df_result_byweight_2[:15]], ignore_index=True)
        df_combined_shuffled = df_combined.sample(
            frac=1).reset_index(drop=True)

    # print(df_combined_shuffled)

    return render_template('index2.html', dataframe=df_combined_shuffled,
                           travel_date=data['date'],
                           travel_region=data['region'],
                           travel_time=data['time'],
                           input_data=data)


# 路徑規劃
@app.route('/route', methods=['POST'])
def route_plan():

    # ------ Part1 User input parameters
    # 使用者選擇的想去景點名稱
    names=[]
    # if request.is_json:
    #     print(request.is_json)
    #     print("-------test-----------")
    #     selected_items_from_html = json.loads(request.form.get('selected_items'))
    #     selected_items=selected_items_from_html
    #     print(selected_items)
    #     # global names
    #     names = [item.strip().split('\n')[0].strip()
    #              for item in selected_items]
    #     print(names)
    # else:
    #     t_module.sleep(20)
    #     print("------錯誤-----")
# print(request.is_json)
    print("-------test-----------")
    selected_items_from_html = json.loads(request.form.get('selected_items'))
    selected_items=selected_items_from_html["selectedItems"]
    print(selected_items)
    names = []
    for item in selected_items:
        name = item.strip().split('\n')[0].strip()
        names.append(name)

    
    print(names)


    # 查詢資料庫並列出景點資訊
    df_user_choose_view = fgs.get_result_by_name(names)
    # print(df_user_choose_view)
    df_user_choose_view = df_user_choose_view[df_user_choose_view['name'].isin(
        names)]
    # 使用 params_route_input 中的變數或函式
    input_date_str = request.form.get('travel_date')

    tmp_depart_time = request.form.get('travel_time')
    if tmp_depart_time is not None:
        tmp_depart_time += ':00'
    else:
        tmp_depart_time = '00:00:00'

    depart_time = datetime.strptime(tmp_depart_time, '%H:%M:%S').time()
    rw_city = request.form.get('travel_region')
    weekday_num, weekday_str = best_route.date2weekday(
        input_date_str)  # 日期轉換星期

    # 推薦系統相關參數
    n_spots = df_user_choose_view.shape[0]  # params_route_input.n_spots

    # Google API key
    YOUR_API_KEY = best_route.random_api()

    # stay_time_min、weekday_opentime_dict 為空值則先補值(for測試後面要改)
    df_user_choose_view['stay_time_min'] = df_user_choose_view['stay_time_min'].replace(
        '', np.nan)
    df_user_choose_view['stay_time_min'] = df_user_choose_view['stay_time_min'].fillna(
        '60')
    tmp_list = '[1, 1, 1, 1, 1, 1, 1]'
    df_user_choose_view['weekday_opentime_dict'] = df_user_choose_view['weekday_opentime_dict'].fillna(
        tmp_list)

    # 資料型態轉換 by eval()
    df_user_choose_view['weekday_opentime_dict'] = df_user_choose_view['weekday_opentime_dict'].apply(
        eval)
    df_user_choose_view['is_open_list'] = df_user_choose_view['is_open_list'].apply(
        eval)

    # 原selected_city_nspots 改用adjustment_df 過濾格式，暫時用的，需要請改
    df_selected = best_route.adjustment_df(df_user_choose_view, weekday_str)

    # ------ Part2 route-plan algorithm
    start_time = t_module.time()

    # 判斷是否有有效路徑，result=case1,2,3,4
    result_case = 0
    df_route_record = best_route.directions_api_result(
        df_selected, optimize=True, YOUR_API_KEY=YOUR_API_KEY)

    # (2023/09/08 新增) 選到開車無法抵達景點
    if df_route_record.empty:
        #print("DataFrame is empty")
        return render_template('route.html', message="很抱歉發生錯誤 即將回到首頁")

    valid_count, df_route_record_allTrue = best_route.valid_route(
        df_selected, depart_time, df_route_record)
    adjusted_depart_time = depart_time  # 用以判斷出發時間是否需調整

    #print(f'{valid_count} routes are valid!')

    # case1. 第一層邏輯即找到路徑
    if valid_count > 0:
        optimal_id = best_route.optimal_route_id(df_route_record_allTrue)
        # optimal_route_df = df_route_record[df_route_record['route_id'] == optimal_id]
        # (2023/08/30修正) 原process_row有問題[已解決] → 說明：process_row使用參數為index非id(兩者相差1)
        optimal_index = optimal_id - 1
        df_optimal_route = best_route.process_row(
            df_route_record, df_selected, optimal_index, depart_time)

        print('case1: optimal_route_id:', optimal_id)
        result_case = 1

    else:
        # (2023/09/07 新增) case1-adjusted: 第一層邏輯找不到路徑，嘗試調整出發時間
        adjusted_depart_time = depart_time
        while adjusted_depart_time >= dt_time(0, 0) and adjusted_depart_time <= dt_time(20, 0):
            # print('------------------------------------------------')
            #print('case1-adjust TRY!!')
            valid_count, df_route_record_allTrue = best_route.valid_route(
                df_selected, adjusted_depart_time, df_route_record)
            if valid_count > 0:
                break  # 找到了有效路徑，可跳出迴圈
            else:
                # 如果 adjusted_depart_time 小於 depart_time，不斷提前半小時遞迴嘗試
                if adjusted_depart_time != dt_time(0, 0) and adjusted_depart_time <= depart_time:
                    if adjusted_depart_time.minute == 30:
                        adjusted_depart_time = dt_time(
                            adjusted_depart_time.hour, adjusted_depart_time.minute - 30)
                    else:
                        adjusted_depart_time = dt_time(
                            adjusted_depart_time.hour - 1, 30)
                # 當 adjusted_depart_time 已為 00:00:00，則轉換為延後半小時遞迴嘗試
                else:
                    if adjusted_depart_time == dt_time(0, 0):
                        adjusted_depart_time = depart_time

                    if adjusted_depart_time.minute == 30:
                        adjusted_depart_time = dt_time(
                            adjusted_depart_time.hour + 1, 0)
                    else:
                        adjusted_depart_time = dt_time(
                            adjusted_depart_time.hour, adjusted_depart_time.minute + 30)

            #print('TRY adjusted_depart_time ',valid_count, adjusted_depart_time)

        if valid_count > 0:
            # 有有效路徑
            print('case1-adjust: When depart_time=',
                  adjusted_depart_time, '有有效路徑')
            print('valid count ', valid_count)
            result_case = '1-adjust'
            optimal_id = best_route.optimal_route_id(df_route_record_allTrue)
            optimal_index = optimal_id - 1
            df_optimal_route = best_route.process_row(
                df_route_record, df_selected, optimal_index, adjusted_depart_time)

        else:
            # case2. 將景點先以opentime_list進行排序，再排路徑
            # 將原 df_selected 先以 opentime_list進行排序
            df_selected_sorted = best_route.df_selected_sorted_by_opentime(
                df_selected)
            df_route_record = best_route.directions_api_result(
                df_selected_sorted, optimize=False, YOUR_API_KEY=YOUR_API_KEY)

            valid_count, df_route_record_allTrue = best_route.valid_route(
                df_selected, depart_time, df_route_record)

            if valid_count > 0:
                # (2023/09/03) 調整為新邏輯
                optimal_id = best_route.optimal_route_id(
                    df_route_record_allTrue)
                # optimal_route_df = df_route_record[df_route_record['route_id'] == optimal_id]
                optimal_index = optimal_id - 1
                df_optimal_route = best_route.process_row(
                    df_route_record, df_selected, optimal_index, depart_time)
                #print('case2: optimal_route_id:', optimal_id)
                result_case = 2

            # case3. 調整出發時間，嘗試尋找有效路徑
            # (2023/09/07) 邏輯調整：半小時為單位尋找有效路徑
            # (2023/09/07) 邏輯調整：新增adjust_depart_time 與 延後出發時間
            else:
                adjusted_depart_time = depart_time
                while adjusted_depart_time >= dt_time(0, 0) and adjusted_depart_time < dt_time(20, 0):
                    valid_count, df_route_record_allTrue = best_route.valid_route(
                        df_selected, adjusted_depart_time, df_route_record)
                    if valid_count > 0:
                        break  # 找到了有效路徑，可跳出迴圈
                    else:
                        # 如果 adjusted_depart_time 小於 depart_time，不斷提前半小時遞迴嘗試
                        if adjusted_depart_time != dt_time(0, 0) and adjusted_depart_time <= depart_time:
                            if adjusted_depart_time.minute == 30:
                                adjusted_depart_time = dt_time(
                                    adjusted_depart_time.hour, adjusted_depart_time.minute - 30)
                            else:
                                adjusted_depart_time = dt_time(
                                    adjusted_depart_time.hour - 1, 30)
                        # 當 adjusted_depart_time 已為 00:00:00，則轉換為延後半小時遞迴嘗試
                        else:
                            if adjusted_depart_time == dt_time(0, 0):
                                adjusted_depart_time = depart_time

                            if adjusted_depart_time.minute == 30:
                                adjusted_depart_time = dt_time(
                                    adjusted_depart_time.hour + 1, 0)
                            else:
                                adjusted_depart_time = dt_time(
                                    adjusted_depart_time.hour, adjusted_depart_time.minute + 30)

                if valid_count > 0:
                    # 有有效路徑
                    #('case3: When depart_time=', adjusted_depart_time, '有有效路徑')
                    result_case = 3
                    optimal_id = best_route.optimal_route_id(
                        df_route_record_allTrue)
                    optimal_index = optimal_id - 1
                    df_optimal_route = best_route.process_row(
                        df_route_record, df_selected, optimal_index, adjusted_depart_time)

                # case4. case 1/2/3 皆無法找到有效路徑
                else:
                    # 無有效路徑
                    #print('case4: 無有效路徑!!')
                    result_case = 4
                    # 暫以index=0(route_id=1)代替，確保網頁可呈現結果
                    optimal_id = 1
                    optimal_index = optimal_id - 1
                    df_optimal_route = best_route.process_row(
                        df_route_record, df_selected, optimal_index, depart_time)

            # 用於檢查
            # break

    # 計時結束
    end_time = t_module.time()
    total_time = end_time - start_time

    # 取得起點和終點的 latitude 和 longitude
    df_optimal_route_is_spot = df_optimal_route[df_optimal_route['is_spot']]
    origin_lat = df_optimal_route_is_spot.iloc[0]['latitude']
    origin_lng = df_optimal_route_is_spot.iloc[0]['longitude']
    destination_lat = df_optimal_route_is_spot.iloc[-1]['latitude']
    destination_lng = df_optimal_route_is_spot.iloc[-1]['longitude']

    # # 取得 waypoints 資料
    waypoints = df_optimal_route_is_spot.iloc[1:-1][['latitude',
                                                     'longitude']].to_dict(orient='records')

# (2023/09/12) 新增點跟點間的導航連結
    # (2023/09/13) 考量午餐與晚餐進行修正
    df_optimal_route['navi_link'] = ""

    for index, row in df_optimal_route.iterrows():
        if index > 0 and row['is_spot']:
            # (version 1) URL by 景點經緯度
            prev_index = index - 1
            while df_optimal_route.iloc[prev_index]['is_spot'] == False:
                prev_index = prev_index - 1

            prev_row = df_optimal_route.iloc[prev_index]
            start_lat = prev_row['latitude']
            start_lon = prev_row['longitude']
            end_lat = row['latitude']
            end_lon = row['longitude']
            # 導航URL
            navi_url = f"https://www.google.com/maps/dir/{start_lat},{start_lon}/{end_lat},{end_lon}"

            # (version 2) URL by 景點名稱
            # start_loc = prev_row['optimal_order_name']
            # end_loc = row['optimal_order_name']
            # navi_url = f"https://www.google.com/maps/dir/{start_loc}/{end_loc}"

            # 將導航URL存儲在 navi_link 欄位中
            df_optimal_route.at[index, 'navi_link'] = navi_url

    # HTML 變數結果呈現
    # ----- Table 1
    # 將變數轉換成 DataFrame
    data = {
        '使用者輸入': ['出發日期', '旅程起始時間', '建議起始時間', '旅遊地點', '景點數量'],
        '數值': [input_date_str, depart_time, adjusted_depart_time, rw_city, n_spots]
    }
    df_variables = pd.DataFrame(data)
    # 將 df_variables 轉換成 HTML 表格
    variables_table_html = df_variables.to_html(classes='table', index=False)

    # ----- Table 2
    # 創建一個包含變數的字典
    data = {
        '最佳路徑計算結果': ['case', '有效路徑數', '最佳路徑編號', '程式執行時間(s)', '使用API_KEY(末六碼)'],
        '數值': [result_case, valid_count, optimal_id, total_time, YOUR_API_KEY[-6:]]
    }
    df_variables = pd.DataFrame(data)
    # 將 df_variables 轉換成 HTML 表格
    route_table_html = df_variables.to_html(classes='table', index=False)

    # ----- Table 3
    # 將變數字典轉換成 DataFrame
    df_variables = pd.DataFrame(df_optimal_route)
    # 將 df_optimal_route 轉換成 HTML 表格
    table_html = df_optimal_route.to_html(classes='table', index=False)

    # ----- Table 4 (for flask & front-end)
    # 要篩選的多個欄位名稱
    filtered_columns = ["optimal_order_name",
                        "starttime", "endtime", "leg", "navi_link"]
    df_optimal_route_for_flask = df_optimal_route[filtered_columns]
    df_optimal_route_for_flask["starttime"] = df_optimal_route_for_flask["starttime"].apply(lambda x: str(x)[:5])
    df_optimal_route_for_flask["endtime"] = df_optimal_route_for_flask["endtime"].apply(lambda x: str(x)[:5])
    df_optimal_route_for_flask["leg"] = df_optimal_route_for_flask["leg"].apply(lambda x: str(x)[:5])
    table_for_flask_html = df_optimal_route_for_flask.to_html(
        classes='table', index=False)
    # print(df_optimal_route_for_flask)
    names=[]
    return render_template('index3.html',
                           route_table_html=route_table_html, variables_table_html=variables_table_html, table_html=table_html,
                           table_for_flask_html=table_for_flask_html, df_optimal_route_for_flask=df_optimal_route_for_flask,
                           origin_lat=origin_lat,
                           origin_lng=origin_lng, destination_lat=destination_lat, destination_lng=destination_lng, waypoints=waypoints, YOUR_API_KEY=YOUR_API_KEY)

    # return render_template('route.html',
    #                        route_table_html=route_table_html, variables_table_html=variables_table_html, table_html=table_html,
    #                        table_for_flask_html = table_for_flask_html,
    #                        origin_lat=origin_lat,
    #                        origin_lng=origin_lng, destination_lat=destination_lat, destination_lng=destination_lng, waypoints=waypoints, YOUR_API_KEY=YOUR_API_KEY)


# xxxxxxxxxxxxxxxxxxxxxxxxxxxx 旅遊系統 end xxxxxxxxxxxxxxxxxxxxxxxxxxxx


if __name__ == "__main__":
    app.run(debug=True)
