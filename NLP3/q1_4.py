import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import math

# return a tuple with the 2 vectors x and t
# where the xi values are equi-distant on the [0,1] segment (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
# and t is ti = y(xi) + Normal(mu, sigma)
def generateDataset(N, f, sigma):
    x =np.linspace(0.0, 1.0, num=N) # (that is, x1 = 0, x2=1/N-1, x3=2/N-1..., xN = 1.0)
    t = [f(xi) + np.random.normal(0.0, sigma, 1)[0] for xi in x]
    return (x,t)

# return Q(x) = (Q0(x) ... QM(x))T = (1 x x^2 x^3 ... x^M)^T
def phi(x,M):
    fi = np.matrix([math.pow(x, i) for i in np.arange(0,M+1)])
    return fi.T 

#which given the dataset (x, t) of size N, and the parameters M, alpha, and
# sigma2 (the variance), returns a tuple of 2 functions (m(x) var(x)) 
# which are the mean and variance of the predictive distribution inferred
# from the dataset, based on the parameters and the normal prior over w.
def bayesianEstimator(X, t, M, alpha, sigma2):
    I = np.eye(M+1)          
    B = (1.0/sigma2)
    S = np.linalg.inv(alpha*I + B*sum([np.dot(phi(xn,M),phi(xn,M).T) for xn in X]))
    def m(x):
        su = sum([np.dot(phi(xn,M), tn) for xn,tn in zip(X,t)])
        Ssum = np.dot(S,su)
        BxTs = B * np.dot(phi(x,M).T, Ssum)
        r = BxTs.item(0)
        return  r
    def var(x):
        phix = phi(x,M)
        phiTS = np.dot(phix.T,S)
        return sigma2 + np.dot(phiTS, phix) 
    return (m, var)

def drawPlot(xt, t, f, m, var):
    x = np.linspace(0.0, 1.0, num=100)
    vf = np.vectorize(f)
    vm = np.vectorize(m)
    vvar = np.vectorize(var)
    y = vf(x)
    ym = vm(x)
    yvar = vvar(x)
    yvar2 = [math.pow(yvi,0.5) for yvi in yvar]
    yvarup = y + yvar2
    yvardown = y - yvar2
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xt,t, s=50,marker= 'o',edgecolors ='blue', facecolor='none' )
    plt.plot(x,y,lw=2,color= 'green')
    plt.plot(x,ym,lw=2,color= 'red')
    plt.plot(x,yvarup,lw=1,color= 'red',alpha=0.3)
    plt.plot(x,yvardown,lw=1,color= 'red',alpha=0.3)
    plt.title('N = %d' % len(t))
    plt.show()

def run(N):
    def f(x): return math.sin(2*math.pi*x)
    (x,t) = generateDataset(N, f, 0.03);
    alpha = 0.005
    sigma2 = 1/11.1
    M = 9 
    (m,var) = bayesianEstimator(x, t, M, alpha, sigma2)
    drawPlot(x, t, f, m, var)

def main():    
    run(10)
    run(100)
    
if __name__ == '__main__':
    main() 