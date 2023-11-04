import os
import pandas as pd
import csv

def check_file_existence(folder_path, file_name):
    # 拼接文件的完整路径
    file_path = os.path.join(folder_path, file_name)

    # 使用 os 模块的 isfile 函数检查文件是否存在
    if os.path.isfile(file_path):
        return True
    else:
        return False
    
def read_all_csv_files_in_folder(folder_path):
    # 获取指定文件夹内的所有文件名
    file_list = os.listdir(folder_path)

    # 创建一个空的DataFrame，用于存储合并后的数据
    combined_df = pd.DataFrame()

    # 循环遍历文件列表，读取所有CSV文件的内容，并将其合并到combined_df中
    for filename in file_list:
        if filename.lower().endswith('.csv'):  # 检查文件扩展名是否为CSV
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df


def check_csv_file_lines(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        line_count = 0
        
        for row in csvreader:
            line_count += 1
        
        return line_count
    
# 填值進整條csv column
def fill_value_in_csv_files(folder_path, filename_to_modify, fill_value, target_column):
    # 組合目標檔案的完整路徑
    file_path = os.path.join(folder_path, filename_to_modify)
    
    # 讀取 CSV 檔案
    df = pd.read_csv(file_path)
    
    # 將指定值填入目標欄位
    df[target_column] = fill_value
    
    # 儲存修改後的資料回到原檔案
    df.to_csv(file_path, index=False, encoding='utf-8-sig')