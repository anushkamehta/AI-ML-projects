import numpy as np
import sys
import csv

lambda_input = int(sys.argv[1])
sigma2_input = float(sys.argv[2])
X_train = np.genfromtxt(sys.argv[3], delimiter = ",")
y_train = np.genfromtxt(sys.argv[4])
X_test = np.genfromtxt(sys.argv[5], delimiter = ",")
X_train = np.matrix(X_train)
X_test = np.matrix(X_test)
y_train = np.transpose(np.matrix(y_train))

def ridge_regression(X_train, y_train):
    b = np.transpose(X_train)*X_train   
    num_dims = np.shape(X_train)[1]
    a = lambda_input*np.identity(num_dims)
    c = np.transpose(X_train)*y_train
    wrr = np.linalg.inv(a+b)*c
    return wrr

wRR = ridge_regression(X_train, y_train)
np.savetxt("wRR_" + str(lambda_input) + ".csv", wRR, delimiter="\n") 


def active_learning(X_train, y_train, X_test):
    n = 10
    locations = []
    num_dims = np.shape(X_train)[1]
    num_observations = len(X_test)
    indexes = list(range(1, num_observations+1))
    prior = np.linalg.inv(lambda_input*np.identity(num_dims) + (sigma2_input**-1)*(X_train.T)*X_train)

    while len(locations) <= n:
        sols = []
        for i in range(num_observations):
            sigma_temp = np.linalg.inv(np.linalg.inv(prior) + (sigma2_input**-1)*(X_test[i].T)*(X_test[i]))
            entr = sigma2_input + X_test[i]*sigma_temp*X_test[i].T
            sols.append(entr)
        best_x = np.argmax(sols)

        prior = np.linalg.inv(np.linalg.inv(prior) + (sigma2_input**-1)*(X_test[best_x].T)*X_test[best_x])
        X_test = np.delete(X_test,best_x,0)
        num_observations = len(X_test)
        locations.append(indexes[best_x])
        indexes.remove(indexes[best_x])
    return locations

active = active_learning(X_train, y_train, X_test) 
filename = "active_{}_{}.csv".format(str(lambda_input), str(int(sigma2_input)))

with open(filename, 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerow(active)
