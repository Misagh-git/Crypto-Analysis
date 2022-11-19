import pandas as pd
import numpy as np
import functions as func
import os
import re

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

for ind in m15chart_collection[0].index:
    if ind==1:
        m15chart_collection[0]['NEWCOL']='HELLO'

print (m15chart_collection[0].iterrows()[0]['CLOSE'])