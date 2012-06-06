import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

def  generateDataset3(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=3*N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    pairs = [(xi, f(xi) + np.random.normal(0.0, sigma, 1)[0]) for xi in x]
    np.random.shuffle(x) 
    test = pairs[:N]
    train = pairs[N:N*2]
    dev =pairs[N*2:]
    xts , tts = zip(*test)
    xtr , ttr = zip(*train)
    xdv , tdv = zip(*dev)
    return ((xts,tts),(xtr,ttr),(xdv,tdv))

# y(x) = w0 + w1x + w2x^2 + ... + wMx^M
def Y(w,x):
    return [sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)])  for xi in x]

# E(w) = 0.5*sum(y(xi) - ti)^2 = 0.5*sum(sum(wk*xi^k) - ti)^2
def least_squares(w,x,t):
    return 0.5*sum([math.pow(sum([wk*(math.pow(xi,k)) for k,wk in enumerate(w)]) - ti , 2) for xi,ti in zip(x,t)])

#  return  E(w) + lambda*EW(w)
def EPLS(w,x,t,lamda):
    return least_squares(w,x,t) + lamda*0.5*sum([wi*wi for wi in w])

def normalized_error(w,x,t):
    return (1.0/len(t))*math.pow(sum([math.pow(ti - sum([wm*math.pow(xi, m) for m,wm in enumerate(w)]) , 2) for xi,ti in zip(x,t)]), 0.5)

# returns the optimal polynomial of degree M that approximates the dataset 
# according the least squares objective
def optimizePLS(x, t, M, lamda):
    design_matrix = np.array([np.array([math.pow(xi,m) for m in np.arange(M+1)]) for xi in x])  # This is A
    #    A is a matrix of dimension NxM, W is a vector of dimension M and t is a vector of dimension N.)
    #    W_PLS = ((AT*A) + lambda*I)^-1 * AT*t
    prod = np.dot(design_matrix.T, design_matrix)      # prod is (AT*A)
    lamdaI = lamda *np.eye(M+1)         # id is lamda*I
    s = prod + lamdaI                                    # s is (AT*A) + lamda*I)
    i = np.linalg.inv(s)                               # i is (AT*A) + lamda*I)^-1
    m = np.dot(i, design_matrix.T)                     # m is ((AT*A) + lamda*I))*AT
    W_PLS = np.dot(m, t)                               # w is ((AT*A) + lamda*I))*AT*t
    return W_PLS

def optimize_PLS(xt, tt, xv, tv, M):
    for i in np.arange(-20,5):
        lamda = math.pow(10, i)
        w = optimizePLS(xv, tv, M, lamda)
        e = normalized_error(w,xv,tv)
        print e
    return 0 

def normalized_errorPlot(xt, tt, xv, tv, M):
    xl = np.arange(-20,5)
    val = []
    train = []
    for i in xl:
        lamda = math.pow(math.e, i)
        wv = optimizePLS(xv, tv, M, lamda)
        ev = normalized_error(wv,xv,tv)
#        ev = EPLS(wv,xv,tv,lamda)
        wt = optimizePLS(xt, tt, M, lamda)
        et = normalized_error(wt,xt,tt)
#        et = EPLS(wt,xt,tt,lamda)
        val.append(ev)    
        train.append(et)
    plt.title('N = 10')
    plt.plot(xl,val,'r-')
    plt.plot(xl,train,'b-')
    plt.show()
    
def main():
    N = 10
    def f(x): return math.sin(2*math.pi*x)
    a = generateDataset3(N, f, 0.03);
    (xts,tts) = a[0]
    (xtr,ttr) = a[1]
    (xdv,tdv) = a[2]
    optimize_PLS(xtr, ttr, xdv, tdv, 10)
#    optimize_PLS(xtr, ttr, xv, tv, 3)
#    makeSinPlot(x,t,f)
#    print "E(w1) =  %.8f" % least_squares(OptimizeLS(x, t, 1),x,t)
#    print "E(w3) =  %.8f" % least_squares(OptimizeLS(x, t, 3),x,t)
#    print "E(w5) =  %.8f" % least_squares(OptimizeLS(x, t, 5),x,t)
#    print "E(w9) =  %.8f" % least_squares(OptimizeLS(x, t, 9),x,t)
    
if __name__ == '__main__':
    main() 