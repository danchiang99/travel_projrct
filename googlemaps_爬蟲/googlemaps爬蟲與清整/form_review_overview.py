import time
import function.file as file
import function.other_tools as otool


folder_path = 'review/'
start_time = time.time() 
# 读取文件夹内所有CSV文件的内容并合并为一个DataFrame
all_df = file.read_all_csv_files_in_folder(folder_path)
all_df = all_df.drop(['Unnamed: 0'],axis = 1)
end_time = time.time() 
print("run times: ",otool.get_run_times(end_time,start_time))
all_df.to_csv('result/review_overview.csv',encoding='utf-8-sig')