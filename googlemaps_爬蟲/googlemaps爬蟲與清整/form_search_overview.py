import pandas as pd
import time
import function.file as file
import function.other_tools as otool

# 讀取search
df_search_result = file.read_all_csv_files_in_folder('search/')

# 刪除重複景點
df_search_result = df_search_result.drop_duplicates(subset='name', keep='first')
df_search_result.reset_index(drop=True, inplace=True)
df_search_result = df_search_result.drop(['Unnamed: 0'],axis = 1)
df_search_result.to_csv('result/tmp_search_norepeat_result.csv',encoding='utf-8-sig')

# 開啟review.csv
start_time = time.time() 
# df_review_result_all = file.read_all_csv_files_in_folder('review/')
df_review_result_all =  pd.read_csv('result/review_overview.csv')
end_time = time.time() 
print("run times: ",otool.get_run_times(end_time,start_time))

# df_review_result_all.head(3)

# 只留一筆
df_review_result_norepeat = df_review_result_all.drop_duplicates(subset='rw_name', keep='first')
df_review_result_norepeat.reset_index(drop=True, inplace=True)
df_review_result_norepeat
# 存檔
df_review_result_norepeat = df_review_result_norepeat.drop(['Unnamed: 0'],axis = 1)
df_review_result_norepeat.to_csv('result/tmp_review_norepeat_result.csv',encoding='utf-8-sig')
df_r = df_review_result_norepeat
df_s = df_search_result
# 開啟staytime.csv
df_search_staytime =  pd.read_csv('result/search_addstaytime.csv')
# 不知道為甚麼名字中會有空格 但取代掉
df_s['name'] = df_s['name'].str.replace(' ', '')
df_r['rw_name'] = df_r['rw_name'].str.replace(' ', '')
df_search_staytime['name'] = df_search_staytime['name'].str.replace(' ', '')
df_search_staytime.rename(columns={'name': 'tmp_name'}, inplace=True)
# 先合併df_s、df_r 
df_merged = pd.merge(df_s, df_r, left_on='name', right_on='rw_name').drop('rw_name',axis=1)
# 再與df_search_staytime合併
df_merged = pd.merge(df_merged, df_search_staytime, left_on='name', right_on='tmp_name').drop('tmp_name',axis=1)
# df_merged.columns.tolist()
# 刪除多於欄位
df_merged_drop_somecolumn = df_merged.drop(columns=['rw_reviewer',
 'rw_reviewer_page',
 'rw_reviewer_tag',
 'rw_review_time',
 'rw_rating_reviewer',
 'rw_likes',
 'rw_review',
 'rw_review_word',
 'rw_latitude',
 'rw_longitude',
 'rw_current_time',
 'rw_rating_total',
 'rw_rating_count_total',
 'rw_reviewer'])


# df_merged_drop_somecolumn

df_merged_drop_somecolumn.columns.tolist()
df_merged_drop_somecolumn = df_merged_drop_somecolumn.drop(['Unnamed: 0','Unnamed: 0.1','Unnamed: 0.2','Unnamed: 0.3','Unnamed: 0.4'],axis = 1)

df_merged_drop_somecolumn.to_csv('result/search_overview.csv',encoding='utf-8-sig')
