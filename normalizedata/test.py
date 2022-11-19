import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema


#df = pd.DataFrame(xs, columns=['data'])
df = pd.read_csv('D:/BTC-USDT.csv')
n = 10  # number of points to be checked before and after

# Find local peaks

df['min'] = df.iloc[argrelextrema(df.LOW.values, np.less_equal,
                    order=n)[0]]['LOW']
df['max'] = df.iloc[argrelextrema(df.HIGH.values, np.greater_equal,
                    order=n)[0]]['HIGH']

# Plot results

plt.scatter(df.index, df['min'], c='r')
plt.scatter(df.index, df['max'], c='g')
plt.plot(df.index, df['CLOSE'])
plt.show()
print(df['min'])