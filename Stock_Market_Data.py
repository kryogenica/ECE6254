import numpy as np
from iexfinance import Stock
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import urllib
import json
ts = TimeSeries(key='L49GC96YCRJIYSNU', output_format='pandas')

#-------------------------------Alpha Vantage------------------------------------
# This needs to be installed first: pip install alphavantage
# Get json object from Alapha_Vantage server
data, meta_data = ts.get_intraday(symbol='TSLA', outputsize='full')
# Plot the data
data['4. close'].plot()
plt.title('Tesla plot from Alpha Vantage')
plt.show()

#----------------------------------IEX-----------------------------------------
# This needs tob e installed first: pip install iexfinance
# Get Json object from IEX server
tsla = Stock('TSLA')
data = urllib.request.urlopen("https://api.iextrading.com/1.0/stock/tsla/chart/1m").read()
tesla = json.loads(data)
      
#tesla = tsla.get_chart()       #Alternative way to get data
df = pd.DataFrame(tesla)        #Structure the data
# Plot the data
df['close'].plot()
plt.plot(df['date'],df['close'])
plt.title('Tesla plot from IEX')
plt.show()

