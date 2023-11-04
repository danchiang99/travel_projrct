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
import function.week as week
import params.review_input as ri


# review_result
def get_rw_result():
    for i in review:
        current_time = datetime.now()
        rw_current_time_list.append(str(current_time).split(".")[0])
        try:
            rw_name_list.append(overview_review_result.find('h1',class_='DUwDvf').text)
        except:
            rw_name_list.append("")

        try:
            rw_latitude_list.append(rw_latitude)
        except:
            rw_latitude_list.append("")

        try:
            rw_longitude_list.append(rw_longitude)
        except:
            rw_longitude_list.append("")

        try:
            rw_category_list.append(rw_category)
        except:
            rw_category_list.append("")

        rw_tag=""
        try:
            tag_result = introduction_review_result.find_all('li',class_='hpLkke')
            for tag in tag_result:
                rw_tag+=tag.text
                rw_tag+=" "
        except:
            print("error - ","rw_tag_list")
        rw_tag_list.append(rw_tag)

        try:
            rw_introduction_list.append(introduction_review_result.find('p',class_='ZqFyf').text)
        except:
            rw_introduction_list.append("")

        try:
            rw_open_time_list.append(rw_opentime)
        except:
            rw_open_time_list.append("")
        
        # 營業時間細分
        try:
            rw_open_time_Monday_up_list.append(rw_week_all[0])
        except:
            rw_open_time_Monday_up_list.append("")

        try:
            rw_open_time_Monday_down_list.append(rw_week_all[1]) 
        except:
            rw_open_time_Monday_down_list.append("") 
            
        try:
            rw_open_time_Tuesday_up_list.append(rw_week_all[2]) 
        except:
            rw_open_time_Tuesday_up_list.append("")
            
        try:
            rw_open_time_Tuesday_down_list.append(rw_week_all[3])
        except:
            rw_open_time_Tuesday_down_list.append("")
            
        try:
            rw_open_time_Wednesday_up_list.append(rw_week_all[4])
        except:
            rw_open_time_Wednesday_up_list.append("")
            
        try:
            rw_open_time_Wednesday_down_list.append(rw_week_all[5])
        except:
            rw_open_time_Wednesday_down_list.append("")
            
        try:
            rw_open_time_Thursday_up_list.append(rw_week_all[6])
        except:
            rw_open_time_Thursday_up_list.append("")
            
        try:
            rw_open_time_Thursday_down_list.append(rw_week_all[7])
        except:
            rw_open_time_Thursday_down_list.append("")
            
        try:
            rw_open_time_Friday_up_list.append(rw_week_all[8])
        except:
            rw_open_time_Friday_up_list.append("")
            
        try:
            rw_open_time_Friday_down_list.append(rw_week_all[9])
        except:
             rw_open_time_Friday_down_list.append("")
        try:
            rw_open_time_Saturday_up_list.append(rw_week_all[10])
        except:
            rw_open_time_Saturday_up_list.append("")
            
        try:
            rw_open_time_Saturday_down_list.append(rw_week_all[11])
        except:
            rw_open_time_Saturday_down_list.append("")
            
        try:
            rw_open_time_Sunday_up_list.append(rw_week_all[12])
        except:
            rw_open_time_Sunday_up_list.append("")
            
        try:
            rw_open_time_Sunday_down_list.append(rw_week_all[13])
        except:
            rw_open_time_Sunday_down_list.append("")
        
        try:
            rw_rating_total_list.append(rw_rating_total)
        except:
            rw_rating_total_list.append("")

        try:
            rw_rating_count_total_list.append(rw_rating_count_total)
        except:
            rw_rating_count_total_list.append("")
            

        rw_phone_list.append(rw_phone)


        try:
            rw_address_list.append(overview_review_result.find('div',class_='rogA2c').text)
        except:
            rw_address_list.append("")
            
        #---- 地址解析分類
        city, town = week.get_city_town_from_address(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_2(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_3(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_4(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_5(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_6(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_7(overview_review_result.find('div',class_='rogA2c').text)
        if city == None:
            city, town = week.get_city_town_from_address_8(overview_review_result.find('div',class_='rogA2c').text)
        try:
            city = re.sub(r'[0-9\s,]', '', city)
        except:
            pass
        try:
            town = re.sub(r'[0-9\s,]', '', town)
        except:
            pass
        rw_address_city_list.append(city)
        rw_address_town_list.append(town)

            
        try:
            rw_reviewer_list.append(i.find('div',class_='d4r55').text)
        except:
            rw_reviewer_list.append("")

        try:
            rw_reviewer_page_list.append(i.find('button',class_='WEBjve')['data-href'])
        except:
            rw_reviewer_page_list.append("")

        rw_reviewer_tag = i.find('div',class_='RfnDt')
        try:
            rw_reviewer_tag_list.append(rw_reviewer_tag.text)
        except:
            rw_reviewer_tag_list.append("")

        try:
            rw_review_time_list.append(i.find('span',class_='rsqaWe').text)
        except:
            rw_review_time_list.append("")

        try:
            rw_rating_reviewer_list.append(i.find('span',class_='kvMYJc')['aria-label'])
        except:
            rw_rating_reviewer_list.append("")

        try:
            rw_likes = i.find('button',class_='GBkF3d')['aria-label']   
            rw_likes_list.append(rw_likes.replace("喜歡", ""))
        except:
            rw_likes_list.append("")

        review_word = i.find('div',class_='MyEned')
        try:
            rw_review_list.append(review_word.text)
        except:
            rw_review_list.append("")

        review_word = i.find('div',class_='wiI7pd')
        try:
            rw_review_word_list.append(review_word.text)
        except:
            rw_review_word_list.append("")
            
        try: 
            rw_tickets_sale_list.append(rw_tickets_sale)
        except:
            rw_tickets_sale_list.append("")

def clsoe_above_main_windows():
    all_windows = driver.window_handles
    if len(all_windows) >1:
        for i in range(len(all_windows)):
            if i ==0 :
                continue
            driver.switch_to.window(all_windows[i])
            driver.close()
    driver.switch_to.window(all_windows[0])
    otool.timesleep_rand() 

def check_windows_num():
    # 獲取所有打開的視窗
    all_windows = driver.window_handles
    if len(all_windows)> 1:
        print("!!!!!!!!error more window!!!!!!!!")

def choose_windows():
    # 獲取所有打開的視窗
    all_windows = driver.window_handles
    driver.switch_to.window(all_windows[0])
    otool.timesleep_rand() 

folder_path = 'search/'
df_search_result = file.read_all_csv_files_in_folder('search/')

# 刪除重複景點
df_search_result = df_search_result.drop_duplicates(subset='name', keep='first')
df_search_result.reset_index(drop=True, inplace=True)
# print(df_search_result)


sort_type = ri.review_sort_type # 排序方式 0 : 最相關 1: 最新 2: 評分最高 3: 評分最低 
# google評論爬蟲查詢至1130筆後會沒有資料 故建議設定最多滑100次(滑1次10筆資料) 如果程式出錯大概率錯這因google好像會阻擋 錯的話就挑低此參數值 
setdefault_max_review_slip =  ri.review_setdefault_max_review_slip # 評論下滑多少次ex 50 -> 50*10 +10 =500則評論 

# 記錄開始時間
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
for index,run_url in enumerate(df_search_result['Website']):
# index =7
# run_url ='https://www.google.com/maps/place/%E8%87%BA%E5%8C%97%E5%B8%82%E7%AB%8B%E5%8B%95%E7%89%A9%E5%9C%92/data=!4m7!3m6!1s0x3442aa604a32818f:0xaafe06fd09b4d766!8m2!3d24.9985635!4d121.5809857!16zL20vMGJyNTY3!19sChIJj4EySmCqQjQRZte0Cf0G_qo?authuser=0&hl=zh-TW&rclk=1'

    tmpcsvname=""
    for changeword in df_search_result['name'][index]:
        if changeword =="|" or changeword =="/" or changeword =="*" or changeword =="\\" or changeword =="🔆" or changeword =="、" or changeword ==":" :
            tmpcsvname+=" "
        else:
            tmpcsvname +=changeword
    rw_csvname = tmpcsvname+'result.csv'

    if file.check_file_existence('review/', rw_csvname):
        print(rw_csvname,' exist')
        continue
    otool.timesleep_rand()
    driver.get(run_url)

    #---- 變數初始化 ----
    # 評論
    rw_open_time_list = []
    rw_category_list = []
    rw_tag_list=[]
    rw_current_time_list = []
    rw_name_list = []
    rw_latitude_list = []
    rw_longitude_list = []
    rw_introduction_list = []
    rw_rating_total_list = []
    rw_rating_count_total_list = []
    rw_phone_list = []
    rw_address_list = []
    rw_address_city_list = []
    rw_address_town_list = []
    rw_reviewer_list = []
    rw_reviewer_page_list = []
    rw_reviewer_tag_list = []
    rw_review_time_list = []
    rw_rating_reviewer_list = []
    rw_likes_list = []
    rw_review_list = []
    rw_review_word_list = []
    rw_open_time_Monday_up_list = []
    rw_open_time_Monday_down_list = []
    rw_open_time_Tuesday_up_list = []
    rw_open_time_Tuesday_down_list = []
    rw_open_time_Wednesday_up_list = []
    rw_open_time_Wednesday_down_list = []
    rw_open_time_Thursday_up_list = []
    rw_open_time_Thursday_down_list = []
    rw_open_time_Friday_up_list = []
    rw_open_time_Friday_down_list = []
    rw_open_time_Saturday_up_list = []
    rw_open_time_Saturday_down_list = []
    rw_open_time_Sunday_up_list = []
    rw_open_time_Sunday_down_list = []
    rw_tickets_sale_list = []
    # 評論參數
    rw_opentime = ""
    rw_category = ""
    rw_rating_total = ""
    rw_rating_count_total = ""
    rw_latitude = ""
    rw_longitude = ""
    rw_week_all= ['', '', '', '', '','', '', '', '', '','', '', '', '']
    rw_tickets_sale=""
    otool.timesleep_rand()
    rw_phone=""

    otool.timesleep_rand()
    #---- 獲取景點經緯度 ----
    try:
        rw_latitude = run_url.split("data=")[1].split("!")[5].split("d")[1]
    except:
        print(df_search_result['name'][index],'error latitude',end=" ")
    try:
        rw_longitude = run_url.split("data=")[1].split("!")[6].split("d")[1]
    except:
        print(df_search_result['name'][index],'error longitude',end=" ")
    
    otool.timesleep_rand()
    #---- 獲取電話號碼 ----
    try:
        elements = driver.find_elements(By.CLASS_NAME, 'CsEnBe')
        for indexphone,element in enumerate(elements):
            aria_label = element.get_attribute('aria-label')
            if aria_label:
                if aria_label[:4] == "電話號碼":
                    rw_phone = driver.find_elements(By.CLASS_NAME, 'CsEnBe')[indexphone].text
                    break
            if  indexphone == len(elements)-1:   
                rw_phone=""
    except:
        rw_phone=""
    #---- 查詢總攬html ----
    try:
        overview_review_result = BeautifulSoup(driver.page_source, "html.parser")
    except:
        print(df_search_result['name'][index],'error overview_review_result')
    
    #---- 獲取門票售價 ----  
    try:
        rw_tickets_sale = overview_review_result.find_all('div',class_='NKJo9')[0].find('div',class_='drwWxc').text    
    except:
        rw_tickets_sale=''

    #---- 前往簡介 ----
    try:
        # 確認簡介是的位置 是則執行內容
        for tmp_i in range(5):
            if overview_review_result.find_all('div',class_='Gpq6kf')[tmp_i].text == "簡介":
                introduction_btn = driver.find_elements(By.CLASS_NAME, 'hh2c6')[tmp_i]
                introduction_btn.click()
                otool.timesleep_rand()
                #---- 查詢簡介html ----
                introduction_review_result = BeautifulSoup(driver.page_source, "html.parser")
                #---- 返回 ----
                introduction_btn = driver.find_elements(By.CLASS_NAME, 'hh2c6')[0]
                introduction_btn.click()
                otool.timesleep_rand()
                break
            
    except:
        clsoe_above_main_windows()
        print(df_search_result['name'][index],' error - 前往簡介')

    #---- 營業時間處理 ----
    op_time_try_max = 3
    while op_time_try_max>0:
        op_time_try_max -=1
        try:
            # 營業有兩種不同模式，先確認是否是不需要切換頁面的模式
            rw_opentime_result = overview_review_result.find_all('tr',class_='y0skZc')
            if rw_opentime_result != []:
                tmp_1=""
                for ii in rw_opentime_result:
                    tmp_1 += ii.text
                    tmp_1 += " "
                rw_opentime = tmp_1
                op_time_try_max = 0
            # 否，則當成是點擊模式
            else:
                #---- 前往營業時間 ----
                introduction_btn = driver.find_elements(By.CLASS_NAME, 'CsEnBe')[1]
                introduction_btn.click()
                otool.timesleep_rand()
                #---- 查詢營業時間html ----
                opentime_result = BeautifulSoup(driver.page_source, "html.parser")
                #---- 返回 ----
                back_introduction_btn = driver.find_element(By.CLASS_NAME, 'hYBOP.FeXq4d')
                back_introduction_btn.click()
                otool.timesleep_rand()
                tmp_2=opentime_result.find('div',class_='t39EBf')['aria-label'].replace("、", "").replace(" 到 ", "–").replace(".", "").replace(";", "").replace("隱藏本週營業時間", "")
                rw_opentime = tmp_2
                op_time_try_max = 0
            # 如果發生營業時間不存在 暫不處理 讓他進回圈找不到就出去
        except:
             # 儲存照片做debug用
            if op_time_try_max == 0:
                driver.save_screenshot('bug_img/'+df_search_result['name'][index]+"error_營業時間"+'try_'+str(3-op_time_try_max)+'.png')
                check_windows_num()
                clsoe_above_main_windows()
                print(df_search_result['name'][index],' error - 營業時間' )


    #---- 整理營業時間 ----
    opentime_result_byday = week.extract_business_hours_type_1(rw_opentime)
    if opentime_result_byday == {}:
        opentime_result_byday = week.extract_business_hours_type_2(rw_opentime)

    if opentime_result_byday != {}:
        for op_index,op_name in enumerate(week.check_opentime_namelist):
            if op_name in opentime_result_byday:
                rw_week_all[op_index]=opentime_result_byday[op_name]
            else:
                rw_week_all[op_index]=""
    # 分類
    rw_category=df_search_result['category'][index]
    # 總評分與總評分人數
    rw_rating_total = df_search_result['rating'][index]
    rw_rating_count_total = df_search_result['rating_count'][index]


    #---- 前往評論 ----
    try:
        for tmp_j in range(5):
            if overview_review_result.find_all('div',class_='Gpq6kf')[tmp_j].text == "評論":
                review_btn = driver.find_elements(By.CLASS_NAME, 'hh2c6')[tmp_j]
                review_btn.click()
                # otool.timesleep_rand()
                break
    except:
        clsoe_above_main_windows()
        print(df_search_result['name'][index],'no search review')
    else:
        otool.timesleep_rand()
    try:
        # 點選評論排序
    #         btn_sort_review = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.Hu9e2e.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf > div.m6QErb.Pf6ghf.KoSBEe.ecceSd.tLjsW > div.TrU0dc.kdfrQc > button')
        btn_sort_review=driver.find_element(By.XPATH, "//button[@aria-label='排序評論']")
        btn_sort_review.click()

        otool.timesleep_rand()
        # 選取排序方式
        btn_sort_chose = driver.find_elements(By.CLASS_NAME, 'fxNQSd')[sort_type] 
        btn_sort_chose.click()
        otool.timesleep_rand()

        # 評論往下捲動
        # 定位評論區塊
        scrollable_review_block = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf')
        # 因基礎10筆評論資料 每滑動1次多10筆 且執行到約1130筆後就google就爬不動(如下) 故最多只撈取前1000筆評論資料
        # review 20
        # review 30
        # ...
        # review 1130
        # review 1130
        slip_max = min(int((int(df_search_result['rating_count'][index])-10)/10)+1,setdefault_max_review_slip)
        for tmp_slip_rw in range(slip_max):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_review_block)
            otool.timesleep_rand()

    except:
        clsoe_above_main_windows()
        print(df_search_result['name'][index],' error - 評論點擊or下拉' )

     #---- 點擊評論全文 ----
    try:
        all_word_btn = driver.find_elements(By.CLASS_NAME,'w8nwRe')
        for tmpclick in all_word_btn:
    #         print(tmpclick.text)
            if tmpclick.text != "全文":
                continue
            try :
                tmpclick.click()
                otool.timesleep_rand()
            except:
                clsoe_above_main_windows()
                print(df_search_result['name'][index],"error - 全文點擊失敗")
    except:
        clsoe_above_main_windows()
        print(df_search_result['name'][index],' error - 全文點擊搜尋失敗' )
    try:
        review_result = BeautifulSoup(driver.page_source, "html.parser")
        review = review_result.find_all('div',class_='jJc9Ad')
    except:
        print(df_search_result['name'][index],' error - 讀取所有留言失敗(大概率是因為跳出網頁後關閉造成)' )


    #---- get 評論結果 ----
    get_rw_result()

    rw_df = pd.DataFrame({
                            'rw_name':rw_name_list,
                            'rw_current_time':rw_current_time_list,
                            'rw_category':rw_category_list,
                            'rw_tag':rw_tag_list,
                            'rw_tickets_sale':rw_tickets_sale_list,
                            'rw_open_time':rw_open_time_list,
                            'rw_Monday_open':rw_open_time_Monday_up_list,
                            'rw_Monday_close':rw_open_time_Monday_down_list,
                            'rw_Tuesday_open':rw_open_time_Tuesday_up_list,
                            'rw_Tuesday_close':rw_open_time_Tuesday_down_list,
                            'rw_Wednesday_open':rw_open_time_Wednesday_up_list,
                            'rw_Wednesday_close':rw_open_time_Wednesday_down_list,
                            'rw_Thursday_open':rw_open_time_Thursday_up_list,
                            'rw_Thursday_close':rw_open_time_Thursday_down_list,
                            'rw_Friday_open':rw_open_time_Friday_up_list,
                            'rw_Friday_close':rw_open_time_Friday_down_list,
                            'rw_Saturday_open':rw_open_time_Saturday_up_list,
                            'rw_Saturday_close':rw_open_time_Saturday_down_list,
                            'rw_Sunday_open':rw_open_time_Sunday_up_list,
                            'rw_Sunday_close':rw_open_time_Sunday_down_list,      
                            'rw_latitude':rw_latitude_list,
                            'rw_longitude':rw_longitude_list,
                            'rw_introduction':rw_introduction_list,
                            'rw_rating_total':rw_rating_total_list,
                            'rw_rating_count_total':rw_rating_count_total_list,
                            'rw_phone':rw_phone_list,
                            'rw_address':rw_address_list,
                            'rw_reviewer':rw_reviewer_list,
                            'rw_reviewer_page':rw_reviewer_page_list,
                            'rw_reviewer_tag':rw_reviewer_tag_list,
                            'rw_review_time':rw_review_time_list,
                            'rw_rating_reviewer':rw_rating_reviewer_list,
                            'rw_likes':rw_likes_list,
                            'rw_review':rw_review_list,
                            'rw_review_word':rw_review_word_list,
                            'rw_city':rw_address_city_list,
                            'rw_town':rw_address_town_list

                        })
    end_time = time.time()  # 記錄結束時間


    #---- 評論結果存至csv檔 ----
    rw_df.to_csv('review/'+rw_csvname,encoding='utf-8-sig')
    otool.timesleep_rand() 
    count += 1
    print(df_search_result['name'][index])
    print("(",count,") runtimes: ",otool.get_run_times(end_time,start_time))



#---- 關閉瀏覽器 ----
driver.close()
end_time = time.time()  # 記錄結束時間

# 總花費時間
print("已抓取完畢..")
# otool.get_run_times(end_time,start_time)
print("run times: ",otool.get_run_times(end_time,start_time))