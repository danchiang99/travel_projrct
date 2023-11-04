

from geopy.distance import geodesic
import params.params_recommend_input as ppri

# Math Weight
# 公式發想(出版、還會修正)
# https://docs.google.com/spreadsheets/d/1cytnnXh4EC6jKqiniC15g2z1uM_CYL0_dwP7S7BeTVA/edit#gid=0
#
# opentimecheck only equal 0 or 1
# constant 至少為1 避免參數設定錯誤 至少還有被選到機率
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# 需要再加入一個距離的判斷 防止資料有問題


def get_recommend_weight(avgstart, avgstartcount, opentimecheck, real_start):
    result = opentimecheck*(avgstart*ppri.real_rating_x+avgstartcount *
                            ppri.rating_count_x+real_start*ppri.real_rating_x+ppri.constant)
    return float(result)

# here --------------------------------------------


def get_distince(city, view_latitude, view_longitude):
    # 獲得距離
    city_latitude = taiwan_coordinates[city]["緯度"]
    city_longitude = taiwan_coordinates[city]["經度"]
    distince = calculate_distance(
        city_latitude, city_longitude, view_latitude, view_longitude)
    return float(distince)


taiwan_coordinates = {
    "台北市": {"緯度": 25.032969, "經度": 121.565418},
    "新北市": {"緯度": 25.013890, "經度": 121.522633},
    "桃園市": {"緯度": 24.993628, "經度": 121.300979},
    "台中市": {"緯度": 24.147736, "經度": 120.673645},
    "台南市": {"緯度": 22.994821, "經度": 120.196894},
    "高雄市": {"緯度": 22.627278, "經度": 120.301435},
    "基隆市": {"緯度": 25.127603, "經度": 121.739183},
    "新竹市": {"緯度": 24.803950, "經度": 120.964688},
    "新竹縣": {"緯度": 24.838722, "經度": 121.014666},
    "苗栗縣": {"緯度": 24.560159, "經度": 120.815436},
    "彰化縣": {"緯度": 24.080000, "經度": 120.541000},
    "南投縣": {"緯度": 23.960998, "經度": 120.971863},
    "雲林縣": {"緯度": 23.709203, "經度": 120.431337},
    "嘉義市": {"緯度": 23.479834, "經度": 120.449111},
    "嘉義縣": {"緯度": 23.451842, "經度": 120.255461},
    "屏東縣": {"緯度": 22.551975, "經度": 120.548759},
    "宜蘭縣": {"緯度": 24.702107, "經度": 121.737750},
    "花蓮縣": {"緯度": 23.993630, "經度": 121.601571},
    "台東縣": {"緯度": 22.791213, "經度": 121.134293},
    "澎湖縣": {"緯度": 23.565479, "經度": 119.566158},
    "金門縣": {"緯度": 24.434667, "經度": 118.317089},
    "連江縣": {"緯度": 26.160469, "經度": 119.949869}
}


def calculate_distance(lat1, lon1, lat2, lon2):
    # 使用geodesic函數計算兩個經緯度之間的距離
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    distance = geodesic(coords_1, coords_2).kilometers
    return distance

# 測試範例
# lat1, lon1 = 25.035502, 121.5201832  # 國立中正紀念堂的經緯度
# lat2, lon2 = 25.0296587, 121.5362867  # 大安森林公園的經緯度


# distance_km = calculate_distance(lat1, lon1, lat2, lon2)
# print(f"兩個經緯度之間的距離為: {distance_km:.2f} 公里")
# here --------------------------------------------
