from __future__ import division
import numpy as np
import sys
import csv

"""
Probabilistic matrix factorisation-decomposes matrix M into U and V matrices
with parameters defined as below
objective.csv contains objective function along each row.
"""
train_data = np.genfromtxt(sys.argv[1], delimiter = ",")

lam = 2
sigma2 = 0.1
iterations = 50

def PMF(train_data):
    print_itr = [10, 25, 50]
    Nu = int(np.amax(train_data[:,0]))
    Nv = int(np.amax(train_data[:,1]))
    obj = np.zeros((iterations,1))
    m = np.zeros((Nu, Nv))
    #print(Nu, Nv)
    const1 = 0.5/0.1 #1/2*sigma2
    const2 = lam/2 
    d = 5
    const3 = lam*sigma2*np.eye(d)
    V = np.random.normal(0, (1/lam), (Nv, d))
    #print(V.shape)
    U = np.zeros((Nu, d))
    #print(U.shape)
    for row in train_data:
        #print(row)
        i,j = int(row[0]), int(row[1])
        rating = row[2]
        m[i-1,j-1] = rating
    rating_i, user_v = [], []

    for i in range(Nu):
        temp = train_data[train_data[:,0] == i+1][:,1] 
        rating_i.append(temp.astype(np.int64))

    for i in range(Nv):
        temp = train_data[train_data[:,1] == i+1][:,0]
        user_v.append(temp.astype(np.int64))

    #print(m.shape)
    for itr in range(iterations):
        for i in range(Nu):
            #M = np.zeros(d)
            prod = rating_i[i]
            Vi = V[prod-1]
            a = np.linalg.inv(const3 + (Vi.T).dot(Vi))
            
            b = (Vi*m[i,prod-1][:,None]).sum(axis=0)
            ui = a.dot(b)
            U[i] = ui
        
      

        for j in range(Nv):
            user = user_v[j]
            Uj = U[user-1]
            c = np.linalg.inv(const3 + (Uj.T).dot(Uj))
            
            d = (Uj*m[user-1,j][:,None]).sum(axis=0)
            
            vj = c.dot(d)
            V[j] = vj    
        
        l3 = 0
        for val in train_data:
            i,j = int(val[0]), int(val[1])
            l3 = l3 + (val[2] - np.dot(U[i-1,:],V[j-1,:]))**2
        l3 = l3/(2*sigma2)
        l1 = lam*0.5*(((np.linalg.norm(U, axis=1))**2).sum())     
        l2 = lam*0.5*(((np.linalg.norm(V, axis=1))**2).sum())
        obj[itr] = -l3-l1-l2
        if itr+1 in print_itr:
            
            path1 = "U-{}.csv".format(str(itr+1))
            with open(path1, "w") as file:
                writer = csv.writer(file, delimiter=',', lineterminator='\n')
                for val in U:
                    writer.writerow(val)   
            #Write output to file
            path2 = "V-{}.csv".format(str(itr+1))
            with open(path2, "w") as file:
                writer = csv.writer(file, delimiter=',', lineterminator='\n')
                for val in V:
                    writer.writerow(val)             
     
    with open("objective.csv", "w") as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')
        for val in obj:
            writer.writerow(val)
    return obj, U, V


# Assuming the PMF function returns Loss L, U_matrices and V_matrices (refer to lecture)
L, U_matrices, V_matrices = PMF(train_data)
print(L.shape, V_matrices.shape, U_matrices.shape) #verification

