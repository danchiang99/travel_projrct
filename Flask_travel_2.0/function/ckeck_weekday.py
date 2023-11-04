from datetime import datetime

# 假設日期是 '2023-08-25' 格式

def get_week_day(date_string):
    date_format = '%Y-%m-%d'

    # 將日期字串轉換為 datetime 物件
    date_object = datetime.strptime(date_string, date_format)

    # 獲得星期幾的數字（0-6，0 表示星期一，6 表示星期日）
    weekday_number = date_object.weekday()

    return weekday_number
