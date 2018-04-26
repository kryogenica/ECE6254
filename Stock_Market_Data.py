import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import csv
import os
import time
import json
from sklearn import svm
import copy

#Before first time, RUN: pip install alpha_vantage
ts = TimeSeries(key='L49GC96YCRJIYSNU', output_format='csv')
ti = TechIndicators(key='L49GC96YCRJIYSNU', output_format='json')
bag, names, sector, cheatsheet = [], [], [], []
directory = os.getcwd() + "\\Market_data\\"
frame = 5

#Init
def init():
    global cheatsheet
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("folder:  \Market_data  has been created\nWill attempt to redownload database")
        redownloadall()
    if not os.path.exists(directory + "cheatsheets.txt"):
        redownloadall()
    with open(directory + 'cheatsheet.txt','r') as infile:
        cheatsheet = json.load(infile)
    
#redownload all stocks from API
def redownloadall():    

#-------------------------------Alpha Vantage------------------------------------
    
    bag.append(["FB","AAPL","GOOGL","MSFT","IBM","AMD","NVDA","SNE","AMZN","VMW","WDC","GPRO","STX","FDS"])
    bag.append(["NVS","FMS","PFE","JNJ","AET"])
    bag.append(["WFC","RF","DB","BBT","PNC","FITB","AXP","GS","JPM","BAC",
                "C","STI"])
    bag.append(["WMT","TGT","HD","LOW","JWN","KSS","GPS","SHLD","BBY","COST","DKS", "SBUX"])
    bag.append(["F","GM","FCAU", "TM","HMC","BWA","TSLA"])
    bag.append(["COP","HAL","XON","BP"])

    sector = ["TECH", "MEDICAL", "FINANCIAL", "RETAIL", "AUTOMOTIVE", "ENERGY", "MISC"]

    names.append(['Facebook', 'Apple', 'Google', 'Microsoft', 'IBM', 'AMD', 'NVIDIA', 'Sony', 'Amazon', 'vmware', 'Western Digital',
                  'GoPro', 'Seagate', 'FactSet'])
    names.append(['Novartis', 'Fresanius', 'Pfizer', 'Johnson & Johnson', 'Aetna'])
    names.append(['Wells fargo', 'Regions', 'deutsch bank', 'BB&T', 'PNC', 'FifthThird', 'American Express',
                  'Goldman Sachs', 'JP Morgan Chase', 'Bank of America', 'Citigroup', 'Suntrust'])
    names.append(['Walmart', 'target','home depot', 'lowes', 'NordStrom', 'Kohls', 'GAP', 'Sears', 'Bestbuy', 'Costco', 'dicks', 'starbucks'])
    names.append(['Ford', 'GM', 'Fiat Chrysler', 'Toyota', 'Honda', 'Borg Warner', 'Tesla'])
    names.append(['Conoco', 'Halliburton', 'Exxon', 'BP'])

    index, i = 0, 0
    while (i < len(bag)):
        a = 0
        while (a < len(bag[i])):
            file = (directory + bag[i][a] + ".csv")
            rsifile = (directory + bag[i][a] + "_RSI.txt")
            cheatsheet.append({'handle' : bag[i][a] , 'name' : names[i][a], 'sector': sector[i], 'path': file})
            if not os.path.exists(file):
                time.sleep(3)
                data, meta_data = ts.get_daily(symbol = bag[i][a], outputsize = 'full')
                spamWriter = csv.writer(open(file, 'w', newline=''), delimiter=',')
                for row in data:
                    spamWriter.writerow(row)
                print("file: ", bag[i][a], ".csv has been created")
            if not os.path.exists(rsifile):
                time.sleep(3)
                rsi = ti.get_rsi(symbol=bag[i][a],series_type='open')
                with open(rsifile,'w') as outfile:
                    json.dump(rsi,outfile)
                print("file: ", bag[i][a], "_RSI.txt has been created")    
            a += 1
            index += 1
        i+=1
        
        with open(directory + 'cheatsheet.txt','w') as outfile:
            json.dump(cheatsheet,outfile)
         
#download stock from API
def download(name):
        file = (directory + name + ".csv")
        try:
            data, meta_data = ts.get_daily(symbol = name, outputsize = 'full')
        except:
            print("\nERROR! AlphaVantage api - could not connect or bad call")
            return
        spamWriter = csv.writer(open(file, 'w', newline=''), delimiter=',')
        for row in data:
            spamWriter.writerow(row)
        time.sleep(.5)
        statinfo = os.stat(file)
        if statinfo.st_size < 5000:
            print("\nERROR! file:",name,"is too small, error during creation")
            return
        #if name not in cheatsheet:
        #    print("file added to cheatsheet", name)
        #    cheatsheet.append({'handle' : name , 'name' : "unknown", 'sector': sector[6], 'path': file})
        print("file: ", name, " has been created")


