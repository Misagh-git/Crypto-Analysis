import pandas as pd
chart_list=[]

df = pd.read_csv('D:/Kucoin_Spot/BTC-USDT_H1.csv')
df.rename(columns={'Time': 'unixtime'}, inplace=True)
df.insert(0, 'DATE', (pd.to_datetime(df['unixtime'], unit='s')).dt.date)
df.insert(1, 'TIME', (pd.to_datetime(df['unixtime'], unit='s')).dt.time)
columnsTitles = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'AMOUNT', 'unixtime']
df = df.reindex(columns=columnsTitles)
df['diff'] = df['unixtime'].diff()
chart_list.append(df)


#df.to_csv('D:/BTC-USDT_H1.csv')
