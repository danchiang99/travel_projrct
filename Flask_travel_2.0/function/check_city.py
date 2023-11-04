# (廢棄)因為前端傳來的value就是搜尋的keyword
def get_city(city):

    city_options = {
        '臺北市': '台北市',
        'NTPC': '新北市',
        'TYN': '桃園市',
        'TXG': '台中市',
        'TNN': '台南市',
        'KHH': '高雄市',
        '1': '選項1',
        '2': '選項2',
        '3': '選項3'
    }
    city_cheinese = city_options[city]
    return city_cheinese

