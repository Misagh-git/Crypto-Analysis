import pandas as pd
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

for x in m15chart_collection:
    func.insertdatetimecolumn(x)
    func.computeMACD(x, 12, 26, 9)
    ch_h1= [y for y in h1chart_collection if x.name == y.name][0]
    x['MACD'].shift<x['']

m15chart_collection[0].to_csv('D:/btc.csv')

print(h1chart_collection[0].name)
