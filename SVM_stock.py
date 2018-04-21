#Use Scikit learn to train various SVM
import numpy as np

#loads csv data into a ndarray

midrange=300
maxrange=500

X_train_open=0
y_train_open=0
X_holdout_open=0
y_holdout_open=0
X_train_low=0
y_train_low=0
X_holdout_low=0
y_holdout_low=0
X_train_high=0
y_train_high=0
X_holdout_high=0
y_holdout_high=0

a="X_train_"
b="y_train_"
c="X_holdout_"
d="y_holdout_"

for z in ["open","low","high"]:
    
    globals()["my_data_" + z] = np.genfromtxt(z+"_data_normed.csv",delimiter=',')
    globals()["Means_" + z] = np.genfromtxt("Means_"+z+".csv",delimiter=',')
    globals()["Stds_" + z] = np.genfromtxt("Stds_"+z+".csv",delimiter=',')

    globals()[a + z]=globals()["my_data_" + z][0:midrange,0:-2]
    globals()[b + z]=globals()["my_data_" + z][0:midrange,-1]

    globals()[c + z]=globals()["my_data_" + z][midrange:maxrange,0:-2]
    globals()[d + z]=globals()["my_data_" + z][midrange:maxrange,-1]

from sklearn import svm
#Training
clf_open = svm.NuSVR(C=2.0, cache_size=500, nu=0.5, coef0=1, degree=3, kernel='poly', max_iter=-1, shrinking=True, tol=0.01, verbose=False)
clf_open.fit(X_train_open, y_train_open)

clf_low = svm.NuSVR(C=2.0, cache_size=500, nu=0.5, coef0=1, degree=3, kernel='poly', max_iter=-1, shrinking=True, tol=0.01, verbose=False)
clf_low.fit(X_train_low, y_train_low)

clf_high = svm.NuSVR(C=2.0, cache_size=500, nu=0.5, coef0=1, degree=3, kernel='poly', max_iter=-1, shrinking=True, tol=0.01, verbose=False)
clf_high.fit(X_train_high, y_train_high)

Back_to_normal_y_holdout_open=((np.multiply(y_holdout_open,Stds_open[midrange:maxrange]))+Means_open[midrange:maxrange])
Back_to_normal_y_holdout_high=((np.multiply(y_holdout_high,Stds_high[midrange:maxrange]))+Means_high[midrange:maxrange])
Back_to_normal_y_holdout_low=((np.multiply(y_holdout_low,Stds_low[midrange:maxrange]))+Means_low[midrange:maxrange])

print (X_holdout_open[0,1:21].shape)
print (Stds_open[midrange].shape)
print (Stds_open[midrange])

Back_to_normal_X_holdout_open=((np.multiply(X_holdout_open[0,1:21],Stds_open[midrange]))+Means_open[midrange])
Back_to_normal_X_holdout_high=((np.multiply(X_holdout_high[0,1:21],Stds_high[midrange]))+Means_high[midrange])
Back_to_normal_X_holdout_low=((np.multiply(X_holdout_low[0,1:21],Stds_low[midrange]))+Means_low[midrange])


#SOME LOOP HERE
i=0

y_pred_open=clf_open.predict(np.reshape(X_holdout_open[i],(1,X_holdout_open[i,:].shape[0])))
y_pred_low=clf_low.predict(np.reshape(X_holdout_low[i],(1,X_holdout_low[i,:].shape[0])))
y_pred_high=clf_high.predict(np.reshape(X_holdout_open[i],(1,X_holdout_open[i,:].shape[0])))

Normal_y_pred_open=(y_pred_open*Stds_open[midrange+i])+(Means_open[midrange+i])
Normal_y_pred_high=(y_pred_high*Stds_high[midrange+i])+(Means_high[midrange+i])
Normal_y_pred_low=(y_pred_low*Stds_low[midrange+i])+(Means_low[midrange+i])


Normal_y_pred_open=((np.multiply(y_pred_open,Stds_open[midrange:maxrange]))+Means_open[midrange:maxrange])


import matplotlib.pyplot as plt
plt.plot(Back_to_normal_y_holdout_open[30:50])
plt.plot(Normal_y_pred_open[30:50])
#plt.show()
plt.savefig('Prediction_of_crypto.png',dpi=1000)

Dif=y_pred_open-y_holdout_open
print (np.linalg.norm(Dif)/y_holdout_open.shape[0])
