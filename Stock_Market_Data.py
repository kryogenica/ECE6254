import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import csv
import os
import time
import json
from sklearn import datasets, svm

ts = TimeSeries(key='L49GC96YCRJIYSNU', output_format='csv')
ti = TechIndicators(key='L49GC96YCRJIYSNU', output_format='json')
bag, names, sector, cheatsheet = [], [], [], []
directory = os.getcwd() + "\\Market_data\\"

def init():
    global cheatsheet
    if not os.path.exists(directory):
        os.makedirs(directory)
        print("folder:  \Market_data  has been created\nWill attempt to redownload database")
        redownloadall()
    if not os.path.exists(directory + "cheatsheets.txt"):
        redownloadall()
    with open('cheatsheet.txt','r') as infile:
        cheatsheet = json.load(infile)
    
def redownloadall():    

#-------------------------------Alpha Vantage------------------------------------
    
    bag.append(["FB","AAPL","GOOGL","MSFT","IBM","AMD","NVDA","SNE","AMZN","VMW","WDC","GPRO","STX","FDS"])
    bag.append(["NVS","FMS","PFE","JNJ","AET"])
    bag.append(["WFC","RF","DB","BBT","PNC","FITB","AXP","GS","JPM","BAC",
                "C","STI"])
    bag.append(["WMT","TGT","HD","LOW","JWN","KSS","GPS","SHLD","BBY","COST","DKS"])
    bag.append(["F","GM","FCAU", "TM","HMC","BWA","TSLA"])
    bag.append(["COP","HAL","XOM","BP"])

    sector = ["TECH", "MEDICAL", "FINANCIAL", "RETAIL", "AUTOMOTIVE", "ENERGY", "MISC"]

    names.append(['Facebook', 'Apple', 'Google', 'Microsoft', 'IBM', 'AMD', 'NVIDIA', 'Sony', 'Amazon', 'vmware', 'Western Digital',
                  'GoPro', 'Seagate', 'FactSet'])
    names.append(['Novartis', 'Fresanius', 'Pfizer', 'Johnson & Johnson', 'Aetna'])
    names.append(['Wells fargo', 'Regions', 'deutsch bank', 'BB&T', 'PNC', 'FifthThird', 'American Express',
                  'Goldman Sachs', 'JP Morgan Chase', 'Bank of America', 'Citigroup', 'Suntrust'])
    names.append(['Walmart', 'target','home depot', 'lowes', 'NordStrom', 'Kohls', 'GAP', 'Sears', 'Bestbuy', 'Costco', 'dicks'])
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
        if name not in cheatsheet:
            print("file added to cheatsheet")
            cheatsheet.append({'handle' : name , 'name' : "unknown", 'sector': sector[6], 'path': file})
        print("file: ", name, " has been created")



def output(stock, start, end, window):
    chart = [[],[]]
#    chart[:1] = [[],[]]
    
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
    while q + window + 1 < len(trial):
        try:
            
            year = trial['timestamp'][q+1][0] + trial['timestamp'][q+1][1] +trial['timestamp'][q+1][2] +trial['timestamp'][q+1][3]
        except:
            print("\nERROR! no stock data for selected timeframe!",start, " - ", end)
            return
        year = float(year)
        if year > end:
            q += 1
        else:
            secday = trial['open'][q]
            firstday = trial['open'][q + window]
            percentchange = (secday - firstday)/firstday
            chart[1].append(percentchange)
            chart[0].append(trial['timestamp'][q + window])
            if year < start:
                break
            else:
                q += 1
    #print(chart[0])
    return chart
    
    

def dataset(stock, start, end, window, results):
    chart = [[],[]]
    cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        #print(cheatitem[0]['path'].replace(".csv","_RSI.txt"))
        with open(cheatitem[0]['path'].replace(".csv","_RSI.txt"),'r') as infile:
            trial = json.load(infile)
            #print(trial[0][(results[0][5])]['RSI'])
    except:
        cheatitem = [item for item in cheatsheet if item["name"].lower() == stock.lower()]
    try:
        with open(cheatitem[0]['path'].replace(".csv","_RSI.txt"),'r') as infile:
            trial = json.load(infile)
    except:
        download(stock)
        cheatitem = [item for item in cheatsheet if item["handle"].lower() == stock.lower()]
    try:
        with open(cheatitem[0]['path'].replace(".csv","_RSI.txt"),'r') as infile:
            trial = json.load(infile)
    except:
        print("\nERROR! Could not find that stock:", stock,"! are you sure you entered the right name?")
        return
    q = 0
    #print(trial[0])
    while q + window + 1  < len(results[0]):
#        try:
#            year = results[0][q+2][0] + results[0][q + 2][1] + results[0][q + 2][2] + results[0][q + 2][3]
#        except:
#            print("\nERROR! no stock data for selected timeframe!",start, " - ", end)
#            return
        #year = float(year)
        #if year > end:
        #    q += 1
        #else:
        value = trial[0][(results[0][q + 1])]['RSI']
        #print(value)
        chart[1].append(value)
        chart[0].append((results[0][q + 1]))
        #if year < start:
        #break
        #else:
        q += 1
    #print(chart[0][300])
    return chart


    
try:
    cheatsheet
    sector
except:
    print('missing information, will attempt to refill')
    redownloadall()

init()




def forminputs(x):
    #x = np.array(x)
    for i in range(len(x[1])):
        x[1][i] = float(x[1][i])
    x = [x[1]]
    x = np.transpose(x)
    ##Normalize the data
    Xaverage = np.mean(x, axis = 0)             ##calculate average
    Xnormal = x - Xaverage                      ##substract average
    Xdeviation = np.std(Xnormal, axis = 0)      ##calculate standard deviation
    return (Xnormal / Xdeviation)
    
def formoutputs(y):
    del y[1][-7 :-1]
    y = np.abs(y[1])/y[1]
    for i in range(len(y)):
        if (y[i] != 1 and y[i] != -1):
            y[i] = 0

    return np.ravel(np.reshape(y,(len(y),1)))







trainY = output('amd',2014,2015,5)
trainX = dataset('amd',2014,2015,5, trainY)

testY = output('amd',2016,2017,5)
testX = dataset('amd',2016,2017,5, testY)

trainX = forminputs(trainX)
trainY = formoutputs(trainY)
testX = forminputs(testX)
testY = formoutputs(testY)


for n in testY:
        if n != 1 and n != -1:
            print(n)    
            n = 0
#POLY KERNEL PROBLEM 1
for bull in range (1, 2):
    for b in range(-8, -4):
        degree = bull
        weight = np.exp(bull)
        clf = svm.SVC(C = weight, kernel='poly', degree = bull)
        clf.fit(trainX,trainY)

#ERROR
        Pe = 1 - clf.score(testX,testY)
        #Pe = clf.predict(testX,testY)
        print('Error: ', Pe)
        print('C: ', weight)
        print('Support Vectors: ', len(clf.support_vectors_))
        print(' ')

#RBF KERNEL PROBLEM 2
for i in range (0, 2):
    for b in range(-8, -4):
        print('rbf')
        gamma = np.exp(b)
        weight = np.exp(i)
        clf = svm.SVC(C = weight, kernel='rbf')
        print('prefit')
        clf.fit(trainX,trainY)
#ERROR
        print('pretest')
        Pe = 1 - clf.score(testX,testY)
        print('Error: ', Pe)
        print('C: ', weight)
        print('gamma: ', gamma)
        print('Support Vectors: ', len(clf.support_vectors_))
        print(' ')
        
