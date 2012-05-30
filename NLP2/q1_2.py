import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    c =np.random.normal(0.0, sigma, 1)
    def ti(xi): return f(xi) + np.random.normal(0.0, sigma, 1)[0] 
    vti = np.vectorize(ti)
    t = vti(x)
    return (x,t)

def Y(w,x):
    return [sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)])  for xi in x]

def least_squares(w,x,t):
    return 0.5*sum([math.pow(sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)]) - ti , 2) for xi,ti in zip(x,t)])

# returns the optimal polynomial of degree M that approximates the dataset 
# according the least squares objective
def OptimizeLS(x, t, M):
    design_matrix = np.array([np.array([math.pow(xi,m) for m in np.arange(M+1)]) for xi in x])  # This is A
    design_matrix.shape # This is a NxM matrix
    #    A is a matrix of dimension NxM, W is a vector of dimension M and t is a vector of dimension N.)
    #    W_LS = ((AT*A)^-1)*AT*t
    t.shape                                             # This is a vector of dim N  
    prod = np.dot(design_matrix.T, design_matrix)      # prod is (AT*A)
    prod.shape
    i = np.linalg.inv(prod)                            # i is (AT*A)^-1)
    i.shape
    m = np.dot(i, design_matrix.T)                     # m is ((AT*A)^-1)*AT
    m.shape
    W_LS = np.dot(m, t)                                # w is ((AT*A)^-1)*AT*t
    W_LS.shape
    return W_LS

def makeSinPlot(x,t,f):
    vf = np.vectorize(f)
    y = vf(x)
    fig = plt.figure()
    wls1 = OptimizeLS(x, t, 1)
    w1 = Y(wls1,x)
    wls3 = OptimizeLS(x, t, 3)
    w3 = Y(wls3,x)
    wls5 = OptimizeLS(x, t, 5)
    w5 = Y(wls5,x)
    wls10 = OptimizeLS(x, t, 10)
    w10 = Y(wls10,x)
    print y
    print w1
    print w3
    print w5
    plt.plot(x,w1,'r-')
    plt.plot(x,w3,'b-')
    plt.plot(x,w5,'y-')
#    plt.plot(x,w10,'g--')
    plt.plot(x,y,'k-')
    plt.show()
    
    
def main():
    N = 10
    f = math.sin
    (x,t) = generateDataset(N, f, 0.03);
#    makeSinPlot(x,t,f)
    print least_squares(OptimizeLS(x, t, 1),x,t)
    print least_squares(OptimizeLS(x, t, 3),x,t)
    print least_squares(OptimizeLS(x, t, 5),x,t)
    print least_squares(OptimizeLS(x, t, 10),x,t)
#    print OptimizeLS(x, t, 0)
#    print OptimizeLS(x, t, 1)
#    print OptimizeLS(x, t, 3)
#    print OptimizeLS(x, t, 5)
#    print OptimizeLS(x, t, 10)
    
if __name__ == '__main__':
    main() 