#retrieve stock data from list
def stockdata(stock, start, end):
    chart = [[],[],[]]
    #ATTEMPT TO FIND STOCK DATA
    cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        trial = pd.read_csv(cheatitem[0]['path'])
    except:
        cheatitem = [item for item in cheatsheet if item["name"].lower() == stock.lower()]
    try:
        trial = pd.read_csv(cheatitem[0]['path'])
    except:
        download(stock)
        cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        trial = pd.read_csv(cheatitem[0]['path'])

    except:
        print("\nERROR! Could not find that stock:", stock,"! are you sure you entered the right name?")
        return
    q = 0
    while q + 1 < len(trial):  
        # CONVERT ENDING DATE TO FLOATS         
        year = trial['timestamp'][q+1][0] + trial['timestamp'][q+1][1] +trial['timestamp'][q+1][2] +trial['timestamp'][q+1][3]
        month = trial['timestamp'][q+1][5] + trial['timestamp'][q+1][6]
        day = trial['timestamp'][q+1][8] + trial['timestamp'][q+1][9]
        year, month, day = float(year), float(month), float(day)
        # CHECK IF WITHIN TIME WINDOW
        if year > end[0] or (month > end[1] and year == end[0]) or (month == end[1] and year == end[0] and day > end[2]):
            q += 1
        else:     
            #COPY STOCK DATA TO LIST
            chart[0].append(trial['timestamp'][q])
            chart[1].append(trial['open'][q])
            chart[2].append(trial['close'][q])
            #chart[3].append(trial['high'][q])
            #chart[4].append(trial['low'][q])
            #chart[5].append(trial['volume'][q])
            if year <= start[0] and month <= start[1] and day <= start[2]:
                break
            else:
                q += 1
    #CHANGE DIRECTION OF LISTS => (EARLIEST TO LATES)
    for i in range(len(chart)):
        chart[i] = list(reversed(chart[i]))
    #EXIT FUNCTION
    return chart
    
    

def indicator(stock, window, results, index):
    chart = [[],[]]
    cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        with open(cheatitem[0]['path'].replace(".csv","_" + index + ".txt"),'r') as infile:
            trial = json.load(infile)
    except:
        cheatitem = [item for item in cheatsheet if item["name"].lower() == stock.lower()]
    try:
        with open(cheatitem[0]['path'].replace(".csv","_" + index + ".txt"),'r') as infile:
            trial = json.load(infile)
    except:
        download(stock)
        cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        with open(cheatitem[0]['path'].replace(".csv","_" + index + ".txt"),'r') as infile:
            trial = json.load(infile)
    except:
        print("\nERROR! Could not find that stock:", stock,"! are you sure you entered the right name?")
        return
    q = 0
    while q < len(results[0]):
        value = trial[0][(results[0][q])][index]
        chart[1].append(value)
        chart[0].append((results[0][q]))
        q += 1
    
    return chart


    
try:
    cheatsheet
    sector
except:
    print('missing information, will attempt to refill')
    redownloadall()

init()




def forminputs(a):
    x = copy.deepcopy(a)
    buzz = []
    for i in range(len(x[1])):
        data = [float(x[1][i])]
        for a in range(len(x)-1):
            data.append(float(x[a+1][i]))
        buzz.append(data)
    x = buzz
    
    ##Normalize the data
    Xaverage = np.mean(x, axis = 0)             ##calculate average
    Xnormal = x - Xaverage                      ##substract average
    Xdeviation = np.std(Xnormal, axis = 0)      ##calculate standard deviation)
    return (Xnormal / Xdeviation)

def formoutputs(a):
    y = copy.deepcopy(a)
    y = np.ravel(np.reshape(y[1],(len(y[1]),1)))
    y = [round(x * 100) for x in y]
    return y

def shiftleft(x,shift):
    a = copy.deepcopy(x)
    for i in range(len(a)):
        del a[i][-(shift+1):-1]
    return a

def shiftright(x,shift):
    a = copy.deepcopy(x)
    for i in range(len(a)):
        del a[i][:shift]
    return a

def change(x):
    a = 0
    rate = copy.deepcopy(x)
    while a < len(rate) - 1:
        rate[a] = rate[a+1] - rate[a]
        a += 1
    del rate[-1]
    return rate

def vol(d, f):
    ch = [0]*f
    dif = [0]*f
    volatility = 0
    
    mean = [0]*(len(d))
    std = [0]*(len(d))
    for a in range(len(d)-f):
        for i in range(f):
            ch[i] = ((d[a+i+1]/d[a+i])-1)
            dif[i] = ((d[a+i+1] - d[a+i])/(d[a+i]))
        std[a] = np.std(ch, axis = 0)
        mean[a] = np.mean(dif, axis = 0)
    volatility = np.median(std, axis = 0)
    result = [0]*(len(std)-frame)
    for i in range(len(std)-frame):
        if std[i] > volatility and mean[i] > 0:
            result[i] = 4 #'green'
        elif std[i] > volatility and mean[i] < 0:
            result[i] = 3 #'red'
        elif std[i] < volatility and mean[i] > 0:
            result[i] = 2 #'blue'
        else: result[i] = 1 #'magenta'
    return result

def factor(y):
    for i in range(len(y)):
        if y[i] == 2 or y[i] == 4:
            y[i] = 1
        else:
            y[i] = -1
    return y

data = stockdata('AMZN', [2010,4,6], [2016,4,6])
volatility = vol(data[2],frame)
trainX = shiftleft(data,frame)
slope = change(trainX[1])
slope.append(0)
trainX.append(slope)
x = forminputs(trainX)
y = np.ravel(np.reshape(volatility,(len(volatility),1)))
y = factor(y)

testdata = stockdata('AMZN', [2017,1,8], [2017,6,20])
testvol = vol(testdata[2],frame)
testX = shiftleft(testdata,frame)
testslope = change(testX[1])
testslope.append(0)
testX.append(testslope)
tx = forminputs(testX)
ty = np.ravel(np.reshape(testvol,(len(testvol),1)))
ty = factor(ty)


#SVM TRIAL AND TEST
for i in range (-1, 0):
    for b in range(-2, -1):
        weight = np.exp(i)
        gamma = np.exp(b)
        clf = svm.SVC(C = weight, kernel='rbf')
        clf.fit(x,y)
#ERROR
        Pe = 1 - clf.score(tx,ty)
        print("PE: ", Pe)
        pred = clf.predict(tx)
        for i in range(len(pred)):
            if pred[i] > 0:
                pred[i] = pred[i]*800
            else: pred[i] = pred[i]*-700

plt.plot(testdata[2])
plt.plot(pred)
