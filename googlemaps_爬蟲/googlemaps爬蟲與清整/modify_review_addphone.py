from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas  as pd
from datetime import datetime
import re 

import function.file as file
import function.other_tools as otool

folder_path = 'search/'
df_search_result = file.read_all_csv_files_in_folder('search/')

# 刪除重複景點
df_search_result = df_search_result.drop_duplicates(subset='name', keep='first')
df_search_result.reset_index(drop=True, inplace=True)
# df_search_result.head(2)

start_time = time.time() 
count = 0
# 逐一載入評論
#---- driver 設定 ----
# s = Service("./geckodriver.exe")
s = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=s)
# 最大視窗
driver.maximize_window() 
# totalleft = 0
check_review_line_less_2_flag = False
rw_csvname=''
for index,run_url in enumerate(df_search_result['Website']):
#     index = 0
#     run_url = df_search_result['Website'][0]
#     print(df_search_result['Website'][index],end="")
    folder_path = 'C:/Users/User/Desktop/googleapi/googlemaps爬蟲_ver10/review/'  
    tmpcsvname=""
    for changeword in df_search_result['name'][index]:
        if changeword =="|" or changeword =="/" or changeword =="*" or changeword =="\\" or changeword =="🔆" or changeword =="、" or changeword ==":" :
            tmpcsvname+=" "
        else:
            tmpcsvname +=changeword
    
    rw_csvname = tmpcsvname+'result.csv'
    print(df_search_result['name'][index],end=" ")
    try:
        df = pd.read_csv(folder_path+rw_csvname)
#         print(df)
    except:
        continue
    try:
        if pd.isna(df['rw_phone'][2]):
            pass
#         if df['rw_phone'][2] !="NaN":
        else:
            print(df['rw_phone'][2],' continue')
            continue
    except:
        continue
    driver.get(run_url)
    overview_review_result = BeautifulSoup(driver.page_source, "html.parser")
    otool.timesleep_rand()
    try:
        elements = driver.find_elements(By.CLASS_NAME, 'CsEnBe')
        for i,element in enumerate(elements):
            aria_label = element.get_attribute('aria-label')
            if aria_label:
                if aria_label[:4] == "電話號碼":
                    rw_phone = driver.find_elements(By.CLASS_NAME, 'CsEnBe')[i].text
                    break
            if  i == len(elements)-1:   
                rw_phone=""
    except:
        rw_phone=""

    if rw_phone == "":
        continue
    fill_value = rw_phone
    print(rw_phone)
    target_column = 'rw_phone'  # 將此處替換為目標欄位名稱

    file.fill_value_in_csv_files(folder_path,rw_csvname, fill_value, target_column)
