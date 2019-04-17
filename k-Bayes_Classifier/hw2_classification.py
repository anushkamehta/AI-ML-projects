from __future__ import division
import numpy as np
import sys

X_train = np.genfromtxt(sys.argv[1], delimiter=",")
y_train = np.genfromtxt(sys.argv[2])
X_test = np.genfromtxt(sys.argv[3], delimiter=",")

def get_prior_mean_covar(X_train, y_train):
    k_labels = set(y_train)
    K = len(k_labels)
    n = len(X_train)
    pi = [y_train.tolist().count(i)/float(n) for i in k_labels]
    pi = np.matrix(pi).T
    means, covs = [], []
    for i in k_labels:
         x = X_train[(y_train == i)]
         mean = np.mean(x, axis = 0)

         cov = ((x - mean).T).dot((x-mean))/float(len(x))
         means.append(mean)
         covs.append(cov)
    return pi , means, covs

def pluginClassifier(X_train, y_train, X_test):
    k_labels = set(y_train)
    print(len(k_labels))
    pi, mean, cov = get_prior_mean_covar(X_train, y_train) 
    prob = np.zeros((len(X_test),len(k_labels)))
    posterior = np.zeros((len(X_test),len(k_labels)))
    for i in range(len(k_labels)):
        a = np.linalg.inv(cov[i])
        b = (np.linalg.det(cov[i]))**-0.5
        for j, x in enumerate(X_test):
            c = (mean[i] - x)
            prob[j,i] = pi[i]*b*np.exp(-0.5*((c.T).dot(a)).dot(c))
    for i, x in enumerate(X_test):
        summ = prob[i].sum()
        posterior[i] = prob[i]*1.0/summ

    return posterior
final_outputs = pluginClassifier(X_train, y_train, X_test) 

np.savetxt("probs_test.csv", final_outputs, delimiter=",") 
