import pandas as pd
import numpy as np
import functions as func
import os
import re

# green is below of price in asc trend

rootfolder = 'D:/Main_Spot/'
all_files = os.listdir(rootfolder)
h1files = [x for x in all_files if "H1" in x]
m15files = [x for x in all_files if "M15" in x]

h1chart_collection = []
m15chart_collection = []

for x in h1files:
    h1chart_collection.append(pd.read_csv(rootfolder + x))
    h1chart_collection[len(h1chart_collection) - 1].name = re.sub('_H1.csv', '', x)

for x in m15files:
    m15chart_collection.append(pd.read_csv(rootfolder + x))
    m15chart_collection[len(m15chart_collection) - 1].name = re.sub('_M15.csv', '', x)

for x in h1chart_collection:
    func.insertdatetimecolumn(x)
    func.computeICHIMUKO(x, 9, 26, 52)
    x['kumotype'] = np.where(x['senkou_span_a'] >= x['lead_span_b'], 'Up Kumo', 'DownKumo')

for x in m15chart_collection:
    func.insertdatetimecolumn(x)
    func.computeMACD(x, 12, 26, 9)
    ch_h1 = [y for y in h1chart_collection if x.name == y.name][0]

    tradecondition = [
        (x['MACD'].shift() < x['Signal'].shift()) & (x['MACD'] > x['Signal']),
        (x['MACD'].shift() > x['Signal'].shift()) & (x['MACD'] < x['Signal'])]
    choices = ['BUY', 'SELL']
    x['macd_cross'] = np.select(tradecondition, choices, default='NA')
    for index, row in x.iterrows():
        if row['macd_cross'] == 'BUY' or row['macd_cross'] == 'SELL':
            ti = row['TIME']
            da = row['DATE']
            h1_row_da = ch_h1.loc[ch_h1['DATE'] == da]
            h1_row_ti = h1_row_da.loc[ch_h1['TIME'] == ti]
            print(h1_row_ti)
            breakpoint()

m15chart_collection[0].to_csv('D:/' + m15chart_collection[0].name + '.csv')

# print(m15chart_collection[0])
