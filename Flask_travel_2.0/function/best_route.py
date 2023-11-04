# 最佳路徑
'''
 @author: wei
 @version: 4.0 (2023/09/11)
 @description: 
 v1.0: 此版本為基本路徑規劃功能(尚未加上規劃時間調整 & 排不出路徑替代方案)
 v2.0: 新增路徑時程規劃的時間調整 & 原先排不出路徑情況的替代方案
        1. 景點starttime補至整點(以15分鐘為單位)
        2. 在時程規劃預留用餐時間(午餐與晚餐)
            (若出發時間超過(>=)13:00則不預留午餐/若出發時間超過(>=)19:00則不預留晚餐時段)
        3. 新增v1.0版本排不出路徑替代方案
            case1 : 在未調整下即可找到路徑規劃(先找最短路徑→再排時間)
            case2 : 先將景點依營業時間做排序再進行路徑規劃(先排時間→再排路徑)
            case3 : 調整(提前)出發時間後，能找到有效路徑(提供建議旅程起始時間)
            case4 : 上述調整皆無法找到有效路徑

 v3.0: 新增程式邏輯以處理特殊情況(e.g. 出發時間調整,跨天...)
 (9/8) 1. 建議出發時間邏輯新增(增加延後調整)(新增變數:建議出發時間)
       2. 新增case1-adjusted : case1排不出路徑情況調整出發時間可得有效路徑
       3. 跨天情況處理: 判斷景點starttime/endtime是否小於出發時間

 v4.0: 新增景點間導航連結 & 特殊情況處理邏輯
(9/11) 1. DirectionsStatus： e.g.遇開車無法抵達之景點 => return message: 請重新選擇景點
       2. process_row()調整：若raw_starttime原已跨天則不改為open_start

'''

from datetime import datetime, timedelta, time as dt_time
import itertools
import csv
import time as t_module
import json
import requests
from params import params_route_input
import pandas as pd
import random
import numpy as np


# Part1: Simulate Recommendation system & selected spots 
def selected_city_nspots(df, rw_city, n_spots, weekday_num, weekday_str):

    # -- 篩選縣市別
    df = df[df['rw_city'] == rw_city]
    # -- 篩選出發日有營業的景點 is_open_list[weekday_num] == 1
    df = df[df['is_open_list'].apply(lambda x: x[weekday_num] == 1)]
    df = df.reset_index(drop=True)

    # -- 隨機取景點數
    random_numbers = random.sample(range(df.shape[0]), n_spots)
    df_selected = df.iloc[random_numbers]

    # 篩選該營業日的時間區段
    opentimes = df_selected['weekday_opentime_dict'].apply(
        lambda x: x.get(weekday_str))
    df_selected.loc[:, 'opentime_list'] = opentimes
    # 調整欄位名稱
    df_selected = df_selected.rename(columns={'stay_time_min': 'staytime'})

    selected_columns = ['name', 'latitude',
                        'longitude', 'opentime_list', 'staytime']
    df_selected = df_selected[selected_columns]

    # 將 'staytime' 轉換為 HH:MM 格式的時間
    df_selected['staytime'] = pd.to_timedelta(df_selected['staytime'], unit='m').apply(
        lambda x: (datetime.min + x).time().strftime('%H:%M:%S'))

    return df_selected

def adjustment_df(df,weekday_str):
    # 調整欄位名稱
    opentimes = df['weekday_opentime_dict'].apply(
        lambda x: x.get(weekday_str))
    df.loc[:, 'opentime_list'] = opentimes
    df = df.rename(columns={'stay_time_min': 'staytime'})
    # df = df.rename(columns={'is_open_list': 'opentime_list'})
    selected_columns = ['name', 'latitude',
                        'longitude', 'opentime_list', 'staytime']
    df = df[selected_columns]
    

    # df['staytime'] = pd.to_timedelta(df['staytime'], unit='m').apply(
    #     lambda x: (datetime.min + x).time().strftime('%H:%M:%S'))
    df['staytime'] = df['staytime'].astype(int)
    def minutes_to_time(minutes):
        hours = minutes // 60
        minutes = minutes % 60
        return str(timedelta(hours=hours, minutes=minutes))

    df['staytime'] = df['staytime'].apply(minutes_to_time)

    return df

