import pandas as pd


def insertdatetimecolumn(df):
    df.rename(columns={'Time': 'unixtime'}, inplace=True)
    data = df['unixtime']
    df.insert(0, 'DATE', (pd.to_datetime(data, unit='s')).dt.date)
    df.insert(1, 'TIME', (pd.to_datetime(data, unit='s')).dt.time)
    columnstitles = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'AMOUNT', 'unixtime']
    df = df.reindex(columns=columnstitles)
    df['diff'] = df['unixtime'].diff()
    return df



def computeMACD(df, n_fast, n_slow, n_smooth):
    fastEMA = df['CLOSE'].ewm(span=n_fast, min_periods=n_slow).mean()
    slowEMA = df['CLOSE'].ewm(span=n_slow, min_periods=n_slow).mean()
    df['MACD'] = pd.Series(fastEMA - slowEMA, name='MACD')
    df['Signal'] = pd.Series(df['MACD'].ewm(span=n_smooth, min_periods=n_smooth).mean(), name='Signal')
    df['MACDhist'] = pd.Series(df['MACD'] - df['Signal'], name='MACDhist')
    return df

def computeICHIMUKO(df, tenken,keyjun,senkob):
    # Define length of Tenkan Sen or Conversion Line
    cl_period = tenken

    # Define length of Kijun Sen or Base Line
    bl_period = keyjun

    # Define length of Senkou Sen B or Leading Span B
    lead_span_b_period = senkob

    period9_high = df['HIGH'].rolling(cl_period).max()
    period9_low = df['LOW'].rolling(cl_period).min()
    df['tenkan_sen'] = (period9_high + period9_low) / 2

    period26_high = df['HIGH'].rolling(bl_period).max()
    period26_low = df['LOW'].rolling(bl_period).min()
    df['kijun_sen'] = (period26_high + period26_low) / 2

    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(bl_period - 1)

    high_120 = df['HIGH'].rolling(lead_span_b_period).max()
    low_120 = df['LOW'].rolling(lead_span_b_period).min()
    df['lead_span_b'] = ((high_120 + low_120) / 2).shift(bl_period - 1)

    # Calculate lagging span
    df['lagging_span'] = df['CLOSE'].shift(-bl_period)
    return df

