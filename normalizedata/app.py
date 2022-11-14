import pandas as pd

df = pd.read_csv('D:/Kucoin_Spot/BTC-USDT_H1.csv')
df.rename(columns={'Time': 'unixtime'}, inplace=True)
df.insert(0, 'DATE', (pd.to_datetime(df['unixtime'], unit='s')).dt.date)
df.insert(1, 'TIME', (pd.to_datetime(df['unixtime'], unit='s')).dt.time)
columnsTitles = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'AMOUNT', 'unixtime']
df = df.reindex(columns=columnsTitles)
df['diff'] = df['unixtime'].diff()


#---------Implement MACD-----------------
k = df['CLOSE'].ewm(span=12, adjust=False, min_periods=12).mean()
d = df['CLOSE'].ewm(span=26, adjust=False, min_periods=26).mean()
macd = k - d
macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
macd_h = macd - macd_s
df['macd'] = df.index.map(macd)
df['macd_h'] = df.index.map(macd_h)
df['macd_s'] = df.index.map(macd_s)
#---------Finish MACD-------------------


#ICHI MOKU Implement

period9_high = df['High'].rolling(window=9).max()
period9_low = df['Low'].rolling(window=9).min()
df['tenkan_sen'] = (period9_high + period9_low) / 2

period26_high = pd.rolling_max(df['HIGH'], window=26)
period26_low = pd.rolling_min(df['LOW'], window=26)
df['kijun_sen'] = (period26_high + period26_low) / 2

df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

period52_high = pd.rolling_max(df['HIGH'], window=52)
period52_low = pd.rolling_min(df['LOW'], window=52)
df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

df['chikou_span'] = df['CLOSE'].shift(-22)


print(df.tail())
#df.to_csv('D:/BTC-USDT_H1.csv')
