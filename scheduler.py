import sched
import time
import os

import pandas as pd
from preprocessing import parse_to_dataframe
from filter_data import filter_df_on_locations

scheduler = sched.scheduler(time.time, time.sleep)

#initialize global dataframe
os.system("python download_data.py")
df = filter_df_on_locations(parse_to_dataframe(),"Tilburg", "Eindhoven")
print(df.shape)

def get_data(name):  
    global df
    print("Get data: #", name , ", ", time.time())
    os.system("python download_data.py")
    
    full_df = parse_to_dataframe()
    frames = [df, filter_df_on_locations(full_df,"Tilburg", "Eindhoven")]
    df = pd.concat(frames)
	
    print(df.shape)
	
for x in range(0, 60):
    df1 = scheduler.enter(60 * x, 1, get_data, (x,))

print("Script started at ", time.time())

scheduler.run()

df.to_csv("data/traveltime.csv", sep='|')

