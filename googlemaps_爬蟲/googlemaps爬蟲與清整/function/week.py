
import re


def extract_business_hours_type_2(input_string):
    # 使用正则表达式匹配每日的营业时间
    pattern = r'(星期一|星期二|星期三|星期四|星期五|星期六|星期日)24 小時營業'
    matches = re.findall(pattern, input_string)

    business_hours = {}
    for match in matches:
        try:
            day_up = weekdays_dict[match]+'_up'
            day_down = weekdays_dict[match]+'_down'
        except:
            print('error'+match)
            day_up = match+'_up'
            day_down = match+'_down'
        business_hours[day_up] = "0000"
        business_hours[day_down] = "2400"

    return business_hours

def extract_business_hours_type_1(input_string):
    # 使用正则表达式匹配每日的营业时间
    pattern = r'(星期一|星期二|星期三|星期四|星期五|星期六|星期日)(\d{2}:\d{2})–(\d{2}:\d{2})'
    matches = re.findall(pattern, input_string)

    business_hours = {}
    for match in matches:
        try:
            day_up = weekdays_dict[match[0]]+'_up'
            day_down = weekdays_dict[match[0]]+'_down'
        except:
            print('error'+match[0])
            day_up = match[0]+'_up'
            day_down = match[0]+'_down'
        if match[1]:  # 判断是否有时间范围
            business_hours[day_up] = match[1].replace(":", "")
            business_hours[day_down] = match[2].replace(":", "")

    return business_hours

def get_city_town_from_address(address):
    pattern = r"(\d+)(.+?[市縣])(.+?[區鄉鎮市村])"
    match = re.search(pattern, address)
    if match:
        city = match.group(2)
        town = match.group(3)
        return city, town
    return None, None

def get_city_town_from_address_2(address):
    pattern = r"(.+?[市縣])(.+?[區鄉鎮市村])"
    match = re.search(pattern, address)
    if match:
        city = match.group(1)
        town = match.group(2)
        return city, town
    return None, None

def get_city_town_from_address_3(address):
    # 正則表達式模式
    pattern = r'[路街道](.*?[區鄉鎮市村])(\D+[縣市])'
    match = re.search(pattern, address)

    if match:
        city = match.group(2)
        town = match.group(1)
        return city, town
    else:
        return None, None

def get_city_town_from_address_4(address):
    # 正則表達式模式
    pattern = r', (.*?[區鄉鎮市村])(\D+[縣市])'
    match = re.search(pattern, address)

    if match:
        city = match.group(2)
        town = match.group(1)
        return city, town
    else:
        return None, None

def get_city_town_from_address_5(address):
    # 正則表達式模式
    pattern = r'[路街道](\D+[縣市])(.*?[區鄉鎮市村])'
    match = re.search(pattern, address)

    if match:
        city = match.group(2)
        town = match.group(1)
        return city, town
    else:
        return None, None

def get_city_town_from_address_6(address):
    # 正則表達式模式
    pattern = r'[路街道](.*?[區鄉鎮市村])(\D+[縣市])'
    match = re.search(pattern, address)

    if match:
        city = match.group(2)
        town = match.group(1)
        return city, town
    else:
        return None, None

def get_city_town_from_address_7(address):
    # 正則表達式模式
    pattern = r', (.*?[區鄉鎮市村])(\D+[縣市])'
    match = re.search(pattern, address)

    if match:
        city = match.group(2)
        town = match.group(1)
        return city, town
    else:
        return None, None
    
def get_city_town_from_address_8(address):
    pattern = r"(.+?[市縣])"
    match = re.search(pattern, address)
    if match:
        city = match.group(0)
        return city, None
    return None, None

def change_city_town_from_address(address):
    pattern = r"[區鄉鎮市村](.+?[市縣])"
    match = re.search(pattern, address)
    if match:
        city = match.group(1)
        return city
    return None

weekdays_dict = {
    '星期一': 'Monday',
    '星期二': 'Tuesday',
    '星期三': 'Wednesday',
    '星期四': 'Thursday',
    '星期五': 'Friday',
    '星期六': 'Saturday',
    '星期日': 'Sunday'
}
check_opentime_namelist=['Monday_up', 
                         'Monday_down', 
                         'Tuesday_up', 
                         'Tuesday_down', 
                         'Wednesday_up', 
                         'Wednesday_down', 
                         'Thursday_up', 
                         'Thursday_down', 
                         'Friday_up', 
                         'Friday_down', 
                         'Saturday_up', 
                         'Saturday_down', 
                         'Sunday_up' ,
                         'Sunday_down']