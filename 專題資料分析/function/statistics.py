import pandas as pd

# detect outlier:  Detect by arbitrary boundary
# 根據給定的上界和下界來偵測指定欄位中的異常值，並列印出相關統計信息和被標記的異常值
def outlier_detect_arbitrary(data,col,upper_fence,lower_fence):
    '''
    identify outliers based on arbitrary boundaries passed to the function.
    '''

    para = (upper_fence, lower_fence)
    tmp = pd.concat([data[col]>upper_fence,data[col]<lower_fence],axis=1)
    outlier_index = tmp.any(axis=1)
    # print(outlier_index)
    print('Num of outlier detected:',outlier_index.value_counts()[1])
    print('Proportion of outlier detected',outlier_index.value_counts()[1]/len(outlier_index))    
    return outlier_index, para

# index,para = outlier_detect_arbitrary(data=data,col='Fare',upper_fence=300,lower_fence=5)
# print('Upper bound:',para[0],'\nLower bound:',para[1])
# # check the 19 found outliers
# data.loc[index,'Fare'].sort_values()

# detect outlier: IQR method
# IQR 方法是一種常用的檢測異常值的統計方法，通常用於確定資料中的極端值是否可能是異常值
def outlier_detect_IQR(data,col,threshold=3):
    '''
    outlier detection by Interquartile Ranges Rule, also known as Tukey's test. 
    calculate the IQR ( 75th quantile - 25th quantile) 
    and the 25th 75th quantile. 
    Any value beyond:
        upper bound = 75th quantile + （IQR * threshold）
        lower bound = 25th quantile - （IQR * threshold）   
    are regarded as outliers. Default threshold is 3.
    '''
     
    IQR = data[col].quantile(0.75) - data[col].quantile(0.25)
    Lower_fence = data[col].quantile(0.25) - (IQR * threshold)
    Upper_fence = data[col].quantile(0.75) + (IQR * threshold)
    para = (Upper_fence, Lower_fence)
    tmp = pd.concat([data[col]>Upper_fence,data[col]<Lower_fence],axis=1)
    outlier_index = tmp.any(axis=1)
    print('Num of outlier detected:',outlier_index.value_counts()[1])
    print('Proportion of outlier detected',outlier_index.value_counts()[1]/len(outlier_index))
    return outlier_index, para

# index,para = outlier_detect_IQR(data=data,col='Fare',threshold=5)
# print('Upper bound:',para[0],'\nLower bound:',para[1])
# # check the 31 found outliers
# data.loc[index,'Fare'].sort_values()

# detect outlier: Mean and Standard Deviation Method
# 一種基於平均值和標準差的異常值檢測方法，可以用來快速識別出相對明顯的異常值
def outlier_detect_mean_std(data,col,threshold=3):
    '''
    outlier detection by Mean and Standard Deviation Method.
    If a value is a certain number(called threshold) of standard deviations away 
    from the mean, that data point is identified as an outlier. 
    Default threshold is 3.

    This method can fail to detect outliers because the outliers increase the standard deviation. 
    The more extreme the outlier, the more the standard deviation is affected.
    '''
   
    Upper_fence = data[col].mean() + threshold * data[col].std()
    Lower_fence = data[col].mean() - threshold * data[col].std()   
    para = (Upper_fence, Lower_fence)   
    tmp = pd.concat([data[col]>Upper_fence,data[col]<Lower_fence],axis=1)
    outlier_index = tmp.any(axis=1)
    print('Num of outlier detected:',outlier_index.value_counts()[1])
    print('Proportion of outlier detected',outlier_index.value_counts()[1]/len(outlier_index))
    return outlier_index, para

# index,para = outlier_detect_mean_std(data=data,col='Fare',threshold=3)
# print('Upper bound:',para[0],'\nLower bound:',para[1])
# # check the 20 found outliers
# data.loc[index,'Fare'].sort_values()

