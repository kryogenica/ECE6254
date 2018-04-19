#Loads csv file into array only comformed by one feature
#The size of the rows are deterimined by the window_step size 
import numpy as np

##########Difernece between High and low in time window

#loads csv data into a ndarray
my_data = np.genfromtxt('Historical_eth-usd_data.txt',delimiter=',')
window_step=21 #Sets the window size

#Set matrix A to contain rows of time frame Lows
feature=1 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]

#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i
Mins=(A[:,0:-1].min(axis=1).reshape(A.shape[0],1))

del A
#Set matrix A to contain rows of time frame Highs
feature=2 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]

#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i
#Get the maximum of each row
Maxs=(A[:,0:-1].max(axis=1).reshape(A.shape[0],1))

#Set a column to contain the dif between Highs and Lows.
#Normalized by minus mean and divided by std.
Reach=(Maxs-Mins)
Reach=((Reach-(Reach).mean(axis=0))/((Reach-(Reach).mean(axis=0)).std(axis=0)))
del A,Maxs,Mins

################Reshaping dataset to contain data on opening prices and reach

feature=3 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]

#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i    

#We calculate the mean of each row without including the last value
Means=((A[:,0:-1].mean(axis=1)).reshape(A.shape[0],1))
np.savetxt("Means_open.csv", Means, delimiter=",")
Means=(np.repeat(Means,A.shape[1],axis=1))

Temp=(A[:,0:-1]-Means[:,0:-1])
Temp=np.square(Temp)

#We calculate the std of each row without including the last value
Stds=(Temp.std(axis=1).reshape(A.shape[0],1))
np.savetxt("Stds_open.csv", Stds, delimiter=",")
Stds=(np.repeat(Stds,A.shape[1],axis=1))

#All rows are normalized minus mean and divided by std.
Normed_stock=(np.divide((A-Means),Stds))
del A,Means,Stds,Temp

#Append vector and array. Order matters.
Full_stock=np.c_[Reach,Normed_stock]
np.savetxt("Open_data_normed.csv", Full_stock, delimiter=",")
del Normed_stock
del Full_stock

#############Low Data

feature=1 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]
#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i

#We calculate the mean of each row without including the last value
Means=((A[:,0:-1].mean(axis=1)).reshape(A.shape[0],1))
np.savetxt("Means_low.csv", Means, delimiter=",")
Means=(np.repeat(Means,A.shape[1],axis=1))

Temp=(A[:,0:-1]-Means[:,0:-1])
Temp=np.square(Temp)

#We calculate the std of each row without including the last value
Stds=(Temp.std(axis=1).reshape(A.shape[0],1))
np.savetxt("Stds_low.csv", Stds, delimiter=",")
Stds=(np.repeat(Stds,A.shape[1],axis=1))

#All rows are normalized minus mean and divided by std.
Normed_stock=(np.divide((A-Means),Stds))

#Append vector and array. Order counts.
Full_stock=np.c_[Reach,Normed_stock]

np.savetxt("Low_data_normed.csv", Full_stock, delimiter=",")
del Normed_stock
del Full_stock
#############High Data
del A
feature=2 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]
#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i

#We calculate the mean of each row without including the last value
Means=((A[:,0:-1].mean(axis=1)).reshape(A.shape[0],1))
np.savetxt("Means_high.csv", Means, delimiter=",")
Means=(np.repeat(Means,A.shape[1],axis=1))

Temp=(A[:,0:-1]-Means[:,0:-1])
Temp=np.square(Temp)

#We calculate the std of each row without including the last value
Stds=(Temp.std(axis=1).reshape(A.shape[0],1))
np.savetxt("Stds_high.csv", Stds, delimiter=",")
Stds=(np.repeat(Stds,A.shape[1],axis=1))

#All rows are normalized minus mean and divided by std.
Normed_stock=(np.divide((A-Means),Stds))

#Append vector and array. Order counts.
Full_stock=np.c_[Reach,Normed_stock]

np.savetxt("High_data_normed.csv", Full_stock, delimiter=",")
