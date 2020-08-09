from library import *
import pprint

#### --------------- main program ------------------

country_name = 'Latvia'

year = 1981

download_data(country_name,year)

stats = prepare_data(country_name,year)

pprint.pprint(stats)

first_plot(stats,country_name,year)

plt.show()

