import os
import csv
import pandas as pd

def main(folder_path):
    # 取得資料夾內所有檔案
    file_list = os.listdir(folder_path)
    
    for filename in file_list:
        if filename.endswith('.csv'):
            csv_path = os.path.join(folder_path, filename)
            df = pd.read_csv(csv_path,encoding='utf-8-sig')
            try:
                second_row = df.iloc[0]
                # print(second_row['rw_name'])
                if  second_row.isnull().all():
                    print(f"刪除檔案: {filename}")
                    os.remove(csv_path)
            except:
                print(f"刪除檔案2: {filename}")
                os.remove(csv_path)
            # has_values = second_row.isnull().all()  # 檢查是否所有值都為空
            # print(second_row.isnull().all())


if __name__ == "__main__":
    folder_path = "review/"  # 設定資料夾路徑
    main(folder_path)