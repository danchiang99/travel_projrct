import csv
import sqlite3

# 连接到SQLite数据库（如果文件不存在会自动创建）
conn = sqlite3.connect('travel.db')
cursor = conn.cursor()

# 创建表
create_table_sql = '''
CREATE TABLE IF NOT EXISTS view_overview (
keyword	string	,
name	string	,
current_time	string	,
rating	string	,
rating_count	string	,
category	string	,
address	string	,
introduce	string	,
Website	string	,
img	string	,
latitude	string	,
longitude	string	,
rw_category	string	,
rw_tag	string	,
rw_tickets_sale	string	,
rw_open_time	string	,
rw_Monday_open	string	,
rw_Monday_close	string	,
rw_Tuesday_open	string	,
rw_Tuesday_close	string	,
rw_Wednesday_open	string	,
rw_Wednesday_close	string	,
rw_Thursday_open	string	,
rw_Thursday_close	string	,
rw_Friday_open	string	,
rw_Friday_close	string	,
rw_Saturday_open	string	,
rw_Saturday_close	string	,
rw_Sunday_open	string	,
rw_Sunday_close	string	,
rw_introduction	string	,
rw_phone	string	,
rw_address	string	,
rw_city	string	,
rw_town	string	,
stay_time_min	string	,
weekday_opentime_dict   string  ,
is_open_list    string,
new_star_label    string,
good    string,
neutral    string,
bad    string,
brief_intro string,
span_intro_ string,
label_lCr01 string,
label_lCr02 string,
new_cate3 string,
ncat_label02 string,
c_lab021 string,
c_lab022 string,
c_lab023 string

)
'''
cursor.execute(create_table_sql)
conn.commit()

# 读取CSV文件并插入数据到表中
csv_file_path = './file/search_clear_final.csv'
with open(csv_file_path, 'r', encoding='utf-8-sig') as csv_file:

    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        insert_sql = '''
        INSERT INTO view_overview (keyword,name,current_time,rating,rating_count,category,address,introduce,Website,img,latitude,longitude,rw_category,rw_tag,rw_tickets_sale,rw_open_time,rw_Monday_open,rw_Monday_close,rw_Tuesday_open,rw_Tuesday_close,rw_Wednesday_open,rw_Wednesday_close,rw_Thursday_open,rw_Thursday_close,rw_Friday_open,rw_Friday_close,rw_Saturday_open,rw_Saturday_close,rw_Sunday_open,rw_Sunday_close,rw_introduction,rw_phone,rw_address,rw_city,rw_town,stay_time_min,weekday_opentime_dict,is_open_list,new_star_label,good,neutral,bad,brief_intro,span_intro_,label_lCr01,label_lCr02,new_cate3,ncat_label02,c_lab021,c_lab022,c_lab023) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        values = (row['keyword'],row['name'],row['current_time'],row['rating'],row['rating_count'],row['category'],
                row['address'],row['introduce'],row['Website'],row['img'],row['latitude'],row['longitude'],row['rw_category'],
                row['rw_tag'],row['rw_tickets_sale'],row['rw_open_time'],row['rw_Monday_open'],row['rw_Monday_close'],row['rw_Tuesday_open'],
                row['rw_Tuesday_close'],row['rw_Wednesday_open'],row['rw_Wednesday_close'],row['rw_Thursday_open'],row['rw_Thursday_close'],
                row['rw_Friday_open'],row['rw_Friday_close'],row['rw_Saturday_open'],row['rw_Saturday_close'],row['rw_Sunday_open'],row['rw_Sunday_close'],
                row['rw_introduction'],row['rw_phone'],row['rw_address'],row['rw_city'],row['rw_town'],row['stay_time_min'],row['weekday_opentime_dict'],row['is_open_list'],
                row['new_star_label'],row['good'],row['neutral'],row['bad'],
                row['brief_intro'],row['span_intro_'],
                row['label_lCr01'],row['label_lCr02'],row['new_cate3'],row['ncat_label02'],
                row['c_lab021'],row['c_lab022'],row['c_lab023'])  # 根据CSV列名修改
        cursor.execute(insert_sql, values)
        conn.commit()

# 关闭连接
conn.close()
print("done")