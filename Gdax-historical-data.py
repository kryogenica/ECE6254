#PULLING HISTORICAL GDAX DATA
#Uses library from https://github.com/danpaquin/gdax-python
import time
import datetime
import gdax
import csv
import tzlocal

def main(argv1,argv2,argv3):
    period = 0.34 #helps with not exceeding requests per second
    #create a a new file where pulled data will be saved
    file_handler = open('Historical_eth-usd_data.txt', 'w')
    #writes a specific header in the order in which data is pulled from the web
    file_handler.write("time,low,high,open,close,volume\n")
    #We throttle public endpoints by IP: 3 requests per second
    #Up to 6 requests per second in bursts
    #A maximum of 300 candel sticks are permitted to be pulled per request
    points = 300
    history_step = (argv3*points)
    count = 0
    for i in range(argv1,argv2,history_step):
        #Create a web connection
        public_client = gdax.PublicClient()
        #First step
        primera = int(i)
        #Second step
        ultima = int(i+history_step)
        #Get local time zone
        tz = tzlocal.get_localzone()
        #strat time
        comienzo = datetime.datetime.fromtimestamp(primera).astimezone(tz)
        #final time
        final = datetime.datetime.fromtimestamp(ultima).astimezone(tz)
        #https://docs.gdax.com/#get-historic-rates
        history = public_client.get_product_historic_rates(product_id='ETH-USD', start=comienzo, end=final, granularity=argv3)
        #Set file and parameter to be saved
        to_write_into = csv.writer(file_handler, delimiter=",")
        #Write into csv file
        to_write_into.writerows(history)
        #Sleep to no exceed the number of requests (3) per second
        time.sleep(period)
        #debugging purposes
        print (count)
        count = count+1
    #close memory for file    
    file_handler.close()

if __name__=="__main__":
    #arguments are {iso8601 start time, iso8601 end time, granularity}
    #granularity values permitted {60, 300, 900, 3600, 21600, 86400} in seconds
    main(1514352720,1514500346,300)
#12/15/2017 - 3pm - GTC-5 - Timestamp:1513368000 - iso8601:2017-12-15T15 :00:00-05:00
#12/15/2017 - 4pm - GTC-5 - Timestamp:1513371600 - iso8601:2017-12-15T16 :00:00-05:00
# if dates are fed in the incorrect order, this script will not get any historical data
