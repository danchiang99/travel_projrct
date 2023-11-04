from datetime import datetime

# from geopy.distance import geodesic

# 假設日期是 '2023-08-25' 格式
def get_week_day(date_string):
    date_format = '%Y-%m-%d'

    # 將日期字串轉換為 datetime 物件
    date_object = datetime.strptime(date_string, date_format)

    # 獲得星期幾的數字（0-6，0 表示星期一，6 表示星期日）
    weekday_number = date_object.weekday()

    return weekday_number


# def calculate_distance(lat1, lon1, lat2, lon2):
#     # 使用geodesic函數計算兩個經緯度之間的距離
#     coords_1 = (lat1, lon1)
#     coords_2 = (lat2, lon2)
#     distance = geodesic(coords_1, coords_2).kilometers
#     return distance

# # 測試範例
# lat1, lon1 = 25.035502, 121.5201832  # 國立中正紀念堂的經緯度
# lat2, lon2 = 25.0296587, 121.5362867  # 大安森林公園的經緯度
# distance_km = calculate_distance(lat1, lon1, lat2, lon2)
# print(f"兩個經緯度之間的距離為: {distance_km:.2f} 公里")



#檢查營業時間
class OpentimeCheck:
    def check(self, travel_time, close, stay_time):
        travel_time = int(travel_time.replace(":", ""))
        try:
            if int(travel_time+stay_time) >= int(close):
                return 0
            else:
                return 1
        except:
            return 0 

    def opentime_check(self, weekday, travel_time, df_result, index):
        #stay_time先設100，因為目前有空值，等之後補完空值再換下方參數
        stay_time = 100

        # a = int(df_result.loc[index,'stay_time_min'])
        # stay_time = (a//60)*100+a%60
        b = [] #存放星期一到星期日是否開業，例如[1,0,1,1,1,1,0]
        for i in range(7):
            try:
                c = eval(df_result.loc[index,"is_open_list"])[i]
                b.append(int(c))
            except:
                c = 0
                b.append(int(c))
        monday_open, tuesday_open, wednesday_open, thursday_open, friday_open, saturday_open, sunday_open = b[0], b[1], b[2], b[3], b[4], b[5], b[6]
        
        d = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
        e = [] #存放星期一到星期日關店時間
        for i in d:
            try:
                f = eval(df_result.loc[index,"weekday_opentime_dict"])[i][0][-5:].replace(":","")
                e.append(int(f))
            except:
                f = 0
                e.append(int(f))
        monday_time, tuesday_time, wednesday_time, thursday_time, friday_time, saturday_time, sunday_time = e[0], e[1], e[2], e[3], e[4], e[5], e[6]

        if int(weekday) == 0 and monday_open == 1:
            close = monday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 1 and tuesday_open == 1:
            close = tuesday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 2 and wednesday_open == 1:
            close = wednesday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 3 and thursday_open == 1:
            close = thursday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 4 and friday_open == 1:
            close = friday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 5 and saturday_open == 1:
            close = saturday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        elif int(weekday) == 6 and sunday_open == 1:
            close = sunday_time
            return self.check(travel_time=travel_time, close=close, stay_time=stay_time)
        else:
            return 0

