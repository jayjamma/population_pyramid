import time
from library import *

countries = list(country_index.keys())

country_name = countries[13]

y_start = 1950
y_end   = 2100

for year in range(y_start,y_end):
	
    download_data(country_name,year)
    time.sleep(1)
