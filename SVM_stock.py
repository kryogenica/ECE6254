#Use Scikit learn to train various SVM
import numpy as np

#loads csv data into a ndarray
my_data = np.genfromtxt('Open_data_normed.csv',delimiter=',')
Means = np.genfromtxt('Means_open.csv',delimiter=',')
Stds = np.genfromtxt('Stds_open.csv',delimiter=',')

X_train=my_data[0:300,0:-2]
y_train=my_data[0:300,-1]

X_holdout=my_data[300:500,0:-2]
y_holdout=my_data[300:500,-1]

from sklearn import svm
clf = svm.NuSVR(C=2.0, cache_size=500, nu=0.5, coef0=1, degree=3, kernel='poly', max_iter=-1, shrinking=True, tol=0.01, verbose=False)
clf.fit(X_train, y_train)

y_pred=clf.predict(X_holdout)

Back_to_normal_pred=((np.multiply(y_pred,Stds[300:500]))+Means[300:500])
Back_to_normal_holdout=((np.multiply(y_holdout,Stds[300:500]))+Means[300:500])

import matplotlib.pyplot as plt
plt.plot(Back_to_normal_holdout[30:50])
plt.plot(Back_to_normal_pred[30:50])
#plt.show()
plt.savefig('Prediction_of_crypto.png',dpi=1000)

Dif=y_pred-y_holdout
print (np.linalg.norm(Dif)/y_holdout.shape[0])