# detect outlier: MAD method
# （即中位數的絕對偏差）
# MAD 方法的優點是它不受資料分佈的影響，並且可以識別出較少的極端值。然而，它的一個限制是閾值的選擇可能需要基於特定情況進行調整。
# MAD 方法是一種基於絕對中位數差的異常值檢測方法，它在某些情況下可以比其他方法更具備穩定性
def outlier_detect_MAD(data,col,threshold=3.5):
    """
    outlier detection by Median and Median Absolute Deviation Method (MAD)
    The median of the residuals is calculated. Then, the difference is calculated between each historical value and this median. 
    These differences are expressed as their absolute values, and a new median is calculated and multiplied by 
    an empirically derived constant to yield the median absolute deviation (MAD). 
    If a value is a certain number of MAD away from the median of the residuals, 
    that value is classified as an outlier. The default threshold is 3 MAD.
    
    This method is generally more effective than the mean and standard deviation method for detecting outliers, 
    but it can be too aggressive in classifying values that are not really extremely different. 
    Also, if more than 50% of the data points have the same value, MAD is computed to be 0, 
    so any value different from the residual median is classified as an outlier.
    """
    
    median = data[col].median()
    median_absolute_deviation = np.median([np.abs(y - median) for y in data[col]])
    modified_z_scores = pd.Series([0.6745 * (y - median) / median_absolute_deviation for y in data[col]])
    outlier_index = np.abs(modified_z_scores) > threshold
    print('Num of outlier detected:',outlier_index.value_counts()[1])
    print('Proportion of outlier detected',outlier_index.value_counts()[1]/len(outlier_index))
    return outlier_index

# # too aggressive for our dataset, about 18% of cases are detected as outliers.
# index = outlier_detect_MAD(data=data,col='Fare',threshold=3.5)
# data.loc[index,'Fare'].sort_values()

# handle outlier: windsorization 
# 處理異常值的方法，通過使用指定的值來替代檢測到的異常值，從而避免異常值對分析的影響
def windsorization(data,col,para,strategy='both'):
    """
    top-coding & bottom coding (capping the maximum of a distribution at an arbitrarily set value,vice versa)
    """
    
    data_copy = data.copy(deep=True)  
    if strategy == 'both':
        data_copy.loc[data_copy[col]>para[0],col] = para[0]
        data_copy.loc[data_copy[col]<para[1],col] = para[1]
    elif strategy == 'top':
        data_copy.loc[data_copy[col]>para[0],col] = para[0]
    elif strategy == 'bottom':
        data_copy.loc[data_copy[col]<para[1],col] = para[1]  
    return data_copy

# use any of the detection method above
# index,para = outlier_detect_arbitrary(data,'Fare',300,5)
# print('Upper bound:',para[0],'\nLower bound:',para[1])
# print('before handling outlier:')
# print(data[255:275])
# print('after handling outlier:')
# # see index 258,263,271 have been replaced with top/bottom coding
# data3 = windsorization(data=data,col='Fare',para=para,strategy='both')
# print(data3[255:275])

# handle outlier: drop outlier
# 處理異常值的方法，通過刪除異常值所對應的觀察，來保證後續分析的準確性和一致性。
def drop_outlier(data,outlier_index):
    """
    drop the cases that are outliers
    """
    
    data_copy = data[~outlier_index]
    return data_copy
# use any of the detection method above
# index,para = outlier_detect_arbitrary(data,'Fare',300,5)
# print('Upper bound:',para[0],'\nLower bound:',para[1])

# drop the outlier.
# we can see no more observations have value >300 or <5. They've been removed.
# data4 = drop_outlier(data=data,outlier_index=index)
# print(data4.Fare.max())
# print(data4.Fare.min())

# handle outlier: impute with mean 
# 處理異常值的方法，通過用平均值（或中位數、眾數）來替代異常值所對應的變數值，以達到對數據進行修正的目的
def impute_outlier_with_avg(data,col,outlier_index,strategy='mean'):
    """
    impute outlier with mean/median/most frequent values of that variable.
    """
    
    data_copy = data.copy(deep=True)
    if strategy=='mean':
        data_copy.loc[outlier_index,col] = data_copy[col].mean()
    elif strategy=='median':
        data_copy.loc[outlier_index,col] = data_copy[col].median()
    elif strategy=='mode':
        data_copy.loc[outlier_index,col] = data_copy[col].mode()[0]   
        
    return data_copy
