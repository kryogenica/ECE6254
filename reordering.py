#Loads csv file into array only comformed by one feature
#The size of the rows are deterimined by the window_step size 
import numpy as np

#loads csv data into a ndarray
my_data = np.genfromtxt('Historical_eth-usd_data.txt',delimiter=',')
window_step=5 #Sets the window size
feature=3 #Order: time,low,high,open,close,volume
prev_i=window_step+1 #Will help with setting the range when extracting data
#An array is initialized with the first data points
A=my_data[1:window_step+1,feature]

#range naturally ensures that the last vector is the same dim as the others
for i in range(((window_step)+(window_step)+1),my_data.shape[0],window_step):
    #Helps concatenate our vectors into an array
    A=np.r_['0,2',A,my_data[prev_i:i,feature]]
    prev_i=i #rest to previous i 
print (A)

