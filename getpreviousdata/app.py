import functions as func
from functions import main
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from functions import get_coin_list
import os

pa = 'D:/Kucoin_Spot/'
all_files = os.listdir(pa)
h1files = [x for x in all_files if "H1" in x]
m15files = [x for x in all_files if "M15" in x]

h1symbol = [s.strip('_H1.csv') for s in h1files]
m15symbol = [m.strip('_M15.csv') for m in m15files]

target_sym = []
for x in h1symbol:
    if m15symbol.count(x) == 0 and func.is_downloadable(x):
        target_sym.append(x)

#main(target_sym[1])

print(len(target_sym))

with ThreadPoolExecutor(max_workers=10) as pool:
	futures = [pool.submit(main, symbol) for symbol in target_sym]
	for future in as_completed(futures):
		result = future.result()