# # use any of the detection method above
# index,para = outlier_detect_arbitrary(data,'Fare',300,5)
# print('Upper bound:',para[0],'\nLower bound:',para[1])
# # see index 258,263,271 have been replaced with mean

# data5 = impute_outlier_with_avg(data=data,col='Fare',
#                                    outlier_index=index,strategy='mean')
# print(data5[255:275])

"""
參數標準化的一些常用做法
ss = StandardScaler().fit(X_train[['Fare']])
mms = MinMaxScaler().fit(X_train[['Fare']])

這種方法適用於數據集中存在離群值（outliers）的情況，因為它使用的是中位數而不是均值，而中位數對異常值更不敏感
rs = RobustScaler().fit(X_train[['Fare']])

對數轉換（Logarithmic transformation）
data_log['Fare_log'] = np.log(data_log['Fare'] + 1)

# feature encoding:　One-hot encoding
import category_encoders as ce
ord_enc = ce.OrdinalEncoder(cols=['Sex']).fit(X_train,y_train)
data4 = ord_enc.transform(data)
print(data4.head(5))

data1 = pd.get_dummies(data,dtype = float)

KBinsDiscretizer 是 scikit-learn 中用於連續特徵離散化（binning）的類別之一。它可以將連續的數值特徵劃分成多個區間，從而將連續數值轉換為離散值。這對於一些機器學習算法和特徵工程來說是很有用的，因為某些算法可能對離散特徵有更好的適應性。
from sklearn.preprocessing import KBinsDiscretizer
enc_equal_width = KBinsDiscretizer(n_bins=3,encode='ordinal',strategy='uniform').fit(X_train[['Fare']])

# Square root transformation
平方根轉換（Square root transformation），通過對數據的每個值
這種轉換在某些情況下可以幫助調整數值特徵的分佈，使其更接近常態分佈，或者在一些情況下可以減小變異性
data_square =  X_train.copy(deep=True)
data_square['Fare_square'] = (data_square['Fare'])**(0.5)
print(data_rec.head(10))

# Exponential transformation
數轉換（Exponential transformation），透過對每個數據值進行 0.2 次方運算，創建了新的 Fare_exp 欄位。這種轉換可以用來調整數據的分佈，特別是在數據值分布較廣的情況下，可以將高數值部分拉近，使分佈更接近正態分佈
data_exp =  X_train.copy(deep=True)
data_exp['Fare_exp'] = (data_exp['Fare'])** 0.2
print(data_exp.head(10))

# Box-cox transformation
Box-Cox轉換是一種用於調整數據分佈的方法，它可以將數據轉換為更加接近正態分佈的形式。這可以對某些機器學習模型的效能有所提升，因為這些模型在正態分佈的數據上表現較好
Box-Cox轉換通常在數據存在右偏（正偏）或左偏（負偏）時使用，以調整數據分佈為更加對稱的形式，從而使模型的表現更好
from sklearn.preprocessing import PowerTransformer
pt = PowerTransformer().fit(X_train[['Fare']])
data_box = X_train.copy(deep=True)
data_box['Fare_boxcox'] = pt.transform(data_box[['Fare']])
print(data_box.head(6))
data_box['Fare_boxcox'].hist()


# Quantile transformation
使用了分位數轉換（Quantile transformation）。分位數轉換是一種將數據轉換為均勻分佈或正態分佈的方法之一，可以使數據的分佈更加平滑，並且可以減少極端值的影響
分位數轉換是一種調整數據分佈的有效方法，可以用於消除極端值的影響，使數據的分佈更加穩定和平滑
from sklearn.preprocessing import QuantileTransformer
qt = QuantileTransformer(output_distribution='normal').fit(X_train[['Fare']])
data_qu = X_train.copy(deep=True)
data_qu['Fare_qt'] = qt.transform(data_qu[['Fare']])
print(data_qu.head(6))
data_qu['Fare_qt'].hist()


"""