import pandas as pd
import functions as func
import os

df = pd.read_csv('D:/Kucoin_Spot/BTC-USDT_H1.csv')
df.rename(columns={'Time': 'unixtime'}, inplace=True)
df.insert(0, 'DATE', (pd.to_datetime(df['unixtime'], unit='s')).dt.date)
df.insert(1, 'TIME', (pd.to_datetime(df['unixtime'], unit='s')).dt.time)
columnsTitles = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'AMOUNT', 'unixtime']
df = df.reindex(columns=columnsTitles)
df['diff'] = df['unixtime'].diff()
df=func.computeMACD(df,12,26,9)
df=func.computeICHIMUKO(df,9,26,52)

all_files = os.listdir('D:/Kucoin_Spot/')
h1files = [x for x in all_files if "H1" in x]
m15files = [x for x in all_files if "M15" in x]
