import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    t = [f(xi) + np.random.normal(0.0, sigma, 1)[0] for xi in x]
    return (x,t)

# y(x) = w0 + w1x + w2x^2 + ... + wMx^M
def Y(w,x):
    return [sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)])  for xi in x]

# E(w) = 0.5*sum(y(xi) - ti)^2 = 0.5*sum(sum(wk*xi^k) - ti)^2
def least_squares(w,x,t):
    return 0.5*sum([math.pow(sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)]) - ti , 2) for xi,ti in zip(x,t)])

# returns the optimal polynomial of degree M that approximates the dataset 
# according the least squares objective
#    W_LS = ((AT*A)^-1)*AT*t
#    A is a matrix of dimension NxM, W is a vector of dimension M and t is a vector of dimension N.)
def OptimizeLS(x, t, M):
    design_matrix = np.array([np.array([math.pow(xi,m) for m in np.arange(M+1)]) for xi in x])  # This is A
    prod = np.dot(design_matrix.T, design_matrix)      # prod is (AT*A)
    i = np.linalg.inv(prod)                            # i is (AT*A)^-1)
    m = np.dot(i, design_matrix.T)                     # m is ((AT*A)^-1)*AT
    W_LS = np.dot(m, t)                                # w is ((AT*A)^-1)*AT*t
    return W_LS

def makeSinPlot(x,t,f,M,c):
    vf = np.vectorize(f)
    y = vf(x)
    fig = plt.figure()
    wls = OptimizeLS(x, t, M)
    w = Y(wls,x)
    sizes = [40,50,70]
    ax = fig.add_subplot(111)
    ax.scatter(x,t, s=sizes,marker = '.', facecolor='red' )
    plt.title('M = %d' % M)
    plt.plot(x,w,c)
    plt.plot(x,y,'k-')
    plt.show()
    
def main():
    N = 10
    f = math.sin
    (x,t) = generateDataset(N, f, 0.03);
    makeSinPlot(x,t,f,1,'r-')
    makeSinPlot(x,t,f,3,'y-')
    makeSinPlot(x,t,f,5,'g-')
    makeSinPlot(x,t,f,9,'b-')
    print "E(w1) =  %.8f" % least_squares(OptimizeLS(x, t, 1),x,t)
    print "E(w3) =  %.8f" % least_squares(OptimizeLS(x, t, 3),x,t)
    print "E(w5) =  %.8f" % least_squares(OptimizeLS(x, t, 5),x,t)
    print "E(w9) =  %.8f" % least_squares(OptimizeLS(x, t, 9),x,t)
    
if __name__ == '__main__':
    main() 
