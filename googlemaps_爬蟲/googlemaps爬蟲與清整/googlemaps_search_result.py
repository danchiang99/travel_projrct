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

import function.file as file
import function.other_tools as otool
import params.search_input as si


# introduction overview
def get_io_result():
    io_result = introduction.find_all('div',class_='bfdHYd')
    for index,i in enumerate(io_result):
        io_keyword_list.append(search_keyword)
        try:
            io_name_list.append(i.find('div',class_='NrDZNb').text)
        except:
            io_name_list.append("")
 
        current_time = datetime.now()
        io_current_time_list.append(str(current_time).split(".")[0])
        try:
            io_rating_list.append(i.find('span',class_='MW4etd').text)
            io_rating_count_list.append(i.find('span',class_='UY7F9').text.replace("(", "").replace(")", "").replace(",", ""))
        except:
            io_rating_list.append("")
            io_rating_count_list.append("")
        io_category = i.find_all('div',class_='W4Efsd')[1]
        # print(io_category.find('div').text )
        tmp_success_flag = False
        if io_category.find('div').text ==[]:
            io_address_list.append("")
            io_category_list.append("")
            tmp_success_flag = True
        else:
            tmpstr=""
            for tmp in io_category.find('div').text:
                if tmp =="·" or tmp ==" ":
                    tmp_success_flag = True
                    io_category_list.append(tmpstr)
                    try:
                        io_address_list.append( io_category.find_all('span')[2].text.replace("·", "").replace(" ", ""))
                    except:
                        io_address_list.append("")
                    break
                tmpstr += tmp
                if tmpstr == io_category.find('div').text:
                    tmp_success_flag = True
                    io_category_list.append(tmpstr)
                    io_address_list.append("")
        if tmp_success_flag == False:
            io_address_list.append("")
            io_category_list.append("")

        try:
            io_introduce_list.append(io_category.find_all('div')[1].text)
        except:
            io_introduce_list.append("")
        try:
            io_Website_list.append( total_result[index]['href'])
        except:
            io_Website_list.append("")
        try:
            io_img_list.append( i.find('img')['src'])
        except:
            io_img_list.append("")
        try:
            io_latitude_list.append( total_result[index]['href'].split("data=")[1].split("!")[5].split("d")[1] )
        except:
            io_latitude_list.append("")
        try:
            io_longitude_list.append(total_result[index]['href'].split("data=")[1].split("!")[6].split("d")[1])
        except:
            io_longitude_list.append("")

# 記錄開始時間
start_time = time.time() 

#---- driver 設定 ----
# s = Service("./geckodriver.exe")
s = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=s)

# 最大視窗
driver.maximize_window() 
check_search_line_less_2_flag=False
for keyword in si.all_search_list:
    search_keyword = keyword
    tmp_search_keyword = ''
    for j in search_keyword:
        if j ==" ":
            tmp_search_keyword+="_"
        else:
            tmp_search_keyword+=j
    csvname = tmp_search_keyword+'result.csv'
    if file.check_file_existence('search/', csvname):
        print(csvname,' exist')
    #   確認檔案是否為空、異常用  
        file_path = os.path.join('search', csvname)
        is_over_2_lines = file.check_csv_file_lines(file_path)
        if is_over_2_lines <2:
            print('!!!!!!!!!',csvname,' less 2 search')
            check_search_line_less_2_flag = True
        else:
            continue
        
    url ='https://www.google.com/maps'
    driver.get(url)
    otool.timesleep_rand()
    # 輸入查詢關鍵字
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_keyword)
    otool.timesleep_rand()
    # 送出關鍵字
    btn_search = driver.find_element(By.CLASS_NAME, "mL3xi")
    btn_search.click()
    otool.timesleep_rand()

    # 相關查詢參數輸入
    search_max = si.search_max #設定要搜尋多少筆資料(如果google有的話) 最小設定11

    #---- 變數初始化 ----
    # 搜尋結果
    io_current_time_list = []
    io_keyword_list = []
    io_name_list = []
    io_rating_list = []
    io_rating_count_list = []
    io_category_list = []
    io_address_list = []
    io_introduce_list = []
    io_Website_list = []
    io_img_list = []
    io_latitude_list = []
    io_longitude_list = []
#       確認檔案是否為空、檢測異常用  
    if check_search_line_less_2_flag ==True:
        time.sleep(2)
        driver.save_screenshot('check_img/'+tmp_search_keyword+'.png')
    
    # 搜尋結果往下捲動
    # 第一批搜尋結果的XPATH從3開始到11，每一個結果號碼+2，第一次迭代直接拉到最下方，後續每次移動1個結果，就可以保證一直產生新的結果
    otool.timesleep_rand()
    for i in range(11, search_max, 2):
        try:        
            scrollable_search_result_block = driver.find_element(By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{i}]/div/a')
        except:
            break
        else:
            driver.execute_script("arguments[0].scrollIntoView();", scrollable_search_result_block)
            otool.timesleep_rand()

    #---- 查詢html ----
    otool.timesleep_rand()
    introduction = BeautifulSoup(driver.page_source, "html.parser")
    total_result = introduction.find_all('a',class_='hfpxzc')
    otool.timesleep_rand()

    #---- get 搜尋結果 ----
    get_io_result()    
    io_df = pd.DataFrame({
                            'keyword':io_keyword_list,
                            'name':io_name_list,
                            'current_time':io_current_time_list,
                            'rating':io_rating_list,
                            'rating_count':io_rating_count_list,
                            'category':io_category_list,
                            'address':io_address_list,
                            'introduce':io_introduce_list,
                            'Website':io_Website_list,
                            'img':io_img_list,
                            'latitude':io_latitude_list,
                            'longitude':io_longitude_list
    })

    #---- 搜尋結果存至csv檔 ----
    io_df.to_csv('search/'+csvname,encoding='utf-8-sig')

    end_time = time.time()  # 記錄結束時間

    # 總花費時間
    print("run times: ",otool.get_run_times(end_time,start_time))

#---- 關閉瀏覽器 ----
driver.close()
