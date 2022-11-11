import csv
import json
import os.path
import requests as rq


def get_coin_list() -> list:
    baseurl = ' https://api.kucoin.com'
    symbol_list_url = '/api/v2/symbols'
    fullpath = baseurl + symbol_list_url
    symbol_dict = json.loads((rq.get(fullpath)).text)
    return_list = []
    for sym in symbol_dict["data"]:
        if sym["quoteCurrency"] == 'USDT':
            return_list.append(sym["symbol"])
    return return_list


def download_data(coinname: str, startcandle: int, endcandle: int, timeframe: str) -> list:
    baseurl = ' https://api.kucoin.com'
    klines_url = baseurl + '/api/v1/market/candles?type=' + timeframe + '&symbol=' + coinname + '&startAt=' + str(
        startcandle) + '&endAt=' + str(endcandle)
    error_code = 0
    while error_code != 200000:
        fetch_data = rq.get(klines_url).text
        temp_dict = json.loads(fetch_data)
        error_code = int(temp_dict['code'])
        print(error_code)
    return temp_dict["data"]


def is_downloadable(coinname: str) -> bool:
    time_const = 900 * 1400
    base_time = 1577836800 - time_const
    lines_url = 'https://api.kucoin.com/api/v1/market/candles?type=15min&symbol={0}&startAt={1}&endAt={2}'.format(
        coinname, str(
            base_time), str(1667766600))
    fetch_data = rq.get(lines_url).text
    temp_dict = json.loads(fetch_data)
    error_code = int(temp_dict['code'])
    retval = True
    if error_code == 400100:
        retval = False
    return retval


def write_file(c_n: str, per: str, tar_list: list, s_p: str):
    fields = ['Time', 'OPEN', 'CLOSE', 'HIGH', 'LOW', 'VOLUME', 'AMOUNT']
    completepath = os.path.join(s_p, c_n + '_' + per + ".csv")
    with open(completepath, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(tar_list)


def main(sym: str):
    # breakpoint()
    print(sym)
    time_const = 900 * 1400
    base_time = 1577836800 - time_const
    end_time = base_time + time_const
    target_list = []
    save_path = 'D:/Kucoin_Spot/'
    while end_time <= 1667766600:
        base_time = end_time
        end_time = end_time + time_const
        temp_list = download_data(sym, base_time, end_time, '15min')
        if len(temp_list) > 1:
            t_list = temp_list.reverse()
            target_list = target_list + temp_list
            temp_list.clear()
    write_file(sym, 'M15', target_list, save_path)
    target_list.clear()
