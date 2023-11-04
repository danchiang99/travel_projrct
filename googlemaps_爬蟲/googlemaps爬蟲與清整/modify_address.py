import os
import re
import pandas as pd
import function.week as week

# 获取指定文件夹内的所有文件名
folder_path ='review/'
file_list = os.listdir(folder_path)

# 循环遍历文件列表，读取所有CSV文件的内容，并将其合并到combined_df中
for filename in file_list:
    if filename.lower().endswith('.csv'):  # 检查文件扩展名是否为CSV
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)
        try:
            if pd.isna(df['rw_address'][0]):
                pass
            else:
               
                if pd.isna(df['rw_city'][0]):
                    # print(df['rw_address'][0])
                    city, town = week.get_city_town_from_address_2(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address_3(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address_4(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address_5(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address_6(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address_7(df['rw_address'][0])
                    if city == None:
                        city, town = week.get_city_town_from_address(df['rw_address'][0])
                    if city == None:
                        # print(df['rw_address'][0],end=" ")
                        city, town = week.get_city_town_from_address_8(df['rw_address'][0])
                        # print(city,end=" ")
                    try:
                        city = re.sub(r'[0-9\s,號]', '', city)
                    except:
                        pass
                    try:
                        town = re.sub(r'[0-9\s,]', '', town)
                    except:
                        pass
                    # print(city)
                    df['rw_city'] = city
                    df['rw_town'] = town
                    # print(city)
                    # print(town)

                    df.to_csv(file_path, index=False, encoding='utf-8-sig')

                # 地址名稱修改
                if pd.isna(df['rw_address'][0]):
                    pass
                else:
                
                    if pd.isna(df['rw_city'][0]):
                        pass
                    else:
                        if any(char.isspace() for char in df['rw_city'][0]):
                            city = week.change_city_town_from_address(df['rw_city'][0])
                            try:
                                city = re.sub(r'[0-9\s,號]', '', city)
                            except:
                                pass
                            df['rw_city'] = city
                        df.to_csv(file_path, index=False, encoding='utf-8-sig')     
        except:
            continue
        try:
            df = pd.read_csv(file_path)
            if len(df['rw_city'][0])>3:
                match = re.search(r"[區鄉鎮市村號灣](.+?[市縣])", df['rw_city'][0])
                city = df['rw_city'][0]
                if match:
                    city = match.group(1)
                print('rw_city',df['rw_city'][0],end=" ")
                print('rw_name',df['rw_name'][0])
                print(city)
                df['rw_city'] = city
                df.to_csv(file_path, index=False, encoding='utf-8-sig') 
        except:
            continue




