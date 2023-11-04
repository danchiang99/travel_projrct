爬蟲爬完並清整好後
資料會存為search_overview.csv

clear_search_overview.ipynb
開啟search_overview.csv
整理各城市景點數量 並將桃園縣 改桃園市
修正地址為空值的狀況
部分景點因為url格式問題造成經緯度讀取不到，故修正
建議停留時間轉分鐘
刪除部分分類為餐廳、小吃等景點
新增營業時間用欄位


clear_search_after model.csv
經過貼標後產生新的csv
new_search_clear.csv
與分類後的景點csv
spotsoverview.v3_5981semi_c_lab023.csv

將兩個表格內容合併
處理營業時間空值
處理建議停留時間空值
處理經緯度跑出城市的問題
處理交通無法抵達景點問題
處理外島資訊

還有時間的話想處
town等空值資訊

