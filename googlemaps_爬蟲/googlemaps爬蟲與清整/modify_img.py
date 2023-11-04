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
path = 'search/'
file_list = [file for file in os.listdir(path) if file.endswith('.csv')]
start_time = time.time() 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 啟用 headless 模式
chrome_options.add_argument('--disable-gpu')  # 在 headless 模式下禁用 GPU


# 逐一讀取 CSV 檔案
for file in file_list:
    file_path = os.path.join(path, file)
    # print(f"Reading {file_path}")
    df_search_result = pd.read_csv(file_path)
    # 刪除重複景點
    df_search_result = df_search_result.drop_duplicates(subset='name', keep='first')
    df_search_result.reset_index(drop=True, inplace=True)
    # df_search_result.head(2)
    mistake_img = df_search_result.loc[df_search_result['img'].apply(lambda x: (isinstance(x, str) and not x.startswith('https://lh5')) if pd.notna(x) else True)]
    # mistake_img = df_search_result.loc[df_search_result['img'].apply(lambda x: (isinstance(x, str) and not x.startswith('https://')) if pd.notna(x) else True)]


    #---- driver 設定 ----
    s = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=chrome_options)
    # 最大視窗
    driver.maximize_window() 
    check_review_line_less_2_flag = False
    rw_csvname=''
    for index,run_url in enumerate(mistake_img['Website']):
        driver.get(run_url)
        otool.timesleep_rand()
        # print(mistake_img['name'].iloc[index])
        print(f"modify {file_path}")
        maxtry=0
        while maxtry<3:
            overview_review_result = BeautifulSoup(driver.page_source, "html.parser")
            target_result = overview_review_result.find('div',class_='RZ66Rb')
            try:
                img_result = target_result.find('img')
                print(mistake_img['name'].iloc[index],end="")
                print(img_result['src'])
                df_search_result.loc[df_search_result['name'] == mistake_img['name'].iloc[index], 'img'] = img_result['src']
                maxtry = 3
            except:
                maxtry +=1
                otool.timesleep_rand()
                print(mistake_img['name'].iloc[index],'maxtry times',maxtry)
                

        otool.timesleep_rand()


    end_time = time.time()  # 記錄結束時間
    df_search_result.to_csv(file_path,encoding='utf-8-sig')
    # 總花費時間
    print("run times: ",otool.get_run_times(end_time,start_time))

#---- 關閉瀏覽器 ----
driver.close()