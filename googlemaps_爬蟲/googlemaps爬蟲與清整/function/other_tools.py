import random
import time

def timesleep_rand():
#     return time.sleep(random.randint(1, 2))
    return time.sleep(random.uniform(1,2))



def has_non_digits_using_isdigit(s):
    return s.isdigit()

def get_run_times(end_time,start_time):
    return str(int((end_time-start_time)/3600))+" hr "+str(int((end_time-start_time)/60)-int((end_time-start_time)/3600)*60)+" min "+str(round((end_time-start_time)%60,2))+" sec "
    # print("run times: ",)