# Part2
def date2weekday(input_date_str):
    # 將輸入日期字串轉換為日期物件
    input_date = datetime.strptime(input_date_str, '%Y-%m-%d')

    # 使用weekday()方法獲取星期幾（0-6，0表示星期一，6表示星期日）
    weekday_num = input_date.weekday()

    # 根據weekday_num轉換成星期幾的字串
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    weekday_str = weekdays[weekday_num]
    # print(f"{input_date_str} 是 {weekday_str}")

    return weekday_num, weekday_str

def random_api():
    # 開啟並讀取檔案
    # api_file = './file/teamapikey.txt'
    api_file = 'C:/Users/User/Desktop/Flask_travel_2.0/file/teamapikey.txt'
    with open(api_file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # 跳過標題行
        key_list = [row[1] for row in csv_reader]  # 提取所有的key

    # 從key_list中隨機選取一個key
    random_key = random.choice(key_list)

    return random_key

def directions_api_result(df, optimize, YOUR_API_KEY):
    
    df_selected = df
    
    # ---------- Part 1 建立景點 dict
    # 將DataFrame的latitude、longitude和name欄位轉換成locations_dict字典
    locations_dict = df_selected[['latitude', 'longitude']].apply(lambda x: ','.join(map(str, x)), axis=1).to_dict()
    # 將name欄位作為字典的值
    locations_dict = {loc: name for loc, name in zip(locations_dict.values(), df_selected['name'].str.strip())}
    locations = list(locations_dict.keys()) # 取景點經緯度
    
    all_url = []
    route_record = []
    count = 1
    
    # for case1
    if optimize == True:
        # ---------- Part 2 計算排列組合，建立route_record = {'route_id':count, 'url':url, 'loc_comb':loc_comb}
        # 找出n個景點的所有起迄點的排列組合(n*(n-1))
        combinations = list(itertools.permutations(locations, 2))

        for pair in combinations:
            start_loc = pair[0]
            end_loc = pair[1]

            # 透過差集取出中繼點
            difference_set = set(locations).difference(set([start_loc,end_loc]))
            difference_set = list(difference_set)
            waypoints = 'optimize:true|' + '|'.join(difference_set) # Optimize route

            # Create a dict to store location combination
            loc_comb = {}
            loc_comb['start_loc'] = start_loc # str
            loc_comb['end_loc'] = end_loc # str
            loc_comb['waypoints'] = difference_set # list
            #print([locations_dict[i] for i in difference_set]) # 中繼點組合

            url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + start_loc + "&destination="+ end_loc + "&waypoints="+ waypoints + "&mode=driving" + "&key=" + YOUR_API_KEY
            #print(url)
            all_url.append(url)

            path = {'route_id':count, 'url':url, 'loc_comb':loc_comb}
            route_record.append(path)
            count += 1

    # (2023/09/03 新增)原先邏輯排不出路徑情況，先以時間排序再排計算最佳路徑
    # for case2
    else:
        start_loc = list(locations_dict.keys())[0]
        end_loc = list(locations_dict.keys())[-1]

        # 透過差集取出中繼點 (使用差集會改變順序導致邏輯不符，故調整如下)
        #difference_set = set(locations).difference(set([start_loc,end_loc]))
        #difference_set = list(difference_set)
        difference_set = list(locations_dict.keys())[1:-1]
        waypoints = 'optimize:false|' + '|'.join(difference_set)
        
        # Create a dict to store location combination
        loc_comb = {}
        loc_comb['start_loc'] = start_loc # str
        loc_comb['end_loc'] = end_loc # str
        loc_comb['waypoints'] = difference_set # list
        #print([locations_dict[i] for i in difference_set]) # 中繼點組合

        url = "https://maps.googleapis.com/maps/api/directions/json?origin=" + start_loc + "&destination="+ end_loc + "&waypoints="+ waypoints + "&mode=driving" + "&key=" + YOUR_API_KEY
        #print(url)
        all_url.append(url)

        path = {'route_id':count, 'url':url, 'loc_comb':loc_comb}
        route_record.append(path)
        count += 1
            
    # ---------- Part 3 解析url回傳內容
    payload={}
    headers = {}
    df_route_record = pd.DataFrame(route_record)
    # 初始化新增的欄位
    df_route_record['optimal_order_name'] = None
    df_route_record['each_leg_distance'] = None
    df_route_record['each_leg_duration'] = None


    for index, route in enumerate(route_record):

        url = route['url']
        routeid = route['route_id']
        loc_comb = route['loc_comb']

        response = requests.request("GET", url, headers=headers, data=payload)
        result = json.loads(response.text) # type(result) = dict

        # (2023/09/11 新增) 當景點無法開車抵達，則回傳空的df_route_record
        # (2023/09/12 備註) (DirectionsStatus)當API回應無效的 DirectionsResult，則回傳空df
        # if 'routes' not in result or not result['routes']:
        if result['status'].lower() != 'ok':
            # 如果result['routes']為空，跳出for迴圈並回傳空的df_route_record
            print(f"Route {routeid} has no routes available.")
            df_route_record = pd.DataFrame()  # 创建一个空的DataFrame
            return df_route_record

        # print(result.keys()) # dict_keys(['geocoded_waypoints', 'routes', 'status'])
        result_dict = result['routes'][0]

        # 各路徑距離與時間
        total_distance = 0
        total_duration = 0
        # (20230814) 紀錄每個legs的distance與duration
        each_leg_distance = []
        each_leg_duration = []

        for i in range(len(result_dict['legs'])):
            
            # (2023/08/29) 調整
            distance_text = result_dict['legs'][i]['distance']['text']
            duration_text = result_dict['legs'][i]['duration']['text']
            
            distance = float(distance_text.split()[0])
            # duration 單位可能為 XX小時YY分鐘 or ZZ分鐘
            duration = [value for value in duration_text.split() if value.isdigit()]
            duration_value = 0
            if len(duration) == 2:
                duration_value += int(duration[0]) * 60 + int(duration[1])
            elif len(duration) == 1:
                duration_value += int(duration[0])

            total_distance += distance
            total_duration += duration_value

            # (20230814) 紀錄每個legs的distance與duration
            each_leg_distance.append(distance)
            each_leg_duration.append(duration_value)

        # 各路徑最佳路徑景點排序(waypoint_order)
        waypoint_order = result_dict['waypoint_order'] # list

        # 紀錄路徑景點順序 start_loc + waypoints by waypoint_order + end_loc
        # 將中途點的景點經緯度依照waypoint_order的index取出
        route_loc_order = [route['loc_comb']['start_loc']] + [loc_comb['waypoints'][j] for j in waypoint_order] + [route['loc_comb']['end_loc']]
        # 將經緯度轉換為景點名稱
        route_loc_order_name = [locations_dict[latlon] for latlon in route_loc_order]

        #print(f'route {routeid}: {total_distance} km , {total_duration} mins')
        #print(route_loc_order_name)

        # Append to df_route_record
        df_route_record.at[index, 'total_distance'] = total_distance
        df_route_record.at[index, 'total_duration'] = total_duration
        df_route_record.at[index, 'optimal_order_name'] = route_loc_order_name

        # (20230814) 紀錄每個legs的distance與duration
        df_route_record.at[index, 'each_leg_distance'] = each_leg_distance
        df_route_record.at[index, 'each_leg_duration'] = each_leg_duration


    return df_route_record

def check_time_interval(time_intervals, target_time):
    # 轉換時間區間字符串為時間物件
    time_ranges = []
    for interval in time_intervals:
        start_str, end_str = interval.split('–')
        start_time = datetime.strptime(start_str, '%H:%M').time()
        end_time = datetime.strptime(end_str, '%H:%M').time()
        time_ranges.append((start_time, end_time))

    # 判斷是否在任意時間區間內
    is_within_interval = any(start_time <= target_time <=
                             end_time for start_time, end_time in time_ranges)

    if is_within_interval:
        return True
    else:
        return False


# v2.0 新增函數 adjust_time / adjust_time_with_dining
def adjust_time(time_obj):
    hh, mm = time_obj.hour, time_obj.minute
#     # version1:
#     if 0 < mm < 30:
#         return time_obj.replace(minute=30)
#     elif 30 < mm < 60:
#         new_hh = (hh + 1) % 24
#         return time_obj.replace(hour=new_hh, minute=0)
    
    # version2:
    if 0 < mm < 15:
        return time_obj.replace(minute=15)
    elif 15 < mm < 30:
        return time_obj.replace(minute=30)
    elif 30 < mm < 45:
        return time_obj.replace(minute=45)
    elif 45 < mm < 60:
        new_hh = (hh + 1) % 24
        return time_obj.replace(hour=new_hh, minute=0)
    else:
        return time_obj

def adjust_time_with_dining(time_obj, df_dining_time, lunch_flag, dinner_flag):
    hh, mm, ss = time_obj.hour, time_obj.minute, time_obj.second
    # 增加午餐時間(12:00)
    if datetime.strptime("12:00:00", "%H:%M:%S").time() <= time_obj and lunch_flag == 0: # <= datetime.strptime("13:00:00", "%H:%M:%S").time():
        lunch_flag = 1
        new_hh = (hh + 1) % 24
        new_time_obj = time_obj.replace(hour=new_hh)
        
        lunch_starttime = time_obj
        lunch_endtime = new_time_obj
        new_row = {
            'optimal_order_name': '午餐',
            'starttime': lunch_starttime,
            'endtime': lunch_endtime,
            'is_valid': 1,
            'is_spot': 0
        }
        df_dining_time = pd.concat([df_dining_time, pd.DataFrame([new_row])], ignore_index=True, sort=False)

        
        return new_time_obj, df_dining_time, lunch_flag, dinner_flag
    
    # 增加晚餐時間(18:00)
    elif datetime.strptime("18:00:00", "%H:%M:%S").time() <= time_obj and dinner_flag == 0: # <= datetime.strptime("18:00:00", "%H:%M:%S").time():
        dinner_flag = 1
        new_hh = (hh + 1) % 24
        new_time_obj = time_obj.replace(hour=new_hh)
        
        dinner_starttime = time_obj
        dinner_endtime = new_time_obj
        new_row = {
            'optimal_order_name': '晚餐',
            'starttime': dinner_starttime,
            'endtime': dinner_endtime,
            'is_valid': 1,
            'is_spot': 0
        }
        df_dining_time = pd.concat([df_dining_time, pd.DataFrame([new_row])], ignore_index=True, sort=False)
        
        return new_time_obj, df_dining_time, lunch_flag, dinner_flag
    else:
        return time_obj, df_dining_time, lunch_flag, dinner_flag

def process_row(df_route_record, df_selected, row_index, depart_time):
    
    # ---- Step 1
    # 建立包含 optimal_order_name 和 each_leg_duration 的暫時 DataFrame
    temp_df = df_route_record.loc[row_index, ['optimal_order_name', 'each_leg_duration']].to_frame().T

    # 將 optimal_order_name 欄位展開成一個 Series
    optimal_order_series = temp_df['optimal_order_name'].explode()

    # 將展開後的 Series 與 df_selected 進行連接
    # optimal_order_name 與 景點基本資訊(df_selected)串接
    new_df = pd.merge(optimal_order_series, df_selected, left_on='optimal_order_name', right_on='name', how='left')

    # 在 each_leg_duration 中的每個 list 前面加入 0
    # 將調整後的 each_leg_duration 加入到 new_df 的 leg 欄位中
    new_df['leg'] = [0] + temp_df['each_leg_duration'].iloc[0]
    new_df = new_df[['optimal_order_name', 'latitude', 'longitude', 'opentime_list', 'staytime', 'leg']]
    new_df['leg'] = pd.to_datetime(new_df['leg'], unit='m').dt.strftime('%H:%M:%S')
    new_df['leg'] = pd.to_datetime(new_df['leg'], format='%H:%M:%S').dt.time
    
    # ---- Step 2 (2023/08/31) 新增用餐時間
    # 創建紀錄用餐時間的DataFrame
    data = {
        'optimal_order_name': [],
        'latitude': [],
        'longitude': [],
        'opentime_list': [],
        'staytime': [],
        'leg': [],
        'starttime': [],
        'endtime': [],
        'is_valid': [],
        'is_spot': []
    }
    df_dining_time = pd.DataFrame(data)
    
    # 增加flag判斷是否排用餐時段
    lunch_flag = 0
    dinner_flag = 0
   
    # 出發時間超過13:00 不排午餐
    if depart_time >= datetime.strptime("13:00:00", "%H:%M:%S").time():
        lunch_flag = 1
    # 出發時間超過19:00 不排晚餐
    if depart_time >= datetime.strptime("19:00:00", "%H:%M:%S").time():
        dinner_flag = 1

    # ---- Step 3
    # 轉換時間格式並計算 starttime 和 endtime
    new_df['staytime'] = new_df['staytime'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time())
    new_df['leg'] = new_df['leg'].apply(lambda t: datetime.combine(datetime.today(), t).time())

    new_df['starttime'] = None
    new_df['endtime'] = None

    for i in range(len(new_df)):
        if i == 0:
            raw_starttime  = datetime.combine(datetime.today(), depart_time).time()
            # (2023/09/03 新增)starttime若早於open_start則改為於open_start
            # (邏輯待確認: 出發時間是否需先調整?)
            #opentime_start = datetime.strptime(new_df.at[i, 'opentime_list'][0][:5], "%H:%M").time()
            #raw_starttime = opentime_start if raw_starttime < opentime_start else raw_starttime
            
            # (2023/08/31 調整)將starttime調成整點 & 依據用餐時間調整
            adjusted_starttime = adjust_time(raw_starttime)
            adjusted_starttime_with_dine, df_dining_time, lunch_flag, dinner_flag = adjust_time_with_dining(adjusted_starttime, df_dining_time, lunch_flag, dinner_flag)
            
            new_df.at[i, 'starttime'] = adjusted_starttime_with_dine
            new_df.at[i, 'endtime'] = (datetime.combine(datetime.today(), new_df.at[i, 'starttime']) + timedelta(hours=new_df.at[i, 'staytime'].hour, minutes=new_df.at[i, 'staytime'].minute)).time()
        else:
            # (2023/08/31 調整)將starttime調成整點(:00)or半(:30) => adjusted_starttime
            # (2023/08/31 調整)將starttime依據用餐時間調整       => adjusted_starttime_with_dine
            raw_starttime = (datetime.combine(datetime.today(), new_df.at[i - 1, 'endtime']) + timedelta(hours=new_df.at[i, 'leg'].hour, minutes=new_df.at[i, 'leg'].minute)).time()

            # (2023/09/03 新增)starttime若早於open_start則改為於open_start
            # (2023/09/11 調整)若raw_starttime原已跨天則不改為open_start
            opentime_start = datetime.strptime(new_df.at[i, 'opentime_list'][0][:5], "%H:%M").time()
            raw_starttime = opentime_start if raw_starttime < opentime_start and raw_starttime > depart_time else raw_starttime

            adjusted_starttime = adjust_time(raw_starttime)
            adjusted_starttime_with_dine, df_dining_time, lunch_flag, dinner_flag = adjust_time_with_dining(adjusted_starttime, df_dining_time, lunch_flag, dinner_flag)
            
            new_df.at[i, 'starttime'] = adjusted_starttime_with_dine
            new_df.at[i, 'endtime'] = (datetime.combine(datetime.today(), new_df.at[i, 'starttime']) + timedelta(hours=new_df.at[i, 'staytime'].hour, minutes=new_df.at[i, 'staytime'].minute)).time()        

        #print(i, new_df.iloc[i]['optimal_order_name'], adjusted_starttime_with_dine)   
                
    new_df['is_valid'] = new_df.apply(lambda row: check_time_interval(row['opentime_list'], row['starttime']) and check_time_interval(row['opentime_list'], row['endtime']), axis=1)

    # (2023/09/08) 若時間點跨天，則is_valid修改為 False，以避免跨天情形
    # Function to update 'is_valid'
    def update_is_valid_starttime(row):
        if row['starttime'] < depart_time:
            return False
        else:
            return row['is_valid']
        
    def update_is_valid_endtime(row):
        if row['endtime'] < depart_time:
            return False
        else:
            return row['is_valid']
        
    # Update 'is_valid' based on starttime
    new_df['is_valid'] = new_df.apply(update_is_valid_starttime, axis=1)
    new_df['is_valid'] = new_df.apply(update_is_valid_endtime, axis=1)

    new_df['is_valid'] = new_df['is_valid'].astype(int)
    new_df['is_spot'] = 1

    # 垂直串聯兩個 DataFrame，並根據 starttime 欄位值由小到大進行排序
    concatenated_df = pd.concat([new_df, df_dining_time], ignore_index=True).sort_values(by='starttime')
    concatenated_df['is_valid'] = concatenated_df['is_valid'].astype(bool)
    concatenated_df['is_spot'] = concatenated_df['is_spot'].astype(bool)
    
    # 預留用餐時段(1HR)，但不給定特定時間
    concatenated_df.loc[concatenated_df['is_spot'] == False, 'staytime'] = datetime.strptime("1:00:00", "%H:%M:%S").time()
    concatenated_df.loc[concatenated_df['is_spot'] == False, ['starttime', 'endtime']] = np.nan

    # 重新設置索引
    concatenated_df = concatenated_df.reset_index(drop=True)

    return concatenated_df

def valid_route(df_selected, depart_time, df):
    
    df_route_record = df
    alltrue_indices = []
    valid_count = 0
    
    # 對 df_route_record 的每一列資料進行處理
    for i in range(len(df_route_record)):
        result = process_row(df_route_record, df_selected, i, depart_time)
        is_all_valid = result['is_valid'].all()

        if is_all_valid:
            alltrue_indices.append(i)
            valid_count += 1
        else:
            pass
            
    df_route_record_allTrue = df_route_record.iloc[alltrue_indices]
    
    return valid_count, df_route_record_allTrue

def optimal_route_id(df):
    df_route_record_allTrue = df
    
    # 找到 total_duration 最小值對應的索引 (df_route_record_allTrue)
    min_duration_index = df_route_record_allTrue['total_duration'].idxmin()
    min_duration_route = df_route_record_allTrue.loc[min_duration_index]
    
    return min_duration_route['route_id']


# v2.0 新增函數 df_selected_sorted_by_opentime (for case2)
# 定義自定義排序函數
def custom_sort(row):
    open_starttime = row[0][:5]
    open_endtime = row[-1][-5:]
    
    if open_starttime == '00:00' and open_endtime == '23:59':
        return (2, open_starttime, open_endtime)
    else:
        return (1, open_starttime, open_endtime)
    
def df_selected_sorted_by_opentime(df_selected):
    
    # 使用自定義排序函數對 opentime_list 進行排序
    df_selected_sorted = df_selected.copy()
    df_selected_sorted['opentime_list'] = df_selected_sorted['opentime_list'].apply(custom_sort)

    # 對DataFrame按照opentime_list列進行排序
    df_sorted = df_selected_sorted.sort_values(by='opentime_list')
    # 重置索引
    df_sorted.reset_index(drop=True, inplace=True)
    
    # 根據 name 欄位合併 df_selected_test 和 df_sorted
    df_merged = df_sorted.merge(df_selected[['name', 'opentime_list']], on='name', how='left')

    # 將合併後的 opentime_list_x 欄位的內容替換為 opentime_list_y 欄位的內容
    df_merged['opentime_list_x'] = df_merged['opentime_list_y']

    # 刪除多餘的欄位
    df_merged.drop(columns=['opentime_list_y'], inplace=True)

    # 重命名欄位為 opentime_list
    df_merged.rename(columns={'opentime_list_x': 'opentime_list'}, inplace=True)
     
    # df_merged = df_selected sorted by opentime
    return df_merged